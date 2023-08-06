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
            fp, pathname, description = imp.find_module('_svd_', [dirname(__file__)])
        except ImportError:
            import _svd_
            return _svd_
        if fp is not None:
            try:
                _mod = imp.load_module('_svd_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _svd_ = swig_import_helper()
    del swig_import_helper
else:
    import _svd_
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

_svd_.defaultDense_swigconstant(_svd_)
defaultDense = _svd_.defaultDense

_svd_.notRequired_swigconstant(_svd_)
notRequired = _svd_.notRequired

_svd_.requiredInPackedForm_swigconstant(_svd_)
requiredInPackedForm = _svd_.requiredInPackedForm

_svd_.data_swigconstant(_svd_)
data = _svd_.data

_svd_.lastInputId_swigconstant(_svd_)
lastInputId = _svd_.lastInputId

_svd_.singularValues_swigconstant(_svd_)
singularValues = _svd_.singularValues

_svd_.leftSingularMatrix_swigconstant(_svd_)
leftSingularMatrix = _svd_.leftSingularMatrix

_svd_.rightSingularMatrix_swigconstant(_svd_)
rightSingularMatrix = _svd_.rightSingularMatrix

_svd_.lastResultId_swigconstant(_svd_)
lastResultId = _svd_.lastResultId

_svd_.outputOfStep1ForStep3_swigconstant(_svd_)
outputOfStep1ForStep3 = _svd_.outputOfStep1ForStep3

_svd_.outputOfStep1ForStep2_swigconstant(_svd_)
outputOfStep1ForStep2 = _svd_.outputOfStep1ForStep2

_svd_.lastPartialResultId_swigconstant(_svd_)
lastPartialResultId = _svd_.lastPartialResultId

_svd_.outputOfStep2ForStep3_swigconstant(_svd_)
outputOfStep2ForStep3 = _svd_.outputOfStep2ForStep3

_svd_.lastDistributedPartialResultCollectionId_swigconstant(_svd_)
lastDistributedPartialResultCollectionId = _svd_.lastDistributedPartialResultCollectionId

_svd_.finalResultFromStep2Master_swigconstant(_svd_)
finalResultFromStep2Master = _svd_.finalResultFromStep2Master

_svd_.lastDistributedPartialResultId_swigconstant(_svd_)
lastDistributedPartialResultId = _svd_.lastDistributedPartialResultId

_svd_.finalResultFromStep3_swigconstant(_svd_)
finalResultFromStep3 = _svd_.finalResultFromStep3

_svd_.lastDistributedPartialResultStep3Id_swigconstant(_svd_)
lastDistributedPartialResultStep3Id = _svd_.lastDistributedPartialResultStep3Id

_svd_.inputOfStep2FromStep1_swigconstant(_svd_)
inputOfStep2FromStep1 = _svd_.inputOfStep2FromStep1

_svd_.lastMasterInputId_swigconstant(_svd_)
lastMasterInputId = _svd_.lastMasterInputId

_svd_.inputOfStep3FromStep1_swigconstant(_svd_)
inputOfStep3FromStep1 = _svd_.inputOfStep3FromStep1

_svd_.inputOfStep3FromStep2_swigconstant(_svd_)
inputOfStep3FromStep2 = _svd_.inputOfStep3FromStep2

_svd_.lastFinalizeOnLocalInputId_swigconstant(_svd_)
lastFinalizeOnLocalInputId = _svd_.lastFinalizeOnLocalInputId
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
        this = _svd_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["leftSingularMatrix"] = _svd_.Parameter_leftSingularMatrix_set
    __swig_getmethods__["leftSingularMatrix"] = _svd_.Parameter_leftSingularMatrix_get
    if _newclass:
        leftSingularMatrix = _swig_property(_svd_.Parameter_leftSingularMatrix_get, _svd_.Parameter_leftSingularMatrix_set)
    __swig_setmethods__["rightSingularMatrix"] = _svd_.Parameter_rightSingularMatrix_set
    __swig_getmethods__["rightSingularMatrix"] = _svd_.Parameter_rightSingularMatrix_get
    if _newclass:
        rightSingularMatrix = _swig_property(_svd_.Parameter_rightSingularMatrix_get, _svd_.Parameter_rightSingularMatrix_set)
    __swig_destroy__ = _svd_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _svd_.Parameter_swigregister
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
        this = _svd_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _svd_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _svd_.Input_get(self, id)

    def set(self, id, value):
        return _svd_.Input_set(self, id, value)

    def getNumberOfColumns(self, nFeatures):
        return _svd_.Input_getNumberOfColumns(self, nFeatures)

    def getNumberOfRows(self, nRows):
        return _svd_.Input_getNumberOfRows(self, nRows)

    def check(self, parameter, method):
        return _svd_.Input_check(self, parameter, method)
Input_swigregister = _svd_.Input_swigregister
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
        this = _svd_.new_DistributedStep2Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _svd_.DistributedStep2Input_set(self, id, ptr)

    def get(self, id):
        return _svd_.DistributedStep2Input_get(self, id)

    def add(self, id, key, value):
        return _svd_.DistributedStep2Input_add(self, id, key, value)

    def getNBlocks(self):
        return _svd_.DistributedStep2Input_getNBlocks(self)

    def check(self, parameter, method):
        return _svd_.DistributedStep2Input_check(self, parameter, method)
    __swig_destroy__ = _svd_.delete_DistributedStep2Input
    __del__ = lambda self: None
DistributedStep2Input_swigregister = _svd_.DistributedStep2Input_swigregister
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
        this = _svd_.new_DistributedStep3Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _svd_.DistributedStep3Input_get(self, id)

    def set(self, id, value):
        return _svd_.DistributedStep3Input_set(self, id, value)

    def getSizes(self, nFeatures, nVectors):
        return _svd_.DistributedStep3Input_getSizes(self, nFeatures, nVectors)

    def check(self, parameter, method):
        return _svd_.DistributedStep3Input_check(self, parameter, method)
    __swig_destroy__ = _svd_.delete_DistributedStep3Input
    __del__ = lambda self: None
DistributedStep3Input_swigregister = _svd_.DistributedStep3Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _svd_.OnlinePartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_svd_.OnlinePartialResult_serializationTag)

    def getSerializationTag(self):
        return _svd_.OnlinePartialResult_getSerializationTag(self)

    def __init__(self):
        this = _svd_.new_OnlinePartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _svd_.delete_OnlinePartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _svd_.OnlinePartialResult_get(self, id)

    def set(self, id, value):
        return _svd_.OnlinePartialResult_set(self, id, value)

    def check(self, *args):
        return _svd_.OnlinePartialResult_check(self, *args)

    def getNumberOfColumns(self):
        return _svd_.OnlinePartialResult_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _svd_.OnlinePartialResult_getNumberOfRows(self)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _svd_.OnlinePartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _svd_.OnlinePartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _svd_.OnlinePartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _svd_.OnlinePartialResult_initialize_Float32(self, input, parameter, method)

