# Copyright 2014-2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_layers_', [dirname(__file__)])
        except ImportError:
            import _layers_
            return _layers_
        if fp is not None:
            try:
                _mod = imp.load_module('_layers_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _layers_ = swig_import_helper()
    del swig_import_helper
else:
    import _layers_
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0


try:
    import weakref
    weakref_proxy = weakref.proxy
except:
    weakref_proxy = lambda x: x


import daal.algorithms.neural_networks.initializers
import daal.algorithms.neural_networks
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_layers_.tensorInput_swigconstant(_layers_)
tensorInput = _layers_.tensorInput

_layers_.collectionInput_swigconstant(_layers_)
collectionInput = _layers_.collectionInput

_layers_.lastLayerInputLayout_swigconstant(_layers_)
lastLayerInputLayout = _layers_.lastLayerInputLayout

_layers_.tensorResult_swigconstant(_layers_)
tensorResult = _layers_.tensorResult

_layers_.collectionResult_swigconstant(_layers_)
collectionResult = _layers_.collectionResult

_layers_.lastLayerResultLayout_swigconstant(_layers_)
lastLayerResultLayout = _layers_.lastLayerResultLayout
class Parameter(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _layers_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["weightsInitializer"] = _layers_.Parameter_weightsInitializer_set
    __swig_getmethods__["weightsInitializer"] = _layers_.Parameter_weightsInitializer_get
    if _newclass:
        weightsInitializer = _swig_property(_layers_.Parameter_weightsInitializer_get, _layers_.Parameter_weightsInitializer_set)
    __swig_setmethods__["biasesInitializer"] = _layers_.Parameter_biasesInitializer_set
    __swig_getmethods__["biasesInitializer"] = _layers_.Parameter_biasesInitializer_get
    if _newclass:
        biasesInitializer = _swig_property(_layers_.Parameter_biasesInitializer_get, _layers_.Parameter_biasesInitializer_set)
    __swig_setmethods__["predictionStage"] = _layers_.Parameter_predictionStage_set
    __swig_getmethods__["predictionStage"] = _layers_.Parameter_predictionStage_get
    if _newclass:
        predictionStage = _swig_property(_layers_.Parameter_predictionStage_get, _layers_.Parameter_predictionStage_set)
    __swig_setmethods__["propagateGradient"] = _layers_.Parameter_propagateGradient_set
    __swig_getmethods__["propagateGradient"] = _layers_.Parameter_propagateGradient_get
    if _newclass:
        propagateGradient = _swig_property(_layers_.Parameter_propagateGradient_get, _layers_.Parameter_propagateGradient_set)
    __swig_setmethods__["weightsAndBiasesInitialized"] = _layers_.Parameter_weightsAndBiasesInitialized_set
    __swig_getmethods__["weightsAndBiasesInitialized"] = _layers_.Parameter_weightsAndBiasesInitialized_get
    if _newclass:
        weightsAndBiasesInitialized = _swig_property(_layers_.Parameter_weightsAndBiasesInitialized_get, _layers_.Parameter_weightsAndBiasesInitialized_set)
    __swig_setmethods__["allowInplaceComputation"] = _layers_.Parameter_allowInplaceComputation_set
    __swig_getmethods__["allowInplaceComputation"] = _layers_.Parameter_allowInplaceComputation_get
    if _newclass:
        allowInplaceComputation = _swig_property(_layers_.Parameter_allowInplaceComputation_get, _layers_.Parameter_allowInplaceComputation_set)
    __swig_destroy__ = _layers_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _layers_.Parameter_swigregister
Parameter_swigregister(Parameter)

class NextLayers(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, NextLayers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, NextLayers, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _layers_.new_NextLayers(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _layers_.delete_NextLayers
    __del__ = lambda self: None

    def size(self):
        return _layers_.NextLayers_size(self)

    def push_back(self, index):
        return _layers_.NextLayers_push_back(self, index)

    def add(self, index):
        return _layers_.NextLayers_add(self, index)

    def __getitem__(self, i):
        return _layers_.NextLayers___getitem__(self, i)

    def __setitem__(self, i, v):
        return _layers_.NextLayers___setitem__(self, i, v)
NextLayers_swigregister = _layers_.NextLayers_swigregister
NextLayers_swigregister(NextLayers)

class LayerDescriptor(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerDescriptor, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LayerDescriptor, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _layers_.new_LayerDescriptor(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def index(self):
        return _layers_.LayerDescriptor_index(self)

    def addNext(self, index):
        return _layers_.LayerDescriptor_addNext(self, index)

    def layer(self):
        return _layers_.LayerDescriptor_layer(self)

    def nextLayers(self):
        return _layers_.LayerDescriptor_nextLayers(self)
    __swig_destroy__ = _layers_.delete_LayerDescriptor
    __del__ = lambda self: None
LayerDescriptor_swigregister = _layers_.LayerDescriptor_swigregister
LayerDescriptor_swigregister(LayerDescriptor)

class LayerIface(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LayerIface, name)
    __repr__ = _swig_repr
    __swig_setmethods__["forwardLayer"] = _layers_.LayerIface_forwardLayer_set
    __swig_getmethods__["forwardLayer"] = _layers_.LayerIface_forwardLayer_get
    if _newclass:
        forwardLayer = _swig_property(_layers_.LayerIface_forwardLayer_get, _layers_.LayerIface_forwardLayer_set)
    __swig_setmethods__["backwardLayer"] = _layers_.LayerIface_backwardLayer_set
    __swig_getmethods__["backwardLayer"] = _layers_.LayerIface_backwardLayer_get
    if _newclass:
        backwardLayer = _swig_property(_layers_.LayerIface_backwardLayer_get, _layers_.LayerIface_backwardLayer_set)

    def __init__(self):
        this = _layers_.new_LayerIface()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _layers_.delete_LayerIface
    __del__ = lambda self: None
LayerIface_swigregister = _layers_.LayerIface_swigregister
LayerIface_swigregister(LayerIface)

from numpy import float64, float32, intc


LayerData = daal.data_management.KeyValueDataCollection

from . import abs
from . import average_pooling1d
from . import average_pooling2d
from . import average_pooling3d
from . import backward
from . import batch_normalization
from . import concat
from . import convolution2d
from . import dropout
from . import eltwise_sum
from . import elu
from . import forward
from . import fullyconnected
from . import lcn
from . import locallyconnected2d
from . import logistic
from . import loss
from . import lrn
from . import maximum_pooling1d
from . import maximum_pooling2d
from . import maximum_pooling3d
from . import pooling1d
from . import pooling2d
from . import pooling3d
from . import prelu
from . import relu
from . import reshape
from . import smoothrelu
from . import softmax
from . import spatial_average_pooling2d
from . import spatial_maximum_pooling2d
from . import spatial_pooling2d
from . import spatial_stochastic_pooling2d
from . import split
from . import stochastic_pooling2d
from . import tanh
from . import transposed_conv2d

# This file is compatible with both classic and new-style classes.


