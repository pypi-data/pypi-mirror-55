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
            fp, pathname, description = imp.find_module('_kmeans_', [dirname(__file__)])
        except ImportError:
            import _kmeans_
            return _kmeans_
        if fp is not None:
            try:
                _mod = imp.load_module('_kmeans_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _kmeans_ = swig_import_helper()
    del swig_import_helper
else:
    import _kmeans_
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

_kmeans_.lloydDense_swigconstant(_kmeans_)
lloydDense = _kmeans_.lloydDense

_kmeans_.defaultDense_swigconstant(_kmeans_)
defaultDense = _kmeans_.defaultDense

_kmeans_.lloydCSR_swigconstant(_kmeans_)
lloydCSR = _kmeans_.lloydCSR

_kmeans_.euclidean_swigconstant(_kmeans_)
euclidean = _kmeans_.euclidean

_kmeans_.lastDistanceType_swigconstant(_kmeans_)
lastDistanceType = _kmeans_.lastDistanceType

_kmeans_.data_swigconstant(_kmeans_)
data = _kmeans_.data

_kmeans_.inputCentroids_swigconstant(_kmeans_)
inputCentroids = _kmeans_.inputCentroids

_kmeans_.lastInputId_swigconstant(_kmeans_)
lastInputId = _kmeans_.lastInputId

_kmeans_.partialResults_swigconstant(_kmeans_)
partialResults = _kmeans_.partialResults

_kmeans_.lastMasterInputId_swigconstant(_kmeans_)
lastMasterInputId = _kmeans_.lastMasterInputId

_kmeans_.nObservations_swigconstant(_kmeans_)
nObservations = _kmeans_.nObservations

_kmeans_.partialSums_swigconstant(_kmeans_)
partialSums = _kmeans_.partialSums

_kmeans_.partialObjectiveFunction_swigconstant(_kmeans_)
partialObjectiveFunction = _kmeans_.partialObjectiveFunction

_kmeans_.partialGoalFunction_swigconstant(_kmeans_)
partialGoalFunction = _kmeans_.partialGoalFunction

_kmeans_.partialAssignments_swigconstant(_kmeans_)
partialAssignments = _kmeans_.partialAssignments

_kmeans_.partialCandidatesDistances_swigconstant(_kmeans_)
partialCandidatesDistances = _kmeans_.partialCandidatesDistances

_kmeans_.partialCandidatesCentroids_swigconstant(_kmeans_)
partialCandidatesCentroids = _kmeans_.partialCandidatesCentroids

_kmeans_.lastPartialResultId_swigconstant(_kmeans_)
lastPartialResultId = _kmeans_.lastPartialResultId

_kmeans_.centroids_swigconstant(_kmeans_)
centroids = _kmeans_.centroids

_kmeans_.assignments_swigconstant(_kmeans_)
assignments = _kmeans_.assignments

_kmeans_.objectiveFunction_swigconstant(_kmeans_)
objectiveFunction = _kmeans_.objectiveFunction

_kmeans_.goalFunction_swigconstant(_kmeans_)
goalFunction = _kmeans_.goalFunction

_kmeans_.nIterations_swigconstant(_kmeans_)
nIterations = _kmeans_.nIterations

_kmeans_.lastResultId_swigconstant(_kmeans_)
lastResultId = _kmeans_.lastResultId
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
        this = _kmeans_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nClusters"] = _kmeans_.Parameter_nClusters_set
    __swig_getmethods__["nClusters"] = _kmeans_.Parameter_nClusters_get
    if _newclass:
        nClusters = _swig_property(_kmeans_.Parameter_nClusters_get, _kmeans_.Parameter_nClusters_set)
    __swig_setmethods__["maxIterations"] = _kmeans_.Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _kmeans_.Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_kmeans_.Parameter_maxIterations_get, _kmeans_.Parameter_maxIterations_set)
    __swig_setmethods__["accuracyThreshold"] = _kmeans_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _kmeans_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_kmeans_.Parameter_accuracyThreshold_get, _kmeans_.Parameter_accuracyThreshold_set)
    __swig_setmethods__["gamma"] = _kmeans_.Parameter_gamma_set
    __swig_getmethods__["gamma"] = _kmeans_.Parameter_gamma_get
    if _newclass:
        gamma = _swig_property(_kmeans_.Parameter_gamma_get, _kmeans_.Parameter_gamma_set)
    __swig_setmethods__["distanceType"] = _kmeans_.Parameter_distanceType_set
    __swig_getmethods__["distanceType"] = _kmeans_.Parameter_distanceType_get
    if _newclass:
        distanceType = _swig_property(_kmeans_.Parameter_distanceType_get, _kmeans_.Parameter_distanceType_set)
    __swig_setmethods__["assignFlag"] = _kmeans_.Parameter_assignFlag_set
    __swig_getmethods__["assignFlag"] = _kmeans_.Parameter_assignFlag_get
    if _newclass:
        assignFlag = _swig_property(_kmeans_.Parameter_assignFlag_get, _kmeans_.Parameter_assignFlag_set)

    def check(self):
        return _kmeans_.Parameter_check(self)
    __swig_destroy__ = _kmeans_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _kmeans_.Parameter_swigregister
