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
            fp, pathname, description = imp.find_module('_prediction17_', [dirname(__file__)])
        except ImportError:
            import _prediction17_
            return _prediction17_
        if fp is not None:
            try:
                _mod = imp.load_module('_prediction17_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _prediction17_ = swig_import_helper()
    del swig_import_helper
else:
    import _prediction17_
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
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.initializers
import daal.algorithms.neural_networks
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_prediction17_.defaultDense_swigconstant(_prediction17_)
defaultDense = _prediction17_.defaultDense

_prediction17_.feedforwardDense_swigconstant(_prediction17_)
feedforwardDense = _prediction17_.feedforwardDense

_prediction17_.prediction_swigconstant(_prediction17_)
prediction = _prediction17_.prediction

_prediction17_.lastResultId_swigconstant(_prediction17_)
lastResultId = _prediction17_.lastResultId

_prediction17_.predictionCollection_swigconstant(_prediction17_)
predictionCollection = _prediction17_.predictionCollection

_prediction17_.lastResultCollectionId_swigconstant(_prediction17_)
lastResultCollectionId = _prediction17_.lastResultCollectionId
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
    __swig_getmethods__["serializationTag"] = lambda x: _prediction17_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_prediction17_.Result_serializationTag)

    def getSerializationTag(self):
        return _prediction17_.Result_getSerializationTag(self)

    def __init__(self):
        this = _prediction17_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getResult(self, id):
        return _prediction17_.Result_getResult(self, id)

    def getResultCollection(self, id):
        return _prediction17_.Result_getResultCollection(self, id)

    def get(self, id, key):
        return _prediction17_.Result_get(self, id, key)

    def setResult(self, id, value):
        return _prediction17_.Result_setResult(self, id, value)

    def setResultCollection(self, id, value):
        return _prediction17_.Result_setResultCollection(self, id, value)

    def add(self, id, key, value):
        return _prediction17_.Result_add(self, id, key, value)

    def check(self, input, par, method):
        return _prediction17_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _prediction17_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _prediction17_.Result_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _prediction17_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _prediction17_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _prediction17_.Result_serializationTag()
Result_serializationTag = _prediction17_.Result_serializationTag

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

    def __init__(self, batchSize_=1, allocateWeightsAndBiases_=False):
        this = _prediction17_.new_Parameter(batchSize_, allocateWeightsAndBiases_)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["batchSize"] = _prediction17_.Parameter_batchSize_set
    __swig_getmethods__["batchSize"] = _prediction17_.Parameter_batchSize_get
    if _newclass:
        batchSize = _swig_property(_prediction17_.Parameter_batchSize_get, _prediction17_.Parameter_batchSize_set)
    __swig_setmethods__["allocateWeightsAndBiases"] = _prediction17_.Parameter_allocateWeightsAndBiases_set
    __swig_getmethods__["allocateWeightsAndBiases"] = _prediction17_.Parameter_allocateWeightsAndBiases_get
    if _newclass:
        allocateWeightsAndBiases = _swig_property(_prediction17_.Parameter_allocateWeightsAndBiases_get, _prediction17_.Parameter_allocateWeightsAndBiases_set)
    __swig_destroy__ = _prediction17_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _prediction17_.Parameter_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _prediction17_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_prediction17_.Model_serializationTag)

    def getSerializationTag(self):
        return _prediction17_.Model_getSerializationTag(self)

    def __init__(self, *args):
        this = _prediction17_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_getmethods__["create"] = lambda x: _prediction17_.Model_create
    if _newclass:
        create = staticmethod(_prediction17_.Model_create)
    __swig_destroy__ = _prediction17_.delete_Model
    __del__ = lambda self: None

    def setLayers(self, forwardLayers, nextLayers):
        return _prediction17_.Model_setLayers(self, forwardLayers, nextLayers)

    def getLayers(self):
        return _prediction17_.Model_getLayers(self)

    def getLayer(self, index):
        return _prediction17_.Model_getLayer(self, index)

    def allocate_Float64(self, sampleSize, parameter=None):
        r"""
    This function is specialized for float64"""
        return _prediction17_.Model_allocate_Float64(self, sampleSize, parameter)


    def allocate_Float32(self, sampleSize, parameter=None):
        r"""
    This function is specialized for float32"""
        return _prediction17_.Model_allocate_Float32(self, sampleSize, parameter)

Model_swigregister = _prediction17_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _prediction17_.Model_serializationTag()
Model_serializationTag = _prediction17_.Model_serializationTag

def Model_create(*args):
    return _prediction17_.Model_create(*args)
Model_create = _prediction17_.Model_create

def Model_Float64(forwardLayersForModel, nextLayersForModel, dummy, storeWeightsInTable):
    val = _prediction17_.new_Model_Float64(forwardLayersForModel, nextLayersForModel, dummy, storeWeightsInTable)
    return val

def Model_Float32(forwardLayersForModel, nextLayersForModel, dummy, storeWeightsInTable):
    val = _prediction17_.new_Model_Float32(forwardLayersForModel, nextLayersForModel, dummy, storeWeightsInTable)
    return val


_prediction17_.data_swigconstant(_prediction17_)
data = _prediction17_.data

