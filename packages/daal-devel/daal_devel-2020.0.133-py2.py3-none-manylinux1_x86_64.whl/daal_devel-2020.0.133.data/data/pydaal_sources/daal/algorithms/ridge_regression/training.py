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
            fp, pathname, description = imp.find_module('_training22_', [dirname(__file__)])
        except ImportError:
            import _training22_
            return _training22_
        if fp is not None:
            try:
                _mod = imp.load_module('_training22_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training22_ = swig_import_helper()
    del swig_import_helper
else:
    import _training22_
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


import daal.algorithms.ridge_regression
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.linear_model
import daal.algorithms.regression
import daal.algorithms.linear_model.training
import daal.algorithms.regression.training

_training22_.defaultDense_swigconstant(_training22_)
defaultDense = _training22_.defaultDense

_training22_.normEqDense_swigconstant(_training22_)
normEqDense = _training22_.normEqDense

_training22_.data_swigconstant(_training22_)
data = _training22_.data

_training22_.dependentVariables_swigconstant(_training22_)
dependentVariables = _training22_.dependentVariables

_training22_.lastInputId_swigconstant(_training22_)
lastInputId = _training22_.lastInputId

_training22_.partialModels_swigconstant(_training22_)
partialModels = _training22_.partialModels

_training22_.lastStep2MasterInputId_swigconstant(_training22_)
lastStep2MasterInputId = _training22_.lastStep2MasterInputId

_training22_.partialModel_swigconstant(_training22_)
partialModel = _training22_.partialModel

_training22_.lastPartialResultID_swigconstant(_training22_)
lastPartialResultID = _training22_.lastPartialResultID

_training22_.model_swigconstant(_training22_)
model = _training22_.model

_training22_.lastResultId_swigconstant(_training22_)
lastResultId = _training22_.lastResultId
class InputIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, InputIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getNumberOfFeatures(self):
        return _training22_.InputIface_getNumberOfFeatures(self)

    def getNumberOfDependentVariables(self):
        return _training22_.InputIface_getNumberOfDependentVariables(self)
    __swig_destroy__ = _training22_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _training22_.InputIface_swigregister
InputIface_swigregister(InputIface)

class Input(daal.algorithms.linear_model.training.Input, InputIface):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Input, InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Input, InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _training22_.Input_get(self, id)

    def set(self, id, value):
        return _training22_.Input_set(self, id, value)

    def getNumberOfFeatures(self):
        return _training22_.Input_getNumberOfFeatures(self)

    def getNumberOfDependentVariables(self):
        return _training22_.Input_getNumberOfDependentVariables(self)

    def check(self, par, method):
        return _training22_.Input_check(self, par, method)
Input_swigregister = _training22_.Input_swigregister
Input_swigregister(Input)

class PartialResult(daal.algorithms.linear_model.training.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training22_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training22_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _training22_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _training22_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getPartialResult(self, id):
        return _training22_.PartialResult_getPartialResult(self, id)

    def getNumberOfFeatures(self):
        return _training22_.PartialResult_getNumberOfFeatures(self)

    def getNumberOfDependentVariables(self):
        return _training22_.PartialResult_getNumberOfDependentVariables(self)

    def setPartialResult(self, id, value):
        return _training22_.PartialResult_setPartialResult(self, id, value)

    def check(self, *args):
        return _training22_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training22_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training22_.PartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training22_.PartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training22_.PartialResult_initialize_Float32(self, input, parameter, method)

    __swig_destroy__ = _training22_.delete_PartialResult
    __del__ = lambda self: None
PartialResult_swigregister = _training22_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _training22_.PartialResult_serializationTag()
PartialResult_serializationTag = _training22_.PartialResult_serializationTag

class Result(daal.algorithms.linear_model.training.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training22_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training22_.Result_serializationTag)

    def getSerializationTag(self):
        return _training22_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training22_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training22_.Result_get(self, id)

    def set(self, id, value):
        return _training22_.Result_set(self, id, value)

    def check(self, *args):
        return _training22_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _training22_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _training22_.Result_allocate_Float32(self, *args)

    __swig_destroy__ = _training22_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _training22_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training22_.Result_serializationTag()
Result_serializationTag = _training22_.Result_serializationTag

class DistributedInput_Step1Local(_object):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step1Local, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step1Local, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _training22_.new_DistributedInput_Step1Local()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None
DistributedInput_Step1Local_swigregister = _training22_.DistributedInput_Step1Local_swigregister
DistributedInput_Step1Local_swigregister(DistributedInput_Step1Local)

class DistributedInput_Step2Master(daal.algorithms.Input, InputIface):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input, InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step2Master, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input, InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step2Master, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_DistributedInput_Step2Master(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training22_.DistributedInput_Step2Master_get(self, id)

    def set(self, id, ptr):
        return _training22_.DistributedInput_Step2Master_set(self, id, ptr)

    def add(self, id, partialResult):
        return _training22_.DistributedInput_Step2Master_add(self, id, partialResult)

    def getNumberOfFeatures(self):
        return _training22_.DistributedInput_Step2Master_getNumberOfFeatures(self)

    def getNumberOfDependentVariables(self):
        return _training22_.DistributedInput_Step2Master_getNumberOfDependentVariables(self)

    def check(self, parameter, method):
        return _training22_.DistributedInput_Step2Master_check(self, parameter, method)
    __swig_destroy__ = _training22_.delete_DistributedInput_Step2Master
    __del__ = lambda self: None
DistributedInput_Step2Master_swigregister = _training22_.DistributedInput_Step2Master_swigregister
DistributedInput_Step2Master_swigregister(DistributedInput_Step2Master)

class Batch_Float64NormEqDense(daal.algorithms.linear_model.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64NormEqDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training22_.Batch_Float64NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Batch_Float64NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Batch_Float64NormEqDense_input_get, _training22_.Batch_Float64NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Batch_Float64NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Batch_Float64NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Batch_Float64NormEqDense_parameter_get, _training22_.Batch_Float64NormEqDense_parameter_set)

    def __init__(self, *args):
        this = _training22_.new_Batch_Float64NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Batch_Float64NormEqDense
    __del__ = lambda self: None

    def getInput(self):
        return _training22_.Batch_Float64NormEqDense_getInput(self)

    def getMethod(self):
        return _training22_.Batch_Float64NormEqDense_getMethod(self)

    def getResult(self):
        return _training22_.Batch_Float64NormEqDense_getResult(self)

    def resetResult(self):
        return _training22_.Batch_Float64NormEqDense_resetResult(self)

    def clone(self):
        return _training22_.Batch_Float64NormEqDense_clone(self)

    def compute(self):
        return _training22_.Batch_Float64NormEqDense_compute(self)
Batch_Float64NormEqDense_swigregister = _training22_.Batch_Float64NormEqDense_swigregister
Batch_Float64NormEqDense_swigregister(Batch_Float64NormEqDense)

class Batch_Float32NormEqDense(daal.algorithms.linear_model.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32NormEqDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training22_.Batch_Float32NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Batch_Float32NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Batch_Float32NormEqDense_input_get, _training22_.Batch_Float32NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Batch_Float32NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Batch_Float32NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Batch_Float32NormEqDense_parameter_get, _training22_.Batch_Float32NormEqDense_parameter_set)

    def __init__(self, *args):
        this = _training22_.new_Batch_Float32NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Batch_Float32NormEqDense
    __del__ = lambda self: None

    def getInput(self):
        return _training22_.Batch_Float32NormEqDense_getInput(self)

    def getMethod(self):
        return _training22_.Batch_Float32NormEqDense_getMethod(self)

    def getResult(self):
        return _training22_.Batch_Float32NormEqDense_getResult(self)

    def resetResult(self):
        return _training22_.Batch_Float32NormEqDense_resetResult(self)

    def clone(self):
        return _training22_.Batch_Float32NormEqDense_clone(self)

    def compute(self):
        return _training22_.Batch_Float32NormEqDense_compute(self)
Batch_Float32NormEqDense_swigregister = _training22_.Batch_Float32NormEqDense_swigregister
Batch_Float32NormEqDense_swigregister(Batch_Float32NormEqDense)

class Online_Float64NormEqDense(daal.algorithms.linear_model.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64NormEqDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training22_.Online_Float64NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Online_Float64NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Online_Float64NormEqDense_input_get, _training22_.Online_Float64NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Online_Float64NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Online_Float64NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Online_Float64NormEqDense_parameter_get, _training22_.Online_Float64NormEqDense_parameter_set)

    def __init__(self, *args):
        this = _training22_.new_Online_Float64NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Online_Float64NormEqDense
    __del__ = lambda self: None

    def getInput(self):
        return _training22_.Online_Float64NormEqDense_getInput(self)

    def getMethod(self):
        return _training22_.Online_Float64NormEqDense_getMethod(self)

    def getPartialResult(self):
        return _training22_.Online_Float64NormEqDense_getPartialResult(self)

    def getResult(self):
        return _training22_.Online_Float64NormEqDense_getResult(self)

    def clone(self):
        return _training22_.Online_Float64NormEqDense_clone(self)

    def compute(self):
        return _training22_.Online_Float64NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Online_Float64NormEqDense_finalizeCompute(self)
Online_Float64NormEqDense_swigregister = _training22_.Online_Float64NormEqDense_swigregister
Online_Float64NormEqDense_swigregister(Online_Float64NormEqDense)

class Online_Float32NormEqDense(daal.algorithms.linear_model.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32NormEqDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training22_.Online_Float32NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Online_Float32NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Online_Float32NormEqDense_input_get, _training22_.Online_Float32NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Online_Float32NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Online_Float32NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Online_Float32NormEqDense_parameter_get, _training22_.Online_Float32NormEqDense_parameter_set)

    def __init__(self, *args):
        this = _training22_.new_Online_Float32NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Online_Float32NormEqDense
    __del__ = lambda self: None

    def getInput(self):
        return _training22_.Online_Float32NormEqDense_getInput(self)

    def getMethod(self):
        return _training22_.Online_Float32NormEqDense_getMethod(self)

    def getPartialResult(self):
        return _training22_.Online_Float32NormEqDense_getPartialResult(self)

    def getResult(self):
        return _training22_.Online_Float32NormEqDense_getResult(self)

    def clone(self):
        return _training22_.Online_Float32NormEqDense_clone(self)

    def compute(self):
        return _training22_.Online_Float32NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Online_Float32NormEqDense_finalizeCompute(self)
Online_Float32NormEqDense_swigregister = _training22_.Online_Float32NormEqDense_swigregister
Online_Float32NormEqDense_swigregister(Online_Float32NormEqDense)

class Distributed_Step1LocalFloat64NormEqDense(Online_Float64NormEqDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64NormEqDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64NormEqDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64NormEqDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_Distributed_Step1LocalFloat64NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Distributed_Step1LocalFloat64NormEqDense
    __del__ = lambda self: None

    def clone(self):
        return _training22_.Distributed_Step1LocalFloat64NormEqDense_clone(self)

    def compute(self):
        return _training22_.Distributed_Step1LocalFloat64NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Distributed_Step1LocalFloat64NormEqDense_finalizeCompute(self)
Distributed_Step1LocalFloat64NormEqDense_swigregister = _training22_.Distributed_Step1LocalFloat64NormEqDense_swigregister
Distributed_Step1LocalFloat64NormEqDense_swigregister(Distributed_Step1LocalFloat64NormEqDense)

class Distributed_Step1LocalFloat32NormEqDense(Online_Float32NormEqDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32NormEqDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32NormEqDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32NormEqDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_Distributed_Step1LocalFloat32NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Distributed_Step1LocalFloat32NormEqDense
    __del__ = lambda self: None

    def clone(self):
        return _training22_.Distributed_Step1LocalFloat32NormEqDense_clone(self)

    def compute(self):
        return _training22_.Distributed_Step1LocalFloat32NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Distributed_Step1LocalFloat32NormEqDense_finalizeCompute(self)
Distributed_Step1LocalFloat32NormEqDense_swigregister = _training22_.Distributed_Step1LocalFloat32NormEqDense_swigregister
Distributed_Step1LocalFloat32NormEqDense_swigregister(Distributed_Step1LocalFloat32NormEqDense)

class Distributed_Step2MasterFloat64NormEqDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64NormEqDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_Distributed_Step2MasterFloat64NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Distributed_Step2MasterFloat64NormEqDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_getPartialResult(self)

    def setResult(self, res):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_setResult(self, res)

    def getResult(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_getResult(self)

    def clone(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_clone(self)
    __swig_setmethods__["input"] = _training22_.Distributed_Step2MasterFloat64NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Distributed_Step2MasterFloat64NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Distributed_Step2MasterFloat64NormEqDense_input_get, _training22_.Distributed_Step2MasterFloat64NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Distributed_Step2MasterFloat64NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Distributed_Step2MasterFloat64NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Distributed_Step2MasterFloat64NormEqDense_parameter_get, _training22_.Distributed_Step2MasterFloat64NormEqDense_parameter_set)

    def compute(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Distributed_Step2MasterFloat64NormEqDense_finalizeCompute(self)
Distributed_Step2MasterFloat64NormEqDense_swigregister = _training22_.Distributed_Step2MasterFloat64NormEqDense_swigregister
Distributed_Step2MasterFloat64NormEqDense_swigregister(Distributed_Step2MasterFloat64NormEqDense)

class Distributed_Step2MasterFloat32NormEqDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32NormEqDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32NormEqDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training22_.new_Distributed_Step2MasterFloat32NormEqDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training22_.delete_Distributed_Step2MasterFloat32NormEqDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_getPartialResult(self)

    def setResult(self, res):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_setResult(self, res)

    def getResult(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_getResult(self)

    def clone(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_clone(self)
    __swig_setmethods__["input"] = _training22_.Distributed_Step2MasterFloat32NormEqDense_input_set
    __swig_getmethods__["input"] = _training22_.Distributed_Step2MasterFloat32NormEqDense_input_get
    if _newclass:
        input = _swig_property(_training22_.Distributed_Step2MasterFloat32NormEqDense_input_get, _training22_.Distributed_Step2MasterFloat32NormEqDense_input_set)
    __swig_setmethods__["parameter"] = _training22_.Distributed_Step2MasterFloat32NormEqDense_parameter_set
    __swig_getmethods__["parameter"] = _training22_.Distributed_Step2MasterFloat32NormEqDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training22_.Distributed_Step2MasterFloat32NormEqDense_parameter_get, _training22_.Distributed_Step2MasterFloat32NormEqDense_parameter_set)

    def compute(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_compute(self)

    def finalizeCompute(self):
        return _training22_.Distributed_Step2MasterFloat32NormEqDense_finalizeCompute(self)
Distributed_Step2MasterFloat32NormEqDense_swigregister = _training22_.Distributed_Step2MasterFloat32NormEqDense_swigregister
Distributed_Step2MasterFloat32NormEqDense_swigregister(Distributed_Step2MasterFloat32NormEqDense)

from numpy import float64, float32, intc

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            return DistributedInput_Step1Local(*args)
        if step == daal.step2Master:
            return DistributedInput_Step2Master(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == normEqDense:
                        return Distributed_Step1LocalFloat64NormEqDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == normEqDense:
                        return Distributed_Step1LocalFloat32NormEqDense(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == normEqDense:
                        return Distributed_Step2MasterFloat64NormEqDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == normEqDense:
                        return Distributed_Step2MasterFloat32NormEqDense(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == normEqDense:
                return Batch_Float64NormEqDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == normEqDense:
                return Batch_Float32NormEqDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")

class Online(object):
    r"""Factory class for different types of Online."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == normEqDense:
                return Online_Float64NormEqDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == normEqDense:
                return Online_Float32NormEqDense(*args)

        raise RuntimeError("No appropriate constructor found for Online")


# This file is compatible with both classic and new-style classes.


