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
            fp, pathname, description = imp.find_module('_zscore_', [dirname(__file__)])
        except ImportError:
            import _zscore_
            return _zscore_
        if fp is not None:
            try:
                _mod = imp.load_module('_zscore_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _zscore_ = swig_import_helper()
    del swig_import_helper
else:
    import _zscore_
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

_zscore_.defaultDense_swigconstant(_zscore_)
defaultDense = _zscore_.defaultDense

_zscore_.sumDense_swigconstant(_zscore_)
sumDense = _zscore_.sumDense

_zscore_.data_swigconstant(_zscore_)
data = _zscore_.data

_zscore_.lastInputId_swigconstant(_zscore_)
lastInputId = _zscore_.lastInputId

_zscore_.normalizedData_swigconstant(_zscore_)
normalizedData = _zscore_.normalizedData

_zscore_.means_swigconstant(_zscore_)
means = _zscore_.means

_zscore_.variances_swigconstant(_zscore_)
variances = _zscore_.variances

_zscore_.lastResultId_swigconstant(_zscore_)
lastResultId = _zscore_.lastResultId

_zscore_.none_swigconstant(_zscore_)
none = _zscore_.none

_zscore_.mean_swigconstant(_zscore_)
mean = _zscore_.mean

_zscore_.variance_swigconstant(_zscore_)
variance = _zscore_.variance
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
        this = _zscore_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _zscore_.Input_get(self, id)

    def set(self, id, ptr):
        return _zscore_.Input_set(self, id, ptr)

    def check(self, par, method):
        return _zscore_.Input_check(self, par, method)
Input_swigregister = _zscore_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _zscore_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_zscore_.Result_serializationTag)

    def getSerializationTag(self):
        return _zscore_.Result_getSerializationTag(self)

    def __init__(self, *args):
        this = _zscore_.new_Result(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _zscore_.Result_get(self, id)

    def set(self, id, value):
        return _zscore_.Result_set(self, id, value)

    def check(self, arg2, par, method):
        return _zscore_.Result_check(self, arg2, par, method)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _zscore_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _zscore_.Result_allocate_Float32(self, *args)

Result_swigregister = _zscore_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _zscore_.Result_serializationTag()
Result_serializationTag = _zscore_.Result_serializationTag

class BaseParameter(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BaseParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BaseParameter, name)
    __repr__ = _swig_repr

    def __init__(self, doScale=True):
        this = _zscore_.new_BaseParameter(doScale)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["resultsToCompute"] = _zscore_.BaseParameter_resultsToCompute_set
    __swig_getmethods__["resultsToCompute"] = _zscore_.BaseParameter_resultsToCompute_get
    if _newclass:
        resultsToCompute = _swig_property(_zscore_.BaseParameter_resultsToCompute_get, _zscore_.BaseParameter_resultsToCompute_set)
    __swig_setmethods__["doScale"] = _zscore_.BaseParameter_doScale_set
    __swig_getmethods__["doScale"] = _zscore_.BaseParameter_doScale_get
    if _newclass:
        doScale = _swig_property(_zscore_.BaseParameter_doScale_get, _zscore_.BaseParameter_doScale_set)
    __swig_destroy__ = _zscore_.delete_BaseParameter
    __del__ = lambda self: None
BaseParameter_swigregister = _zscore_.BaseParameter_swigregister
BaseParameter_swigregister(BaseParameter)

class BatchImpl(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getResult(self):
        return _zscore_.BatchImpl_getResult(self)

    def getParameter(self):
        return _zscore_.BatchImpl_getParameter(self)

    def parameter(self, *args):
        return _zscore_.BatchImpl_parameter(self, *args)

    def setResult(self, result):
        return _zscore_.BatchImpl_setResult(self, result)

    def clone(self):
        return _zscore_.BatchImpl_clone(self)
    __swig_destroy__ = _zscore_.delete_BatchImpl
    __del__ = lambda self: None
    __swig_setmethods__["input"] = _zscore_.BatchImpl_input_set
    __swig_getmethods__["input"] = _zscore_.BatchImpl_input_get
    if _newclass:
        input = _swig_property(_zscore_.BatchImpl_input_get, _zscore_.BatchImpl_input_set)
BatchImpl_swigregister = _zscore_.BatchImpl_swigregister
BatchImpl_swigregister(BatchImpl)

class Batch_Float64DefaultDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def parameter(self, *args):
        return _zscore_.Batch_Float64DefaultDense_parameter(self, *args)

    def getParameter(self):
        return _zscore_.Batch_Float64DefaultDense_getParameter(self)

    def getMethod(self):
        return _zscore_.Batch_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _zscore_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _zscore_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _zscore_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float64SumDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Batch_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Batch_Float64SumDense
    __del__ = lambda self: None

    def parameter(self, *args):
        return _zscore_.Batch_Float64SumDense_parameter(self, *args)

    def getParameter(self):
        return _zscore_.Batch_Float64SumDense_getParameter(self)

    def getMethod(self):
        return _zscore_.Batch_Float64SumDense_getMethod(self)

    def clone(self):
        return _zscore_.Batch_Float64SumDense_clone(self)

    def compute(self):
        return _zscore_.Batch_Float64SumDense_compute(self)
Batch_Float64SumDense_swigregister = _zscore_.Batch_Float64SumDense_swigregister
Batch_Float64SumDense_swigregister(Batch_Float64SumDense)

class Batch_Float32DefaultDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def parameter(self, *args):
        return _zscore_.Batch_Float32DefaultDense_parameter(self, *args)

    def getParameter(self):
        return _zscore_.Batch_Float32DefaultDense_getParameter(self)

    def getMethod(self):
        return _zscore_.Batch_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _zscore_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _zscore_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _zscore_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Batch_Float32SumDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Batch_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Batch_Float32SumDense
    __del__ = lambda self: None

    def parameter(self, *args):
        return _zscore_.Batch_Float32SumDense_parameter(self, *args)

    def getParameter(self):
        return _zscore_.Batch_Float32SumDense_getParameter(self)

    def getMethod(self):
        return _zscore_.Batch_Float32SumDense_getMethod(self)

    def clone(self):
        return _zscore_.Batch_Float32SumDense_clone(self)

    def compute(self):
        return _zscore_.Batch_Float32SumDense_compute(self)
Batch_Float32SumDense_swigregister = _zscore_.Batch_Float32SumDense_swigregister
Batch_Float32SumDense_swigregister(Batch_Float32SumDense)

class Parameter_Float64DefaultDense(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Parameter_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["moments"] = _zscore_.Parameter_Float64DefaultDense_moments_set
    __swig_getmethods__["moments"] = _zscore_.Parameter_Float64DefaultDense_moments_get
    if _newclass:
        moments = _swig_property(_zscore_.Parameter_Float64DefaultDense_moments_get, _zscore_.Parameter_Float64DefaultDense_moments_set)

    def check(self):
        return _zscore_.Parameter_Float64DefaultDense_check(self)
    __swig_destroy__ = _zscore_.delete_Parameter_Float64DefaultDense
    __del__ = lambda self: None
Parameter_Float64DefaultDense_swigregister = _zscore_.Parameter_Float64DefaultDense_swigregister
Parameter_Float64DefaultDense_swigregister(Parameter_Float64DefaultDense)

class Parameter_Float64SumDense(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Parameter_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Parameter_Float64SumDense
    __del__ = lambda self: None
Parameter_Float64SumDense_swigregister = _zscore_.Parameter_Float64SumDense_swigregister
Parameter_Float64SumDense_swigregister(Parameter_Float64SumDense)

class Parameter_Float32DefaultDense(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Parameter_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["moments"] = _zscore_.Parameter_Float32DefaultDense_moments_set
    __swig_getmethods__["moments"] = _zscore_.Parameter_Float32DefaultDense_moments_get
    if _newclass:
        moments = _swig_property(_zscore_.Parameter_Float32DefaultDense_moments_get, _zscore_.Parameter_Float32DefaultDense_moments_set)

    def check(self):
        return _zscore_.Parameter_Float32DefaultDense_check(self)
    __swig_destroy__ = _zscore_.delete_Parameter_Float32DefaultDense
    __del__ = lambda self: None
Parameter_Float32DefaultDense_swigregister = _zscore_.Parameter_Float32DefaultDense_swigregister
Parameter_Float32DefaultDense_swigregister(Parameter_Float32DefaultDense)

class Parameter_Float32SumDense(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _zscore_.new_Parameter_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _zscore_.delete_Parameter_Float32SumDense
    __del__ = lambda self: None
Parameter_Float32SumDense_swigregister = _zscore_.Parameter_Float32SumDense_swigregister
Parameter_Float32SumDense_swigregister(Parameter_Float32SumDense)

from numpy import float64, float32, intc

class Parameter(object):
    r"""Factory class for different types of Parameter."""
    def __new__(cls,
                fptype,
                method,
                *args, **kwargs):
        if fptype == float64:
            if method == defaultDense:
                return Parameter_Float64DefaultDense(*args)
            if method == sumDense:
                return Parameter_Float64SumDense(*args)
        if fptype == float32:
            if method == defaultDense:
                return Parameter_Float32DefaultDense(*args)
            if method == sumDense:
                return Parameter_Float32SumDense(*args)

        raise RuntimeError("No appropriate constructor found for Parameter")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Batch_Float64SumDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Batch_Float32SumDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


