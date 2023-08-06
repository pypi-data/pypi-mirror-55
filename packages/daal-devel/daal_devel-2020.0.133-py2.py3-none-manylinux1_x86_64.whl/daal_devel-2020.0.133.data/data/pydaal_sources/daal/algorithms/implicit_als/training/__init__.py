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
            fp, pathname, description = imp.find_module('_training12_', [dirname(__file__)])
        except ImportError:
            import _training12_
            return _training12_
        if fp is not None:
            try:
                _mod = imp.load_module('_training12_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training12_ = swig_import_helper()
    del swig_import_helper
else:
    import _training12_
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


import daal.algorithms.implicit_als
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_training12_.defaultDense_swigconstant(_training12_)
defaultDense = _training12_.defaultDense

_training12_.fastCSR_swigconstant(_training12_)
fastCSR = _training12_.fastCSR

_training12_.data_swigconstant(_training12_)
data = _training12_.data

_training12_.lastNumericTableInputId_swigconstant(_training12_)
lastNumericTableInputId = _training12_.lastNumericTableInputId

_training12_.inputModel_swigconstant(_training12_)
inputModel = _training12_.inputModel

_training12_.lastModelInputId_swigconstant(_training12_)
lastModelInputId = _training12_.lastModelInputId

_training12_.partialModel_swigconstant(_training12_)
partialModel = _training12_.partialModel

_training12_.lastPartialModelInputId_swigconstant(_training12_)
lastPartialModelInputId = _training12_.lastPartialModelInputId

_training12_.inputOfStep2FromStep1_swigconstant(_training12_)
inputOfStep2FromStep1 = _training12_.inputOfStep2FromStep1

_training12_.lastMasterInputId_swigconstant(_training12_)
lastMasterInputId = _training12_.lastMasterInputId

_training12_.outputOfStep1ForStep2_swigconstant(_training12_)
outputOfStep1ForStep2 = _training12_.outputOfStep1ForStep2

_training12_.lastDistributedPartialResultStep1Id_swigconstant(_training12_)
lastDistributedPartialResultStep1Id = _training12_.lastDistributedPartialResultStep1Id

_training12_.outputOfStep2ForStep4_swigconstant(_training12_)
outputOfStep2ForStep4 = _training12_.outputOfStep2ForStep4

_training12_.lastDistributedPartialResultStep2Id_swigconstant(_training12_)
lastDistributedPartialResultStep2Id = _training12_.lastDistributedPartialResultStep2Id

_training12_.partialModelBlocksToNode_swigconstant(_training12_)
partialModelBlocksToNode = _training12_.partialModelBlocksToNode

_training12_.inputOfStep3FromInit_swigconstant(_training12_)
inputOfStep3FromInit = _training12_.inputOfStep3FromInit

_training12_.lastStep3LocalCollectionInputId_swigconstant(_training12_)
lastStep3LocalCollectionInputId = _training12_.lastStep3LocalCollectionInputId

_training12_.offset_swigconstant(_training12_)
offset = _training12_.offset

_training12_.lastStep3LocalNumericTableInputId_swigconstant(_training12_)
lastStep3LocalNumericTableInputId = _training12_.lastStep3LocalNumericTableInputId

_training12_.outputOfStep3ForStep4_swigconstant(_training12_)
outputOfStep3ForStep4 = _training12_.outputOfStep3ForStep4

_training12_.lastDistributedPartialResultStep3Id_swigconstant(_training12_)
lastDistributedPartialResultStep3Id = _training12_.lastDistributedPartialResultStep3Id

_training12_.partialModels_swigconstant(_training12_)
partialModels = _training12_.partialModels

_training12_.lastStep4LocalPartialModelsInputId_swigconstant(_training12_)
lastStep4LocalPartialModelsInputId = _training12_.lastStep4LocalPartialModelsInputId

_training12_.partialData_swigconstant(_training12_)
partialData = _training12_.partialData

_training12_.inputOfStep4FromStep2_swigconstant(_training12_)
inputOfStep4FromStep2 = _training12_.inputOfStep4FromStep2

_training12_.lastStep4LocalNumericTableInputId_swigconstant(_training12_)
lastStep4LocalNumericTableInputId = _training12_.lastStep4LocalNumericTableInputId

_training12_.outputOfStep4ForStep1_swigconstant(_training12_)
outputOfStep4ForStep1 = _training12_.outputOfStep4ForStep1

_training12_.outputOfStep4ForStep3_swigconstant(_training12_)
outputOfStep4ForStep3 = _training12_.outputOfStep4ForStep3

_training12_.outputOfStep4_swigconstant(_training12_)
outputOfStep4 = _training12_.outputOfStep4

_training12_.lastDistributedPartialResultStep4Id_swigconstant(_training12_)
lastDistributedPartialResultStep4Id = _training12_.lastDistributedPartialResultStep4Id

_training12_.model_swigconstant(_training12_)
model = _training12_.model

_training12_.lastResultId_swigconstant(_training12_)
lastResultId = _training12_.lastResultId
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
        this = _training12_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_Input
    __del__ = lambda self: None

    def getTable(self, id):
        return _training12_.Input_getTable(self, id)

    def getModel(self, id):
        return _training12_.Input_getModel(self, id)

    def setTable(self, id, ptr):
        return _training12_.Input_setTable(self, id, ptr)

    def setModel(self, id, ptr):
        return _training12_.Input_setModel(self, id, ptr)

    def getNumberOfUsers(self):
        return _training12_.Input_getNumberOfUsers(self)

    def getNumberOfItems(self):
        return _training12_.Input_getNumberOfItems(self)

    def check(self, parameter, method):
        return _training12_.Input_check(self, parameter, method)
Input_swigregister = _training12_.Input_swigregister
Input_swigregister(Input)

class DistributedPartialResultStep1(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResultStep1, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResultStep1, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training12_.DistributedPartialResultStep1_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training12_.DistributedPartialResultStep1_serializationTag)

    def getSerializationTag(self):
        return _training12_.DistributedPartialResultStep1_getSerializationTag(self)

    def __init__(self):
        this = _training12_.new_DistributedPartialResultStep1()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedPartialResultStep1
    __del__ = lambda self: None

    def get(self, id):
        return _training12_.DistributedPartialResultStep1_get(self, id)

    def set(self, id, ptr):
        return _training12_.DistributedPartialResultStep1_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _training12_.DistributedPartialResultStep1_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training12_.DistributedPartialResultStep1_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training12_.DistributedPartialResultStep1_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep1_swigregister = _training12_.DistributedPartialResultStep1_swigregister
DistributedPartialResultStep1_swigregister(DistributedPartialResultStep1)

def DistributedPartialResultStep1_serializationTag():
    return _training12_.DistributedPartialResultStep1_serializationTag()
DistributedPartialResultStep1_serializationTag = _training12_.DistributedPartialResultStep1_serializationTag

class DistributedPartialResultStep2(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResultStep2, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResultStep2, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training12_.DistributedPartialResultStep2_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training12_.DistributedPartialResultStep2_serializationTag)

    def getSerializationTag(self):
        return _training12_.DistributedPartialResultStep2_getSerializationTag(self)

    def __init__(self):
        this = _training12_.new_DistributedPartialResultStep2()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedPartialResultStep2
    __del__ = lambda self: None

    def get(self, id):
        return _training12_.DistributedPartialResultStep2_get(self, id)

    def set(self, id, ptr):
        return _training12_.DistributedPartialResultStep2_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _training12_.DistributedPartialResultStep2_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training12_.DistributedPartialResultStep2_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training12_.DistributedPartialResultStep2_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep2_swigregister = _training12_.DistributedPartialResultStep2_swigregister
DistributedPartialResultStep2_swigregister(DistributedPartialResultStep2)

def DistributedPartialResultStep2_serializationTag():
    return _training12_.DistributedPartialResultStep2_serializationTag()
DistributedPartialResultStep2_serializationTag = _training12_.DistributedPartialResultStep2_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _training12_.DistributedPartialResultStep3_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training12_.DistributedPartialResultStep3_serializationTag)

    def getSerializationTag(self):
        return _training12_.DistributedPartialResultStep3_getSerializationTag(self)

    def __init__(self):
        this = _training12_.new_DistributedPartialResultStep3()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedPartialResultStep3
    __del__ = lambda self: None

    def get(self, *args):
        return _training12_.DistributedPartialResultStep3_get(self, *args)

    def set(self, id, ptr):
        return _training12_.DistributedPartialResultStep3_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _training12_.DistributedPartialResultStep3_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training12_.DistributedPartialResultStep3_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training12_.DistributedPartialResultStep3_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep3_swigregister = _training12_.DistributedPartialResultStep3_swigregister