OnlinePartialResult_swigregister = _svd_.OnlinePartialResult_swigregister
OnlinePartialResult_swigregister(OnlinePartialResult)

def OnlinePartialResult_serializationTag():
    return _svd_.OnlinePartialResult_serializationTag()
OnlinePartialResult_serializationTag = _svd_.OnlinePartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _svd_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_svd_.Result_serializationTag)

    def getSerializationTag(self):
        return _svd_.Result_getSerializationTag(self)

    def __init__(self):
        this = _svd_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _svd_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _svd_.Result_get(self, id)

    def set(self, id, value):
        return _svd_.Result_set(self, id, value)

    def check(self, *args):
        return _svd_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _svd_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _svd_.Result_allocate_Float32(self, *args)

Result_swigregister = _svd_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _svd_.Result_serializationTag()
Result_serializationTag = _svd_.Result_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _svd_.DistributedPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_svd_.DistributedPartialResult_serializationTag)

    def getSerializationTag(self):
        return _svd_.DistributedPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _svd_.new_DistributedPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _svd_.delete_DistributedPartialResult
    __del__ = lambda self: None

    def get(self, id, idx):
        return _svd_.DistributedPartialResult_get(self, id, idx)

    def getResult(self, id):
        return _svd_.DistributedPartialResult_getResult(self, id)

    def setCollection(self, id, value):
        return _svd_.DistributedPartialResult_setCollection(self, id, value)

    def setResult(self, id, value):
        return _svd_.DistributedPartialResult_setResult(self, id, value)

    def check(self, *args):
        return _svd_.DistributedPartialResult_check(self, *args)

    def getCollection(self, *args):
        return _svd_.DistributedPartialResult_getCollection(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _svd_.DistributedPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _svd_.DistributedPartialResult_allocate_Float32(self, input, parameter, method)

DistributedPartialResult_swigregister = _svd_.DistributedPartialResult_swigregister
DistributedPartialResult_swigregister(DistributedPartialResult)

def DistributedPartialResult_serializationTag():
    return _svd_.DistributedPartialResult_serializationTag()
DistributedPartialResult_serializationTag = _svd_.DistributedPartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _svd_.DistributedPartialResultStep3_serializationTag
    if _newclass:
        serializationTag = staticmethod(_svd_.DistributedPartialResultStep3_serializationTag)

    def getSerializationTag(self):
        return _svd_.DistributedPartialResultStep3_getSerializationTag(self)

    def __init__(self):
        this = _svd_.new_DistributedPartialResultStep3()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _svd_.delete_DistributedPartialResultStep3
    __del__ = lambda self: None

    def get(self, id):
        return _svd_.DistributedPartialResultStep3_get(self, id)

    def set(self, id, value):
        return _svd_.DistributedPartialResultStep3_set(self, id, value)

    def check(self, *args):
        return _svd_.DistributedPartialResultStep3_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _svd_.DistributedPartialResultStep3_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _svd_.DistributedPartialResultStep3_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep3_swigregister = _svd_.DistributedPartialResultStep3_swigregister
DistributedPartialResultStep3_swigregister(DistributedPartialResultStep3)

def DistributedPartialResultStep3_serializationTag():
    return _svd_.DistributedPartialResultStep3_serializationTag()
DistributedPartialResultStep3_serializationTag = _svd_.DistributedPartialResultStep3_serializationTag

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
    __swig_setmethods__["input"] = _svd_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Batch_Float64DefaultDense_input_get, _svd_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Batch_Float64DefaultDense_parameter_get, _svd_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, res):
        return _svd_.Batch_Float64DefaultDense_setResult(self, res)

    def clone(self):
        return _svd_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _svd_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _svd_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _svd_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Batch_Float32DefaultDense_input_get, _svd_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Batch_Float32DefaultDense_parameter_get, _svd_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, res):
        return _svd_.Batch_Float32DefaultDense_setResult(self, res)

    def clone(self):
        return _svd_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _svd_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _svd_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _svd_.Batch_Float32DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Online_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Online_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Online_Float64DefaultDense_input_get, _svd_.Online_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Online_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Online_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Online_Float64DefaultDense_parameter_get, _svd_.Online_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Online_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Online_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Online_Float64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Online_Float64DefaultDense_getPartialResult(self)

    def setResult(self, res):
        return _svd_.Online_Float64DefaultDense_setResult(self, res)

    def setPartialResult(self, partialResult, initFlag=False):
        return _svd_.Online_Float64DefaultDense_setPartialResult(self, partialResult, initFlag)

    def checkFinalizeComputeParams(self):
        return _svd_.Online_Float64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Online_Float64DefaultDense_clone(self)

    def compute(self):
        return _svd_.Online_Float64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Online_Float64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Online_Float64DefaultDense
    __del__ = lambda self: None