Parameter_swigregister(Parameter)

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
        return _kmeans_.InputIface_getNumberOfFeatures(self)
    __swig_destroy__ = _kmeans_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _kmeans_.InputIface_swigregister
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
        this = _kmeans_.new_Input()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kmeans_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _kmeans_.Input_get(self, id)

    def set(self, id, ptr):
        return _kmeans_.Input_set(self, id, ptr)

    def getNumberOfFeatures(self):
        return _kmeans_.Input_getNumberOfFeatures(self)

    def check(self, par, method):
        return _kmeans_.Input_check(self, par, method)
Input_swigregister = _kmeans_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _kmeans_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_kmeans_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _kmeans_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _kmeans_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kmeans_.delete_PartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _kmeans_.PartialResult_get(self, id)

    def set(self, id, ptr):
        return _kmeans_.PartialResult_set(self, id, ptr)

    def getNumberOfFeatures(self):
        return _kmeans_.PartialResult_getNumberOfFeatures(self)

    def check(self, *args):
        return _kmeans_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _kmeans_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _kmeans_.PartialResult_allocate_Float32(self, input, parameter, method)

PartialResult_swigregister = _kmeans_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _kmeans_.PartialResult_serializationTag()
PartialResult_serializationTag = _kmeans_.PartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _kmeans_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_kmeans_.Result_serializationTag)

    def getSerializationTag(self):
        return _kmeans_.Result_getSerializationTag(self)

    def __init__(self):
        this = _kmeans_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kmeans_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _kmeans_.Result_get(self, id)

    def set(self, id, ptr):
        return _kmeans_.Result_set(self, id, ptr)

    def check(self, *args):
        return _kmeans_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _kmeans_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _kmeans_.Result_allocate_Float32(self, *args)

Result_swigregister = _kmeans_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _kmeans_.Result_serializationTag()
Result_serializationTag = _kmeans_.Result_serializationTag

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
        this = _kmeans_.new_DistributedStep2MasterInput()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kmeans_.delete_DistributedStep2MasterInput
    __del__ = lambda self: None

    def get(self, id):
        return _kmeans_.DistributedStep2MasterInput_get(self, id)

    def set(self, id, ptr):
        return _kmeans_.DistributedStep2MasterInput_set(self, id, ptr)

    def add(self, id, value):
        return _kmeans_.DistributedStep2MasterInput_add(self, id, value)

    def getNumberOfFeatures(self):
        return _kmeans_.DistributedStep2MasterInput_getNumberOfFeatures(self)

    def check(self, par, method):
        return _kmeans_.DistributedStep2MasterInput_check(self, par, method)
DistributedStep2MasterInput_swigregister = _kmeans_.DistributedStep2MasterInput_swigregister
DistributedStep2MasterInput_swigregister(DistributedStep2MasterInput)

