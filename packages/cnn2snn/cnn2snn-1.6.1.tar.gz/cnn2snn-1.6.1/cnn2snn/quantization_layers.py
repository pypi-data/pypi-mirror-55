#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

# Tensorflow imports
import tensorflow as tf
from tensorflow.python.keras import backend
import tensorflow.keras.backend as K
from tensorflow.keras import layers
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.framework import ops, common_shapes
from tensorflow.python.ops import nn
from tensorflow.python.ops import standard_ops, gen_math_ops
from tensorflow.python.eager import context
from .quantization_ops import WeightFloat, BaseWeightQuantizer, ceil_through


def _check_layer_default_params(**kwargs):
    """Raises error if some layer parameters are wrongly set.

    Some parameters must be set to their default values since other values
    are not compatible with Akida:
    - 'data_format': for all layers, this must be default ('channels_last')
    - 'activation': for Dense, Conv2D and SeparableConv2D, this must be
        default (None).
    - 'dilation_rate': for Conv2D and SeparableConv2D, this must be
        default ((1,1)).
    - 'depth_multiplier': for SeparableConv2D, this must be default (1).

    Note that this check only look at the presence of the parameters and
    not their values: even if the parameter is present with default
    value, an error will be raised.

    :param **kwargs: all kwargs given to the layer constructor
    :type **kwargs: dictionary
    """
    if 'data_format' in kwargs:
        raise ValueError("'data_format' parameter must NOT be defined "
                         " in the layer parameters.")
    if 'activation' in kwargs:
        raise ValueError("'activation' parameter must NOT be defined"
                         " in the layer parameters.")
    if 'dilation_rate' in kwargs:
        raise ValueError("'dilation_rate' parameter must NOT be defined"
                         " in the layer parameters.")
    if 'depth_multiplier' in kwargs:
        raise ValueError("'depth_multiplier' parameter must NOT be defined"
                         " in the layer parameters.")