Online_Float64DefaultDense_swigregister = _svd_.Online_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Online_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Online_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Online_Float32DefaultDense_input_get, _svd_.Online_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Online_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Online_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Online_Float32DefaultDense_parameter_get, _svd_.Online_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Online_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Online_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Online_Float32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Online_Float32DefaultDense_getPartialResult(self)

    def setResult(self, res):
        return _svd_.Online_Float32DefaultDense_setResult(self, res)

    def setPartialResult(self, partialResult, initFlag=False):
        return _svd_.Online_Float32DefaultDense_setPartialResult(self, partialResult, initFlag)

    def checkFinalizeComputeParams(self):
        return _svd_.Online_Float32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Online_Float32DefaultDense_clone(self)

    def compute(self):
        return _svd_.Online_Float32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Online_Float32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Online_Float32DefaultDense
    __del__ = lambda self: None
Online_Float32DefaultDense_swigregister = _svd_.Online_Float32DefaultDense_swigregister
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
        this = _svd_.new_Distributed_Step1LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _svd_.Distributed_Step1LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step1LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step1LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step1LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DefaultDense_swigregister = _svd_.Distributed_Step1LocalFloat64DefaultDense_swigregister
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
        this = _svd_.new_Distributed_Step1LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _svd_.Distributed_Step1LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step1LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step1LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step1LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DefaultDense_swigregister = _svd_.Distributed_Step1LocalFloat32DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Distributed_Step2MasterFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Distributed_Step2MasterFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Distributed_Step2MasterFloat64DefaultDense_input_get, _svd_.Distributed_Step2MasterFloat64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Distributed_Step2MasterFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Distributed_Step2MasterFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Distributed_Step2MasterFloat64DefaultDense_parameter_get, _svd_.Distributed_Step2MasterFloat64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Distributed_Step2MasterFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step2MasterFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step2MasterFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64DefaultDense_swigregister = _svd_.Distributed_Step2MasterFloat64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Distributed_Step2MasterFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Distributed_Step2MasterFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Distributed_Step2MasterFloat32DefaultDense_input_get, _svd_.Distributed_Step2MasterFloat32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Distributed_Step2MasterFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Distributed_Step2MasterFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Distributed_Step2MasterFloat32DefaultDense_parameter_get, _svd_.Distributed_Step2MasterFloat32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Distributed_Step2MasterFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step2MasterFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step2MasterFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32DefaultDense_swigregister = _svd_.Distributed_Step2MasterFloat32DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Distributed_Step3LocalFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Distributed_Step3LocalFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Distributed_Step3LocalFloat64DefaultDense_input_get, _svd_.Distributed_Step3LocalFloat64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Distributed_Step3LocalFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Distributed_Step3LocalFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Distributed_Step3LocalFloat64DefaultDense_parameter_get, _svd_.Distributed_Step3LocalFloat64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Distributed_Step3LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_setPartialResult(self, partialRes)

    def setResult(self, res):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_setResult(self, res)

    def checkFinalizeComputeParams(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step3LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step3LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step3LocalFloat64DefaultDense_swigregister = _svd_.Distributed_Step3LocalFloat64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _svd_.Distributed_Step3LocalFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _svd_.Distributed_Step3LocalFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_svd_.Distributed_Step3LocalFloat32DefaultDense_input_get, _svd_.Distributed_Step3LocalFloat32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _svd_.Distributed_Step3LocalFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _svd_.Distributed_Step3LocalFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_svd_.Distributed_Step3LocalFloat32DefaultDense_parameter_get, _svd_.Distributed_Step3LocalFloat32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _svd_.new_Distributed_Step3LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_getMethod(self)

    def getResult(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_getResult(self)

    def getPartialResult(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_setPartialResult(self, partialRes)

    def setResult(self, res):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_setResult(self, res)

    def checkFinalizeComputeParams(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _svd_.Distributed_Step3LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _svd_.delete_Distributed_Step3LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step3LocalFloat32DefaultDense_swigregister = _svd_.Distributed_Step3LocalFloat32DefaultDense_swigregister
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


