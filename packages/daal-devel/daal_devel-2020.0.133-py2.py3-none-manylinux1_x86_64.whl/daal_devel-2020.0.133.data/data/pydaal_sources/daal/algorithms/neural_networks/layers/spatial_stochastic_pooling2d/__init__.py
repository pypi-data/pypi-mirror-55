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
            fp, pathname, description = imp.find_module('_spatial_stochastic_pooling2d_', [dirname(__file__)])
        except ImportError:
            import _spatial_stochastic_pooling2d_
            return _spatial_stochastic_pooling2d_
        if fp is not None:
            try:
                _mod = imp.load_module('_spatial_stochastic_pooling2d_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _spatial_stochastic_pooling2d_ = swig_import_helper()
    del swig_import_helper
else:
    import _spatial_stochastic_pooling2d_
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


import daal.algorithms.neural_networks.layers.spatial_pooling2d
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
import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_spatial_stochastic_pooling2d_.defaultDense_swigconstant(_spatial_stochastic_pooling2d_)
defaultDense = _spatial_stochastic_pooling2d_.defaultDense

_spatial_stochastic_pooling2d_.auxSelectedIndices_swigconstant(_spatial_stochastic_pooling2d_)
auxSelectedIndices = _spatial_stochastic_pooling2d_.auxSelectedIndices

_spatial_stochastic_pooling2d_.lastLayerDataId_swigconstant(_spatial_stochastic_pooling2d_)
lastLayerDataId = _spatial_stochastic_pooling2d_.lastLayerDataId

_spatial_stochastic_pooling2d_.auxInputDimensions_swigconstant(_spatial_stochastic_pooling2d_)
auxInputDimensions = _spatial_stochastic_pooling2d_.auxInputDimensions

_spatial_stochastic_pooling2d_.lastLayerDataNumericTableId_swigconstant(_spatial_stochastic_pooling2d_)
lastLayerDataNumericTableId = _spatial_stochastic_pooling2d_.lastLayerDataNumericTableId
class Parameter(daal.algorithms.neural_networks.layers.spatial_pooling2d.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.spatial_pooling2d.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.spatial_pooling2d.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, pyramidHeight, firstIndex, secondIndex):
        this = _spatial_stochastic_pooling2d_.new_Parameter(pyramidHeight, firstIndex, secondIndex)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["seed"] = _spatial_stochastic_pooling2d_.Parameter_seed_set
    __swig_getmethods__["seed"] = _spatial_stochastic_pooling2d_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_spatial_stochastic_pooling2d_.Parameter_seed_get, _spatial_stochastic_pooling2d_.Parameter_seed_set)
    __swig_setmethods__["engine"] = _spatial_stochastic_pooling2d_.Parameter_engine_set
    __swig_getmethods__["engine"] = _spatial_stochastic_pooling2d_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_spatial_stochastic_pooling2d_.Parameter_engine_get, _spatial_stochastic_pooling2d_.Parameter_engine_set)
    __swig_destroy__ = _spatial_stochastic_pooling2d_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _spatial_stochastic_pooling2d_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Batch_Float64DefaultDense(daal.algorithms.neural_networks.layers.LayerIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.LayerIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.LayerIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _spatial_stochastic_pooling2d_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _spatial_stochastic_pooling2d_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_spatial_stochastic_pooling2d_.Batch_Float64DefaultDense_parameter_get, _spatial_stochastic_pooling2d_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, pyramidHeight, nDimensions):
        this = _spatial_stochastic_pooling2d_.new_Batch_Float64DefaultDense(pyramidHeight, nDimensions)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _spatial_stochastic_pooling2d_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _spatial_stochastic_pooling2d_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.neural_networks.layers.LayerIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.LayerIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.LayerIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _spatial_stochastic_pooling2d_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _spatial_stochastic_pooling2d_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_spatial_stochastic_pooling2d_.Batch_Float32DefaultDense_parameter_get, _spatial_stochastic_pooling2d_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, pyramidHeight, nDimensions):
        this = _spatial_stochastic_pooling2d_.new_Batch_Float32DefaultDense(pyramidHeight, nDimensions)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _spatial_stochastic_pooling2d_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _spatial_stochastic_pooling2d_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' in kwargs and kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
        if 'fptype' not in kwargs or kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


from . import backward
from . import forward

# This file is compatible with both classic and new-style classes.


