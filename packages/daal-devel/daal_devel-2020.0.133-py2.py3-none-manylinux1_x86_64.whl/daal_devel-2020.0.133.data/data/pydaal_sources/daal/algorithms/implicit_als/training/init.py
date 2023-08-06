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
            fp, pathname, description = imp.find_module('_init1_', [dirname(__file__)])
        except ImportError:
            import _init1_
            return _init1_
        if fp is not None:
            try:
                _mod = imp.load_module('_init1_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _init1_ = swig_import_helper()
    del swig_import_helper
else:
    import _init1_
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


import daal.algorithms.implicit_als.training
import daal.algorithms.implicit_als
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_init1_.defaultDense_swigconstant(_init1_)
defaultDense = _init1_.defaultDense

_init1_.fastCSR_swigconstant(_init1_)
fastCSR = _init1_.fastCSR

_init1_.data_swigconstant(_init1_)
data = _init1_.data

_init1_.lastInputId_swigconstant(_init1_)
lastInputId = _init1_.lastInputId

_init1_.inputOfStep2FromStep1_swigconstant(_init1_)
inputOfStep2FromStep1 = _init1_.inputOfStep2FromStep1

_init1_.lastStep2LocalInputId_swigconstant(_init1_)
lastStep2LocalInputId = _init1_.lastStep2LocalInputId

_init1_.outputOfInitForComputeStep3_swigconstant(_init1_)
outputOfInitForComputeStep3 = _init1_.outputOfInitForComputeStep3

_init1_.offsets_swigconstant(_init1_)
offsets = _init1_.offsets

_init1_.lastPartialResultBaseId_swigconstant(_init1_)
lastPartialResultBaseId = _init1_.lastPartialResultBaseId

_init1_.partialModel_swigconstant(_init1_)
partialModel = _init1_.partialModel

_init1_.lastPartialResultId_swigconstant(_init1_)
lastPartialResultId = _init1_.lastPartialResultId

_init1_.outputOfStep1ForStep2_swigconstant(_init1_)
outputOfStep1ForStep2 = _init1_.outputOfStep1ForStep2

_init1_.lastPartialResultCollectionId_swigconstant(_init1_)
lastPartialResultCollectionId = _init1_.lastPartialResultCollectionId

_init1_.transposedData_swigconstant(_init1_)
transposedData = _init1_.transposedData

_init1_.lastDistributedPartialResultStep2Id_swigconstant(_init1_)
lastDistributedPartialResultStep2Id = _init1_.lastDistributedPartialResultStep2Id

_init1_.model_swigconstant(_init1_)
model = _init1_.model

_init1_.lastResultId_swigconstant(_init1_)
lastResultId = _init1_.lastResultId
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

    def __init__(self, nFactors=10, fullNUsers=0, seed=777777):
        this = _init1_.new_Parameter(nFactors, fullNUsers, seed)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nFactors"] = _init1_.Parameter_nFactors_set
    __swig_getmethods__["nFactors"] = _init1_.Parameter_nFactors_get
    if _newclass:
        nFactors = _swig_property(_init1_.Parameter_nFactors_get, _init1_.Parameter_nFactors_set)
    __swig_setmethods__["fullNUsers"] = _init1_.Parameter_fullNUsers_set
    __swig_getmethods__["fullNUsers"] = _init1_.Parameter_fullNUsers_get
    if _newclass:
        fullNUsers = _swig_property(_init1_.Parameter_fullNUsers_get, _init1_.Parameter_fullNUsers_set)
    __swig_setmethods__["seed"] = _init1_.Parameter_seed_set
    __swig_getmethods__["seed"] = _init1_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_init1_.Parameter_seed_get, _init1_.Parameter_seed_set)
    __swig_setmethods__["engine"] = _init1_.Parameter_engine_set
    __swig_getmethods__["engine"] = _init1_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_init1_.Parameter_engine_get, _init1_.Parameter_engine_set)

    def check(self):
        return _init1_.Parameter_check(self)
    __swig_destroy__ = _init1_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _init1_.Parameter_swigregister
Parameter_swigregister(Parameter)

