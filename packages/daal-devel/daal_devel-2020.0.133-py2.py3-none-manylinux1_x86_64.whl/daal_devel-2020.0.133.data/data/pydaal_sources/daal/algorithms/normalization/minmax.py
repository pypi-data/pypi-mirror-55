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
            fp, pathname, description = imp.find_module('_minmax_', [dirname(__file__)])
        except ImportError:
            import _minmax_
            return _minmax_
        if fp is not None:
            try:
                _mod = imp.load_module('_minmax_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _minmax_ = swig_import_helper()
    del swig_import_helper
else:
    import _minmax_
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


import daal.algorithms.low_order_moments
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_minmax_.defaultDense_swigconstant(_minmax_)
defaultDense = _minmax_.defaultDense

_minmax_.data_swigconstant(_minmax_)
data = _minmax_.data

_minmax_.lastInputId_swigconstant(_minmax_)
lastInputId = _minmax_.lastInputId

_minmax_.normalizedData_swigconstant(_minmax_)
normalizedData = _minmax_.normalizedData

_minmax_.lastResultId_swigconstant(_minmax_)
lastResultId = _minmax_.lastResultId
class ParameterBase(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ParameterBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ParameterBase, name)
    __repr__ = _swig_repr

    def __init__(self, lowerBound, upperBound, momentsForParameterBase):
        this = _minmax_.new_ParameterBase(lowerBound, upperBound, momentsForParameterBase)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["lowerBound"] = _minmax_.ParameterBase_lowerBound_set
    __swig_getmethods__["lowerBound"] = _minmax_.ParameterBase_lowerBound_get
    if _newclass:
        lowerBound = _swig_property(_minmax_.ParameterBase_lowerBound_get, _minmax_.ParameterBase_lowerBound_set)
    __swig_setmethods__["upperBound"] = _minmax_.ParameterBase_upperBound_set
    __swig_getmethods__["upperBound"] = _minmax_.ParameterBase_upperBound_get
    if _newclass:
        upperBound = _swig_property(_minmax_.ParameterBase_upperBound_get, _minmax_.ParameterBase_upperBound_set)
    __swig_setmethods__["moments"] = _minmax_.ParameterBase_moments_set
    __swig_getmethods__["moments"] = _minmax_.ParameterBase_moments_get
    if _newclass:
        moments = _swig_property(_minmax_.ParameterBase_moments_get, _minmax_.ParameterBase_moments_set)

    def check(self):
        return _minmax_.ParameterBase_check(self)
    __swig_destroy__ = _minmax_.delete_ParameterBase
    __del__ = lambda self: None
ParameterBase_swigregister = _minmax_.ParameterBase_swigregister
ParameterBase_swigregister(ParameterBase)

class Input(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _minmax_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _minmax_.Input_get(self, id)

    def set(self, id, ptr):
        return _minmax_.Input_set(self, id, ptr)

    def check(self, par, method):
        return _minmax_.Input_check(self, par, method)
Input_swigregister = _minmax_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _minmax_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_minmax_.Result_serializationTag)

    def getSerializationTag(self):
        return _minmax_.Result_getSerializationTag(self)

    def __init__(self):
        this = _minmax_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _minmax_.Result_get(self, id)

    def set(self, id, value):
        return _minmax_.Result_set(self, id, value)

    def check(self, arg2, par, method):
        return _minmax_.Result_check(self, arg2, par, method)

    def allocate_Float64(self, input, method):
        r"""
    This function is specialized for float64"""
        return _minmax_.Result_allocate_Float64(self, input, method)


    def allocate_Float32(self, input, method):
        r"""
    This function is specialized for float32"""
        return _minmax_.Result_allocate_Float32(self, input, method)

Result_swigregister = _minmax_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _minmax_.Result_serializationTag()
Result_serializationTag = _minmax_.Result_serializationTag

class Parameter_Float64(ParameterBase):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float64, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _minmax_.new_Parameter_Float64(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Parameter_Float64
    __del__ = lambda self: None
Parameter_Float64_swigregister = _minmax_.Parameter_Float64_swigregister
Parameter_Float64_swigregister(Parameter_Float64)

class Parameter_Float32(ParameterBase):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float32, name, value)
    __swig_getmethods__ = {}
    for _s in [ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float32, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _minmax_.new_Parameter_Float32(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Parameter_Float32
    __del__ = lambda self: None
Parameter_Float32_swigregister = _minmax_.Parameter_Float32_swigregister
Parameter_Float32_swigregister(Parameter_Float32)

class Batch_Float64DefaultDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _minmax_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _minmax_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_minmax_.Batch_Float64DefaultDense_input_get, _minmax_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _minmax_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _minmax_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_minmax_.Batch_Float64DefaultDense_parameter_get, _minmax_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _minmax_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _minmax_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _minmax_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _minmax_.Batch_Float64DefaultDense_setResult(self, result)

    def clone(self):
        return _minmax_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _minmax_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _minmax_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _minmax_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _minmax_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_minmax_.Batch_Float32DefaultDense_input_get, _minmax_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _minmax_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _minmax_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_minmax_.Batch_Float32DefaultDense_parameter_get, _minmax_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _minmax_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _minmax_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _minmax_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _minmax_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _minmax_.Batch_Float32DefaultDense_setResult(self, result)

    def clone(self):
        return _minmax_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _minmax_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _minmax_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

from numpy import float64, float32, intc

class Parameter(object):
    r"""Factory class for different types of Parameter."""
    def __new__(cls,
                fptype,
                *args, **kwargs):
        if fptype == float64:
            return Parameter_Float64(*args)
        if fptype == float32:
            return Parameter_Float32(*args)

        raise RuntimeError("No appropriate constructor found for Parameter")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


