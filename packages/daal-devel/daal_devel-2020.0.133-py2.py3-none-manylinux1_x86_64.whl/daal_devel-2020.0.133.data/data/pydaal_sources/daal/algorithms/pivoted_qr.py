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
            fp, pathname, description = imp.find_module('_pivoted_qr_', [dirname(__file__)])
        except ImportError:
            import _pivoted_qr_
            return _pivoted_qr_
        if fp is not None:
            try:
                _mod = imp.load_module('_pivoted_qr_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pivoted_qr_ = swig_import_helper()
    del swig_import_helper
else:
    import _pivoted_qr_
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


import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_pivoted_qr_.defaultDense_swigconstant(_pivoted_qr_)
defaultDense = _pivoted_qr_.defaultDense

_pivoted_qr_.data_swigconstant(_pivoted_qr_)
data = _pivoted_qr_.data

_pivoted_qr_.lastInputId_swigconstant(_pivoted_qr_)
lastInputId = _pivoted_qr_.lastInputId

_pivoted_qr_.matrixQ_swigconstant(_pivoted_qr_)
matrixQ = _pivoted_qr_.matrixQ

_pivoted_qr_.matrixR_swigconstant(_pivoted_qr_)
matrixR = _pivoted_qr_.matrixR

_pivoted_qr_.permutationMatrix_swigconstant(_pivoted_qr_)
permutationMatrix = _pivoted_qr_.permutationMatrix

_pivoted_qr_.lastResultId_swigconstant(_pivoted_qr_)
lastResultId = _pivoted_qr_.lastResultId
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

    def __init__(self, *args):
        this = _pivoted_qr_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["permutedColumns"] = _pivoted_qr_.Parameter_permutedColumns_set
    __swig_getmethods__["permutedColumns"] = _pivoted_qr_.Parameter_permutedColumns_get
    if _newclass:
        permutedColumns = _swig_property(_pivoted_qr_.Parameter_permutedColumns_get, _pivoted_qr_.Parameter_permutedColumns_set)
    __swig_destroy__ = _pivoted_qr_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _pivoted_qr_.Parameter_swigregister
Parameter_swigregister(Parameter)

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
        this = _pivoted_qr_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pivoted_qr_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _pivoted_qr_.Input_get(self, id)

    def set(self, id, value):
        return _pivoted_qr_.Input_set(self, id, value)

    def check(self, par, method):
        return _pivoted_qr_.Input_check(self, par, method)
Input_swigregister = _pivoted_qr_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _pivoted_qr_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_pivoted_qr_.Result_serializationTag)

    def getSerializationTag(self):
        return _pivoted_qr_.Result_getSerializationTag(self)

    def __init__(self):
        this = _pivoted_qr_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pivoted_qr_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _pivoted_qr_.Result_get(self, id)

    def set(self, id, value):
        return _pivoted_qr_.Result_set(self, id, value)

    def check(self, arg2, par, method):
        return _pivoted_qr_.Result_check(self, arg2, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _pivoted_qr_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _pivoted_qr_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _pivoted_qr_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _pivoted_qr_.Result_serializationTag()
Result_serializationTag = _pivoted_qr_.Result_serializationTag

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
    __swig_setmethods__["input"] = _pivoted_qr_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _pivoted_qr_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_pivoted_qr_.Batch_Float64DefaultDense_input_get, _pivoted_qr_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _pivoted_qr_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _pivoted_qr_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pivoted_qr_.Batch_Float64DefaultDense_parameter_get, _pivoted_qr_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _pivoted_qr_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _pivoted_qr_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _pivoted_qr_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, res):
        return _pivoted_qr_.Batch_Float64DefaultDense_setResult(self, res)

    def clone(self):
        return _pivoted_qr_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _pivoted_qr_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _pivoted_qr_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _pivoted_qr_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _pivoted_qr_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _pivoted_qr_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_pivoted_qr_.Batch_Float32DefaultDense_input_get, _pivoted_qr_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _pivoted_qr_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _pivoted_qr_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pivoted_qr_.Batch_Float32DefaultDense_parameter_get, _pivoted_qr_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _pivoted_qr_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _pivoted_qr_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _pivoted_qr_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, res):
        return _pivoted_qr_.Batch_Float32DefaultDense_setResult(self, res)

    def clone(self):
        return _pivoted_qr_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _pivoted_qr_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _pivoted_qr_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _pivoted_qr_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

from numpy import float64, float32, intc

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