class DistributedParameter(Parameter):
    __swig_setmethods__ = {}
    for _s in [Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter, name)
    __repr__ = _swig_repr

    def __init__(self, nFactors=10, fullNUsers=0, seed=777777):
        this = _init1_.new_DistributedParameter(nFactors, fullNUsers, seed)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["partition"] = _init1_.DistributedParameter_partition_set
    __swig_getmethods__["partition"] = _init1_.DistributedParameter_partition_get
    if _newclass:
        partition = _swig_property(_init1_.DistributedParameter_partition_get, _init1_.DistributedParameter_partition_set)

    def check(self):
        return _init1_.DistributedParameter_check(self)
    __swig_destroy__ = _init1_.delete_DistributedParameter
    __del__ = lambda self: None
DistributedParameter_swigregister = _init1_.DistributedParameter_swigregister
DistributedParameter_swigregister(DistributedParameter)

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
        this = _init1_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init1_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _init1_.Input_get(self, id)

    def set(self, id, ptr):
        return _init1_.Input_set(self, id, ptr)

    def getNumberOfItems(self):
        return _init1_.Input_getNumberOfItems(self)

    def check(self, parameter, method):
        return _init1_.Input_check(self, parameter, method)
Input_swigregister = _init1_.Input_swigregister
Input_swigregister(Input)

class PartialResultBase(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResultBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResultBase, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init1_.PartialResultBase_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init1_.PartialResultBase_serializationTag)

    def getSerializationTag(self):
        return _init1_.PartialResultBase_getSerializationTag(self)

    def __init__(self, nElements=0):
        this = _init1_.new_PartialResultBase(nElements)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getCollection(self, *args):
        return _init1_.PartialResultBase_getCollection(self, *args)

    def setCollection(self, id, ptr):
        return _init1_.PartialResultBase_setCollection(self, id, ptr)

    def check(self, input, parameter, method):
        return _init1_.PartialResultBase_check(self, input, parameter, method)
    __swig_destroy__ = _init1_.delete_PartialResultBase
    __del__ = lambda self: None
PartialResultBase_swigregister = _init1_.PartialResultBase_swigregister
PartialResultBase_swigregister(PartialResultBase)

def PartialResultBase_serializationTag():
    return _init1_.PartialResultBase_serializationTag()
PartialResultBase_serializationTag = _init1_.PartialResultBase_serializationTag

class PartialResult(PartialResultBase):
    __swig_setmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init1_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init1_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _init1_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init1_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getPartialModel(self, id):
        return _init1_.PartialResult_getPartialModel(self, id)

    def setPartialModel(self, id, ptr):
        return _init1_.PartialResult_setPartialModel(self, id, ptr)

    def getTablesCollection(self, *args):
        return _init1_.PartialResult_getTablesCollection(self, *args)

    def setTablesCollection(self, id, ptr):
        return _init1_.PartialResult_setTablesCollection(self, id, ptr)

    def check(self, input, parameter, method):
        return _init1_.PartialResult_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init1_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init1_.PartialResult_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _init1_.delete_PartialResult
    __del__ = lambda self: None
PartialResult_swigregister = _init1_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _init1_.PartialResult_serializationTag()
PartialResult_serializationTag = _init1_.PartialResult_serializationTag

class DistributedPartialResultStep2(PartialResultBase):
    __swig_setmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResultStep2, name, value)
    __swig_getmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResultStep2, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init1_.DistributedPartialResultStep2_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init1_.DistributedPartialResultStep2_serializationTag)

    def getSerializationTag(self):
        return _init1_.DistributedPartialResultStep2_getSerializationTag(self)

    def __init__(self):
        this = _init1_.new_DistributedPartialResultStep2()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getTable(self, id):
        return _init1_.DistributedPartialResultStep2_getTable(self, id)

    def setTable(self, id, ptr):
        return _init1_.DistributedPartialResultStep2_setTable(self, id, ptr)

    def check(self, input, parameter, method):
        return _init1_.DistributedPartialResultStep2_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init1_.DistributedPartialResultStep2_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init1_.DistributedPartialResultStep2_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _init1_.delete_DistributedPartialResultStep2
    __del__ = lambda self: None
