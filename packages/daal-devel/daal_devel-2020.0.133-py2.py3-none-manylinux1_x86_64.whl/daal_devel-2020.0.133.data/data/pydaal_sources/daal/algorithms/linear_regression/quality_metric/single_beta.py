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
            fp, pathname, description = imp.find_module('_single_beta_', [dirname(__file__)])
        except ImportError:
            import _single_beta_
            return _single_beta_
        if fp is not None:
            try:
                _mod = imp.load_module('_single_beta_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _single_beta_ = swig_import_helper()
    del swig_import_helper
else:
    import _single_beta_
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


import daal.algorithms.linear_regression
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.linear_model
import daal.algorithms.regression
import daal.algorithms.quality_metric

_single_beta_.defaultDense_swigconstant(_single_beta_)
defaultDense = _single_beta_.defaultDense

_single_beta_.expectedResponses_swigconstant(_single_beta_)
expectedResponses = _single_beta_.expectedResponses

_single_beta_.predictedResponses_swigconstant(_single_beta_)
predictedResponses = _single_beta_.predictedResponses

_single_beta_.lastDataInputId_swigconstant(_single_beta_)
lastDataInputId = _single_beta_.lastDataInputId

_single_beta_.model_swigconstant(_single_beta_)
model = _single_beta_.model

_single_beta_.lastModelInputId_swigconstant(_single_beta_)
lastModelInputId = _single_beta_.lastModelInputId

_single_beta_.rms_swigconstant(_single_beta_)
rms = _single_beta_.rms

_single_beta_.variance_swigconstant(_single_beta_)
variance = _single_beta_.variance

_single_beta_.zScore_swigconstant(_single_beta_)
zScore = _single_beta_.zScore

_single_beta_.confidenceIntervals_swigconstant(_single_beta_)
confidenceIntervals = _single_beta_.confidenceIntervals

_single_beta_.inverseOfXtX_swigconstant(_single_beta_)
inverseOfXtX = _single_beta_.inverseOfXtX

_single_beta_.lastResultId_swigconstant(_single_beta_)
lastResultId = _single_beta_.lastResultId

_single_beta_.betaCovariances_swigconstant(_single_beta_)
betaCovariances = _single_beta_.betaCovariances

_single_beta_.lastResultDataCollectionId_swigconstant(_single_beta_)
lastResultDataCollectionId = _single_beta_.lastResultDataCollectionId
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

    def __init__(self, alphaVal=0.05, accuracyVal=0.001):
        this = _single_beta_.new_Parameter(alphaVal, accuracyVal)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _single_beta_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["alpha"] = _single_beta_.Parameter_alpha_set
    __swig_getmethods__["alpha"] = _single_beta_.Parameter_alpha_get
    if _newclass:
        alpha = _swig_property(_single_beta_.Parameter_alpha_get, _single_beta_.Parameter_alpha_set)
    __swig_setmethods__["accuracyThreshold"] = _single_beta_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _single_beta_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_single_beta_.Parameter_accuracyThreshold_get, _single_beta_.Parameter_accuracyThreshold_set)

    def check(self):
        return _single_beta_.Parameter_check(self)
Parameter_swigregister = _single_beta_.Parameter_swigregister
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
    __swig_getmethods__["downCast"] = lambda x: _single_beta_.Input_downCast
    if _newclass:
        downCast = staticmethod(_single_beta_.Input_downCast)

    def __init__(self):
        this = _single_beta_.new_Input()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _single_beta_.delete_Input
    __del__ = lambda self: None

    def getDataInput(self, id):
        return _single_beta_.Input_getDataInput(self, id)

    def setDataInput(self, id, value):
        return _single_beta_.Input_setDataInput(self, id, value)

    def getModelInput(self, id):
        return _single_beta_.Input_getModelInput(self, id)

    def setModelInput(self, id, value):
        return _single_beta_.Input_setModelInput(self, id, value)

    def check(self, par, method):
        return _single_beta_.Input_check(self, par, method)
Input_swigregister = _single_beta_.Input_swigregister
Input_swigregister(Input)

def Input_downCast(r):
    return _single_beta_.Input_downCast(r)
Input_downCast = _single_beta_.Input_downCast

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
    __swig_getmethods__["downCast"] = lambda x: _single_beta_.Result_downCast
    if _newclass:
        downCast = staticmethod(_single_beta_.Result_downCast)

    def __init__(self):
        this = _single_beta_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getResult(self, id):
        return _single_beta_.Result_getResult(self, id)

    def setResult(self, id, value):
        return _single_beta_.Result_setResult(self, id, value)

    def getResultDataCollection(self, id):
        return _single_beta_.Result_getResultDataCollection(self, id)

    def get(self, id, index):
        return _single_beta_.Result_get(self, id, index)

    def setResultDataCollection(self, id, value):
        return _single_beta_.Result_setResultDataCollection(self, id, value)

    def check(self, input, par, method):
        return _single_beta_.Result_check(self, input, par, method)

    def getSerializationTag(self):
        return _single_beta_.Result_getSerializationTag(self)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _single_beta_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _single_beta_.Result_allocate_Float32(self, input, par, method)

    __swig_destroy__ = _single_beta_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _single_beta_.Result_swigregister
Result_swigregister(Result)

def Result_downCast(r):
    return _single_beta_.Result_downCast(r)
Result_downCast = _single_beta_.Result_downCast

class Batch_Float64DefaultDense(daal.algorithms.quality_metric.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.quality_metric.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.quality_metric.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _single_beta_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _single_beta_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_single_beta_.Batch_Float64DefaultDense_input_get, _single_beta_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _single_beta_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _single_beta_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_single_beta_.Batch_Float64DefaultDense_parameter_get, _single_beta_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _single_beta_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _single_beta_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _single_beta_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _single_beta_.Batch_Float64DefaultDense_setResult(self, result)

    def setInput(self, other):
        return _single_beta_.Batch_Float64DefaultDense_setInput(self, other)

    def clone(self):
        return _single_beta_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _single_beta_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _single_beta_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _single_beta_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.quality_metric.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.quality_metric.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.quality_metric.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _single_beta_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _single_beta_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_single_beta_.Batch_Float32DefaultDense_input_get, _single_beta_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _single_beta_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _single_beta_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_single_beta_.Batch_Float32DefaultDense_parameter_get, _single_beta_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _single_beta_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _single_beta_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _single_beta_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _single_beta_.Batch_Float32DefaultDense_setResult(self, result)

    def setInput(self, other):
        return _single_beta_.Batch_Float32DefaultDense_setInput(self, other)

    def clone(self):
        return _single_beta_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _single_beta_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _single_beta_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _single_beta_.Batch_Float32DefaultDense_swigregister
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


