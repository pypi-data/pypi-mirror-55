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
            fp, pathname, description = imp.find_module('_init_', [dirname(__file__)])
        except ImportError:
            import _init_
            return _init_
        if fp is not None:
            try:
                _mod = imp.load_module('_init_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _init_ = swig_import_helper()
    del swig_import_helper
else:
    import _init_
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


import daal.algorithms.engines.mt19937
import daal.algorithms.engines
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_init_.data_swigconstant(_init_)
data = _init_.data

_init_.lastInputId_swigconstant(_init_)
lastInputId = _init_.lastInputId

_init_.weights_swigconstant(_init_)
weights = _init_.weights

_init_.means_swigconstant(_init_)
means = _init_.means

_init_.lastResultId_swigconstant(_init_)
lastResultId = _init_.lastResultId

_init_.covariances_swigconstant(_init_)
covariances = _init_.covariances

_init_.lastResultCovariancesId_swigconstant(_init_)
lastResultCovariancesId = _init_.lastResultCovariancesId

_init_.defaultDense_swigconstant(_init_)
defaultDense = _init_.defaultDense
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
        this = _init_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init_.delete_Parameter
    __del__ = lambda self: None

    def check(self):
        return _init_.Parameter_check(self)
    __swig_setmethods__["nComponents"] = _init_.Parameter_nComponents_set
    __swig_getmethods__["nComponents"] = _init_.Parameter_nComponents_get
    if _newclass:
        nComponents = _swig_property(_init_.Parameter_nComponents_get, _init_.Parameter_nComponents_set)
    __swig_setmethods__["nTrials"] = _init_.Parameter_nTrials_set
    __swig_getmethods__["nTrials"] = _init_.Parameter_nTrials_get
    if _newclass:
        nTrials = _swig_property(_init_.Parameter_nTrials_get, _init_.Parameter_nTrials_set)
    __swig_setmethods__["nIterations"] = _init_.Parameter_nIterations_set
    __swig_getmethods__["nIterations"] = _init_.Parameter_nIterations_get
    if _newclass:
        nIterations = _swig_property(_init_.Parameter_nIterations_get, _init_.Parameter_nIterations_set)
    __swig_setmethods__["seed"] = _init_.Parameter_seed_set
    __swig_getmethods__["seed"] = _init_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_init_.Parameter_seed_get, _init_.Parameter_seed_set)
    __swig_setmethods__["accuracyThreshold"] = _init_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _init_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_init_.Parameter_accuracyThreshold_get, _init_.Parameter_accuracyThreshold_set)
    __swig_setmethods__["covarianceStorage"] = _init_.Parameter_covarianceStorage_set
    __swig_getmethods__["covarianceStorage"] = _init_.Parameter_covarianceStorage_get
    if _newclass:
        covarianceStorage = _swig_property(_init_.Parameter_covarianceStorage_get, _init_.Parameter_covarianceStorage_set)
    __swig_setmethods__["engine"] = _init_.Parameter_engine_set
    __swig_getmethods__["engine"] = _init_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_init_.Parameter_engine_get, _init_.Parameter_engine_set)
Parameter_swigregister = _init_.Parameter_swigregister
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
        this = _init_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init_.delete_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _init_.Input_set(self, id, ptr)

    def get(self, id):
        return _init_.Input_get(self, id)

    def check(self, par, method):
        return _init_.Input_check(self, par, method)
Input_swigregister = _init_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _init_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init_.Result_serializationTag)

    def getSerializationTag(self):
        return _init_.Result_getSerializationTag(self)

    def __init__(self):
        this = _init_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init_.delete_Result
    __del__ = lambda self: None

    def setResult(self, id, ptr):
        return _init_.Result_setResult(self, id, ptr)

    def setCovariances(self, id, ptr):
        return _init_.Result_setCovariances(self, id, ptr)

    def getResult(self, id):
        return _init_.Result_getResult(self, id)

    def getCovariances(self, *args):
        return _init_.Result_getCovariances(self, *args)

    def check(self, input, par, method):
        return _init_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _init_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _init_.Result_serializationTag()
Result_serializationTag = _init_.Result_serializationTag

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

    def __init__(self, *args):
        this = _init_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init_.Batch_Float64DefaultDense_getMethod(self)

    def setResult(self, result):
        return _init_.Batch_Float64DefaultDense_setResult(self, result)

    def getResult(self):
        return _init_.Batch_Float64DefaultDense_getResult(self)

    def clone(self):
        return _init_.Batch_Float64DefaultDense_clone(self)
    __swig_setmethods__["input"] = _init_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _init_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_init_.Batch_Float64DefaultDense_input_get, _init_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _init_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _init_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init_.Batch_Float64DefaultDense_parameter_get, _init_.Batch_Float64DefaultDense_parameter_set)

    def compute(self):
        return _init_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _init_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _init_.Batch_Float64DefaultDense_swigregister
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

    def __init__(self, *args):
        this = _init_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init_.Batch_Float32DefaultDense_getMethod(self)

    def setResult(self, result):
        return _init_.Batch_Float32DefaultDense_setResult(self, result)

    def getResult(self):
        return _init_.Batch_Float32DefaultDense_getResult(self)

    def clone(self):
        return _init_.Batch_Float32DefaultDense_clone(self)
    __swig_setmethods__["input"] = _init_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _init_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_init_.Batch_Float32DefaultDense_input_get, _init_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _init_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _init_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init_.Batch_Float32DefaultDense_parameter_get, _init_.Batch_Float32DefaultDense_parameter_set)

    def compute(self):
        return _init_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _init_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _init_.Batch_Float32DefaultDense_swigregister
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