_prediction17_.lastTensorInputId_swigconstant(_prediction17_)
lastTensorInputId = _prediction17_.lastTensorInputId

_prediction17_.model_swigconstant(_prediction17_)
model = _prediction17_.model

_prediction17_.lastModelInputId_swigconstant(_prediction17_)
lastModelInputId = _prediction17_.lastModelInputId
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
        this = _prediction17_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _prediction17_.delete_Input
    __del__ = lambda self: None

    def getTensorInput(self, id):
        return _prediction17_.Input_getTensorInput(self, id)

    def setTensorInput(self, id, value):
        return _prediction17_.Input_setTensorInput(self, id, value)

    def getModelInput(self, id):
        return _prediction17_.Input_getModelInput(self, id)

    def setModelInput(self, id, value):
        return _prediction17_.Input_setModelInput(self, id, value)

    def check(self, par, method):
        return _prediction17_.Input_check(self, par, method)
Input_swigregister = _prediction17_.Input_swigregister
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
        this = _prediction17_.new_Topology(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def size(self):
        return _prediction17_.Topology_size(self)

    def push_back(self, layer):
        return _prediction17_.Topology_push_back(self, layer)

    def add(self, *args):
        return _prediction17_.Topology_add(self, *args)

    def clear(self):
        return _prediction17_.Topology_clear(self)

    def get(self, *args):
        return _prediction17_.Topology_get(self, *args)

    def addNext(self, index, next):
        return _prediction17_.Topology_addNext(self, index, next)

    def __getitem__(self, i):
        return _prediction17_.Topology___getitem__(self, i)

    def __setitem__(self, i, v):
        return _prediction17_.Topology___setitem__(self, i, v)
    __swig_destroy__ = _prediction17_.delete_Topology
    __del__ = lambda self: None
Topology_swigregister = _prediction17_.Topology_swigregister
Topology_swigregister(Topology)

class Batch_Float64FeedforwardDense(daal.algorithms.Prediction):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FeedforwardDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _prediction17_.new_Batch_Float64FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _prediction17_.delete_Batch_Float64FeedforwardDense
    __del__ = lambda self: None

    def getResult(self):
        return _prediction17_.Batch_Float64FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _prediction17_.Batch_Float64FeedforwardDense_setResult(self, res)

    def clone(self):
        return _prediction17_.Batch_Float64FeedforwardDense_clone(self)

    def getMethod(self):
        return _prediction17_.Batch_Float64FeedforwardDense_getMethod(self)
    __swig_setmethods__["input"] = _prediction17_.Batch_Float64FeedforwardDense_input_set
    __swig_getmethods__["input"] = _prediction17_.Batch_Float64FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_prediction17_.Batch_Float64FeedforwardDense_input_get, _prediction17_.Batch_Float64FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _prediction17_.Batch_Float64FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _prediction17_.Batch_Float64FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_prediction17_.Batch_Float64FeedforwardDense_parameter_get, _prediction17_.Batch_Float64FeedforwardDense_parameter_set)

    def compute(self):
        return _prediction17_.Batch_Float64FeedforwardDense_compute(self)
Batch_Float64FeedforwardDense_swigregister = _prediction17_.Batch_Float64FeedforwardDense_swigregister
Batch_Float64FeedforwardDense_swigregister(Batch_Float64FeedforwardDense)

class Batch_Float32FeedforwardDense(daal.algorithms.Prediction):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FeedforwardDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FeedforwardDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _prediction17_.new_Batch_Float32FeedforwardDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _prediction17_.delete_Batch_Float32FeedforwardDense
    __del__ = lambda self: None

    def getResult(self):
        return _prediction17_.Batch_Float32FeedforwardDense_getResult(self)

    def setResult(self, res):
        return _prediction17_.Batch_Float32FeedforwardDense_setResult(self, res)

    def clone(self):
        return _prediction17_.Batch_Float32FeedforwardDense_clone(self)

    def getMethod(self):
        return _prediction17_.Batch_Float32FeedforwardDense_getMethod(self)
    __swig_setmethods__["input"] = _prediction17_.Batch_Float32FeedforwardDense_input_set
    __swig_getmethods__["input"] = _prediction17_.Batch_Float32FeedforwardDense_input_get
    if _newclass:
        input = _swig_property(_prediction17_.Batch_Float32FeedforwardDense_input_get, _prediction17_.Batch_Float32FeedforwardDense_input_set)
    __swig_setmethods__["parameter"] = _prediction17_.Batch_Float32FeedforwardDense_parameter_set
    __swig_getmethods__["parameter"] = _prediction17_.Batch_Float32FeedforwardDense_parameter_get
    if _newclass:
        parameter = _swig_property(_prediction17_.Batch_Float32FeedforwardDense_parameter_get, _prediction17_.Batch_Float32FeedforwardDense_parameter_set)

    def compute(self):
        return _prediction17_.Batch_Float32FeedforwardDense_compute(self)
Batch_Float32FeedforwardDense_swigregister = _prediction17_.Batch_Float32FeedforwardDense_swigregister
Batch_Float32FeedforwardDense_swigregister(Batch_Float32FeedforwardDense)

from numpy import float64, float32, intc

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