class Batch_Float64LloydCSR(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Batch_Float64LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Batch_Float64LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Batch_Float64LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Batch_Float64LloydCSR_setResult(self, result)

    def clone(self):
        return _kmeans_.Batch_Float64LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Batch_Float64LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Batch_Float64LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Batch_Float64LloydCSR_input_get, _kmeans_.Batch_Float64LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Batch_Float64LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Batch_Float64LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Batch_Float64LloydCSR_parameter_get, _kmeans_.Batch_Float64LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Batch_Float64LloydCSR_compute(self)
    __swig_destroy__ = _kmeans_.delete_Batch_Float64LloydCSR
    __del__ = lambda self: None
Batch_Float64LloydCSR_swigregister = _kmeans_.Batch_Float64LloydCSR_swigregister
Batch_Float64LloydCSR_swigregister(Batch_Float64LloydCSR)

class Batch_Float64LloydDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Batch_Float64LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Batch_Float64LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Batch_Float64LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Batch_Float64LloydDense_setResult(self, result)

    def clone(self):
        return _kmeans_.Batch_Float64LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Batch_Float64LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Batch_Float64LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Batch_Float64LloydDense_input_get, _kmeans_.Batch_Float64LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Batch_Float64LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Batch_Float64LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Batch_Float64LloydDense_parameter_get, _kmeans_.Batch_Float64LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Batch_Float64LloydDense_compute(self)
    __swig_destroy__ = _kmeans_.delete_Batch_Float64LloydDense
    __del__ = lambda self: None
Batch_Float64LloydDense_swigregister = _kmeans_.Batch_Float64LloydDense_swigregister
Batch_Float64LloydDense_swigregister(Batch_Float64LloydDense)

class Batch_Float32LloydCSR(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Batch_Float32LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Batch_Float32LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Batch_Float32LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Batch_Float32LloydCSR_setResult(self, result)

    def clone(self):
        return _kmeans_.Batch_Float32LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Batch_Float32LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Batch_Float32LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Batch_Float32LloydCSR_input_get, _kmeans_.Batch_Float32LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Batch_Float32LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Batch_Float32LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Batch_Float32LloydCSR_parameter_get, _kmeans_.Batch_Float32LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Batch_Float32LloydCSR_compute(self)
    __swig_destroy__ = _kmeans_.delete_Batch_Float32LloydCSR
    __del__ = lambda self: None
Batch_Float32LloydCSR_swigregister = _kmeans_.Batch_Float32LloydCSR_swigregister
Batch_Float32LloydCSR_swigregister(Batch_Float32LloydCSR)

class Batch_Float32LloydDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Batch_Float32LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Batch_Float32LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Batch_Float32LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Batch_Float32LloydDense_setResult(self, result)

    def clone(self):
        return _kmeans_.Batch_Float32LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Batch_Float32LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Batch_Float32LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Batch_Float32LloydDense_input_get, _kmeans_.Batch_Float32LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Batch_Float32LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Batch_Float32LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Batch_Float32LloydDense_parameter_get, _kmeans_.Batch_Float32LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Batch_Float32LloydDense_compute(self)
    __swig_destroy__ = _kmeans_.delete_Batch_Float32LloydDense
    __del__ = lambda self: None
Batch_Float32LloydDense_swigregister = _kmeans_.Batch_Float32LloydDense_swigregister
Batch_Float32LloydDense_swigregister(Batch_Float32LloydDense)

class Distributed_Step1LocalFloat64LloydCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step1LocalFloat64LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat64LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat64LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step1LocalFloat64LloydCSR_input_get, _kmeans_.Distributed_Step1LocalFloat64LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat64LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat64LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step1LocalFloat64LloydCSR_parameter_get, _kmeans_.Distributed_Step1LocalFloat64LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydCSR_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step1LocalFloat64LloydCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64LloydCSR_swigregister = _kmeans_.Distributed_Step1LocalFloat64LloydCSR_swigregister
Distributed_Step1LocalFloat64LloydCSR_swigregister(Distributed_Step1LocalFloat64LloydCSR)

class Distributed_Step1LocalFloat64LloydDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step1LocalFloat64LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat64LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat64LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step1LocalFloat64LloydDense_input_get, _kmeans_.Distributed_Step1LocalFloat64LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat64LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat64LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step1LocalFloat64LloydDense_parameter_get, _kmeans_.Distributed_Step1LocalFloat64LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step1LocalFloat64LloydDense_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step1LocalFloat64LloydDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64LloydDense_swigregister = _kmeans_.Distributed_Step1LocalFloat64LloydDense_swigregister
Distributed_Step1LocalFloat64LloydDense_swigregister(Distributed_Step1LocalFloat64LloydDense)

class Distributed_Step1LocalFloat32LloydCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step1LocalFloat32LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat32LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat32LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step1LocalFloat32LloydCSR_input_get, _kmeans_.Distributed_Step1LocalFloat32LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat32LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat32LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step1LocalFloat32LloydCSR_parameter_get, _kmeans_.Distributed_Step1LocalFloat32LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydCSR_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step1LocalFloat32LloydCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32LloydCSR_swigregister = _kmeans_.Distributed_Step1LocalFloat32LloydCSR_swigregister
Distributed_Step1LocalFloat32LloydCSR_swigregister(Distributed_Step1LocalFloat32LloydCSR)

class Distributed_Step1LocalFloat32LloydDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step1LocalFloat32LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat32LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step1LocalFloat32LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step1LocalFloat32LloydDense_input_get, _kmeans_.Distributed_Step1LocalFloat32LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat32LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step1LocalFloat32LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step1LocalFloat32LloydDense_parameter_get, _kmeans_.Distributed_Step1LocalFloat32LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step1LocalFloat32LloydDense_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step1LocalFloat32LloydDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32LloydDense_swigregister = _kmeans_.Distributed_Step1LocalFloat32LloydDense_swigregister
Distributed_Step1LocalFloat32LloydDense_swigregister(Distributed_Step1LocalFloat32LloydDense)

class Distributed_Step2MasterFloat64LloydCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step2MasterFloat64LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat64LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat64LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step2MasterFloat64LloydCSR_input_get, _kmeans_.Distributed_Step2MasterFloat64LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat64LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat64LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step2MasterFloat64LloydCSR_parameter_get, _kmeans_.Distributed_Step2MasterFloat64LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydCSR_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step2MasterFloat64LloydCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64LloydCSR_swigregister = _kmeans_.Distributed_Step2MasterFloat64LloydCSR_swigregister
Distributed_Step2MasterFloat64LloydCSR_swigregister(Distributed_Step2MasterFloat64LloydCSR)

class Distributed_Step2MasterFloat64LloydDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step2MasterFloat64LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat64LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat64LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step2MasterFloat64LloydDense_input_get, _kmeans_.Distributed_Step2MasterFloat64LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat64LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat64LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step2MasterFloat64LloydDense_parameter_get, _kmeans_.Distributed_Step2MasterFloat64LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step2MasterFloat64LloydDense_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step2MasterFloat64LloydDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64LloydDense_swigregister = _kmeans_.Distributed_Step2MasterFloat64LloydDense_swigregister
Distributed_Step2MasterFloat64LloydDense_swigregister(Distributed_Step2MasterFloat64LloydDense)

class Distributed_Step2MasterFloat32LloydCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32LloydCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32LloydCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step2MasterFloat32LloydCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat32LloydCSR_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat32LloydCSR_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step2MasterFloat32LloydCSR_input_get, _kmeans_.Distributed_Step2MasterFloat32LloydCSR_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat32LloydCSR_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat32LloydCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step2MasterFloat32LloydCSR_parameter_get, _kmeans_.Distributed_Step2MasterFloat32LloydCSR_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydCSR_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step2MasterFloat32LloydCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32LloydCSR_swigregister = _kmeans_.Distributed_Step2MasterFloat32LloydCSR_swigregister
Distributed_Step2MasterFloat32LloydCSR_swigregister(Distributed_Step2MasterFloat32LloydCSR)

class Distributed_Step2MasterFloat32LloydDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32LloydDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32LloydDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kmeans_.new_Distributed_Step2MasterFloat32LloydDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_getMethod(self)

    def getResult(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_getResult(self)

    def setResult(self, result):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_setResult(self, result)

    def getPartialResult(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_getPartialResult(self)

    def setPartialResult(self, partialRes):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_setPartialResult(self, partialRes)

    def checkFinalizeComputeParams(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_clone(self)
    __swig_setmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat32LloydDense_input_set
    __swig_getmethods__["input"] = _kmeans_.Distributed_Step2MasterFloat32LloydDense_input_get
    if _newclass:
        input = _swig_property(_kmeans_.Distributed_Step2MasterFloat32LloydDense_input_get, _kmeans_.Distributed_Step2MasterFloat32LloydDense_input_set)
    __swig_setmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat32LloydDense_parameter_set
    __swig_getmethods__["parameter"] = _kmeans_.Distributed_Step2MasterFloat32LloydDense_parameter_get
    if _newclass:
        parameter = _swig_property(_kmeans_.Distributed_Step2MasterFloat32LloydDense_parameter_get, _kmeans_.Distributed_Step2MasterFloat32LloydDense_parameter_set)

    def compute(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_compute(self)

    def finalizeCompute(self):
        return _kmeans_.Distributed_Step2MasterFloat32LloydDense_finalizeCompute(self)
    __swig_destroy__ = _kmeans_.delete_Distributed_Step2MasterFloat32LloydDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32LloydDense_swigregister = _kmeans_.Distributed_Step2MasterFloat32LloydDense_swigregister
Distributed_Step2MasterFloat32LloydDense_swigregister(Distributed_Step2MasterFloat32LloydDense)

from numpy import float64, float32, intc

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == lloydCSR:
                        return Distributed_Step1LocalFloat64LloydCSR(*args)
                    if 'method' not in kwargs or kwargs['method'] == lloydDense:
                        return Distributed_Step1LocalFloat64LloydDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == lloydCSR:
                        return Distributed_Step1LocalFloat32LloydCSR(*args)
                    if 'method' not in kwargs or kwargs['method'] == lloydDense:
                        return Distributed_Step1LocalFloat32LloydDense(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == lloydCSR:
                        return Distributed_Step2MasterFloat64LloydCSR(*args)
                    if 'method' not in kwargs or kwargs['method'] == lloydDense:
                        return Distributed_Step2MasterFloat64LloydDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == lloydCSR:
                        return Distributed_Step2MasterFloat32LloydCSR(*args)
                    if 'method' not in kwargs or kwargs['method'] == lloydDense:
                        return Distributed_Step2MasterFloat32LloydDense(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' in kwargs and kwargs['method'] == lloydCSR:
                return Batch_Float64LloydCSR(*args)
            if 'method' not in kwargs or kwargs['method'] == lloydDense:
                return Batch_Float64LloydDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' in kwargs and kwargs['method'] == lloydCSR:
                return Batch_Float32LloydCSR(*args)
            if 'method' not in kwargs or kwargs['method'] == lloydDense:
                return Batch_Float32LloydDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


