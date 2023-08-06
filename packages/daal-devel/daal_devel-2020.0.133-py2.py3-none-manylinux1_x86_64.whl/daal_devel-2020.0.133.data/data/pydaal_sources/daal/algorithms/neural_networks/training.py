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
            fp, pathname, description = imp.find_module('_training20_', [dirname(__file__)])
        except ImportError:
            import _training20_
            return _training20_
        if fp is not None:
            try:
                _mod = imp.load_module('_training20_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training20_ = swig_import_helper()
    del swig_import_helper
else:
    import _training20_
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


import daal.algorithms.neural_networks
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.initializers
import daal.algorithms.engines.mt19937
import daal.algorithms.engines
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.optimization_solver.iterative_solver
import daal.algorithms.optimization_solver
import daal.algorithms.neural_networks.prediction
import daal.algorithms.optimization_solver.sgd
import daal.algorithms.optimization_solver.sum_of_functions
import daal.algorithms.optimization_solver.objective_function

_training20_.defaultDense_swigconstant(_training20_)
defaultDense = _training20_.defaultDense

_training20_.feedforwardDense_swigconstant(_training20_)
feedforwardDense = _training20_.feedforwardDense

_training20_.model_swigconstant(_training20_)
model = _training20_.model

_training20_.lastResultId_swigconstant(_training20_)
lastResultId = _training20_.lastResultId
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
    __swig_getmethods__["serializationTag"] = lambda x: _training20_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training20_.Result_serializationTag)

    def getSerializationTag(self):
        return _training20_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training20_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training20_.Result_get(self, id)

    def set(self, id, value):
        return _training20_.Result_set(self, id, value)

    def check(self, input, par, method):
        return _training20_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training20_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training20_.Result_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _training20_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _training20_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training20_.Result_serializationTag()
Result_serializationTag = _training20_.Result_serializationTag


_training20_.data_swigconstant(_training20_)
data = _training20_.data

_training20_.groundTruth_swigconstant(_training20_)
groundTruth = _training20_.groundTruth

_training20_.lastInputId_swigconstant(_training20_)
lastInputId = _training20_.lastInputId

_training20_.groundTruthCollection_swigconstant(_training20_)
groundTruthCollection = _training20_.groundTruthCollection

_training20_.lastInputCollectionId_swigconstant(_training20_)
lastInputCollectionId = _training20_.lastInputCollectionId

_training20_.inputModel_swigconstant(_training20_)
inputModel = _training20_.inputModel

_training20_.lastStep1LocalInputId_swigconstant(_training20_)
lastStep1LocalInputId = _training20_.lastStep1LocalInputId

_training20_.partialResults_swigconstant(_training20_)
partialResults = _training20_.partialResults

_training20_.lastStep2MasterInputId_swigconstant(_training20_)
lastStep2MasterInputId = _training20_.lastStep2MasterInputId
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
        this = _training20_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Input
    __del__ = lambda self: None

    def getInput(self, id):
        return _training20_.Input_getInput(self, id)

    def getInputCollection(self, *args):
        return _training20_.Input_getInputCollection(self, *args)

    def setInput(self, id, value):
        return _training20_.Input_setInput(self, id, value)

    def setInputCollection(self, id, value):
        return _training20_.Input_setInputCollection(self, id, value)

    def add(self, id, key, value):
        return _training20_.Input_add(self, id, key, value)

    def check(self, par, method):
        return _training20_.Input_check(self, par, method)
Input_swigregister = _training20_.Input_swigregister
Input_swigregister(Input)

