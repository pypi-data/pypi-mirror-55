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
            fp, pathname, description = imp.find_module('_training8_', [dirname(__file__)])
        except ImportError:
            import _training8_
            return _training8_
        if fp is not None:
            try:
                _mod = imp.load_module('_training8_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training8_ = swig_import_helper()
    del swig_import_helper
else:
    import _training8_
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


import daal.algorithms.decision_tree.regression
import daal.algorithms.decision_tree
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.regression
import daal.algorithms.regression.training

_training8_.defaultDense_swigconstant(_training8_)
defaultDense = _training8_.defaultDense

_training8_.data_swigconstant(_training8_)
data = _training8_.data

_training8_.dependentVariables_swigconstant(_training8_)
dependentVariables = _training8_.dependentVariables

_training8_.dataForPruning_swigconstant(_training8_)
dataForPruning = _training8_.dataForPruning

_training8_.dependentVariablesForPruning_swigconstant(_training8_)
dependentVariablesForPruning = _training8_.dependentVariablesForPruning

_training8_.weights_swigconstant(_training8_)
weights = _training8_.weights

_training8_.lastInputId_swigconstant(_training8_)
lastInputId = _training8_.lastInputId

_training8_.model_swigconstant(_training8_)
model = _training8_.model

_training8_.lastResultId_swigconstant(_training8_)
lastResultId = _training8_.lastResultId
class Input(daal.algorithms.regression.training.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.regression.training.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.regression.training.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training8_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training8_.Input_get(self, id)

    def set(self, id, value):
        return _training8_.Input_set(self, id, value)

    def getNumberOfFeatures(self):
        return _training8_.Input_getNumberOfFeatures(self)

    def getNumberOfDependentVariables(self):
        return _training8_.Input_getNumberOfDependentVariables(self)

    def check(self, parameter, method):
        return _training8_.Input_check(self, parameter, method)
    __swig_destroy__ = _training8_.delete_Input
    __del__ = lambda self: None
Input_swigregister = _training8_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.regression.training.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.regression.training.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.regression.training.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training8_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training8_.Result_serializationTag)

    def getSerializationTag(self):
        return _training8_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training8_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training8_.Result_get(self, id)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training8_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training8_.Result_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _training8_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _training8_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training8_.Result_serializationTag()
Result_serializationTag = _training8_.Result_serializationTag

class Batch_Float64DefaultDense(daal.algorithms.regression.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.regression.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.regression.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training8_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _training8_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training8_.Batch_Float64DefaultDense_input_get, _training8_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _training8_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training8_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training8_.Batch_Float64DefaultDense_parameter_get, _training8_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _training8_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getInput(self):
        return _training8_.Batch_Float64DefaultDense_getInput(self)

    def getMethod(self):
        return _training8_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _training8_.Batch_Float64DefaultDense_getResult(self)

    def resetResult(self):
        return _training8_.Batch_Float64DefaultDense_resetResult(self)

    def clone(self):
        return _training8_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _training8_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _training8_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _training8_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.regression.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.regression.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.regression.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training8_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _training8_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training8_.Batch_Float32DefaultDense_input_get, _training8_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _training8_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training8_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training8_.Batch_Float32DefaultDense_parameter_get, _training8_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _training8_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getInput(self):
        return _training8_.Batch_Float32DefaultDense_getInput(self)

    def getMethod(self):
        return _training8_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _training8_.Batch_Float32DefaultDense_getResult(self)

    def resetResult(self):
        return _training8_.Batch_Float32DefaultDense_resetResult(self)

    def clone(self):
        return _training8_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _training8_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _training8_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _training8_.Batch_Float32DefaultDense_swigregister
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