DistributedPartialResultStep2_swigregister = _init1_.DistributedPartialResultStep2_swigregister
DistributedPartialResultStep2_swigregister(DistributedPartialResultStep2)

def DistributedPartialResultStep2_serializationTag():
    return _init1_.DistributedPartialResultStep2_serializationTag()
DistributedPartialResultStep2_serializationTag = _init1_.DistributedPartialResultStep2_serializationTag

class Result(daal.algorithms.implicit_als.training.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.implicit_als.training.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.implicit_als.training.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init1_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init1_.Result_serializationTag)

    def getSerializationTag(self):
        return _init1_.Result_getSerializationTag(self)

    def get(self, id):
        return _init1_.Result_get(self, id)

    def set(self, id, ptr):
        return _init1_.Result_set(self, id, ptr)

    def __init__(self):
        this = _init1_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init1_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _init1_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _init1_.Result_serializationTag()
Result_serializationTag = _init1_.Result_serializationTag

class DistributedInput_Step1Local(Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step1Local, name, value)
    __swig_getmethods__ = {}
    for _s in [Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step1Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init1_.new_DistributedInput_Step1Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init1_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None

    def get(self, id):
        return _init1_.DistributedInput_Step1Local_get(self, id)

    def set(self, id, ptr):
        return _init1_.DistributedInput_Step1Local_set(self, id, ptr)
DistributedInput_Step1Local_swigregister = _init1_.DistributedInput_Step1Local_swigregister
DistributedInput_Step1Local_swigregister(DistributedInput_Step1Local)

class DistributedInput_Step2Local(daal.algorithms.Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step2Local, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step2Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init1_.new_DistributedInput_Step2Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init1_.delete_DistributedInput_Step2Local
    __del__ = lambda self: None

    def get(self, id):
        return _init1_.DistributedInput_Step2Local_get(self, id)

    def set(self, id, ptr):
        return _init1_.DistributedInput_Step2Local_set(self, id, ptr)

    def check(self, parameter, method):
        return _init1_.DistributedInput_Step2Local_check(self, parameter, method)
DistributedInput_Step2Local_swigregister = _init1_.DistributedInput_Step2Local_swigregister
DistributedInput_Step2Local_swigregister(DistributedInput_Step2Local)

class Batch_Float64DefaultDense(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _init1_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_init1_.Batch_Float64DefaultDense_input_get, _init1_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _init1_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Batch_Float64DefaultDense_parameter_get, _init1_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _init1_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, res):
        return _init1_.Batch_Float64DefaultDense_setResult(self, res)

    def clone(self):
        return _init1_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _init1_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _init1_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _init1_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float64FastCSR(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Batch_Float64FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Batch_Float64FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Batch_Float64FastCSR_input_get, _init1_.Batch_Float64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _init1_.Batch_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Batch_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Batch_Float64FastCSR_parameter_get, _init1_.Batch_Float64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Batch_Float64FastCSR_getMethod(self)

    def getResult(self):
        return _init1_.Batch_Float64FastCSR_getResult(self)

    def setResult(self, res):
        return _init1_.Batch_Float64FastCSR_setResult(self, res)

    def clone(self):
        return _init1_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _init1_.Batch_Float64FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None
Batch_Float64FastCSR_swigregister = _init1_.Batch_Float64FastCSR_swigregister
Batch_Float64FastCSR_swigregister(Batch_Float64FastCSR)

class Batch_Float32DefaultDense(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _init1_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_init1_.Batch_Float32DefaultDense_input_get, _init1_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _init1_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Batch_Float32DefaultDense_parameter_get, _init1_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _init1_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, res):
        return _init1_.Batch_Float32DefaultDense_setResult(self, res)

    def clone(self):
        return _init1_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _init1_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _init1_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _init1_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Batch_Float32FastCSR(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Batch_Float32FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Batch_Float32FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Batch_Float32FastCSR_input_get, _init1_.Batch_Float32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _init1_.Batch_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Batch_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Batch_Float32FastCSR_parameter_get, _init1_.Batch_Float32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Batch_Float32FastCSR_getMethod(self)

    def getResult(self):
        return _init1_.Batch_Float32FastCSR_getResult(self)

    def setResult(self, res):
        return _init1_.Batch_Float32FastCSR_setResult(self, res)

    def clone(self):
        return _init1_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _init1_.Batch_Float32FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None
Batch_Float32FastCSR_swigregister = _init1_.Batch_Float32FastCSR_swigregister
Batch_Float32FastCSR_swigregister(Batch_Float32FastCSR)

class Distributed_Step1LocalFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Distributed_Step1LocalFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Distributed_Step1LocalFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Distributed_Step1LocalFloat64FastCSR_input_get, _init1_.Distributed_Step1LocalFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _init1_.Distributed_Step1LocalFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Distributed_Step1LocalFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Distributed_Step1LocalFloat64FastCSR_parameter_get, _init1_.Distributed_Step1LocalFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Distributed_Step1LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Distributed_Step1LocalFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _init1_.Distributed_Step1LocalFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _init1_.Distributed_Step1LocalFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _init1_.Distributed_Step1LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _init1_.Distributed_Step1LocalFloat64FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Distributed_Step1LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64FastCSR_swigregister = _init1_.Distributed_Step1LocalFloat64FastCSR_swigregister
Distributed_Step1LocalFloat64FastCSR_swigregister(Distributed_Step1LocalFloat64FastCSR)

class Distributed_Step1LocalFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Distributed_Step1LocalFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Distributed_Step1LocalFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Distributed_Step1LocalFloat32FastCSR_input_get, _init1_.Distributed_Step1LocalFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _init1_.Distributed_Step1LocalFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _init1_.Distributed_Step1LocalFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init1_.Distributed_Step1LocalFloat32FastCSR_parameter_get, _init1_.Distributed_Step1LocalFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _init1_.new_Distributed_Step1LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Distributed_Step1LocalFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _init1_.Distributed_Step1LocalFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _init1_.Distributed_Step1LocalFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _init1_.Distributed_Step1LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _init1_.Distributed_Step1LocalFloat32FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Distributed_Step1LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32FastCSR_swigregister = _init1_.Distributed_Step1LocalFloat32FastCSR_swigregister
Distributed_Step1LocalFloat32FastCSR_swigregister(Distributed_Step1LocalFloat32FastCSR)

class Distributed_Step2LocalFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Distributed_Step2LocalFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Distributed_Step2LocalFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Distributed_Step2LocalFloat64FastCSR_input_get, _init1_.Distributed_Step2LocalFloat64FastCSR_input_set)

    def __init__(self, *args):
        this = _init1_.new_Distributed_Step2LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Distributed_Step2LocalFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _init1_.Distributed_Step2LocalFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _init1_.Distributed_Step2LocalFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _init1_.Distributed_Step2LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _init1_.Distributed_Step2LocalFloat64FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Distributed_Step2LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat64FastCSR_swigregister = _init1_.Distributed_Step2LocalFloat64FastCSR_swigregister
Distributed_Step2LocalFloat64FastCSR_swigregister(Distributed_Step2LocalFloat64FastCSR)

class Distributed_Step2LocalFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _init1_.Distributed_Step2LocalFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _init1_.Distributed_Step2LocalFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_init1_.Distributed_Step2LocalFloat32FastCSR_input_get, _init1_.Distributed_Step2LocalFloat32FastCSR_input_set)

    def __init__(self, *args):
        this = _init1_.new_Distributed_Step2LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init1_.Distributed_Step2LocalFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _init1_.Distributed_Step2LocalFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _init1_.Distributed_Step2LocalFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _init1_.Distributed_Step2LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _init1_.Distributed_Step2LocalFloat32FastCSR_compute(self)
    __swig_destroy__ = _init1_.delete_Distributed_Step2LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat32FastCSR_swigregister = _init1_.Distributed_Step2LocalFloat32FastCSR_swigregister
Distributed_Step2LocalFloat32FastCSR_swigregister(Distributed_Step2LocalFloat32FastCSR)

from numpy import float64, float32, intc

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            return DistributedInput_Step1Local(*args)
        if step == daal.step2Local:
            return DistributedInput_Step2Local(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat32FastCSR(*args)
        if step == daal.step2Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step2LocalFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step2LocalFloat32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float64FastCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