class Topology(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Topology, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Topology, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training20_.new_Topology(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def size(self):
        return _training20_.Topology_size(self)

    def push_back(self, layer):
        return _training20_.Topology_push_back(self, layer)

    def add(self, *args):
        return _training20_.Topology_add(self, *args)

    def clear(self):
        return _training20_.Topology_clear(self)

    def get(self, *args):
        return _training20_.Topology_get(self, *args)

    def addNext(self, index, next):
        return _training20_.Topology_addNext(self, index, next)

    def __getitem__(self, i):
        return _training20_.Topology___getitem__(self, i)

    def __setitem__(self, i, v):
        return _training20_.Topology___setitem__(self, i, v)
    __swig_destroy__ = _training20_.delete_Topology
    __del__ = lambda self: None
Topology_swigregister = _training20_.Topology_swigregister
Topology_swigregister(Topology)

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
        this = _training20_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["optimizationSolver"] = _training20_.Parameter_optimizationSolver_set
    __swig_getmethods__["optimizationSolver"] = _training20_.Parameter_optimizationSolver_get
    if _newclass:
        optimizationSolver = _swig_property(_training20_.Parameter_optimizationSolver_get, _training20_.Parameter_optimizationSolver_set)
    __swig_setmethods__["engine"] = _training20_.Parameter_engine_set
    __swig_getmethods__["engine"] = _training20_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_training20_.Parameter_engine_get, _training20_.Parameter_engine_set)
    __swig_destroy__ = _training20_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _training20_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Model(daal.algorithms.neural_networks.ModelImpl):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.ModelImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.ModelImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training20_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training20_.Model_serializationTag)

    def getSerializationTag(self):
        return _training20_.Model_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _training20_.Model_create
    if _newclass:
        create = staticmethod(_training20_.Model_create)

    def __init__(self, *args):
        this = _training20_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Model
    __del__ = lambda self: None

    def getForwardLayers(self):
        return _training20_.Model_getForwardLayers(self)

    def getForwardLayer(self, index):
        return _training20_.Model_getForwardLayer(self, index)

    def getBackwardLayers(self):
        return _training20_.Model_getBackwardLayers(self)

    def getBackwardLayer(self, index):
        return _training20_.Model_getBackwardLayer(self, index)

    def getWeightsAndBiasesStorageStatus(self):
        return _training20_.Model_getWeightsAndBiasesStorageStatus(self)

    def setWeightsAndBiases(self, *args):
        return _training20_.Model_setWeightsAndBiases(self, *args)

    def getWeightsAndBiases(self, *args):
        return _training20_.Model_getWeightsAndBiases(self, *args)

    def getWeightsAndBiasesDerivatives(self, *args):
        return _training20_.Model_getWeightsAndBiasesDerivatives(self, *args)

    def setErrors(self, errors):
        return _training20_.Model_setErrors(self, errors)

    def getSolverOptionalArgument(self, index):
        return _training20_.Model_getSolverOptionalArgument(self, index)

    def setSolverOptionalArgument(self, solverOptionalArgument, index):
        return _training20_.Model_setSolverOptionalArgument(self, solverOptionalArgument, index)

    def getSolverOptionalArgumentCollection(self):
        return _training20_.Model_getSolverOptionalArgumentCollection(self)

    def setSolverOptionalArgumentCollection(self, solverOptionalArgumentCollection):
        return _training20_.Model_setSolverOptionalArgumentCollection(self, solverOptionalArgumentCollection)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _training20_.Model_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _training20_.Model_allocate_Float32(self, *args)


    def getPredictionModel_Float64(self):
        r"""
    This function is specialized for float64"""
        return _training20_.Model_getPredictionModel_Float64(self)


    def getPredictionModel_Float32(self):
        r"""
    This function is specialized for float32"""
        return _training20_.Model_getPredictionModel_Float32(self)


    def initialize_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _training20_.Model_initialize_Float64(self, *args)


    def initialize_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _training20_.Model_initialize_Float32(self, *args)

Model_swigregister = _training20_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _training20_.Model_serializationTag()
Model_serializationTag = _training20_.Model_serializationTag

def Model_create(stat=None):
    return _training20_.Model_create(stat)
Model_create = _training20_.Model_create


_training20_.derivatives_swigconstant(_training20_)
derivatives = _training20_.derivatives

_training20_.batchSize_swigconstant(_training20_)
batchSize = _training20_.batchSize

_training20_.lastStep1LocalPartialResultId_swigconstant(_training20_)
lastStep1LocalPartialResultId = _training20_.lastStep1LocalPartialResultId

