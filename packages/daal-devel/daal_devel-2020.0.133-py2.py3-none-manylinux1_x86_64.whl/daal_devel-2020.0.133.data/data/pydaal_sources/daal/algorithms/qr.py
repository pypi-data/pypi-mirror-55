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
            fp, pathname, description = imp.find_module('_qr_', [dirname(__file__)])
        except ImportError:
            import _qr_
            return _qr_
        if fp is not None:
            try:
                _mod = imp.load_module('_qr_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _qr_ = swig_import_helper()
    del swig_import_helper
else:
    import _qr_
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

_qr_.defaultDense_swigconstant(_qr_)
defaultDense = _qr_.defaultDense

_qr_.data_swigconstant(_qr_)
data = _qr_.data

_qr_.lastInputId_swigconstant(_qr_)
lastInputId = _qr_.lastInputId

_qr_.matrixQ_swigconstant(_qr_)
matrixQ = _qr_.matrixQ

_qr_.matrixR_swigconstant(_qr_)
matrixR = _qr_.matrixR

_qr_.lastResultId_swigconstant(_qr_)
lastResultId = _qr_.lastResultId

_qr_.outputOfStep1ForStep3_swigconstant(_qr_)
outputOfStep1ForStep3 = _qr_.outputOfStep1ForStep3

_qr_.outputOfStep1ForStep2_swigconstant(_qr_)
outputOfStep1ForStep2 = _qr_.outputOfStep1ForStep2

_qr_.lastPartialResultId_swigconstant(_qr_)
lastPartialResultId = _qr_.lastPartialResultId

_qr_.outputOfStep2ForStep3_swigconstant(_qr_)
outputOfStep2ForStep3 = _qr_.outputOfStep2ForStep3

_qr_.lastDistributedPartialResultCollectionId_swigconstant(_qr_)
lastDistributedPartialResultCollectionId = _qr_.lastDistributedPartialResultCollectionId

_qr_.finalResultFromStep2Master_swigconstant(_qr_)
finalResultFromStep2Master = _qr_.finalResultFromStep2Master

_qr_.lastDistributedPartialResultId_swigconstant(_qr_)
lastDistributedPartialResultId = _qr_.lastDistributedPartialResultId

_qr_.finalResultFromStep3_swigconstant(_qr_)
finalResultFromStep3 = _qr_.finalResultFromStep3

_qr_.lastDistributedPartialResultStep3Id_swigconstant(_qr_)
lastDistributedPartialResultStep3Id = _qr_.lastDistributedPartialResultStep3Id

_qr_.inputOfStep2FromStep1_swigconstant(_qr_)
inputOfStep2FromStep1 = _qr_.inputOfStep2FromStep1

_qr_.lastMasterInputId_swigconstant(_qr_)
lastMasterInputId = _qr_.lastMasterInputId

_qr_.inputOfStep3FromStep1_swigconstant(_qr_)
inputOfStep3FromStep1 = _qr_.inputOfStep3FromStep1

_qr_.inputOfStep3FromStep2_swigconstant(_qr_)
inputOfStep3FromStep2 = _qr_.inputOfStep3FromStep2

_qr_.lastFinalizeOnLocalInputId_swigconstant(_qr_)
lastFinalizeOnLocalInputId = _qr_.lastFinalizeOnLocalInputId
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
        this = _qr_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _qr_.Input_get(self, id)

    def set(self, id, value):
        return _qr_.Input_set(self, id, value)

    def getNumberOfColumns(self, nFeatures):
        return _qr_.Input_getNumberOfColumns(self, nFeatures)

    def getNumberOfRows(self, nRows):
        return _qr_.Input_getNumberOfRows(self, nRows)

    def check(self, parameter, method):
        return _qr_.Input_check(self, parameter, method)
Input_swigregister = _qr_.Input_swigregister
Input_swigregister(Input)

class DistributedStep2Input(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _qr_.new_DistributedStep2Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getNumberOfColumns(self, nFeatures):
        return _qr_.DistributedStep2Input_getNumberOfColumns(self, nFeatures)

    def set(self, id, ptr):
        return _qr_.DistributedStep2Input_set(self, id, ptr)

    def get(self, id):
        return _qr_.DistributedStep2Input_get(self, id)

    def add(self, id, key, value):
        return _qr_.DistributedStep2Input_add(self, id, key, value)

    def getNBlocks(self):
        return _qr_.DistributedStep2Input_getNBlocks(self)

    def check(self, parameter, method):
        return _qr_.DistributedStep2Input_check(self, parameter, method)
    __swig_destroy__ = _qr_.delete_DistributedStep2Input
    __del__ = lambda self: None
DistributedStep2Input_swigregister = _qr_.DistributedStep2Input_swigregister
DistributedStep2Input_swigregister(DistributedStep2Input)

class DistributedStep3Input(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep3Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep3Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _qr_.new_DistributedStep3Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _qr_.DistributedStep3Input_get(self, id)

    def set(self, id, value):
        return _qr_.DistributedStep3Input_set(self, id, value)

    def getSizes(self, nFeatures, nVectors):
        return _qr_.DistributedStep3Input_getSizes(self, nFeatures, nVectors)

    def check(self, parameter, method):
        return _qr_.DistributedStep3Input_check(self, parameter, method)
    __swig_destroy__ = _qr_.delete_DistributedStep3Input
    __del__ = lambda self: None
DistributedStep3Input_swigregister = _qr_.DistributedStep3Input_swigregister
DistributedStep3Input_swigregister(DistributedStep3Input)

class OnlinePartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlinePartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OnlinePartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _qr_.OnlinePartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_qr_.OnlinePartialResult_serializationTag)

    def getSerializationTag(self):
        return _qr_.OnlinePartialResult_getSerializationTag(self)

    def __init__(self):
        this = _qr_.new_OnlinePartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_OnlinePartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _qr_.OnlinePartialResult_get(self, id)

    def set(self, id, value):
        return _qr_.OnlinePartialResult_set(self, id, value)

    def check(self, *args):
        return _qr_.OnlinePartialResult_check(self, *args)

    def getNumberOfColumns(self):
        return _qr_.OnlinePartialResult_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _qr_.OnlinePartialResult_getNumberOfRows(self)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _qr_.OnlinePartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _qr_.OnlinePartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _qr_.OnlinePartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _qr_.OnlinePartialResult_initialize_Float32(self, input, parameter, method)

OnlinePartialResult_swigregister = _qr_.OnlinePartialResult_swigregister
OnlinePartialResult_swigregister(OnlinePartialResult)

def OnlinePartialResult_serializationTag():
    return _qr_.OnlinePartialResult_serializationTag()
OnlinePartialResult_serializationTag = _qr_.OnlinePartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _qr_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_qr_.Result_serializationTag)

    def getSerializationTag(self):
        return _qr_.Result_getSerializationTag(self)

    def __init__(self):
        this = _qr_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _qr_.Result_get(self, id)

    def set(self, id, value):
        return _qr_.Result_set(self, id, value)

    def check(self, *args):
        return _qr_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _qr_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _qr_.Result_allocate_Float32(self, *args)

Result_swigregister = _qr_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _qr_.Result_serializationTag()
Result_serializationTag = _qr_.Result_serializationTag

class DistributedPartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _qr_.DistributedPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_qr_.DistributedPartialResult_serializationTag)

    def getSerializationTag(self):
        return _qr_.DistributedPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _qr_.new_DistributedPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_DistributedPartialResult
    __del__ = lambda self: None

    def getResult(self, id):
        return _qr_.DistributedPartialResult_getResult(self, id)

    def setCollection(self, id, value):
        return _qr_.DistributedPartialResult_setCollection(self, id, value)

    def setResult(self, id, value):
        return _qr_.DistributedPartialResult_setResult(self, id, value)

    def check(self, *args):
        return _qr_.DistributedPartialResult_check(self, *args)

    def getCollection(self, *args):
        return _qr_.DistributedPartialResult_getCollection(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _qr_.DistributedPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _qr_.DistributedPartialResult_allocate_Float32(self, input, parameter, method)

DistributedPartialResult_swigregister = _qr_.DistributedPartialResult_swigregister
DistributedPartialResult_swigregister(DistributedPartialResult)

def DistributedPartialResult_serializationTag():
    return _qr_.DistributedPartialResult_serializationTag()
DistributedPartialResult_serializationTag = _qr_.DistributedPartialResult_serializationTag

class DistributedPartialResultStep3(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResultStep3, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResultStep3, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _qr_.DistributedPartialResultStep3_serializationTag
    if _newclass:
        serializationTag = staticmethod(_qr_.DistributedPartialResultStep3_serializationTag)

    def getSerializationTag(self):
        return _qr_.DistributedPartialResultStep3_getSerializationTag(self)

    def __init__(self):
        this = _qr_.new_DistributedPartialResultStep3()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_DistributedPartialResultStep3
    __del__ = lambda self: None

    def get(self, id):
        return _qr_.DistributedPartialResultStep3_get(self, id)

    def set(self, id, value):
        return _qr_.DistributedPartialResultStep3_set(self, id, value)

    def check(self, *args):
        return _qr_.DistributedPartialResultStep3_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _qr_.DistributedPartialResultStep3_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _qr_.DistributedPartialResultStep3_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep3_swigregister = _qr_.DistributedPartialResultStep3_swigregister
DistributedPartialResultStep3_swigregister(DistributedPartialResultStep3)

def DistributedPartialResultStep3_serializationTag():
    return _qr_.DistributedPartialResultStep3_serializationTag()
DistributedPartialResultStep3_serializationTag = _qr_.DistributedPartialResultStep3_serializationTag

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

    def __init__(self):
        this = _qr_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _qr_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _qr_.Parameter_swigregister
Parameter_swigregister(Parameter)

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
    __swig_setmethods__["input"] = _qr_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Batch_Float64DefaultDense_input_get, _qr_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Batch_Float64DefaultDense_parameter_get, _qr_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, res):
        return _qr_.Batch_Float64DefaultDense_setResult(self, res)

    def clone(self):
        return _qr_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _qr_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _qr_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _qr_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _qr_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Batch_Float32DefaultDense_input_get, _qr_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Batch_Float32DefaultDense_parameter_get, _qr_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, res):
        return _qr_.Batch_Float32DefaultDense_setResult(self, res)

    def clone(self):
        return _qr_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _qr_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _qr_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _qr_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Online_Float64DefaultDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Online_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Online_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Online_Float64DefaultDense_input_get, _qr_.Online_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Online_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Online_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Online_Float64DefaultDense_parameter_get, _qr_.Online_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Online_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Online_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Online_Float64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Online_Float64DefaultDense_getPartialResult(self)

    def setResult(self, res):
        return _qr_.Online_Float64DefaultDense_setResult(self, res)

    def setPartialResult(self, partialResult, initFlag=False):
        return _qr_.Online_Float64DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _qr_.Online_Float64DefaultDense_clone(self)

    def compute(self):
        return _qr_.Online_Float64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Online_Float64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Online_Float64DefaultDense
    __del__ = lambda self: None