class QuantizedConv2D(layers.Conv2D):
    """A quantization-aware Keras convolutional layer.

    Inherits from Keras Conv2D layer, applying a quantization on weights during
    the forward pass.
    """
    def __init__(self, filters, kernel_size, quantizer=WeightFloat(), **kwargs):
        """Creates a quantization-aware convolutional layer

        :param filters: the number of filters
        :type filters: integer
        :param kernel_size: the kernel spatial dimensions
        :type kernel_size: a tuple of integer
        :param quantizer: the quantizer to apply during the forward pass
        :type quantizer: cnn2snn.WeightQuantizer
        """
        _check_layer_default_params(**kwargs)
        if not isinstance(quantizer, BaseWeightQuantizer):
            raise AttributeError("Quantizer object should be used")
        self.quantizer = quantizer
        super(QuantizedConv2D, self).__init__(filters, kernel_size, **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        :param inputs: input Tensor
        :type inputs: tensorflow.Tensor
        :return: tensorflow.Tensor
        """
        outputs = self._convolution_op(inputs,
                                       self.quantizer.quantize(self.kernel))
        if self.use_bias:
            if self.data_format == "channels_first":
                raise RuntimeError("unsupported data format channels_first")
            else:
                outputs = nn.bias_add(outputs, self.bias, data_format='NHWC')

        return outputs


class QuantizedDepthwiseConv2D(layers.DepthwiseConv2D):
    """A quantization-aware Keras depthwise convolutional layer.

    Inherits from Keras DepthwiseConv2D layer, applying a quantization on
    weights during the forward pass.
    """
    def __init__(self, kernel_size, quantizer=WeightFloat(), **kwargs):
        """Creates a quantization-aware depthwise convolutional layer

        :param kernel_size: the kernel spatial dimensions
        :type kernel_size: a tuple of integer
        :param quantizer: the quantizer to apply during the forward pass
        :type quantizer: cnn2snn.WeightQuantizer
        """
        _check_layer_default_params(**kwargs)
        if not isinstance(quantizer, BaseWeightQuantizer):
            raise AttributeError("Quantizer object should be used")
        self.quantizer = quantizer
        super(QuantizedDepthwiseConv2D, self).__init__(kernel_size, **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        :param inputs: input Tensor
        :type inputs: tensorflow.Tensor
        :return: tensorflow.Tensor
        """
        # We don't support biases
        return backend.depthwise_conv2d(inputs,
                                        self.quantizer.quantize(
                                            self.depthwise_kernel),
                                        strides=self.strides,
                                        padding=self.padding,
                                        dilation_rate=self.dilation_rate,
                                        data_format=self.data_format)


class QuantizedDense(layers.Dense):
    """A quantization-aware Keras dense layer.

    Inherits from Keras Dense layer, applying a quantization on weights during
    the forward pass.
    """
    def __init__(self, units, quantizer=WeightFloat(), **kwargs):
        """Creates a quantization-aware dense layer

        :param units: the number of neurons
        :type units: integer
        :param quantizer: the quantizer to apply during the forward pass
        :type quantizer: cnn2snn.WeightQuantizer
        """
        _check_layer_default_params(**kwargs)
        if not isinstance(quantizer, BaseWeightQuantizer):
            raise AttributeError("Quantizer object should be used")
        self.quantizer = quantizer
        super(QuantizedDense, self).__init__(units, **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        :param inputs: input Tensor
        :type inputs: tensorflow.Tensor
        :return: tensorflow.Tensor
        """
        inputs = ops.convert_to_tensor(inputs)
        kernel = self.quantizer.quantize(self.kernel)
        rank = common_shapes.rank(inputs)
        if rank > 2:
            # Broadcasting is required for the inputs.
            outputs = standard_ops.tensordot(inputs,
                                             kernel, [[rank - 1], [0]])
            # Reshape the output back to the original ndim of the input.
            if not context.executing_eagerly():
                shape = inputs.get_shape().as_list()
                output_shape = shape[:-1] + [self.units]
                outputs.set_shape(output_shape)
        else:
            outputs = gen_math_ops.mat_mul(inputs, kernel)
        if self.use_bias:
            outputs = nn.bias_add(outputs, self.bias)
        return outputs


class QuantizedSeparableConv2D(layers.SeparableConv2D):
    """A quantization-aware Keras separable convolutional layer.

    Inherits from Keras SeparableConv2D layer, applying a quantization on
    weights during the forward pass.
    """
    def __init__(self, filters, kernel_size, quantizer=WeightFloat(), **kwargs):
        """Creates a quantization-aware separable convolutional layer

        :param filters: the number of filters
        :type filters: integer
        :param kernel_size: the kernel spatial dimensions
        :type kernel_size: a tuple of integer
        :param quantizer: the quantizer to apply during the forward pass
        :type quantizer: cnn2snn.WeightQuantizer
        """
        _check_layer_default_params(**kwargs)
        if not isinstance(quantizer, BaseWeightQuantizer):
            raise AttributeError("Quantizer object should be used")
        self.quantizer = quantizer
        super(QuantizedSeparableConv2D, self).__init__(filters, kernel_size, **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        :param inputs: input Tensor
        :type inputs: tensorflow.Tensor
        :return: tensorflow.Tensor
        """
        strides = (1,) + self.strides + (1,)
        outputs = nn.separable_conv2d(
            inputs,
            self.quantizer.quantize(
                self.depthwise_kernel),
            self.quantizer.quantize(
                self.pointwise_kernel),
            strides=strides,
            padding=self.padding.upper(),
            rate=self.dilation_rate,
            data_format=conv_utils.convert_data_format(self.data_format, ndim=4))

        if self.use_bias:
            outputs = nn.bias_add(
                outputs,
                self.bias,
                data_format=conv_utils.convert_data_format(self.data_format, ndim=4))

        return outputs


class BaseQuantizedActivation(layers.Activation):
    """
    Base class for quantized activation layers
    """

    def __init__(self, activation, **kwargs):
        super().__init__(activation=activation, **kwargs)


class ActivationDiscreteRelu(BaseQuantizedActivation):
    """A discrete ReLU Keras Activation

    Activations will be quantized and will have 2^bitwidth values in the range
    [0,6]
    """
    def __init__(self, bitwidth=1, **kwargs):
        """Creates a discrete ReLU for the specified bitwidth

        :param bitwidth: the activation bitwidth
        :type bitwidth: integer
        """
        levels = 2.**bitwidth - 1
        self.relumax_ = min(levels, 6)
        self.bitwidth = bitwidth
        self.gamma_k = self.relumax_ / levels
        self.t0_k = 0.5 * self.relumax_ / levels
        self.step = (2.**bitwidth * self.gamma_k) / 16
        # Legacy parameters, used by cnn2snn.keras2akida: they might be removed
        # later
        self.scale_factor = levels / self.relumax_
        self.threshold = self.t0_k

        super().__init__(activation=self.activation, **kwargs)

    def activation(self, x):
        """Evaluates the activations for the specified input Tensor

        :param x: the input values
        :type x: tensorflow.Tensor
        """
        ceiled_scaled = ceil_through(x / self.gamma_k - 0.5)
        return K.clip(self.gamma_k * ceiled_scaled, 0, self.relumax_)


# A helper to instantiate a Conv2D layer to which a modifier is assigned
def conv2d(filters, kernel_size, modifier=None, **kwargs):
    layer = QuantizedConv2D(filters, kernel_size, quantizer=modifier, **kwargs)
    return layer

# A helper to instantiate a Dense layer to which a modifier is assigned
def dense(units, modifier=None, **kwargs):
    layer = QuantizedDense(units, quantizer=modifier, **kwargs)
    return layer

# A helper to instantiate a Depthwise Conv2D layer to which a modifier is assigned
def depthwise_conv2d(kernel_size, modifier=None, **kwargs):
    layer = QuantizedDepthwiseConv2D(kernel_size, quantizer=modifier, **kwargs)
    return layer

def separable_conv2d(filters, kernel_size, modifier=None, **kwargs):
    layer = QuantizedSeparableConv2D(filters, kernel_size, quantizer=modifier, **kwargs)
    return layer

def batchNormalization(*args, **kwargs):
    return layers.BatchNormalization(*args, **kwargs)


def maxPooling2D(*args, **kwargs):
    return layers.MaxPooling2D(*args, **kwargs)


def activationFloat(type='relu'):
    return lambda **kwargs: layers.Activation(type, **kwargs)


def activationDiscreteRelu(bitwidth=1, **kwargs):
    return ActivationDiscreteRelu(bitwidth, **kwargs)

def activationDiscreteReluBits(bitwidth=1):
    return lambda **kwargs: activationDiscreteRelu(bitwidth, **kwargs)

def batchNormalization(*args, **kwargs):
    return layers.BatchNormalization(*args, **kwargs)