_training20_.resultFromMaster_swigconstant(_training20_)
resultFromMaster = _training20_.resultFromMaster

_training20_.lastStep2MasterPartialResultId_swigconstant(_training20_)
lastStep2MasterPartialResultId = _training20_.lastStep2MasterPartialResultId
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
    __swig_getmethods__["serializationTag"] = lambda x: _training20_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training20_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _training20_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _training20_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_PartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _training20_.PartialResult_get(self, id)

    def set(self, id, value):
        return _training20_.PartialResult_set(self, id, value)

    def check(self, input, par, method):
        return _training20_.PartialResult_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training20_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training20_.PartialResult_allocate_Float32(self, input, parameter, method)

PartialResult_swigregister = _training20_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _training20_.PartialResult_serializationTag()
PartialResult_serializationTag = _training20_.PartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _training20_.DistributedPartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training20_.DistributedPartialResult_serializationTag)

    def getSerializationTag(self):
        return _training20_.DistributedPartialResult_getSerializationTag(self)

    def __init__(self):
        this = _training20_.new_DistributedPartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _training20_.DistributedPartialResult_get(self, id)

    def set(self, id, value):
        return _training20_.DistributedPartialResult_set(self, id, value)

    def check(self, input, par, method):
        return _training20_.DistributedPartialResult_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training20_.DistributedPartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training20_.DistributedPartialResult_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _training20_.delete_DistributedPartialResult
    __del__ = lambda self: None
DistributedPartialResult_swigregister = _training20_.DistributedPartialResult_swigregister
DistributedPartialResult_swigregister(DistributedPartialResult)

def DistributedPartialResult_serializationTag():
    return _training20_.DistributedPartialResult_serializationTag()
DistributedPartialResult_serializationTag = _training20_.DistributedPartialResult_serializationTag

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
        this = _training20_.new_DistributedInput_Step1Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None

    def getStep1LocalInput(self, id):
        return _training20_.DistributedInput_Step1Local_getStep1LocalInput(self, id)

    def setStep1LocalInput(self, id, value):
        return _training20_.DistributedInput_Step1Local_setStep1LocalInput(self, id, value)

    def check(self, par, method):
        return _training20_.DistributedInput_Step1Local_check(self, par, method)
