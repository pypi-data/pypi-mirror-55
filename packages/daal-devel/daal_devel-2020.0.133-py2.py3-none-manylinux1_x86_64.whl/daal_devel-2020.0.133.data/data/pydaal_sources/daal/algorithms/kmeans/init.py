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
            fp, pathname, description = imp.find_module('_init2_', [dirname(__file__)])
        except ImportError:
            import _init2_
            return _init2_
        if fp is not None:
            try:
                _mod = imp.load_module('_init2_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _init2_ = swig_import_helper()
    del swig_import_helper
else:
    import _init2_
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
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_init2_.deterministicDense_swigconstant(_init2_)
deterministicDense = _init2_.deterministicDense

_init2_.defaultDense_swigconstant(_init2_)
defaultDense = _init2_.defaultDense

_init2_.randomDense_swigconstant(_init2_)
randomDense = _init2_.randomDense

_init2_.plusPlusDense_swigconstant(_init2_)
plusPlusDense = _init2_.plusPlusDense

_init2_.parallelPlusDense_swigconstant(_init2_)
parallelPlusDense = _init2_.parallelPlusDense

_init2_.deterministicCSR_swigconstant(_init2_)
deterministicCSR = _init2_.deterministicCSR

_init2_.randomCSR_swigconstant(_init2_)
randomCSR = _init2_.randomCSR

_init2_.plusPlusCSR_swigconstant(_init2_)
plusPlusCSR = _init2_.plusPlusCSR

_init2_.parallelPlusCSR_swigconstant(_init2_)
parallelPlusCSR = _init2_.parallelPlusCSR

_init2_.data_swigconstant(_init2_)
data = _init2_.data

_init2_.lastInputId_swigconstant(_init2_)
lastInputId = _init2_.lastInputId

_init2_.partialResults_swigconstant(_init2_)
partialResults = _init2_.partialResults

_init2_.lastDistributedStep2MasterInputId_swigconstant(_init2_)
lastDistributedStep2MasterInputId = _init2_.lastDistributedStep2MasterInputId

_init2_.internalInput_swigconstant(_init2_)
internalInput = _init2_.internalInput

_init2_.lastDistributedLocalPlusPlusInputDataId_swigconstant(_init2_)
lastDistributedLocalPlusPlusInputDataId = _init2_.lastDistributedLocalPlusPlusInputDataId

_init2_.inputOfStep2_swigconstant(_init2_)
inputOfStep2 = _init2_.inputOfStep2

_init2_.lastDistributedStep2LocalPlusPlusInputId_swigconstant(_init2_)
lastDistributedStep2LocalPlusPlusInputId = _init2_.lastDistributedStep2LocalPlusPlusInputId

_init2_.inputOfStep3FromStep2_swigconstant(_init2_)
inputOfStep3FromStep2 = _init2_.inputOfStep3FromStep2

_init2_.lastDistributedStep3MasterPlusPlusInputId_swigconstant(_init2_)
lastDistributedStep3MasterPlusPlusInputId = _init2_.lastDistributedStep3MasterPlusPlusInputId

_init2_.inputOfStep4FromStep3_swigconstant(_init2_)
inputOfStep4FromStep3 = _init2_.inputOfStep4FromStep3

_init2_.lastDistributedStep4LocalPlusPlusInputId_swigconstant(_init2_)
lastDistributedStep4LocalPlusPlusInputId = _init2_.lastDistributedStep4LocalPlusPlusInputId

_init2_.inputCentroids_swigconstant(_init2_)
inputCentroids = _init2_.inputCentroids

_init2_.inputOfStep5FromStep2_swigconstant(_init2_)
inputOfStep5FromStep2 = _init2_.inputOfStep5FromStep2

_init2_.lastDistributedStep5MasterPlusPlusInputId_swigconstant(_init2_)
lastDistributedStep5MasterPlusPlusInputId = _init2_.lastDistributedStep5MasterPlusPlusInputId

_init2_.inputOfStep5FromStep3_swigconstant(_init2_)
inputOfStep5FromStep3 = _init2_.inputOfStep5FromStep3

_init2_.lastDistributedStep5MasterPlusPlusInputDataId_swigconstant(_init2_)
lastDistributedStep5MasterPlusPlusInputDataId = _init2_.lastDistributedStep5MasterPlusPlusInputDataId

_init2_.partialCentroids_swigconstant(_init2_)
partialCentroids = _init2_.partialCentroids

_init2_.partialClusters_swigconstant(_init2_)
partialClusters = _init2_.partialClusters

_init2_.partialClustersNumber_swigconstant(_init2_)
partialClustersNumber = _init2_.partialClustersNumber

_init2_.lastPartialResultId_swigconstant(_init2_)
lastPartialResultId = _init2_.lastPartialResultId

_init2_.outputOfStep2ForStep3_swigconstant(_init2_)
outputOfStep2ForStep3 = _init2_.outputOfStep2ForStep3

_init2_.outputOfStep2ForStep5_swigconstant(_init2_)
outputOfStep2ForStep5 = _init2_.outputOfStep2ForStep5

_init2_.lastDistributedStep2LocalPlusPlusPartialResultId_swigconstant(_init2_)
lastDistributedStep2LocalPlusPlusPartialResultId = _init2_.lastDistributedStep2LocalPlusPlusPartialResultId

_init2_.internalResult_swigconstant(_init2_)
internalResult = _init2_.internalResult

_init2_.lastDistributedStep2LocalPlusPlusPartialResultDataId_swigconstant(_init2_)
lastDistributedStep2LocalPlusPlusPartialResultDataId = _init2_.lastDistributedStep2LocalPlusPlusPartialResultDataId

_init2_.outputOfStep3ForStep4_swigconstant(_init2_)
outputOfStep3ForStep4 = _init2_.outputOfStep3ForStep4

_init2_.lastDistributedStep3MasterPlusPlusPartialResultId_swigconstant(_init2_)
lastDistributedStep3MasterPlusPlusPartialResultId = _init2_.lastDistributedStep3MasterPlusPlusPartialResultId

_init2_.rngState_swigconstant(_init2_)
rngState = _init2_.rngState

_init2_.outputOfStep3ForStep5_swigconstant(_init2_)
outputOfStep3ForStep5 = _init2_.outputOfStep3ForStep5

_init2_.lastDistributedStep3MasterPlusPlusPartialResultDataId_swigconstant(_init2_)
lastDistributedStep3MasterPlusPlusPartialResultDataId = _init2_.lastDistributedStep3MasterPlusPlusPartialResultDataId

_init2_.outputOfStep4_swigconstant(_init2_)
outputOfStep4 = _init2_.outputOfStep4

_init2_.lastDistributedStep4LocalPlusPlusPartialResultId_swigconstant(_init2_)
lastDistributedStep4LocalPlusPlusPartialResultId = _init2_.lastDistributedStep4LocalPlusPlusPartialResultId

_init2_.candidates_swigconstant(_init2_)
candidates = _init2_.candidates

_init2_.weights_swigconstant(_init2_)
weights = _init2_.weights

_init2_.lastDistributedStep5MasterPlusPlusPartialResultId_swigconstant(_init2_)
lastDistributedStep5MasterPlusPlusPartialResultId = _init2_.lastDistributedStep5MasterPlusPlusPartialResultId

_init2_.centroids_swigconstant(_init2_)
centroids = _init2_.centroids

_init2_.lastResultId_swigconstant(_init2_)
lastResultId = _init2_.lastResultId
class interface1_Parameter(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nClusters"] = _init2_.interface1_Parameter_nClusters_set
    __swig_getmethods__["nClusters"] = _init2_.interface1_Parameter_nClusters_get
    if _newclass:
        nClusters = _swig_property(_init2_.interface1_Parameter_nClusters_get, _init2_.interface1_Parameter_nClusters_set)
    __swig_setmethods__["nRowsTotal"] = _init2_.interface1_Parameter_nRowsTotal_set
    __swig_getmethods__["nRowsTotal"] = _init2_.interface1_Parameter_nRowsTotal_get
    if _newclass:
        nRowsTotal = _swig_property(_init2_.interface1_Parameter_nRowsTotal_get, _init2_.interface1_Parameter_nRowsTotal_set)
    __swig_setmethods__["offset"] = _init2_.interface1_Parameter_offset_set
    __swig_getmethods__["offset"] = _init2_.interface1_Parameter_offset_get
    if _newclass:
        offset = _swig_property(_init2_.interface1_Parameter_offset_get, _init2_.interface1_Parameter_offset_set)
    __swig_setmethods__["seed"] = _init2_.interface1_Parameter_seed_set
    __swig_getmethods__["seed"] = _init2_.interface1_Parameter_seed_get
    if _newclass:
        seed = _swig_property(_init2_.interface1_Parameter_seed_get, _init2_.interface1_Parameter_seed_set)
    __swig_setmethods__["oversamplingFactor"] = _init2_.interface1_Parameter_oversamplingFactor_set
    __swig_getmethods__["oversamplingFactor"] = _init2_.interface1_Parameter_oversamplingFactor_get
    if _newclass:
        oversamplingFactor = _swig_property(_init2_.interface1_Parameter_oversamplingFactor_get, _init2_.interface1_Parameter_oversamplingFactor_set)
    __swig_setmethods__["nRounds"] = _init2_.interface1_Parameter_nRounds_set
    __swig_getmethods__["nRounds"] = _init2_.interface1_Parameter_nRounds_get
    if _newclass:
        nRounds = _swig_property(_init2_.interface1_Parameter_nRounds_get, _init2_.interface1_Parameter_nRounds_set)
    __swig_setmethods__["engine"] = _init2_.interface1_Parameter_engine_set
    __swig_getmethods__["engine"] = _init2_.interface1_Parameter_engine_get
    if _newclass:
        engine = _swig_property(_init2_.interface1_Parameter_engine_get, _init2_.interface1_Parameter_engine_set)

    def check(self):
        return _init2_.interface1_Parameter_check(self)
    __swig_destroy__ = _init2_.delete_interface1_Parameter
    __del__ = lambda self: None
interface1_Parameter_swigregister = _init2_.interface1_Parameter_swigregister
interface1_Parameter_swigregister(interface1_Parameter)

class InputIface(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, InputIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getNumberOfFeatures(self):
        return _init2_.InputIface_getNumberOfFeatures(self)
    __swig_destroy__ = _init2_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _init2_.InputIface_swigregister
InputIface_swigregister(InputIface)

class Input(InputIface):
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _init2_.new_Input()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.Input_get(self, id)

    def set(self, id, ptr):
        return _init2_.Input_set(self, id, ptr)

    def getNumberOfFeatures(self):
        return _init2_.Input_getNumberOfFeatures(self)

    def check(self, par, method):
        return _init2_.Input_check(self, par, method)
Input_swigregister = _init2_.Input_swigregister
Input_swigregister(Input)

class PartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _init2_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_PartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.PartialResult_get(self, id)

    def set(self, id, ptr):
        return _init2_.PartialResult_set(self, id, ptr)

    def getNumberOfFeatures(self):
        return _init2_.PartialResult_getNumberOfFeatures(self)

    def check(self, *args):
        return _init2_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init2_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init2_.PartialResult_allocate_Float32(self, input, parameter, method)

PartialResult_swigregister = _init2_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _init2_.PartialResult_serializationTag()
PartialResult_serializationTag = _init2_.PartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.Result_serializationTag)

    def getSerializationTag(self):
        return _init2_.Result_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.Result_get(self, id)

    def set(self, id, ptr):
        return _init2_.Result_set(self, id, ptr)

    def check(self, *args):
        return _init2_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _init2_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _init2_.Result_allocate_Float32(self, *args)

Result_swigregister = _init2_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _init2_.Result_serializationTag()
Result_serializationTag = _init2_.Result_serializationTag

class DistributedStep2MasterInput(InputIface):
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2MasterInput, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2MasterInput, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _init2_.new_DistributedStep2MasterInput()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep2MasterInput
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.DistributedStep2MasterInput_get(self, id)

    def set(self, id, ptr):
        return _init2_.DistributedStep2MasterInput_set(self, id, ptr)

    def add(self, id, value):
        return _init2_.DistributedStep2MasterInput_add(self, id, value)

    def getNumberOfFeatures(self):
        return _init2_.DistributedStep2MasterInput_getNumberOfFeatures(self)

    def check(self, par, method):
        return _init2_.DistributedStep2MasterInput_check(self, par, method)
DistributedStep2MasterInput_swigregister = _init2_.DistributedStep2MasterInput_swigregister
DistributedStep2MasterInput_swigregister(DistributedStep2MasterInput)

class DistributedStep2LocalPlusPlusParameter(interface1_Parameter):
    __swig_setmethods__ = {}
    for _s in [interface1_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2LocalPlusPlusParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [interface1_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2LocalPlusPlusParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_DistributedStep2LocalPlusPlusParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["firstIteration"] = _init2_.DistributedStep2LocalPlusPlusParameter_firstIteration_set
    __swig_getmethods__["firstIteration"] = _init2_.DistributedStep2LocalPlusPlusParameter_firstIteration_get
    if _newclass:
        firstIteration = _swig_property(_init2_.DistributedStep2LocalPlusPlusParameter_firstIteration_get, _init2_.DistributedStep2LocalPlusPlusParameter_firstIteration_set)
    __swig_setmethods__["outputForStep5Required"] = _init2_.DistributedStep2LocalPlusPlusParameter_outputForStep5Required_set
    __swig_getmethods__["outputForStep5Required"] = _init2_.DistributedStep2LocalPlusPlusParameter_outputForStep5Required_get
    if _newclass:
        outputForStep5Required = _swig_property(_init2_.DistributedStep2LocalPlusPlusParameter_outputForStep5Required_get, _init2_.DistributedStep2LocalPlusPlusParameter_outputForStep5Required_set)

    def check(self):
        return _init2_.DistributedStep2LocalPlusPlusParameter_check(self)
    __swig_destroy__ = _init2_.delete_DistributedStep2LocalPlusPlusParameter
    __del__ = lambda self: None
DistributedStep2LocalPlusPlusParameter_swigregister = _init2_.DistributedStep2LocalPlusPlusParameter_swigregister
DistributedStep2LocalPlusPlusParameter_swigregister(DistributedStep2LocalPlusPlusParameter)

class DistributedStep2LocalPlusPlusInput(Input):
    __swig_setmethods__ = {}
    for _s in [Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2LocalPlusPlusInput, name, value)
    __swig_getmethods__ = {}
    for _s in [Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2LocalPlusPlusInput, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_DistributedStep2LocalPlusPlusInput(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep2LocalPlusPlusInput
    __del__ = lambda self: None

    def getInput(self, id):
        return _init2_.DistributedStep2LocalPlusPlusInput_getInput(self, id)

    def setInput(self, id, ptr):
        return _init2_.DistributedStep2LocalPlusPlusInput_setInput(self, id, ptr)

    def getLocal(self, id):
        return _init2_.DistributedStep2LocalPlusPlusInput_getLocal(self, id)

    def setLocal(self, id, ptr):
        return _init2_.DistributedStep2LocalPlusPlusInput_setLocal(self, id, ptr)

    def getStepInput(self, id):
        return _init2_.DistributedStep2LocalPlusPlusInput_getStepInput(self, id)

    def setStepInput(self, id, ptr):
        return _init2_.DistributedStep2LocalPlusPlusInput_setStepInput(self, id, ptr)

    def check(self, par, method):
        return _init2_.DistributedStep2LocalPlusPlusInput_check(self, par, method)
DistributedStep2LocalPlusPlusInput_swigregister = _init2_.DistributedStep2LocalPlusPlusInput_swigregister
DistributedStep2LocalPlusPlusInput_swigregister(DistributedStep2LocalPlusPlusInput)

class DistributedStep3MasterPlusPlusInput(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep3MasterPlusPlusInput, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep3MasterPlusPlusInput, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_DistributedStep3MasterPlusPlusInput(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _init2_.DistributedStep3MasterPlusPlusInput_get(self, id)

    def set(self, id, ptr):
        return _init2_.DistributedStep3MasterPlusPlusInput_set(self, id, ptr)

    def add(self, id, key, ptr):
        return _init2_.DistributedStep3MasterPlusPlusInput_add(self, id, key, ptr)

    def check(self, par, method):
        return _init2_.DistributedStep3MasterPlusPlusInput_check(self, par, method)
    __swig_destroy__ = _init2_.delete_DistributedStep3MasterPlusPlusInput
    __del__ = lambda self: None
DistributedStep3MasterPlusPlusInput_swigregister = _init2_.DistributedStep3MasterPlusPlusInput_swigregister
DistributedStep3MasterPlusPlusInput_swigregister(DistributedStep3MasterPlusPlusInput)

class DistributedStep4LocalPlusPlusInput(Input):
    __swig_setmethods__ = {}
    for _s in [Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep4LocalPlusPlusInput, name, value)
    __swig_getmethods__ = {}
    for _s in [Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep4LocalPlusPlusInput, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_DistributedStep4LocalPlusPlusInput(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getInput(self, id):
        return _init2_.DistributedStep4LocalPlusPlusInput_getInput(self, id)

    def setInput(self, id, ptr):
        return _init2_.DistributedStep4LocalPlusPlusInput_setInput(self, id, ptr)

    def getLocal(self, id):
        return _init2_.DistributedStep4LocalPlusPlusInput_getLocal(self, id)

    def setLocal(self, id, ptr):
        return _init2_.DistributedStep4LocalPlusPlusInput_setLocal(self, id, ptr)

    def getStepInput(self, id):
        return _init2_.DistributedStep4LocalPlusPlusInput_getStepInput(self, id)

    def setStepInput(self, id, ptr):
        return _init2_.DistributedStep4LocalPlusPlusInput_setStepInput(self, id, ptr)

    def check(self, par, method):
        return _init2_.DistributedStep4LocalPlusPlusInput_check(self, par, method)
    __swig_destroy__ = _init2_.delete_DistributedStep4LocalPlusPlusInput
    __del__ = lambda self: None
DistributedStep4LocalPlusPlusInput_swigregister = _init2_.DistributedStep4LocalPlusPlusInput_swigregister
DistributedStep4LocalPlusPlusInput_swigregister(DistributedStep4LocalPlusPlusInput)

class DistributedStep5MasterPlusPlusInput(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep5MasterPlusPlusInput, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep5MasterPlusPlusInput, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_DistributedStep5MasterPlusPlusInput(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep5MasterPlusPlusInput
    __del__ = lambda self: None

    def getInput(self, id):
        return _init2_.DistributedStep5MasterPlusPlusInput_getInput(self, id)

    def setInput(self, id, ptr):
        return _init2_.DistributedStep5MasterPlusPlusInput_setInput(self, id, ptr)

    def add(self, id, value):
        return _init2_.DistributedStep5MasterPlusPlusInput_add(self, id, value)

    def getStepInput(self, id):
        return _init2_.DistributedStep5MasterPlusPlusInput_getStepInput(self, id)

    def setStepInput(self, id, ptr):
        return _init2_.DistributedStep5MasterPlusPlusInput_setStepInput(self, id, ptr)

    def check(self, par, method):
        return _init2_.DistributedStep5MasterPlusPlusInput_check(self, par, method)
DistributedStep5MasterPlusPlusInput_swigregister = _init2_.DistributedStep5MasterPlusPlusInput_swigregister
DistributedStep5MasterPlusPlusInput_swigregister(DistributedStep5MasterPlusPlusInput)

class DistributedStep2LocalPlusPlusPartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2LocalPlusPlusPartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2LocalPlusPlusPartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.DistributedStep2LocalPlusPlusPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.DistributedStep2LocalPlusPlusPartialResult_serializationTag)

    def getSerializationTag(self):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_DistributedStep2LocalPlusPlusPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep2LocalPlusPlusPartialResult
    __del__ = lambda self: None

    def getOutput(self, id):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_getOutput(self, id)

    def setOutput(self, id, ptr):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_setOutput(self, id, ptr)

    def getLocal(self, id):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_getLocal(self, id)

    def setLocal(self, id, ptr):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_setLocal(self, id, ptr)

    def check(self, *args):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_check(self, *args)

    def initialize(self, input, par, method):
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_initialize(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init2_.DistributedStep2LocalPlusPlusPartialResult_allocate_Float32(self, input, parameter, method)

DistributedStep2LocalPlusPlusPartialResult_swigregister = _init2_.DistributedStep2LocalPlusPlusPartialResult_swigregister
DistributedStep2LocalPlusPlusPartialResult_swigregister(DistributedStep2LocalPlusPlusPartialResult)

def DistributedStep2LocalPlusPlusPartialResult_serializationTag():
    return _init2_.DistributedStep2LocalPlusPlusPartialResult_serializationTag()
DistributedStep2LocalPlusPlusPartialResult_serializationTag = _init2_.DistributedStep2LocalPlusPlusPartialResult_serializationTag

class DistributedStep3MasterPlusPlusPartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep3MasterPlusPlusPartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep3MasterPlusPlusPartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.DistributedStep3MasterPlusPlusPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.DistributedStep3MasterPlusPlusPartialResult_serializationTag)

    def getSerializationTag(self):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_DistributedStep3MasterPlusPlusPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep3MasterPlusPlusPartialResult
    __del__ = lambda self: None

    def getOutput(self, *args):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_getOutput(self, *args)

    def getStepOutput(self, id):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_getStepOutput(self, id)

    def add(self, id, key, ptr):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_add(self, id, key, ptr)

    def check(self, *args):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_check(self, *args)

    def initialize(self, input, par, method):
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_initialize(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init2_.DistributedStep3MasterPlusPlusPartialResult_allocate_Float32(self, input, parameter, method)

DistributedStep3MasterPlusPlusPartialResult_swigregister = _init2_.DistributedStep3MasterPlusPlusPartialResult_swigregister
DistributedStep3MasterPlusPlusPartialResult_swigregister(DistributedStep3MasterPlusPlusPartialResult)

def DistributedStep3MasterPlusPlusPartialResult_serializationTag():
    return _init2_.DistributedStep3MasterPlusPlusPartialResult_serializationTag()
DistributedStep3MasterPlusPlusPartialResult_serializationTag = _init2_.DistributedStep3MasterPlusPlusPartialResult_serializationTag

class DistributedStep4LocalPlusPlusPartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep4LocalPlusPlusPartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep4LocalPlusPlusPartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.DistributedStep4LocalPlusPlusPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.DistributedStep4LocalPlusPlusPartialResult_serializationTag)

    def getSerializationTag(self):
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_DistributedStep4LocalPlusPlusPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep4LocalPlusPlusPartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_get(self, id)

    def set(self, id, ptr):
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_set(self, id, ptr)

    def check(self, *args):
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init2_.DistributedStep4LocalPlusPlusPartialResult_allocate_Float32(self, input, parameter, method)

DistributedStep4LocalPlusPlusPartialResult_swigregister = _init2_.DistributedStep4LocalPlusPlusPartialResult_swigregister
DistributedStep4LocalPlusPlusPartialResult_swigregister(DistributedStep4LocalPlusPlusPartialResult)

def DistributedStep4LocalPlusPlusPartialResult_serializationTag():
    return _init2_.DistributedStep4LocalPlusPlusPartialResult_serializationTag()
DistributedStep4LocalPlusPlusPartialResult_serializationTag = _init2_.DistributedStep4LocalPlusPlusPartialResult_serializationTag

class DistributedStep5MasterPlusPlusPartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep5MasterPlusPlusPartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep5MasterPlusPlusPartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _init2_.DistributedStep5MasterPlusPlusPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_init2_.DistributedStep5MasterPlusPlusPartialResult_serializationTag)

    def getSerializationTag(self):
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _init2_.new_DistributedStep5MasterPlusPlusPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_DistributedStep5MasterPlusPlusPartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_get(self, id)

    def set(self, id, ptr):
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_set(self, id, ptr)

    def check(self, *args):
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _init2_.DistributedStep5MasterPlusPlusPartialResult_allocate_Float32(self, input, parameter, method)

DistributedStep5MasterPlusPlusPartialResult_swigregister = _init2_.DistributedStep5MasterPlusPlusPartialResult_swigregister
DistributedStep5MasterPlusPlusPartialResult_swigregister(DistributedStep5MasterPlusPlusPartialResult)

def DistributedStep5MasterPlusPlusPartialResult_serializationTag():
    return _init2_.DistributedStep5MasterPlusPlusPartialResult_serializationTag()
DistributedStep5MasterPlusPlusPartialResult_serializationTag = _init2_.DistributedStep5MasterPlusPlusPartialResult_serializationTag

class Parameter(interface1_Parameter):
    __swig_setmethods__ = {}
    for _s in [interface1_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [interface1_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nTrials"] = _init2_.Parameter_nTrials_set
    __swig_getmethods__["nTrials"] = _init2_.Parameter_nTrials_get
    if _newclass:
        nTrials = _swig_property(_init2_.Parameter_nTrials_get, _init2_.Parameter_nTrials_set)

    def check(self):
        return _init2_.Parameter_check(self)
    __swig_destroy__ = _init2_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _init2_.Parameter_swigregister
Parameter_swigregister(Parameter)

class DistributedBase(daal.algorithms.Analysis_Distributed):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedBase, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _init2_.delete_DistributedBase
    __del__ = lambda self: None
DistributedBase_swigregister = _init2_.DistributedBase_swigregister
DistributedBase_swigregister(DistributedBase)

class DistributedStep2LocalPlusPlusBase(daal.algorithms.Analysis_Distributed):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedStep2LocalPlusPlusBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedStep2LocalPlusPlusBase, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _init2_.delete_DistributedStep2LocalPlusPlusBase
    __del__ = lambda self: None
DistributedStep2LocalPlusPlusBase_swigregister = _init2_.DistributedStep2LocalPlusPlusBase_swigregister
DistributedStep2LocalPlusPlusBase_swigregister(DistributedStep2LocalPlusPlusBase)

class BatchBase(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchBase, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _init2_.delete_BatchBase
    __del__ = lambda self: None
BatchBase_swigregister = _init2_.BatchBase_swigregister
BatchBase_swigregister(BatchBase)

class Batch_Float64DeterministicDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64DeterministicDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64DeterministicDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64DeterministicDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64DeterministicDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64DeterministicDense_parameter_get, _init2_.Batch_Float64DeterministicDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64DeterministicDense_input_get, _init2_.Batch_Float64DeterministicDense_input_set)

    def compute(self):
        return _init2_.Batch_Float64DeterministicDense_compute(self)
Batch_Float64DeterministicDense_swigregister = _init2_.Batch_Float64DeterministicDense_swigregister
Batch_Float64DeterministicDense_swigregister(Batch_Float64DeterministicDense)

class Batch_Float64RandomDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64RandomDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64RandomDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64RandomDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64RandomDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64RandomDense_parameter_get, _init2_.Batch_Float64RandomDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64RandomDense_input_get, _init2_.Batch_Float64RandomDense_input_set)

    def compute(self):
        return _init2_.Batch_Float64RandomDense_compute(self)
Batch_Float64RandomDense_swigregister = _init2_.Batch_Float64RandomDense_swigregister
Batch_Float64RandomDense_swigregister(Batch_Float64RandomDense)

class Batch_Float64PlusPlusDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64PlusPlusDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64PlusPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64PlusPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64PlusPlusDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64PlusPlusDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64PlusPlusDense_parameter_get, _init2_.Batch_Float64PlusPlusDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64PlusPlusDense_input_get, _init2_.Batch_Float64PlusPlusDense_input_set)

    def compute(self):
        return _init2_.Batch_Float64PlusPlusDense_compute(self)
Batch_Float64PlusPlusDense_swigregister = _init2_.Batch_Float64PlusPlusDense_swigregister
Batch_Float64PlusPlusDense_swigregister(Batch_Float64PlusPlusDense)

class Batch_Float64RandomCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64RandomCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64RandomCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64RandomCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64RandomCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64RandomCSR_parameter_get, _init2_.Batch_Float64RandomCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64RandomCSR_input_get, _init2_.Batch_Float64RandomCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float64RandomCSR_compute(self)
Batch_Float64RandomCSR_swigregister = _init2_.Batch_Float64RandomCSR_swigregister
Batch_Float64RandomCSR_swigregister(Batch_Float64RandomCSR)

class Batch_Float64ParallelPlusDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64ParallelPlusDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64ParallelPlusDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64ParallelPlusDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64ParallelPlusDense_parameter_get, _init2_.Batch_Float64ParallelPlusDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64ParallelPlusDense_input_get, _init2_.Batch_Float64ParallelPlusDense_input_set)

    def compute(self):
        return _init2_.Batch_Float64ParallelPlusDense_compute(self)
Batch_Float64ParallelPlusDense_swigregister = _init2_.Batch_Float64ParallelPlusDense_swigregister
Batch_Float64ParallelPlusDense_swigregister(Batch_Float64ParallelPlusDense)

class Batch_Float64ParallelPlusCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64ParallelPlusCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64ParallelPlusCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64ParallelPlusCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64ParallelPlusCSR_parameter_get, _init2_.Batch_Float64ParallelPlusCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64ParallelPlusCSR_input_get, _init2_.Batch_Float64ParallelPlusCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float64ParallelPlusCSR_compute(self)
Batch_Float64ParallelPlusCSR_swigregister = _init2_.Batch_Float64ParallelPlusCSR_swigregister
Batch_Float64ParallelPlusCSR_swigregister(Batch_Float64ParallelPlusCSR)

class Batch_Float64DeterministicCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64DeterministicCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64DeterministicCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64DeterministicCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64DeterministicCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64DeterministicCSR_parameter_get, _init2_.Batch_Float64DeterministicCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64DeterministicCSR_input_get, _init2_.Batch_Float64DeterministicCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float64DeterministicCSR_compute(self)
Batch_Float64DeterministicCSR_swigregister = _init2_.Batch_Float64DeterministicCSR_swigregister
Batch_Float64DeterministicCSR_swigregister(Batch_Float64DeterministicCSR)

class Batch_Float64PlusPlusCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float64PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float64PlusPlusCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float64PlusPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float64PlusPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float64PlusPlusCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float64PlusPlusCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float64PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float64PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float64PlusPlusCSR_parameter_get, _init2_.Batch_Float64PlusPlusCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float64PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float64PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float64PlusPlusCSR_input_get, _init2_.Batch_Float64PlusPlusCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float64PlusPlusCSR_compute(self)
Batch_Float64PlusPlusCSR_swigregister = _init2_.Batch_Float64PlusPlusCSR_swigregister
Batch_Float64PlusPlusCSR_swigregister(Batch_Float64PlusPlusCSR)

class Batch_Float32DeterministicDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32DeterministicDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32DeterministicDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32DeterministicDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32DeterministicDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32DeterministicDense_parameter_get, _init2_.Batch_Float32DeterministicDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32DeterministicDense_input_get, _init2_.Batch_Float32DeterministicDense_input_set)

    def compute(self):
        return _init2_.Batch_Float32DeterministicDense_compute(self)
Batch_Float32DeterministicDense_swigregister = _init2_.Batch_Float32DeterministicDense_swigregister
Batch_Float32DeterministicDense_swigregister(Batch_Float32DeterministicDense)

class Batch_Float32RandomDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32RandomDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32RandomDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32RandomDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32RandomDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32RandomDense_parameter_get, _init2_.Batch_Float32RandomDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32RandomDense_input_get, _init2_.Batch_Float32RandomDense_input_set)

    def compute(self):
        return _init2_.Batch_Float32RandomDense_compute(self)
Batch_Float32RandomDense_swigregister = _init2_.Batch_Float32RandomDense_swigregister
Batch_Float32RandomDense_swigregister(Batch_Float32RandomDense)

class Batch_Float32PlusPlusDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32PlusPlusDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32PlusPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32PlusPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32PlusPlusDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32PlusPlusDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32PlusPlusDense_parameter_get, _init2_.Batch_Float32PlusPlusDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32PlusPlusDense_input_get, _init2_.Batch_Float32PlusPlusDense_input_set)

    def compute(self):
        return _init2_.Batch_Float32PlusPlusDense_compute(self)
Batch_Float32PlusPlusDense_swigregister = _init2_.Batch_Float32PlusPlusDense_swigregister
Batch_Float32PlusPlusDense_swigregister(Batch_Float32PlusPlusDense)

class Batch_Float32RandomCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32RandomCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32RandomCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32RandomCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32RandomCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32RandomCSR_parameter_get, _init2_.Batch_Float32RandomCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32RandomCSR_input_get, _init2_.Batch_Float32RandomCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float32RandomCSR_compute(self)
Batch_Float32RandomCSR_swigregister = _init2_.Batch_Float32RandomCSR_swigregister
Batch_Float32RandomCSR_swigregister(Batch_Float32RandomCSR)

class Batch_Float32ParallelPlusDense(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32ParallelPlusDense
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32ParallelPlusDense_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32ParallelPlusDense_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32ParallelPlusDense_parameter_get, _init2_.Batch_Float32ParallelPlusDense_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32ParallelPlusDense_input_get, _init2_.Batch_Float32ParallelPlusDense_input_set)

    def compute(self):
        return _init2_.Batch_Float32ParallelPlusDense_compute(self)
Batch_Float32ParallelPlusDense_swigregister = _init2_.Batch_Float32ParallelPlusDense_swigregister
Batch_Float32ParallelPlusDense_swigregister(Batch_Float32ParallelPlusDense)

class Batch_Float32ParallelPlusCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32ParallelPlusCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32ParallelPlusCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32ParallelPlusCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32ParallelPlusCSR_parameter_get, _init2_.Batch_Float32ParallelPlusCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32ParallelPlusCSR_input_get, _init2_.Batch_Float32ParallelPlusCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float32ParallelPlusCSR_compute(self)
Batch_Float32ParallelPlusCSR_swigregister = _init2_.Batch_Float32ParallelPlusCSR_swigregister
Batch_Float32ParallelPlusCSR_swigregister(Batch_Float32ParallelPlusCSR)

class Batch_Float32DeterministicCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32DeterministicCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32DeterministicCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32DeterministicCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32DeterministicCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32DeterministicCSR_parameter_get, _init2_.Batch_Float32DeterministicCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32DeterministicCSR_input_get, _init2_.Batch_Float32DeterministicCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float32DeterministicCSR_compute(self)
Batch_Float32DeterministicCSR_swigregister = _init2_.Batch_Float32DeterministicCSR_swigregister
Batch_Float32DeterministicCSR_swigregister(Batch_Float32DeterministicCSR)

class Batch_Float32PlusPlusCSR(BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Batch_Float32PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _init2_.delete_Batch_Float32PlusPlusCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _init2_.Batch_Float32PlusPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Batch_Float32PlusPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Batch_Float32PlusPlusCSR_setResult(self, result)

    def clone(self):
        return _init2_.Batch_Float32PlusPlusCSR_clone(self)
    __swig_setmethods__["parameter"] = _init2_.Batch_Float32PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Batch_Float32PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Batch_Float32PlusPlusCSR_parameter_get, _init2_.Batch_Float32PlusPlusCSR_parameter_set)
    __swig_setmethods__["input"] = _init2_.Batch_Float32PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Batch_Float32PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Batch_Float32PlusPlusCSR_input_get, _init2_.Batch_Float32PlusPlusCSR_input_set)

    def compute(self):
        return _init2_.Batch_Float32PlusPlusCSR_compute(self)
Batch_Float32PlusPlusCSR_swigregister = _init2_.Batch_Float32PlusPlusCSR_swigregister
Batch_Float32PlusPlusCSR_swigregister(Batch_Float32PlusPlusCSR)

class Distributed_Step1LocalFloat64DeterministicDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64DeterministicDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64DeterministicDense_input_get, _init2_.Distributed_Step1LocalFloat64DeterministicDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64DeterministicDense_parameter_get, _init2_.Distributed_Step1LocalFloat64DeterministicDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64DeterministicDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DeterministicDense_swigregister = _init2_.Distributed_Step1LocalFloat64DeterministicDense_swigregister
Distributed_Step1LocalFloat64DeterministicDense_swigregister(Distributed_Step1LocalFloat64DeterministicDense)

class Distributed_Step1LocalFloat64DeterministicCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64DeterministicCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64DeterministicCSR_input_get, _init2_.Distributed_Step1LocalFloat64DeterministicCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64DeterministicCSR_parameter_get, _init2_.Distributed_Step1LocalFloat64DeterministicCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64DeterministicCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64DeterministicCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DeterministicCSR_swigregister = _init2_.Distributed_Step1LocalFloat64DeterministicCSR_swigregister
Distributed_Step1LocalFloat64DeterministicCSR_swigregister(Distributed_Step1LocalFloat64DeterministicCSR)

class Distributed_Step1LocalFloat64RandomDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64RandomDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64RandomDense_input_get, _init2_.Distributed_Step1LocalFloat64RandomDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64RandomDense_parameter_get, _init2_.Distributed_Step1LocalFloat64RandomDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64RandomDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64RandomDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64RandomDense_swigregister = _init2_.Distributed_Step1LocalFloat64RandomDense_swigregister
Distributed_Step1LocalFloat64RandomDense_swigregister(Distributed_Step1LocalFloat64RandomDense)

class Distributed_Step1LocalFloat64RandomCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64RandomCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64RandomCSR_input_get, _init2_.Distributed_Step1LocalFloat64RandomCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64RandomCSR_parameter_get, _init2_.Distributed_Step1LocalFloat64RandomCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64RandomCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64RandomCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64RandomCSR_swigregister = _init2_.Distributed_Step1LocalFloat64RandomCSR_swigregister
Distributed_Step1LocalFloat64RandomCSR_swigregister(Distributed_Step1LocalFloat64RandomCSR)

class Distributed_Step1LocalFloat64PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64PlusPlusDense_input_get, _init2_.Distributed_Step1LocalFloat64PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64PlusPlusDense_parameter_get, _init2_.Distributed_Step1LocalFloat64PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64PlusPlusDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64PlusPlusDense_swigregister = _init2_.Distributed_Step1LocalFloat64PlusPlusDense_swigregister
Distributed_Step1LocalFloat64PlusPlusDense_swigregister(Distributed_Step1LocalFloat64PlusPlusDense)

class Distributed_Step1LocalFloat64PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64PlusPlusCSR_input_get, _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64PlusPlusCSR_parameter_get, _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64PlusPlusCSR_swigregister = _init2_.Distributed_Step1LocalFloat64PlusPlusCSR_swigregister
Distributed_Step1LocalFloat64PlusPlusCSR_swigregister(Distributed_Step1LocalFloat64PlusPlusCSR)

class Distributed_Step1LocalFloat64ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64ParallelPlusDense_input_get, _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64ParallelPlusDense_parameter_get, _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64ParallelPlusDense_swigregister = _init2_.Distributed_Step1LocalFloat64ParallelPlusDense_swigregister
Distributed_Step1LocalFloat64ParallelPlusDense_swigregister(Distributed_Step1LocalFloat64ParallelPlusDense)

class Distributed_Step1LocalFloat64ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_input_get, _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_parameter_get, _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat64ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64ParallelPlusCSR_swigregister = _init2_.Distributed_Step1LocalFloat64ParallelPlusCSR_swigregister
Distributed_Step1LocalFloat64ParallelPlusCSR_swigregister(Distributed_Step1LocalFloat64ParallelPlusCSR)

class Distributed_Step1LocalFloat32DeterministicDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32DeterministicDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32DeterministicDense_input_get, _init2_.Distributed_Step1LocalFloat32DeterministicDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32DeterministicDense_parameter_get, _init2_.Distributed_Step1LocalFloat32DeterministicDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32DeterministicDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DeterministicDense_swigregister = _init2_.Distributed_Step1LocalFloat32DeterministicDense_swigregister
Distributed_Step1LocalFloat32DeterministicDense_swigregister(Distributed_Step1LocalFloat32DeterministicDense)

class Distributed_Step1LocalFloat32DeterministicCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32DeterministicCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32DeterministicCSR_input_get, _init2_.Distributed_Step1LocalFloat32DeterministicCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32DeterministicCSR_parameter_get, _init2_.Distributed_Step1LocalFloat32DeterministicCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32DeterministicCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32DeterministicCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DeterministicCSR_swigregister = _init2_.Distributed_Step1LocalFloat32DeterministicCSR_swigregister
Distributed_Step1LocalFloat32DeterministicCSR_swigregister(Distributed_Step1LocalFloat32DeterministicCSR)

class Distributed_Step1LocalFloat32RandomDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32RandomDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32RandomDense_input_get, _init2_.Distributed_Step1LocalFloat32RandomDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32RandomDense_parameter_get, _init2_.Distributed_Step1LocalFloat32RandomDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32RandomDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32RandomDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32RandomDense_swigregister = _init2_.Distributed_Step1LocalFloat32RandomDense_swigregister
Distributed_Step1LocalFloat32RandomDense_swigregister(Distributed_Step1LocalFloat32RandomDense)

class Distributed_Step1LocalFloat32RandomCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32RandomCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32RandomCSR_input_get, _init2_.Distributed_Step1LocalFloat32RandomCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32RandomCSR_parameter_get, _init2_.Distributed_Step1LocalFloat32RandomCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32RandomCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32RandomCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32RandomCSR_swigregister = _init2_.Distributed_Step1LocalFloat32RandomCSR_swigregister
Distributed_Step1LocalFloat32RandomCSR_swigregister(Distributed_Step1LocalFloat32RandomCSR)

class Distributed_Step1LocalFloat32PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32PlusPlusDense_input_get, _init2_.Distributed_Step1LocalFloat32PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32PlusPlusDense_parameter_get, _init2_.Distributed_Step1LocalFloat32PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32PlusPlusDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32PlusPlusDense_swigregister = _init2_.Distributed_Step1LocalFloat32PlusPlusDense_swigregister
Distributed_Step1LocalFloat32PlusPlusDense_swigregister(Distributed_Step1LocalFloat32PlusPlusDense)

class Distributed_Step1LocalFloat32PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32PlusPlusCSR_input_get, _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32PlusPlusCSR_parameter_get, _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32PlusPlusCSR_swigregister = _init2_.Distributed_Step1LocalFloat32PlusPlusCSR_swigregister
Distributed_Step1LocalFloat32PlusPlusCSR_swigregister(Distributed_Step1LocalFloat32PlusPlusCSR)

class Distributed_Step1LocalFloat32ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32ParallelPlusDense_input_get, _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32ParallelPlusDense_parameter_get, _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32ParallelPlusDense_swigregister = _init2_.Distributed_Step1LocalFloat32ParallelPlusDense_swigregister
Distributed_Step1LocalFloat32ParallelPlusDense_swigregister(Distributed_Step1LocalFloat32ParallelPlusDense)

class Distributed_Step1LocalFloat32ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step1LocalFloat32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_input_get, _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_parameter_get, _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step1LocalFloat32ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32ParallelPlusCSR_swigregister = _init2_.Distributed_Step1LocalFloat32ParallelPlusCSR_swigregister
Distributed_Step1LocalFloat32ParallelPlusCSR_swigregister(Distributed_Step1LocalFloat32ParallelPlusCSR)

class Distributed_Step2MasterFloat64DeterministicDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat64DeterministicDense(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat64DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat64DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat64DeterministicDense_input_get, _init2_.Distributed_Step2MasterFloat64DeterministicDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat64DeterministicDense_parameter_get, _init2_.Distributed_Step2MasterFloat64DeterministicDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat64DeterministicDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64DeterministicDense_swigregister = _init2_.Distributed_Step2MasterFloat64DeterministicDense_swigregister
Distributed_Step2MasterFloat64DeterministicDense_swigregister(Distributed_Step2MasterFloat64DeterministicDense)

class Distributed_Step2MasterFloat64DeterministicCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat64DeterministicCSR(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat64DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat64DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat64DeterministicCSR_input_get, _init2_.Distributed_Step2MasterFloat64DeterministicCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat64DeterministicCSR_parameter_get, _init2_.Distributed_Step2MasterFloat64DeterministicCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat64DeterministicCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat64DeterministicCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64DeterministicCSR_swigregister = _init2_.Distributed_Step2MasterFloat64DeterministicCSR_swigregister
Distributed_Step2MasterFloat64DeterministicCSR_swigregister(Distributed_Step2MasterFloat64DeterministicCSR)

class Distributed_Step2MasterFloat64RandomDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat64RandomDense(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat64RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat64RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat64RandomDense_input_get, _init2_.Distributed_Step2MasterFloat64RandomDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat64RandomDense_parameter_get, _init2_.Distributed_Step2MasterFloat64RandomDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat64RandomDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat64RandomDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64RandomDense_swigregister = _init2_.Distributed_Step2MasterFloat64RandomDense_swigregister
Distributed_Step2MasterFloat64RandomDense_swigregister(Distributed_Step2MasterFloat64RandomDense)

class Distributed_Step2MasterFloat64RandomCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat64RandomCSR(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat64RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat64RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat64RandomCSR_input_get, _init2_.Distributed_Step2MasterFloat64RandomCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat64RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat64RandomCSR_parameter_get, _init2_.Distributed_Step2MasterFloat64RandomCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat64RandomCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat64RandomCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64RandomCSR_swigregister = _init2_.Distributed_Step2MasterFloat64RandomCSR_swigregister
Distributed_Step2MasterFloat64RandomCSR_swigregister(Distributed_Step2MasterFloat64RandomCSR)

class Distributed_Step2MasterFloat32DeterministicDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DeterministicDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DeterministicDense, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat32DeterministicDense(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat32DeterministicDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat32DeterministicDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat32DeterministicDense_input_get, _init2_.Distributed_Step2MasterFloat32DeterministicDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32DeterministicDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32DeterministicDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat32DeterministicDense_parameter_get, _init2_.Distributed_Step2MasterFloat32DeterministicDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat32DeterministicDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32DeterministicDense_swigregister = _init2_.Distributed_Step2MasterFloat32DeterministicDense_swigregister
Distributed_Step2MasterFloat32DeterministicDense_swigregister(Distributed_Step2MasterFloat32DeterministicDense)

class Distributed_Step2MasterFloat32DeterministicCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DeterministicCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DeterministicCSR, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat32DeterministicCSR(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat32DeterministicCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat32DeterministicCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat32DeterministicCSR_input_get, _init2_.Distributed_Step2MasterFloat32DeterministicCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32DeterministicCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32DeterministicCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat32DeterministicCSR_parameter_get, _init2_.Distributed_Step2MasterFloat32DeterministicCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat32DeterministicCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat32DeterministicCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32DeterministicCSR_swigregister = _init2_.Distributed_Step2MasterFloat32DeterministicCSR_swigregister
Distributed_Step2MasterFloat32DeterministicCSR_swigregister(Distributed_Step2MasterFloat32DeterministicCSR)

class Distributed_Step2MasterFloat32RandomDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32RandomDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32RandomDense, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat32RandomDense(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat32RandomDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat32RandomDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat32RandomDense_input_get, _init2_.Distributed_Step2MasterFloat32RandomDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32RandomDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32RandomDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat32RandomDense_parameter_get, _init2_.Distributed_Step2MasterFloat32RandomDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat32RandomDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat32RandomDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32RandomDense_swigregister = _init2_.Distributed_Step2MasterFloat32RandomDense_swigregister
Distributed_Step2MasterFloat32RandomDense_swigregister(Distributed_Step2MasterFloat32RandomDense)

class Distributed_Step2MasterFloat32RandomCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32RandomCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32RandomCSR, name)
    __repr__ = _swig_repr

    def __init__(self, nClusters, offset=0):
        this = _init2_.new_Distributed_Step2MasterFloat32RandomCSR(nClusters, offset)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2MasterFloat32RandomCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2MasterFloat32RandomCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2MasterFloat32RandomCSR_input_get, _init2_.Distributed_Step2MasterFloat32RandomCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32RandomCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2MasterFloat32RandomCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2MasterFloat32RandomCSR_parameter_get, _init2_.Distributed_Step2MasterFloat32RandomCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step2MasterFloat32RandomCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2MasterFloat32RandomCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32RandomCSR_swigregister = _init2_.Distributed_Step2MasterFloat32RandomCSR_swigregister
Distributed_Step2MasterFloat32RandomCSR_swigregister(Distributed_Step2MasterFloat32RandomCSR)

class Distributed_Step2LocalFloat64PlusPlusDense(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat64PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat64PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat64PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat64PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat64PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat64PlusPlusDense_input_get, _init2_.Distributed_Step2LocalFloat64PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat64PlusPlusDense_parameter_get, _init2_.Distributed_Step2LocalFloat64PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat64PlusPlusDense
    __del__ = lambda self: None
Distributed_Step2LocalFloat64PlusPlusDense_swigregister = _init2_.Distributed_Step2LocalFloat64PlusPlusDense_swigregister
Distributed_Step2LocalFloat64PlusPlusDense_swigregister(Distributed_Step2LocalFloat64PlusPlusDense)

class Distributed_Step2LocalFloat64ParallelPlusDense(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat64ParallelPlusDense_input_get, _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat64ParallelPlusDense_parameter_get, _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat64ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step2LocalFloat64ParallelPlusDense_swigregister = _init2_.Distributed_Step2LocalFloat64ParallelPlusDense_swigregister
Distributed_Step2LocalFloat64ParallelPlusDense_swigregister(Distributed_Step2LocalFloat64ParallelPlusDense)

class Distributed_Step2LocalFloat64PlusPlusCSR(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat64PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat64PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat64PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat64PlusPlusCSR_input_get, _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat64PlusPlusCSR_parameter_get, _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat64PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat64PlusPlusCSR_swigregister = _init2_.Distributed_Step2LocalFloat64PlusPlusCSR_swigregister
Distributed_Step2LocalFloat64PlusPlusCSR_swigregister(Distributed_Step2LocalFloat64PlusPlusCSR)

class Distributed_Step2LocalFloat64ParallelPlusCSR(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_input_get, _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_parameter_get, _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat64ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat64ParallelPlusCSR_swigregister = _init2_.Distributed_Step2LocalFloat64ParallelPlusCSR_swigregister
Distributed_Step2LocalFloat64ParallelPlusCSR_swigregister(Distributed_Step2LocalFloat64ParallelPlusCSR)

class Distributed_Step2LocalFloat32PlusPlusDense(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat32PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat32PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat32PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat32PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat32PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat32PlusPlusDense_input_get, _init2_.Distributed_Step2LocalFloat32PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat32PlusPlusDense_parameter_get, _init2_.Distributed_Step2LocalFloat32PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat32PlusPlusDense
    __del__ = lambda self: None
Distributed_Step2LocalFloat32PlusPlusDense_swigregister = _init2_.Distributed_Step2LocalFloat32PlusPlusDense_swigregister
Distributed_Step2LocalFloat32PlusPlusDense_swigregister(Distributed_Step2LocalFloat32PlusPlusDense)

class Distributed_Step2LocalFloat32ParallelPlusDense(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat32ParallelPlusDense_input_get, _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat32ParallelPlusDense_parameter_get, _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat32ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step2LocalFloat32ParallelPlusDense_swigregister = _init2_.Distributed_Step2LocalFloat32ParallelPlusDense_swigregister
Distributed_Step2LocalFloat32ParallelPlusDense_swigregister(Distributed_Step2LocalFloat32ParallelPlusDense)

class Distributed_Step2LocalFloat32PlusPlusCSR(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat32PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat32PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat32PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat32PlusPlusCSR_input_get, _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat32PlusPlusCSR_parameter_get, _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat32PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat32PlusPlusCSR_swigregister = _init2_.Distributed_Step2LocalFloat32PlusPlusCSR_swigregister
Distributed_Step2LocalFloat32PlusPlusCSR_swigregister(Distributed_Step2LocalFloat32PlusPlusCSR)

class Distributed_Step2LocalFloat32ParallelPlusCSR(DistributedStep2LocalPlusPlusBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2LocalFloat32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedStep2LocalPlusPlusBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2LocalFloat32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step2LocalFloat32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_input_get, _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_parameter_get, _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step2LocalFloat32ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step2LocalFloat32ParallelPlusCSR_swigregister = _init2_.Distributed_Step2LocalFloat32ParallelPlusCSR_swigregister
Distributed_Step2LocalFloat32ParallelPlusCSR_swigregister(Distributed_Step2LocalFloat32ParallelPlusCSR)

class Distributed_Step3MasterFloat64PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat64PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat64PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat64PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat64PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat64PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat64PlusPlusDense_input_get, _init2_.Distributed_Step3MasterFloat64PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat64PlusPlusDense_parameter_get, _init2_.Distributed_Step3MasterFloat64PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat64PlusPlusDense
    __del__ = lambda self: None
Distributed_Step3MasterFloat64PlusPlusDense_swigregister = _init2_.Distributed_Step3MasterFloat64PlusPlusDense_swigregister
Distributed_Step3MasterFloat64PlusPlusDense_swigregister(Distributed_Step3MasterFloat64PlusPlusDense)

class Distributed_Step3MasterFloat64ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat64ParallelPlusDense_input_get, _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat64ParallelPlusDense_parameter_get, _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat64ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step3MasterFloat64ParallelPlusDense_swigregister = _init2_.Distributed_Step3MasterFloat64ParallelPlusDense_swigregister
Distributed_Step3MasterFloat64ParallelPlusDense_swigregister(Distributed_Step3MasterFloat64ParallelPlusDense)

class Distributed_Step3MasterFloat64PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat64PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat64PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat64PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat64PlusPlusCSR_input_get, _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat64PlusPlusCSR_parameter_get, _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat64PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step3MasterFloat64PlusPlusCSR_swigregister = _init2_.Distributed_Step3MasterFloat64PlusPlusCSR_swigregister
Distributed_Step3MasterFloat64PlusPlusCSR_swigregister(Distributed_Step3MasterFloat64PlusPlusCSR)

class Distributed_Step3MasterFloat64ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_input_get, _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_parameter_get, _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat64ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step3MasterFloat64ParallelPlusCSR_swigregister = _init2_.Distributed_Step3MasterFloat64ParallelPlusCSR_swigregister
Distributed_Step3MasterFloat64ParallelPlusCSR_swigregister(Distributed_Step3MasterFloat64ParallelPlusCSR)

class Distributed_Step3MasterFloat32PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat32PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat32PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat32PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat32PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat32PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat32PlusPlusDense_input_get, _init2_.Distributed_Step3MasterFloat32PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat32PlusPlusDense_parameter_get, _init2_.Distributed_Step3MasterFloat32PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat32PlusPlusDense
    __del__ = lambda self: None
Distributed_Step3MasterFloat32PlusPlusDense_swigregister = _init2_.Distributed_Step3MasterFloat32PlusPlusDense_swigregister
Distributed_Step3MasterFloat32PlusPlusDense_swigregister(Distributed_Step3MasterFloat32PlusPlusDense)

class Distributed_Step3MasterFloat32ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat32ParallelPlusDense_input_get, _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat32ParallelPlusDense_parameter_get, _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat32ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step3MasterFloat32ParallelPlusDense_swigregister = _init2_.Distributed_Step3MasterFloat32ParallelPlusDense_swigregister
Distributed_Step3MasterFloat32ParallelPlusDense_swigregister(Distributed_Step3MasterFloat32ParallelPlusDense)

class Distributed_Step3MasterFloat32PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat32PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat32PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat32PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat32PlusPlusCSR_input_get, _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat32PlusPlusCSR_parameter_get, _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat32PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step3MasterFloat32PlusPlusCSR_swigregister = _init2_.Distributed_Step3MasterFloat32PlusPlusCSR_swigregister
Distributed_Step3MasterFloat32PlusPlusCSR_swigregister(Distributed_Step3MasterFloat32PlusPlusCSR)

class Distributed_Step3MasterFloat32ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step3MasterFloat32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step3MasterFloat32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step3MasterFloat32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_input_get, _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_parameter_get, _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step3MasterFloat32ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step3MasterFloat32ParallelPlusCSR_swigregister = _init2_.Distributed_Step3MasterFloat32ParallelPlusCSR_swigregister
Distributed_Step3MasterFloat32ParallelPlusCSR_swigregister(Distributed_Step3MasterFloat32ParallelPlusCSR)

class Distributed_Step4LocalFloat64PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat64PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat64PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat64PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat64PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat64PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat64PlusPlusDense_input_get, _init2_.Distributed_Step4LocalFloat64PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat64PlusPlusDense_parameter_get, _init2_.Distributed_Step4LocalFloat64PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat64PlusPlusDense
    __del__ = lambda self: None
Distributed_Step4LocalFloat64PlusPlusDense_swigregister = _init2_.Distributed_Step4LocalFloat64PlusPlusDense_swigregister
Distributed_Step4LocalFloat64PlusPlusDense_swigregister(Distributed_Step4LocalFloat64PlusPlusDense)

class Distributed_Step4LocalFloat64ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat64ParallelPlusDense_input_get, _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat64ParallelPlusDense_parameter_get, _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat64ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step4LocalFloat64ParallelPlusDense_swigregister = _init2_.Distributed_Step4LocalFloat64ParallelPlusDense_swigregister
Distributed_Step4LocalFloat64ParallelPlusDense_swigregister(Distributed_Step4LocalFloat64ParallelPlusDense)

class Distributed_Step4LocalFloat64PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat64PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat64PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat64PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat64PlusPlusCSR_input_get, _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat64PlusPlusCSR_parameter_get, _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat64PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat64PlusPlusCSR_swigregister = _init2_.Distributed_Step4LocalFloat64PlusPlusCSR_swigregister
Distributed_Step4LocalFloat64PlusPlusCSR_swigregister(Distributed_Step4LocalFloat64PlusPlusCSR)

class Distributed_Step4LocalFloat64ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_input_get, _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_parameter_get, _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat64ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat64ParallelPlusCSR_swigregister = _init2_.Distributed_Step4LocalFloat64ParallelPlusCSR_swigregister
Distributed_Step4LocalFloat64ParallelPlusCSR_swigregister(Distributed_Step4LocalFloat64ParallelPlusCSR)

class Distributed_Step4LocalFloat32PlusPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat32PlusPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat32PlusPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat32PlusPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat32PlusPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat32PlusPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat32PlusPlusDense_input_get, _init2_.Distributed_Step4LocalFloat32PlusPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32PlusPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32PlusPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat32PlusPlusDense_parameter_get, _init2_.Distributed_Step4LocalFloat32PlusPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat32PlusPlusDense
    __del__ = lambda self: None
Distributed_Step4LocalFloat32PlusPlusDense_swigregister = _init2_.Distributed_Step4LocalFloat32PlusPlusDense_swigregister
Distributed_Step4LocalFloat32PlusPlusDense_swigregister(Distributed_Step4LocalFloat32PlusPlusDense)

class Distributed_Step4LocalFloat32ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat32ParallelPlusDense_input_get, _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat32ParallelPlusDense_parameter_get, _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat32ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step4LocalFloat32ParallelPlusDense_swigregister = _init2_.Distributed_Step4LocalFloat32ParallelPlusDense_swigregister
Distributed_Step4LocalFloat32ParallelPlusDense_swigregister(Distributed_Step4LocalFloat32ParallelPlusDense)

class Distributed_Step4LocalFloat32PlusPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat32PlusPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat32PlusPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat32PlusPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat32PlusPlusCSR_input_get, _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat32PlusPlusCSR_parameter_get, _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat32PlusPlusCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat32PlusPlusCSR_swigregister = _init2_.Distributed_Step4LocalFloat32PlusPlusCSR_swigregister
Distributed_Step4LocalFloat32PlusPlusCSR_swigregister(Distributed_Step4LocalFloat32PlusPlusCSR)

class Distributed_Step4LocalFloat32ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step4LocalFloat32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step4LocalFloat32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step4LocalFloat32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_getMethod(self)

    def getPartialResult(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_input_get, _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_parameter_get, _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_compute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step4LocalFloat32ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step4LocalFloat32ParallelPlusCSR_swigregister = _init2_.Distributed_Step4LocalFloat32ParallelPlusCSR_swigregister
Distributed_Step4LocalFloat32ParallelPlusCSR_swigregister(Distributed_Step4LocalFloat32ParallelPlusCSR)

class Distributed_Step5MasterFloat64ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step5MasterFloat64ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step5MasterFloat64ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step5MasterFloat64ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step5MasterFloat64ParallelPlusDense_input_get, _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step5MasterFloat64ParallelPlusDense_parameter_get, _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step5MasterFloat64ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step5MasterFloat64ParallelPlusDense_swigregister = _init2_.Distributed_Step5MasterFloat64ParallelPlusDense_swigregister
Distributed_Step5MasterFloat64ParallelPlusDense_swigregister(Distributed_Step5MasterFloat64ParallelPlusDense)

class Distributed_Step5MasterFloat64ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step5MasterFloat64ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step5MasterFloat64ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step5MasterFloat64ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_input_get, _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_parameter_get, _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step5MasterFloat64ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step5MasterFloat64ParallelPlusCSR_swigregister = _init2_.Distributed_Step5MasterFloat64ParallelPlusCSR_swigregister
Distributed_Step5MasterFloat64ParallelPlusCSR_swigregister(Distributed_Step5MasterFloat64ParallelPlusCSR)

class Distributed_Step5MasterFloat32ParallelPlusDense(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step5MasterFloat32ParallelPlusDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step5MasterFloat32ParallelPlusDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step5MasterFloat32ParallelPlusDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step5MasterFloat32ParallelPlusDense_input_get, _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step5MasterFloat32ParallelPlusDense_parameter_get, _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step5MasterFloat32ParallelPlusDense
    __del__ = lambda self: None
Distributed_Step5MasterFloat32ParallelPlusDense_swigregister = _init2_.Distributed_Step5MasterFloat32ParallelPlusDense_swigregister
Distributed_Step5MasterFloat32ParallelPlusDense_swigregister(Distributed_Step5MasterFloat32ParallelPlusDense)

class Distributed_Step5MasterFloat32ParallelPlusCSR(DistributedBase):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step5MasterFloat32ParallelPlusCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step5MasterFloat32ParallelPlusCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _init2_.new_Distributed_Step5MasterFloat32ParallelPlusCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_getMethod(self)

    def getResult(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_getResult(self)

    def setResult(self, result):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_setResult(self, result)

    def getPartialResult(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_clone(self)
    __swig_setmethods__["input"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_input_set
    __swig_getmethods__["input"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_input_get
    if _newclass:
        input = _swig_property(_init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_input_get, _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_input_set)
    __swig_setmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_parameter_set
    __swig_getmethods__["parameter"] = _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_parameter_get, _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_parameter_set)

    def compute(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_compute(self)

    def finalizeCompute(self):
        return _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_finalizeCompute(self)
    __swig_destroy__ = _init2_.delete_Distributed_Step5MasterFloat32ParallelPlusCSR
    __del__ = lambda self: None
Distributed_Step5MasterFloat32ParallelPlusCSR_swigregister = _init2_.Distributed_Step5MasterFloat32ParallelPlusCSR_swigregister
Distributed_Step5MasterFloat32ParallelPlusCSR_swigregister(Distributed_Step5MasterFloat32ParallelPlusCSR)

from numpy import float64, float32, intc

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == deterministicDense:
                        return Distributed_Step1LocalFloat64DeterministicDense(*args)
                    if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                        return Distributed_Step1LocalFloat64DeterministicCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == randomDense:
                        return Distributed_Step1LocalFloat64RandomDense(*args)
                    if 'method' in kwargs and kwargs['method'] == randomCSR:
                        return Distributed_Step1LocalFloat64RandomCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step1LocalFloat64PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step1LocalFloat64PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step1LocalFloat64ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step1LocalFloat64ParallelPlusCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == deterministicDense:
                        return Distributed_Step1LocalFloat32DeterministicDense(*args)
                    if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                        return Distributed_Step1LocalFloat32DeterministicCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == randomDense:
                        return Distributed_Step1LocalFloat32RandomDense(*args)
                    if 'method' in kwargs and kwargs['method'] == randomCSR:
                        return Distributed_Step1LocalFloat32RandomCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step1LocalFloat32PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step1LocalFloat32PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step1LocalFloat32ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step1LocalFloat32ParallelPlusCSR(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == deterministicDense:
                        return Distributed_Step2MasterFloat64DeterministicDense(*args)
                    if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                        return Distributed_Step2MasterFloat64DeterministicCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == randomDense:
                        return Distributed_Step2MasterFloat64RandomDense(*args)
                    if 'method' in kwargs and kwargs['method'] == randomCSR:
                        return Distributed_Step2MasterFloat64RandomCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == deterministicDense:
                        return Distributed_Step2MasterFloat32DeterministicDense(*args)
                    if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                        return Distributed_Step2MasterFloat32DeterministicCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == randomDense:
                        return Distributed_Step2MasterFloat32RandomDense(*args)
                    if 'method' in kwargs and kwargs['method'] == randomCSR:
                        return Distributed_Step2MasterFloat32RandomCSR(*args)
        if step == daal.step2Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step2LocalFloat64PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step2LocalFloat64ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step2LocalFloat64PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step2LocalFloat64ParallelPlusCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step2LocalFloat32PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step2LocalFloat32ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step2LocalFloat32PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step2LocalFloat32ParallelPlusCSR(*args)
        if step == daal.step3Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step3MasterFloat64PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step3MasterFloat64ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step3MasterFloat64PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step3MasterFloat64ParallelPlusCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step3MasterFloat32PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step3MasterFloat32ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step3MasterFloat32PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step3MasterFloat32ParallelPlusCSR(*args)
        if step == daal.step4Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step4LocalFloat64PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step4LocalFloat64ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step4LocalFloat64PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step4LocalFloat64ParallelPlusCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                        return Distributed_Step4LocalFloat32PlusPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step4LocalFloat32ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                        return Distributed_Step4LocalFloat32PlusPlusCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step4LocalFloat32ParallelPlusCSR(*args)
        if step == daal.step5Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step5MasterFloat64ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step5MasterFloat64ParallelPlusCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                        return Distributed_Step5MasterFloat32ParallelPlusDense(*args)
                    if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                        return Distributed_Step5MasterFloat32ParallelPlusCSR(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == deterministicDense:
                return Batch_Float64DeterministicDense(*args)
            if 'method' in kwargs and kwargs['method'] == randomDense:
                return Batch_Float64RandomDense(*args)
            if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                return Batch_Float64PlusPlusDense(*args)
            if 'method' in kwargs and kwargs['method'] == randomCSR:
                return Batch_Float64RandomCSR(*args)
            if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                return Batch_Float64ParallelPlusDense(*args)
            if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                return Batch_Float64ParallelPlusCSR(*args)
            if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                return Batch_Float64DeterministicCSR(*args)
            if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                return Batch_Float64PlusPlusCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == deterministicDense:
                return Batch_Float32DeterministicDense(*args)
            if 'method' in kwargs and kwargs['method'] == randomDense:
                return Batch_Float32RandomDense(*args)
            if 'method' in kwargs and kwargs['method'] == plusPlusDense:
                return Batch_Float32PlusPlusDense(*args)
            if 'method' in kwargs and kwargs['method'] == randomCSR:
                return Batch_Float32RandomCSR(*args)
            if 'method' in kwargs and kwargs['method'] == parallelPlusDense:
                return Batch_Float32ParallelPlusDense(*args)
            if 'method' in kwargs and kwargs['method'] == parallelPlusCSR:
                return Batch_Float32ParallelPlusCSR(*args)
            if 'method' in kwargs and kwargs['method'] == deterministicCSR:
                return Batch_Float32DeterministicCSR(*args)
            if 'method' in kwargs and kwargs['method'] == plusPlusCSR:
                return Batch_Float32PlusPlusCSR(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