DistributedPartialResultStep3_swigregister(DistributedPartialResultStep3)

def DistributedPartialResultStep3_serializationTag():
    return _training12_.DistributedPartialResultStep3_serializationTag()
DistributedPartialResultStep3_serializationTag = _training12_.DistributedPartialResultStep3_serializationTag

class DistributedPartialResultStep4(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPartialResultStep4, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPartialResultStep4, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training12_.DistributedPartialResultStep4_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training12_.DistributedPartialResultStep4_serializationTag)

    def getSerializationTag(self):
        return _training12_.DistributedPartialResultStep4_getSerializationTag(self)

    def __init__(self):
        this = _training12_.new_DistributedPartialResultStep4()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedPartialResultStep4
    __del__ = lambda self: None

    def get(self, id):
        return _training12_.DistributedPartialResultStep4_get(self, id)

    def set(self, id, ptr):
        return _training12_.DistributedPartialResultStep4_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _training12_.DistributedPartialResultStep4_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training12_.DistributedPartialResultStep4_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training12_.DistributedPartialResultStep4_allocate_Float32(self, input, parameter, method)

DistributedPartialResultStep4_swigregister = _training12_.DistributedPartialResultStep4_swigregister
DistributedPartialResultStep4_swigregister(DistributedPartialResultStep4)