DistributedInput_Step1Local_swigregister = _training20_.DistributedInput_Step1Local_swigregister
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
        this = _training20_.new_DistributedInput_Step2Master(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_DistributedInput_Step2Master
    __del__ = lambda self: None

    def getStep2MasterInput(self, id):
        return _training20_.DistributedInput_Step2Master_getStep2MasterInput(self, id)

    def setStep2MasterInput(self, id, value):
        return _training20_.DistributedInput_Step2Master_setStep2MasterInput(self, id, value)

    def add(self, id, key, value):
        return _training20_.DistributedInput_Step2Master_add(self, id, key, value)

    def check(self, par, method):
        return _training20_.DistributedInput_Step2Master_check(self, par, method)
DistributedInput_Step2Master_swigregister = _training20_.DistributedInput_Step2Master_swigregister
DistributedInput_Step2Master_swigregister(DistributedInput_Step2Master)

class Batch_Float64FeedforwardDense(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FeedforwardDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training20_.new_Batch_Float64FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Batch_Float64FeedforwardDense
    __del__ = lambda self: None

    def initialize(self, sampleSize, topology):
        return _training20_.Batch_Float64FeedforwardDense_initialize(self, sampleSize, topology)

    def getResult(self):
        return _training20_.Batch_Float64FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _training20_.Batch_Float64FeedforwardDense_setResult(self, res)

    def clone(self):
        return _training20_.Batch_Float64FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Batch_Float64FeedforwardDense_getMethod(self)
    __swig_setmethods__["input"] = _training20_.Batch_Float64FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Batch_Float64FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Batch_Float64FeedforwardDense_input_get, _training20_.Batch_Float64FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Batch_Float64FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Batch_Float64FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Batch_Float64FeedforwardDense_parameter_get, _training20_.Batch_Float64FeedforwardDense_parameter_set)

    def compute(self):
        return _training20_.Batch_Float64FeedforwardDense_compute(self)
Batch_Float64FeedforwardDense_swigregister = _training20_.Batch_Float64FeedforwardDense_swigregister
Batch_Float64FeedforwardDense_swigregister(Batch_Float64FeedforwardDense)

class Batch_Float32FeedforwardDense(daal.algorithms.Training_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FeedforwardDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training20_.new_Batch_Float32FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Batch_Float32FeedforwardDense
    __del__ = lambda self: None

    def initialize(self, sampleSize, topology):
        return _training20_.Batch_Float32FeedforwardDense_initialize(self, sampleSize, topology)

    def getResult(self):
        return _training20_.Batch_Float32FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _training20_.Batch_Float32FeedforwardDense_setResult(self, res)

    def clone(self):
        return _training20_.Batch_Float32FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Batch_Float32FeedforwardDense_getMethod(self)
    __swig_setmethods__["input"] = _training20_.Batch_Float32FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Batch_Float32FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Batch_Float32FeedforwardDense_input_get, _training20_.Batch_Float32FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Batch_Float32FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Batch_Float32FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Batch_Float32FeedforwardDense_parameter_get, _training20_.Batch_Float32FeedforwardDense_parameter_set)

    def compute(self):
        return _training20_.Batch_Float32FeedforwardDense_compute(self)
Batch_Float32FeedforwardDense_swigregister = _training20_.Batch_Float32FeedforwardDense_swigregister
Batch_Float32FeedforwardDense_swigregister(Batch_Float32FeedforwardDense)

class Distributed_Step1LocalFloat64FeedforwardDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64FeedforwardDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training20_.Distributed_Step1LocalFloat64FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Distributed_Step1LocalFloat64FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Distributed_Step1LocalFloat64FeedforwardDense_input_get, _training20_.Distributed_Step1LocalFloat64FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Distributed_Step1LocalFloat64FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Distributed_Step1LocalFloat64FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Distributed_Step1LocalFloat64FeedforwardDense_parameter_get, _training20_.Distributed_Step1LocalFloat64FeedforwardDense_parameter_set)

    def __init__(self, *args):
        this = _training20_.new_Distributed_Step1LocalFloat64FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Distributed_Step1LocalFloat64FeedforwardDense
    __del__ = lambda self: None

    def setPartialResult(self, partialResult):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_getPartialResult(self)

    def getResult(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_setResult(self, res)

    def clone(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_getMethod(self)

    def compute(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_compute(self)

    def finalizeCompute(self):
        return _training20_.Distributed_Step1LocalFloat64FeedforwardDense_finalizeCompute(self)
Distributed_Step1LocalFloat64FeedforwardDense_swigregister = _training20_.Distributed_Step1LocalFloat64FeedforwardDense_swigregister
Distributed_Step1LocalFloat64FeedforwardDense_swigregister(Distributed_Step1LocalFloat64FeedforwardDense)

class Distributed_Step1LocalFloat32FeedforwardDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32FeedforwardDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training20_.Distributed_Step1LocalFloat32FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Distributed_Step1LocalFloat32FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Distributed_Step1LocalFloat32FeedforwardDense_input_get, _training20_.Distributed_Step1LocalFloat32FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Distributed_Step1LocalFloat32FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Distributed_Step1LocalFloat32FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Distributed_Step1LocalFloat32FeedforwardDense_parameter_get, _training20_.Distributed_Step1LocalFloat32FeedforwardDense_parameter_set)

    def __init__(self, *args):
        this = _training20_.new_Distributed_Step1LocalFloat32FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Distributed_Step1LocalFloat32FeedforwardDense
    __del__ = lambda self: None

    def setPartialResult(self, partialResult):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_getPartialResult(self)

    def getResult(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_setResult(self, res)

    def clone(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_getMethod(self)

    def compute(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_compute(self)

    def finalizeCompute(self):
        return _training20_.Distributed_Step1LocalFloat32FeedforwardDense_finalizeCompute(self)
Distributed_Step1LocalFloat32FeedforwardDense_swigregister = _training20_.Distributed_Step1LocalFloat32FeedforwardDense_swigregister
Distributed_Step1LocalFloat32FeedforwardDense_swigregister(Distributed_Step1LocalFloat32FeedforwardDense)

class Distributed_Step2MasterFloat64FeedforwardDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64FeedforwardDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training20_.Distributed_Step2MasterFloat64FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Distributed_Step2MasterFloat64FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Distributed_Step2MasterFloat64FeedforwardDense_input_get, _training20_.Distributed_Step2MasterFloat64FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Distributed_Step2MasterFloat64FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Distributed_Step2MasterFloat64FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Distributed_Step2MasterFloat64FeedforwardDense_parameter_get, _training20_.Distributed_Step2MasterFloat64FeedforwardDense_parameter_set)

    def __init__(self, *args):
        this = _training20_.new_Distributed_Step2MasterFloat64FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Distributed_Step2MasterFloat64FeedforwardDense
    __del__ = lambda self: None

    def initialize(self, dataSize, topology):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_initialize(self, dataSize, topology)

    def setPartialResult(self, partialResult):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_getPartialResult(self)

    def getResult(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_getResult(self)

    def clone(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_getMethod(self)

    def compute(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_compute(self)

    def finalizeCompute(self):
        return _training20_.Distributed_Step2MasterFloat64FeedforwardDense_finalizeCompute(self)
Distributed_Step2MasterFloat64FeedforwardDense_swigregister = _training20_.Distributed_Step2MasterFloat64FeedforwardDense_swigregister
Distributed_Step2MasterFloat64FeedforwardDense_swigregister(Distributed_Step2MasterFloat64FeedforwardDense)

class Distributed_Step2MasterFloat32FeedforwardDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32FeedforwardDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training20_.Distributed_Step2MasterFloat32FeedforwardDense_input_set
    __swig_getmethods__["input"] = _training20_.Distributed_Step2MasterFloat32FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_training20_.Distributed_Step2MasterFloat32FeedforwardDense_input_get, _training20_.Distributed_Step2MasterFloat32FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _training20_.Distributed_Step2MasterFloat32FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _training20_.Distributed_Step2MasterFloat32FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training20_.Distributed_Step2MasterFloat32FeedforwardDense_parameter_get, _training20_.Distributed_Step2MasterFloat32FeedforwardDense_parameter_set)

    def __init__(self, *args):
        this = _training20_.new_Distributed_Step2MasterFloat32FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training20_.delete_Distributed_Step2MasterFloat32FeedforwardDense
    __del__ = lambda self: None

    def initialize(self, dataSize, topology):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_initialize(self, dataSize, topology)

    def setPartialResult(self, partialResult):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_getPartialResult(self)

    def getResult(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_getResult(self)

    def clone(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_clone(self)

    def getMethod(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_getMethod(self)

    def compute(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_compute(self)

    def finalizeCompute(self):
        return _training20_.Distributed_Step2MasterFloat32FeedforwardDense_finalizeCompute(self)
Distributed_Step2MasterFloat32FeedforwardDense_swigregister = _training20_.Distributed_Step2MasterFloat32FeedforwardDense_swigregister
Distributed_Step2MasterFloat32FeedforwardDense_swigregister(Distributed_Step2MasterFloat32FeedforwardDense)

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
            if 'fptype' in kwargs and kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                        return Distributed_Step1LocalFloat64FeedforwardDense(*args)
            if 'fptype' not in kwargs or kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                        return Distributed_Step1LocalFloat32FeedforwardDense(*args)
        if step == daal.step2Master:
            if 'fptype' in kwargs and kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                        return Distributed_Step2MasterFloat64FeedforwardDense(*args)
            if 'fptype' not in kwargs or kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                        return Distributed_Step2MasterFloat32FeedforwardDense(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' in kwargs and kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                return Batch_Float64FeedforwardDense(*args)
        if 'fptype' not in kwargs or kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == feedforwardDense:
                return Batch_Float32FeedforwardDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


