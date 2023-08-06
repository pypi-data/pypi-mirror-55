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
            fp, pathname, description = imp.find_module('_forward10_', [dirname(__file__)])
        except ImportError:
            import _forward10_
            return _forward10_
        if fp is not None:
            try:
                _mod = imp.load_module('_forward10_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _forward10_ = swig_import_helper()
    del swig_import_helper
else:
    import _forward10_
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


import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.initializers
import daal.algorithms.neural_networks
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_forward10_.data_swigconstant(_forward10_)
data = _forward10_.data

_forward10_.weights_swigconstant(_forward10_)
weights = _forward10_.weights

_forward10_.biases_swigconstant(_forward10_)
biases = _forward10_.biases

_forward10_.lastInputId_swigconstant(_forward10_)
lastInputId = _forward10_.lastInputId

_forward10_.inputLayerData_swigconstant(_forward10_)
inputLayerData = _forward10_.inputLayerData

_forward10_.lastInputLayerDataId_swigconstant(_forward10_)
lastInputLayerDataId = _forward10_.lastInputLayerDataId

_forward10_.value_swigconstant(_forward10_)
value = _forward10_.value

_forward10_.lastResultId_swigconstant(_forward10_)
lastResultId = _forward10_.lastResultId

_forward10_.resultForBackward_swigconstant(_forward10_)
resultForBackward = _forward10_.resultForBackward

_forward10_.lastResultLayerDataId_swigconstant(_forward10_)
lastResultLayerDataId = _forward10_.lastResultLayerDataId
class InputIface(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, InputIface, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _forward10_.new_InputIface(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _forward10_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _forward10_.InputIface_swigregister
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

    def __init__(self, *args):
        this = _forward10_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _forward10_.delete_Input
    __del__ = lambda self: None

    def getInput(self, id):
        return _forward10_.Input_getInput(self, id)

    def setInput(self, id, ptr):
        return _forward10_.Input_setInput(self, id, ptr)

    def getInputLayerData(self, id):
        return _forward10_.Input_getInputLayerData(self, id)

    def setInputLayerData(self, id, ptr):
        return _forward10_.Input_setInputLayerData(self, id, ptr)

    def check(self, par, method):
        return _forward10_.Input_check(self, par, method)

    def getLayout(self):
        return _forward10_.Input_getLayout(self)

    def getWeightsSizes(self, parameter):
        return _forward10_.Input_getWeightsSizes(self, parameter)

    def getBiasesSizes(self, parameter):
        return _forward10_.Input_getBiasesSizes(self, parameter)

    def addData(self, dataTensor, index):
        return _forward10_.Input_addData(self, dataTensor, index)

    def eraseInputData(self):
        return _forward10_.Input_eraseInputData(self)
Input_swigregister = _forward10_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _forward10_.delete_Result
    __del__ = lambda self: None

    def getValueSize(self, *args):
        return _forward10_.Result_getValueSize(self, *args)

    def getValueCollectionSize(self, inputSize, par, method):
        return _forward10_.Result_getValueCollectionSize(self, inputSize, par, method)

    def getResult(self, id):
        return _forward10_.Result_getResult(self, id)

    def getResultLayerData(self, id):
        return _forward10_.Result_getResultLayerData(self, id)

    def setResult(self, id, ptr):
        return _forward10_.Result_setResult(self, id, ptr)

    def setResultLayerData(self, id, ptr):
        return _forward10_.Result_setResultLayerData(self, id, ptr)

    def getSerializationTag(self):
        return _forward10_.Result_getSerializationTag(self)

    def check(self, input, parameter, method):
        return _forward10_.Result_check(self, input, parameter, method)

    def getLayout(self):
        return _forward10_.Result_getLayout(self)

    def setResultForBackward(self, input):
        return _forward10_.Result_setResultForBackward(self, input)

    def getValue(self, index):
        return _forward10_.Result_getValue(self, index)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _forward10_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _forward10_.Result_allocate_Float32(self, input, par, method)

Result_swigregister = _forward10_.Result_swigregister
Result_swigregister(Result)

class LayerDescriptor(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerDescriptor, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LayerDescriptor, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _forward10_.new_LayerDescriptor(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def index(self):
        return _forward10_.LayerDescriptor_index(self)

    def addNext(self, index):
        return _forward10_.LayerDescriptor_addNext(self, index)

    def layer(self):
        return _forward10_.LayerDescriptor_layer(self)

    def nextLayers(self):
        return _forward10_.LayerDescriptor_nextLayers(self)
    __swig_destroy__ = _forward10_.delete_LayerDescriptor
    __del__ = lambda self: None
LayerDescriptor_swigregister = _forward10_.LayerDescriptor_swigregister
LayerDescriptor_swigregister(LayerDescriptor)

class LayerContainerIfaceImpl(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerContainerIfaceImpl, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, LayerContainerIfaceImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def setupCompute(self):
        return _forward10_.LayerContainerIfaceImpl_setupCompute(self)

    def resetCompute(self):
        return _forward10_.LayerContainerIfaceImpl_resetCompute(self)

    def allocateInput(self):
        return _forward10_.LayerContainerIfaceImpl_allocateInput(self)

    def initializeInput(self):
        return _forward10_.LayerContainerIfaceImpl_initializeInput(self)
    __swig_destroy__ = _forward10_.delete_LayerContainerIfaceImpl
    __del__ = lambda self: None
LayerContainerIfaceImpl_swigregister = _forward10_.LayerContainerIfaceImpl_swigregister
LayerContainerIfaceImpl_swigregister(LayerContainerIfaceImpl)

class LayerIface(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LayerIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _forward10_.delete_LayerIface
    __del__ = lambda self: None

    def getLayerResult(self):
        return _forward10_.LayerIface_getLayerResult(self)

    def getLayerInput(self):
        return _forward10_.LayerIface_getLayerInput(self)

    def getLayerParameter(self):
        return _forward10_.LayerIface_getLayerParameter(self)

    def clone(self):
        return _forward10_.LayerIface_clone(self)

    def allocateResult(self):
        return _forward10_.LayerIface_allocateResult(self)

    def allocateInput(self):
        return _forward10_.LayerIface_allocateInput(self)

    def initializeInput(self):
        return _forward10_.LayerIface_initializeInput(self)

    def addInput(self, result, resultIndex, inputIndex):
        return _forward10_.LayerIface_addInput(self, result, resultIndex, inputIndex)

    def getLayerForPrediction(self):
        return _forward10_.LayerIface_getLayerForPrediction(self)
LayerIface_swigregister = _forward10_.LayerIface_swigregister
LayerIface_swigregister(LayerIface)

class LayerIfaceImpl(LayerIface):
    __swig_setmethods__ = {}
    for _s in [LayerIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LayerIfaceImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [LayerIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LayerIfaceImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _forward10_.delete_LayerIfaceImpl
    __del__ = lambda self: None

    def allocateInput(self):
        return _forward10_.LayerIfaceImpl_allocateInput(self)

    def initializeInput(self):
        return _forward10_.LayerIfaceImpl_initializeInput(self)

    def addInput(self, result, resultIndex, inputIndex):
        return _forward10_.LayerIfaceImpl_addInput(self, result, resultIndex, inputIndex)

    def getLayerForPrediction(self):
        return _forward10_.LayerIfaceImpl_getLayerForPrediction(self)
LayerIfaceImpl_swigregister = _forward10_.LayerIfaceImpl_swigregister
LayerIfaceImpl_swigregister(LayerIfaceImpl)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


