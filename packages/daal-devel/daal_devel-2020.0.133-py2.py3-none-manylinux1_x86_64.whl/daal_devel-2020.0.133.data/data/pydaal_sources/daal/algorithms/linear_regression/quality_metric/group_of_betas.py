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
            fp, pathname, description = imp.find_module('_group_of_betas_', [dirname(__file__)])
        except ImportError:
            import _group_of_betas_
            return _group_of_betas_
        if fp is not None:
            try:
                _mod = imp.load_module('_group_of_betas_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _group_of_betas_ = swig_import_helper()
    del swig_import_helper
else:
    import _group_of_betas_
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

_group_of_betas_.defaultDense_swigconstant(_group_of_betas_)
defaultDense = _group_of_betas_.defaultDense

_group_of_betas_.expectedResponses_swigconstant(_group_of_betas_)
expectedResponses = _group_of_betas_.expectedResponses

_group_of_betas_.predictedResponses_swigconstant(_group_of_betas_)
predictedResponses = _group_of_betas_.predictedResponses

_group_of_betas_.predictedReducedModelResponses_swigconstant(_group_of_betas_)
predictedReducedModelResponses = _group_of_betas_.predictedReducedModelResponses

_group_of_betas_.lastDataInputId_swigconstant(_group_of_betas_)
lastDataInputId = _group_of_betas_.lastDataInputId

_group_of_betas_.expectedMeans_swigconstant(_group_of_betas_)
expectedMeans = _group_of_betas_.expectedMeans

_group_of_betas_.expectedVariance_swigconstant(_group_of_betas_)
expectedVariance = _group_of_betas_.expectedVariance

_group_of_betas_.regSS_swigconstant(_group_of_betas_)
regSS = _group_of_betas_.regSS

_group_of_betas_.resSS_swigconstant(_group_of_betas_)
resSS = _group_of_betas_.resSS

_group_of_betas_.tSS_swigconstant(_group_of_betas_)
tSS = _group_of_betas_.tSS

_group_of_betas_.determinationCoeff_swigconstant(_group_of_betas_)
determinationCoeff = _group_of_betas_.determinationCoeff

_group_of_betas_.fStatistics_swigconstant(_group_of_betas_)
fStatistics = _group_of_betas_.fStatistics

_group_of_betas_.lastResultId_swigconstant(_group_of_betas_)
lastResultId = _group_of_betas_.lastResultId
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

    def __init__(self, nBeta, nBetaReducedModel):
        this = _group_of_betas_.new_Parameter(nBeta, nBetaReducedModel)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _group_of_betas_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["numBeta"] = _group_of_betas_.Parameter_numBeta_set
    __swig_getmethods__["numBeta"] = _group_of_betas_.Parameter_numBeta_get
    if _newclass:
        numBeta = _swig_property(_group_of_betas_.Parameter_numBeta_get, _group_of_betas_.Parameter_numBeta_set)
    __swig_setmethods__["numBetaReducedModel"] = _group_of_betas_.Parameter_numBetaReducedModel_set
    __swig_getmethods__["numBetaReducedModel"] = _group_of_betas_.Parameter_numBetaReducedModel_get
    if _newclass:
        numBetaReducedModel = _swig_property(_group_of_betas_.Parameter_numBetaReducedModel_get, _group_of_betas_.Parameter_numBetaReducedModel_set)
    __swig_setmethods__["accuracyThreshold"] = _group_of_betas_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _group_of_betas_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_group_of_betas_.Parameter_accuracyThreshold_get, _group_of_betas_.Parameter_accuracyThreshold_set)

    def check(self):
        return _group_of_betas_.Parameter_check(self)
Parameter_swigregister = _group_of_betas_.Parameter_swigregister
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
    __swig_getmethods__["downCast"] = lambda x: _group_of_betas_.Input_downCast
    if _newclass:
        downCast = staticmethod(_group_of_betas_.Input_downCast)

    def __init__(self):
        this = _group_of_betas_.new_Input()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _group_of_betas_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _group_of_betas_.Input_get(self, id)

    def set(self, id, value):
        return _group_of_betas_.Input_set(self, id, value)

    def check(self, par, method):
        return _group_of_betas_.Input_check(self, par, method)
Input_swigregister = _group_of_betas_.Input_swigregister
Input_swigregister(Input)

def Input_downCast(r):
    return _group_of_betas_.Input_downCast(r)
Input_downCast = _group_of_betas_.Input_downCast

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
    __swig_getmethods__["downCast"] = lambda x: _group_of_betas_.Result_downCast
    if _newclass:
        downCast = staticmethod(_group_of_betas_.Result_downCast)

    def __init__(self):
        this = _group_of_betas_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _group_of_betas_.Result_get(self, id)

    def set(self, id, value):
        return _group_of_betas_.Result_set(self, id, value)

    def check(self, input, par, method):
        return _group_of_betas_.Result_check(self, input, par, method)

    def getSerializationTag(self):
        return _group_of_betas_.Result_getSerializationTag(self)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _group_of_betas_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _group_of_betas_.Result_allocate_Float32(self, input, par, method)

    __swig_destroy__ = _group_of_betas_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _group_of_betas_.Result_swigregister
Result_swigregister(Result)

def Result_downCast(r):
    return _group_of_betas_.Result_downCast(r)
Result_downCast = _group_of_betas_.Result_downCast

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
    __swig_setmethods__["input"] = _group_of_betas_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _group_of_betas_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_group_of_betas_.Batch_Float64DefaultDense_input_get, _group_of_betas_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _group_of_betas_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _group_of_betas_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_group_of_betas_.Batch_Float64DefaultDense_parameter_get, _group_of_betas_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _group_of_betas_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _group_of_betas_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _group_of_betas_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _group_of_betas_.Batch_Float64DefaultDense_setResult(self, result)

    def setInput(self, other):
        return _group_of_betas_.Batch_Float64DefaultDense_setInput(self, other)

    def clone(self):
        return _group_of_betas_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _group_of_betas_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _group_of_betas_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _group_of_betas_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _group_of_betas_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _group_of_betas_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_group_of_betas_.Batch_Float32DefaultDense_input_get, _group_of_betas_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _group_of_betas_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _group_of_betas_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_group_of_betas_.Batch_Float32DefaultDense_parameter_get, _group_of_betas_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _group_of_betas_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _group_of_betas_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _group_of_betas_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _group_of_betas_.Batch_Float32DefaultDense_setResult(self, result)

    def setInput(self, other):
        return _group_of_betas_.Batch_Float32DefaultDense_setInput(self, other)

    def clone(self):
        return _group_of_betas_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _group_of_betas_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _group_of_betas_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _group_of_betas_.Batch_Float32DefaultDense_swigregister
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


