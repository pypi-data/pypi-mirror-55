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
            fp, pathname, description = imp.find_module('_prediction3_', [dirname(__file__)])
        except ImportError:
            import _prediction3_
            return _prediction3_
        if fp is not None:
            try:
                _mod = imp.load_module('_prediction3_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _prediction3_ = swig_import_helper()
    del swig_import_helper
else:
    import _prediction3_
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


import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_prediction3_.data_swigconstant(_prediction3_)
data = _prediction3_.data

_prediction3_.lastNumericTableInputId_swigconstant(_prediction3_)
lastNumericTableInputId = _prediction3_.lastNumericTableInputId

_prediction3_.model_swigconstant(_prediction3_)
model = _prediction3_.model

_prediction3_.lastModelInputId_swigconstant(_prediction3_)
lastModelInputId = _prediction3_.lastModelInputId

_prediction3_.prediction_swigconstant(_prediction3_)
prediction = _prediction3_.prediction

_prediction3_.probabilities_swigconstant(_prediction3_)
probabilities = _prediction3_.probabilities

_prediction3_.logProbabilities_swigconstant(_prediction3_)
logProbabilities = _prediction3_.logProbabilities

_prediction3_.lastResultId_swigconstant(_prediction3_)
lastResultId = _prediction3_.lastResultId
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
    __swig_destroy__ = _prediction3_.delete_InputIface
    __del__ = lambda self: None

    def getNumberOfRows(self):
        return _prediction3_.InputIface_getNumberOfRows(self)
InputIface_swigregister = _prediction3_.InputIface_swigregister
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
        this = _prediction3_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _prediction3_.delete_Input
    __del__ = lambda self: None

    def getNumberOfRows(self):
        return _prediction3_.Input_getNumberOfRows(self)

    def getTable(self, id):
        return _prediction3_.Input_getTable(self, id)

    def getModel(self, id):
        return _prediction3_.Input_getModel(self, id)

    def setTable(self, id, ptr):
        return _prediction3_.Input_setTable(self, id, ptr)

    def setModel(self, id, ptr):
        return _prediction3_.Input_setModel(self, id, ptr)

    def check(self, parameter, method):
        return _prediction3_.Input_check(self, parameter, method)
Input_swigregister = _prediction3_.Input_swigregister
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
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _prediction3_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_prediction3_.Result_serializationTag)

    def getSerializationTag(self):
        return _prediction3_.Result_getSerializationTag(self)

    def __init__(self):
        this = _prediction3_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _prediction3_.Result_get(self, id)

    def set(self, id, value):
        return _prediction3_.Result_set(self, id, value)

    def check(self, input, parameter, method):
        return _prediction3_.Result_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _prediction3_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _prediction3_.Result_allocate_Float32(self, input, parameter, method)

    __swig_destroy__ = _prediction3_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _prediction3_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _prediction3_.Result_serializationTag()
Result_serializationTag = _prediction3_.Result_serializationTag

class interface2_Result(daal.algorithms.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _prediction3_.interface2_Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_prediction3_.interface2_Result_serializationTag)

    def getSerializationTag(self):
        return _prediction3_.interface2_Result_getSerializationTag(self)

    def __init__(self):
        this = _prediction3_.new_interface2_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _prediction3_.delete_interface2_Result
    __del__ = lambda self: None

    def get(self, id):
        return _prediction3_.interface2_Result_get(self, id)

    def set(self, id, value):
        return _prediction3_.interface2_Result_set(self, id, value)

    def check(self, input, parameter, method):
        return _prediction3_.interface2_Result_check(self, input, parameter, method)
interface2_Result_swigregister = _prediction3_.interface2_Result_swigregister
interface2_Result_swigregister(interface2_Result)

def interface2_Result_serializationTag():
    return _prediction3_.interface2_Result_serializationTag()
interface2_Result_serializationTag = _prediction3_.interface2_Result_serializationTag

class Batch(daal.algorithms.Prediction):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _prediction3_.delete_Batch
    __del__ = lambda self: None

    def getInput(self):
        return _prediction3_.Batch_getInput(self)

    def getResult(self):
        return _prediction3_.Batch_getResult(self)

    def setResult(self, result):
        return _prediction3_.Batch_setResult(self, result)

    def clone(self):
        return _prediction3_.Batch_clone(self)

    def compute(self):
        return _prediction3_.Batch_compute(self)
Batch_swigregister = _prediction3_.Batch_swigregister
Batch_swigregister(Batch)

class interface2_Batch(daal.algorithms.Prediction):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _prediction3_.delete_interface2_Batch
    __del__ = lambda self: None

    def getInput(self):
        return _prediction3_.interface2_Batch_getInput(self)

    def parameter(self):
        return _prediction3_.interface2_Batch_parameter(self)

    def getResult(self):
        return _prediction3_.interface2_Batch_getResult(self)

    def setResult(self, result):
        return _prediction3_.interface2_Batch_setResult(self, result)

    def clone(self):
        return _prediction3_.interface2_Batch_clone(self)
interface2_Batch_swigregister = _prediction3_.interface2_Batch_swigregister
interface2_Batch_swigregister(interface2_Batch)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