def DistributedPartialResultStep4_serializationTag():
    return _training12_.DistributedPartialResultStep4_serializationTag()
DistributedPartialResultStep4_serializationTag = _training12_.DistributedPartialResultStep4_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _training12_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training12_.Result_serializationTag)

    def getSerializationTag(self):
        return _training12_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training12_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training12_.Result_get(self, id)

    def set(self, id, ptr):
        return _training12_.Result_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _training12_.Result_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training12_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training12_.Result_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _training12_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _training12_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training12_.Result_serializationTag()
Result_serializationTag = _training12_.Result_serializationTag

class DistributedInput_Step1Local(daal.algorithms.Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step1Local, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step1Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training12_.new_DistributedInput_Step1Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None

    def get(self, id):
        return _training12_.DistributedInput_Step1Local_get(self, id)

    def set(self, id, ptr):
        return _training12_.DistributedInput_Step1Local_set(self, id, ptr)

    def check(self, parameter, method):
        return _training12_.DistributedInput_Step1Local_check(self, parameter, method)
DistributedInput_Step1Local_swigregister = _training12_.DistributedInput_Step1Local_swigregister
DistributedInput_Step1Local_swigregister(DistributedInput_Step1Local)

class DistributedInput_Step2Master(daal.algorithms.Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step2Master, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step2Master, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training12_.new_DistributedInput_Step2Master(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedInput_Step2Master
    __del__ = lambda self: None

    def get(self, id):
        return _training12_.DistributedInput_Step2Master_get(self, id)

    def set(self, id, ptr):
        return _training12_.DistributedInput_Step2Master_set(self, id, ptr)

    def add(self, id, partialResult):
        return _training12_.DistributedInput_Step2Master_add(self, id, partialResult)

    def check(self, parameter, method):
        return _training12_.DistributedInput_Step2Master_check(self, parameter, method)
DistributedInput_Step2Master_swigregister = _training12_.DistributedInput_Step2Master_swigregister
DistributedInput_Step2Master_swigregister(DistributedInput_Step2Master)

class DistributedInput_Step3Local(daal.algorithms.Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step3Local, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step3Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training12_.new_DistributedInput_Step3Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedInput_Step3Local
    __del__ = lambda self: None

    def getModel(self, id):
        return _training12_.DistributedInput_Step3Local_getModel(self, id)

    def getCollection(self, id):
        return _training12_.DistributedInput_Step3Local_getCollection(self, id)

    def getTable(self, id):
        return _training12_.DistributedInput_Step3Local_getTable(self, id)

    def setModel(self, id, ptr):
        return _training12_.DistributedInput_Step3Local_setModel(self, id, ptr)

    def setCollection(self, id, ptr):
        return _training12_.DistributedInput_Step3Local_setCollection(self, id, ptr)

    def setTable(self, id, ptr):
        return _training12_.DistributedInput_Step3Local_setTable(self, id, ptr)

    def getNumberOfBlocks(self):
        return _training12_.DistributedInput_Step3Local_getNumberOfBlocks(self)

    def getOffset(self):
        return _training12_.DistributedInput_Step3Local_getOffset(self)

    def getOutBlockIndices(self, key):
        return _training12_.DistributedInput_Step3Local_getOutBlockIndices(self, key)

    def check(self, parameter, method):
        return _training12_.DistributedInput_Step3Local_check(self, parameter, method)
DistributedInput_Step3Local_swigregister = _training12_.DistributedInput_Step3Local_swigregister
DistributedInput_Step3Local_swigregister(DistributedInput_Step3Local)

class DistributedInput_Step4Local(daal.algorithms.Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step4Local, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step4Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training12_.new_DistributedInput_Step4Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training12_.delete_DistributedInput_Step4Local
    __del__ = lambda self: None

    def getModels(self, id):
        return _training12_.DistributedInput_Step4Local_getModels(self, id)

    def getTable(self, id):
        return _training12_.DistributedInput_Step4Local_getTable(self, id)

    def setModels(self, id, ptr):
        return _training12_.DistributedInput_Step4Local_setModels(self, id, ptr)

    def setTable(self, id, ptr):
        return _training12_.DistributedInput_Step4Local_setTable(self, id, ptr)

    def getNumberOfRows(self):
        return _training12_.DistributedInput_Step4Local_getNumberOfRows(self)

    def check(self, parameter, method):
        return _training12_.DistributedInput_Step4Local_check(self, parameter, method)
DistributedInput_Step4Local_swigregister = _training12_.DistributedInput_Step4Local_swigregister
DistributedInput_Step4Local_swigregister(DistributedInput_Step4Local)

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
    __swig_setmethods__["input"] = _training12_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _training12_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training12_.Batch_Float64DefaultDense_input_get, _training12_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _training12_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Batch_Float64DefaultDense_parameter_get, _training12_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _training12_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, res):
        return _training12_.Batch_Float64DefaultDense_setResult(self, res)

    def clone(self):
        return _training12_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _training12_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _training12_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _training12_.Batch_Float64DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _training12_.Batch_Float64FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Batch_Float64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Batch_Float64FastCSR_input_get, _training12_.Batch_Float64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Batch_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Batch_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Batch_Float64FastCSR_parameter_get, _training12_.Batch_Float64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Batch_Float64FastCSR_getMethod(self)

    def getResult(self):
        return _training12_.Batch_Float64FastCSR_getResult(self)

    def setResult(self, res):
        return _training12_.Batch_Float64FastCSR_setResult(self, res)

    def clone(self):
        return _training12_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _training12_.Batch_Float64FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None
Batch_Float64FastCSR_swigregister = _training12_.Batch_Float64FastCSR_swigregister
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
    __swig_setmethods__["input"] = _training12_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _training12_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training12_.Batch_Float32DefaultDense_input_get, _training12_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _training12_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Batch_Float32DefaultDense_parameter_get, _training12_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _training12_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, res):
        return _training12_.Batch_Float32DefaultDense_setResult(self, res)

    def clone(self):
        return _training12_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _training12_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _training12_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _training12_.Batch_Float32DefaultDense_swigregister
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
    __swig_setmethods__["input"] = _training12_.Batch_Float32FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Batch_Float32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Batch_Float32FastCSR_input_get, _training12_.Batch_Float32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Batch_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Batch_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Batch_Float32FastCSR_parameter_get, _training12_.Batch_Float32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Batch_Float32FastCSR_getMethod(self)

    def getResult(self):
        return _training12_.Batch_Float32FastCSR_getResult(self)

    def setResult(self, res):
        return _training12_.Batch_Float32FastCSR_setResult(self, res)

    def clone(self):
        return _training12_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _training12_.Batch_Float32FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None
Batch_Float32FastCSR_swigregister = _training12_.Batch_Float32FastCSR_swigregister
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
    __swig_setmethods__["input"] = _training12_.Distributed_Step1LocalFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step1LocalFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step1LocalFloat64FastCSR_input_get, _training12_.Distributed_Step1LocalFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step1LocalFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step1LocalFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step1LocalFloat64FastCSR_parameter_get, _training12_.Distributed_Step1LocalFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step1LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step1LocalFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step1LocalFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step1LocalFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step1LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step1LocalFloat64FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step1LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64FastCSR_swigregister = _training12_.Distributed_Step1LocalFloat64FastCSR_swigregister
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
    __swig_setmethods__["input"] = _training12_.Distributed_Step1LocalFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step1LocalFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step1LocalFloat32FastCSR_input_get, _training12_.Distributed_Step1LocalFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step1LocalFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step1LocalFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step1LocalFloat32FastCSR_parameter_get, _training12_.Distributed_Step1LocalFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step1LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step1LocalFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step1LocalFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step1LocalFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step1LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step1LocalFloat32FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step1LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32FastCSR_swigregister = _training12_.Distributed_Step1LocalFloat32FastCSR_swigregister
Distributed_Step1LocalFloat32FastCSR_swigregister(Distributed_Step1LocalFloat32FastCSR)

class Distributed_Step2MasterFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step2MasterFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step2MasterFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step2MasterFloat64FastCSR_input_get, _training12_.Distributed_Step2MasterFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step2MasterFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step2MasterFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step2MasterFloat64FastCSR_parameter_get, _training12_.Distributed_Step2MasterFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step2MasterFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step2MasterFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step2MasterFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step2MasterFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step2MasterFloat64FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step2MasterFloat64FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step2MasterFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64FastCSR_swigregister = _training12_.Distributed_Step2MasterFloat64FastCSR_swigregister
Distributed_Step2MasterFloat64FastCSR_swigregister(Distributed_Step2MasterFloat64FastCSR)

class Distributed_Step2MasterFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step2MasterFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step2MasterFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step2MasterFloat32FastCSR_input_get, _training12_.Distributed_Step2MasterFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step2MasterFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step2MasterFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step2MasterFloat32FastCSR_parameter_get, _training12_.Distributed_Step2MasterFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step2MasterFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step2MasterFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step2MasterFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step2MasterFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step2MasterFloat32FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step2MasterFloat32FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step2MasterFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32FastCSR_swigregister = _training12_.Distributed_Step2MasterFloat32FastCSR_swigregister
Distributed_Step2MasterFloat32FastCSR_swigregister(Distributed_Step2MasterFloat32FastCSR)

class Distributed_Step3LocalFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3LocalFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3LocalFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step3LocalFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step3LocalFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step3LocalFloat64FastCSR_input_get, _training12_.Distributed_Step3LocalFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step3LocalFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step3LocalFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step3LocalFloat64FastCSR_parameter_get, _training12_.Distributed_Step3LocalFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step3LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step3LocalFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step3LocalFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step3LocalFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step3LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step3LocalFloat64FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step3LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step3LocalFloat64FastCSR_swigregister = _training12_.Distributed_Step3LocalFloat64FastCSR_swigregister
Distributed_Step3LocalFloat64FastCSR_swigregister(Distributed_Step3LocalFloat64FastCSR)

class Distributed_Step3LocalFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3LocalFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3LocalFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step3LocalFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step3LocalFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step3LocalFloat32FastCSR_input_get, _training12_.Distributed_Step3LocalFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step3LocalFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step3LocalFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step3LocalFloat32FastCSR_parameter_get, _training12_.Distributed_Step3LocalFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step3LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step3LocalFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step3LocalFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step3LocalFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step3LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step3LocalFloat32FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step3LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step3LocalFloat32FastCSR_swigregister = _training12_.Distributed_Step3LocalFloat32FastCSR_swigregister
Distributed_Step3LocalFloat32FastCSR_swigregister(Distributed_Step3LocalFloat32FastCSR)

class Distributed_Step4LocalFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step4LocalFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step4LocalFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step4LocalFloat64FastCSR_input_get, _training12_.Distributed_Step4LocalFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step4LocalFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step4LocalFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step4LocalFloat64FastCSR_parameter_get, _training12_.Distributed_Step4LocalFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step4LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step4LocalFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step4LocalFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step4LocalFloat64FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step4LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step4LocalFloat64FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step4LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat64FastCSR_swigregister = _training12_.Distributed_Step4LocalFloat64FastCSR_swigregister
Distributed_Step4LocalFloat64FastCSR_swigregister(Distributed_Step4LocalFloat64FastCSR)

class Distributed_Step4LocalFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training12_.Distributed_Step4LocalFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _training12_.Distributed_Step4LocalFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training12_.Distributed_Step4LocalFloat32FastCSR_input_get, _training12_.Distributed_Step4LocalFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _training12_.Distributed_Step4LocalFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training12_.Distributed_Step4LocalFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training12_.Distributed_Step4LocalFloat32FastCSR_parameter_get, _training12_.Distributed_Step4LocalFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _training12_.new_Distributed_Step4LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _training12_.Distributed_Step4LocalFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training12_.Distributed_Step4LocalFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training12_.Distributed_Step4LocalFloat32FastCSR_getPartialResult(self)

    def clone(self):
        return _training12_.Distributed_Step4LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _training12_.Distributed_Step4LocalFloat32FastCSR_compute(self)
    __swig_destroy__ = _training12_.delete_Distributed_Step4LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat32FastCSR_swigregister = _training12_.Distributed_Step4LocalFloat32FastCSR_swigregister
Distributed_Step4LocalFloat32FastCSR_swigregister(Distributed_Step4LocalFloat32FastCSR)

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
        if step == daal.step3Local:
            return DistributedInput_Step3Local(*args)
        if step == daal.step4Local:
            return DistributedInput_Step4Local(*args)

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
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat32FastCSR(*args)
        if step == daal.step3Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step3LocalFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step3LocalFloat32FastCSR(*args)
        if step == daal.step4Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step4LocalFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == fastCSR:
                        return Distributed_Step4LocalFloat32FastCSR(*args)

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


