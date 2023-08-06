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
            fp, pathname, description = imp.find_module('_backward7_', [dirname(__file__)])
        except ImportError:
            import _backward7_
            return _backward7_
        if fp is not None:
            try:
                _mod = imp.load_module('_backward7_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _backward7_ = swig_import_helper()
    del swig_import_helper
else:
    import _backward7_
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


import daal.algorithms.neural_networks.layers.backward
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
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines
import daal.algorithms.neural_networks.layers.convolution2d
class Input(daal.algorithms.neural_networks.layers.backward.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _backward7_.new_Input()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _backward7_.delete_Input
    __del__ = lambda self: None

    def getLayerData(self, id):
        return _backward7_.Input_getLayerData(self, id)

    def setLayerData(self, id, value):
        return _backward7_.Input_setLayerData(self, id, value)

    def check(self, parameter, method):
        return _backward7_.Input_check(self, parameter, method)
Input_swigregister = _backward7_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.neural_networks.layers.backward.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _backward7_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_backward7_.Result_serializationTag)

    def getSerializationTag(self):
        return _backward7_.Result_getSerializationTag(self)

    def __init__(self):
        this = _backward7_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _backward7_.delete_Result
    __del__ = lambda self: None

    def check(self, input, par, method):
        return _backward7_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _backward7_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _backward7_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _backward7_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _backward7_.Result_serializationTag()
Result_serializationTag = _backward7_.Result_serializationTag

class Batch_Float64DefaultDense(daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _backward7_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _backward7_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_backward7_.Batch_Float64DefaultDense_parameter_get, _backward7_.Batch_Float64DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _backward7_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _backward7_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_backward7_.Batch_Float64DefaultDense_input_get, _backward7_.Batch_Float64DefaultDense_input_set)

    def __init__(self, *args):
        this = _backward7_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _backward7_.Batch_Float64DefaultDense_getMethod(self)

    def getLayerInput(self):
        return _backward7_.Batch_Float64DefaultDense_getLayerInput(self)

    def getLayerParameter(self):
        return _backward7_.Batch_Float64DefaultDense_getLayerParameter(self)

    def getLayerResult(self):
        return _backward7_.Batch_Float64DefaultDense_getLayerResult(self)

    def getResult(self):
        return _backward7_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _backward7_.Batch_Float64DefaultDense_setResult(self, result)

    def clone(self):
        return _backward7_.Batch_Float64DefaultDense_clone(self)

    def allocateResult(self):
        return _backward7_.Batch_Float64DefaultDense_allocateResult(self)

    def compute(self):
        return _backward7_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _backward7_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _backward7_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.backward.LayerIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _backward7_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _backward7_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_backward7_.Batch_Float32DefaultDense_parameter_get, _backward7_.Batch_Float32DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _backward7_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _backward7_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_backward7_.Batch_Float32DefaultDense_input_get, _backward7_.Batch_Float32DefaultDense_input_set)

    def __init__(self, *args):
        this = _backward7_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _backward7_.Batch_Float32DefaultDense_getMethod(self)

    def getLayerInput(self):
        return _backward7_.Batch_Float32DefaultDense_getLayerInput(self)

    def getLayerParameter(self):
        return _backward7_.Batch_Float32DefaultDense_getLayerParameter(self)

    def getLayerResult(self):
        return _backward7_.Batch_Float32DefaultDense_getLayerResult(self)

    def getResult(self):
        return _backward7_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _backward7_.Batch_Float32DefaultDense_setResult(self, result)

    def clone(self):
        return _backward7_.Batch_Float32DefaultDense_clone(self)

    def allocateResult(self):
        return _backward7_.Batch_Float32DefaultDense_allocateResult(self)

    def compute(self):
        return _backward7_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _backward7_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _backward7_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' in kwargs and kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == daal.algorithms.neural_networks.layers.convolution2d.defaultDense:
                return Batch_Float64DefaultDense(*args)
        if 'fptype' not in kwargs or kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == daal.algorithms.neural_networks.layers.convolution2d.defaultDense:
                return Batch_Float32DefaultDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