Online_Float64DefaultDense_swigregister = _qr_.Online_Float64DefaultDense_swigregister
Online_Float64DefaultDense_swigregister(Online_Float64DefaultDense)

class Online_Float32DefaultDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Online_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Online_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Online_Float32DefaultDense_input_get, _qr_.Online_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Online_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Online_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Online_Float32DefaultDense_parameter_get, _qr_.Online_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Online_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Online_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Online_Float32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Online_Float32DefaultDense_getPartialResult(self)

    def setResult(self, res):
        return _qr_.Online_Float32DefaultDense_setResult(self, res)

    def setPartialResult(self, partialResult, initFlag=False):
        return _qr_.Online_Float32DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _qr_.Online_Float32DefaultDense_clone(self)

    def compute(self):
        return _qr_.Online_Float32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Online_Float32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Online_Float32DefaultDense
    __del__ = lambda self: None
Online_Float32DefaultDense_swigregister = _qr_.Online_Float32DefaultDense_swigregister
Online_Float32DefaultDense_swigregister(Online_Float32DefaultDense)

class Distributed_Step1LocalFloat64DefaultDense(Online_Float64DefaultDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64DefaultDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64DefaultDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step1LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _qr_.Distributed_Step1LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step1LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step1LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step1LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DefaultDense_swigregister = _qr_.Distributed_Step1LocalFloat64DefaultDense_swigregister
Distributed_Step1LocalFloat64DefaultDense_swigregister(Distributed_Step1LocalFloat64DefaultDense)

class Distributed_Step1LocalFloat32DefaultDense(Online_Float32DefaultDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32DefaultDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32DefaultDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step1LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _qr_.Distributed_Step1LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step1LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step1LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step1LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DefaultDense_swigregister = _qr_.Distributed_Step1LocalFloat32DefaultDense_swigregister
Distributed_Step1LocalFloat32DefaultDense_swigregister(Distributed_Step1LocalFloat32DefaultDense)

class Distributed_Step2MasterFloat64DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Distributed_Step2MasterFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Distributed_Step2MasterFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Distributed_Step2MasterFloat64DefaultDense_input_get, _qr_.Distributed_Step2MasterFloat64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Distributed_Step2MasterFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Distributed_Step2MasterFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Distributed_Step2MasterFloat64DefaultDense_parameter_get, _qr_.Distributed_Step2MasterFloat64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step2MasterFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step2MasterFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step2MasterFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64DefaultDense_swigregister = _qr_.Distributed_Step2MasterFloat64DefaultDense_swigregister
Distributed_Step2MasterFloat64DefaultDense_swigregister(Distributed_Step2MasterFloat64DefaultDense)

class Distributed_Step2MasterFloat32DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Distributed_Step2MasterFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Distributed_Step2MasterFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Distributed_Step2MasterFloat32DefaultDense_input_get, _qr_.Distributed_Step2MasterFloat32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Distributed_Step2MasterFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Distributed_Step2MasterFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Distributed_Step2MasterFloat32DefaultDense_parameter_get, _qr_.Distributed_Step2MasterFloat32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step2MasterFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step2MasterFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step2MasterFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32DefaultDense_swigregister = _qr_.Distributed_Step2MasterFloat32DefaultDense_swigregister
Distributed_Step2MasterFloat32DefaultDense_swigregister(Distributed_Step2MasterFloat32DefaultDense)

class Distributed_Step3LocalFloat64DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3LocalFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3LocalFloat64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Distributed_Step3LocalFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Distributed_Step3LocalFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Distributed_Step3LocalFloat64DefaultDense_input_get, _qr_.Distributed_Step3LocalFloat64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Distributed_Step3LocalFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Distributed_Step3LocalFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Distributed_Step3LocalFloat64DefaultDense_parameter_get, _qr_.Distributed_Step3LocalFloat64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step3LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_setPartialResult(self, partialRes)

    def setResult(self, res):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_setResult(self, res)

    def checkFinalizeComputeParams(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step3LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step3LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step3LocalFloat64DefaultDense_swigregister = _qr_.Distributed_Step3LocalFloat64DefaultDense_swigregister
Distributed_Step3LocalFloat64DefaultDense_swigregister(Distributed_Step3LocalFloat64DefaultDense)

class Distributed_Step3LocalFloat32DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3LocalFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3LocalFloat32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _qr_.Distributed_Step3LocalFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _qr_.Distributed_Step3LocalFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_qr_.Distributed_Step3LocalFloat32DefaultDense_input_get, _qr_.Distributed_Step3LocalFloat32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _qr_.Distributed_Step3LocalFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _qr_.Distributed_Step3LocalFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_qr_.Distributed_Step3LocalFloat32DefaultDense_parameter_get, _qr_.Distributed_Step3LocalFloat32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _qr_.new_Distributed_Step3LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_getMethod(self)

    def getResult(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_setPartialResult(self, partialRes)

    def setResult(self, res):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_setResult(self, res)

    def checkFinalizeComputeParams(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _qr_.Distributed_Step3LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _qr_.delete_Distributed_Step3LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step3LocalFloat32DefaultDense_swigregister = _qr_.Distributed_Step3LocalFloat32DefaultDense_swigregister
Distributed_Step3LocalFloat32DefaultDense_swigregister(Distributed_Step3LocalFloat32DefaultDense)

from numpy import float64, float32, intc

class Online(object):
    r"""Factory class for different types of Online."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float64DefaultDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float32DefaultDense(*args)

        raise RuntimeError("No appropriate constructor found for Online")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat64DefaultDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat32DefaultDense(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat64DefaultDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat32DefaultDense(*args)
        if step == daal.step3Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step3LocalFloat64DefaultDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step3LocalFloat32DefaultDense(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

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


