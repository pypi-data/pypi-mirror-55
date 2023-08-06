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
            fp, pathname, description = imp.find_module('_transposed_conv2d_', [dirname(__file__)])
        except ImportError:
            import _transposed_conv2d_
            return _transposed_conv2d_
        if fp is not None:
            try:
                _mod = imp.load_module('_transposed_conv2d_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _transposed_conv2d_ = swig_import_helper()
    del swig_import_helper
else:
    import _transposed_conv2d_
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


import daal.algorithms.neural_networks.layers
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

_transposed_conv2d_.defaultDense_swigconstant(_transposed_conv2d_)
defaultDense = _transposed_conv2d_.defaultDense

_transposed_conv2d_.auxData_swigconstant(_transposed_conv2d_)
auxData = _transposed_conv2d_.auxData

_transposed_conv2d_.auxWeights_swigconstant(_transposed_conv2d_)
auxWeights = _transposed_conv2d_.auxWeights

_transposed_conv2d_.lastLayerDataId_swigconstant(_transposed_conv2d_)
lastLayerDataId = _transposed_conv2d_.lastLayerDataId
class KernelSizes(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KernelSizes, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KernelSizes, name)
    __repr__ = _swig_repr

    def __init__(self, first, second):
        this = _transposed_conv2d_.new_KernelSizes(first, second)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _transposed_conv2d_.KernelSizes_size_set
    __swig_getmethods__["size"] = _transposed_conv2d_.KernelSizes_size_get
    if _newclass:
        size = _swig_property(_transposed_conv2d_.KernelSizes_size_get, _transposed_conv2d_.KernelSizes_size_set)
    __swig_destroy__ = _transposed_conv2d_.delete_KernelSizes
    __del__ = lambda self: None
KernelSizes_swigregister = _transposed_conv2d_.KernelSizes_swigregister
KernelSizes_swigregister(KernelSizes)

class Strides(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Strides, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Strides, name)
    __repr__ = _swig_repr

    def __init__(self, first, second):
        this = _transposed_conv2d_.new_Strides(first, second)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _transposed_conv2d_.Strides_size_set
    __swig_getmethods__["size"] = _transposed_conv2d_.Strides_size_get
    if _newclass:
        size = _swig_property(_transposed_conv2d_.Strides_size_get, _transposed_conv2d_.Strides_size_set)
    __swig_destroy__ = _transposed_conv2d_.delete_Strides
    __del__ = lambda self: None
Strides_swigregister = _transposed_conv2d_.Strides_swigregister
Strides_swigregister(Strides)

class Paddings(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Paddings, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Paddings, name)
    __repr__ = _swig_repr

    def __init__(self, first, second):
        this = _transposed_conv2d_.new_Paddings(first, second)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _transposed_conv2d_.Paddings_size_set
    __swig_getmethods__["size"] = _transposed_conv2d_.Paddings_size_get
    if _newclass:
        size = _swig_property(_transposed_conv2d_.Paddings_size_get, _transposed_conv2d_.Paddings_size_set)
    __swig_destroy__ = _transposed_conv2d_.delete_Paddings
    __del__ = lambda self: None
Paddings_swigregister = _transposed_conv2d_.Paddings_swigregister
Paddings_swigregister(Paddings)

class Indices(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Indices, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Indices, name)
    __repr__ = _swig_repr

    def __init__(self, first, second):
        this = _transposed_conv2d_.new_Indices(first, second)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["dims"] = _transposed_conv2d_.Indices_dims_set
    __swig_getmethods__["dims"] = _transposed_conv2d_.Indices_dims_get
    if _newclass:
        dims = _swig_property(_transposed_conv2d_.Indices_dims_get, _transposed_conv2d_.Indices_dims_set)
    __swig_destroy__ = _transposed_conv2d_.delete_Indices
    __del__ = lambda self: None
Indices_swigregister = _transposed_conv2d_.Indices_swigregister
Indices_swigregister(Indices)

class ValueSizes(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ValueSizes, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ValueSizes, name)
    __repr__ = _swig_repr

    def __init__(self, first, second):
        this = _transposed_conv2d_.new_ValueSizes(first, second)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _transposed_conv2d_.ValueSizes_size_set
    __swig_getmethods__["size"] = _transposed_conv2d_.ValueSizes_size_get
    if _newclass:
        size = _swig_property(_transposed_conv2d_.ValueSizes_size_get, _transposed_conv2d_.ValueSizes_size_set)
    __swig_destroy__ = _transposed_conv2d_.delete_ValueSizes
    __del__ = lambda self: None
ValueSizes_swigregister = _transposed_conv2d_.ValueSizes_swigregister
ValueSizes_swigregister(ValueSizes)

class Parameter(daal.algorithms.neural_networks.layers.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _transposed_conv2d_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["indices"] = _transposed_conv2d_.Parameter_indices_set
    __swig_getmethods__["indices"] = _transposed_conv2d_.Parameter_indices_get
    if _newclass:
        indices = _swig_property(_transposed_conv2d_.Parameter_indices_get, _transposed_conv2d_.Parameter_indices_set)
    __swig_setmethods__["groupDimension"] = _transposed_conv2d_.Parameter_groupDimension_set
    __swig_getmethods__["groupDimension"] = _transposed_conv2d_.Parameter_groupDimension_get
    if _newclass:
        groupDimension = _swig_property(_transposed_conv2d_.Parameter_groupDimension_get, _transposed_conv2d_.Parameter_groupDimension_set)
    __swig_setmethods__["kernelSizes"] = _transposed_conv2d_.Parameter_kernelSizes_set
    __swig_getmethods__["kernelSizes"] = _transposed_conv2d_.Parameter_kernelSizes_get
    if _newclass:
        kernelSizes = _swig_property(_transposed_conv2d_.Parameter_kernelSizes_get, _transposed_conv2d_.Parameter_kernelSizes_set)
    __swig_setmethods__["strides"] = _transposed_conv2d_.Parameter_strides_set
    __swig_getmethods__["strides"] = _transposed_conv2d_.Parameter_strides_get
    if _newclass:
        strides = _swig_property(_transposed_conv2d_.Parameter_strides_get, _transposed_conv2d_.Parameter_strides_set)
    __swig_setmethods__["paddings"] = _transposed_conv2d_.Parameter_paddings_set
    __swig_getmethods__["paddings"] = _transposed_conv2d_.Parameter_paddings_get
    if _newclass:
        paddings = _swig_property(_transposed_conv2d_.Parameter_paddings_get, _transposed_conv2d_.Parameter_paddings_set)
    __swig_setmethods__["nKernels"] = _transposed_conv2d_.Parameter_nKernels_set
    __swig_getmethods__["nKernels"] = _transposed_conv2d_.Parameter_nKernels_get
    if _newclass:
        nKernels = _swig_property(_transposed_conv2d_.Parameter_nKernels_get, _transposed_conv2d_.Parameter_nKernels_set)
    __swig_setmethods__["nGroups"] = _transposed_conv2d_.Parameter_nGroups_set
    __swig_getmethods__["nGroups"] = _transposed_conv2d_.Parameter_nGroups_get
    if _newclass:
        nGroups = _swig_property(_transposed_conv2d_.Parameter_nGroups_get, _transposed_conv2d_.Parameter_nGroups_set)
    __swig_setmethods__["valueSizes"] = _transposed_conv2d_.Parameter_valueSizes_set
    __swig_getmethods__["valueSizes"] = _transposed_conv2d_.Parameter_valueSizes_get
    if _newclass:
        valueSizes = _swig_property(_transposed_conv2d_.Parameter_valueSizes_get, _transposed_conv2d_.Parameter_valueSizes_set)
    __swig_destroy__ = _transposed_conv2d_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _transposed_conv2d_.Parameter_swigregister
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
    __swig_setmethods__["parameter"] = _transposed_conv2d_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _transposed_conv2d_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_transposed_conv2d_.Batch_Float64DefaultDense_parameter_get, _transposed_conv2d_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self):
        this = _transposed_conv2d_.new_Batch_Float64DefaultDense()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _transposed_conv2d_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _transposed_conv2d_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["parameter"] = _transposed_conv2d_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _transposed_conv2d_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_transposed_conv2d_.Batch_Float32DefaultDense_parameter_get, _transposed_conv2d_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self):
        this = _transposed_conv2d_.new_Batch_Float32DefaultDense()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _transposed_conv2d_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _transposed_conv2d_.Batch_Float32DefaultDense_swigregister
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


