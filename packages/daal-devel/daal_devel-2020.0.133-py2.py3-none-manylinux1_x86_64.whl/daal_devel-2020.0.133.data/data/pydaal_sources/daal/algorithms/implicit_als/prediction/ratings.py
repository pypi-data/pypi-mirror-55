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
            fp, pathname, description = imp.find_module('_ratings_', [dirname(__file__)])
        except ImportError:
            import _ratings_
            return _ratings_
        if fp is not None:
            try:
                _mod = imp.load_module('_ratings_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _ratings_ = swig_import_helper()
    del swig_import_helper
else:
    import _ratings_
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

_ratings_.defaultDense_swigconstant(_ratings_)
defaultDense = _ratings_.defaultDense

_ratings_.allUsersAllItems_swigconstant(_ratings_)
allUsersAllItems = _ratings_.allUsersAllItems

_ratings_.model_swigconstant(_ratings_)
model = _ratings_.model

_ratings_.lastModelInputId_swigconstant(_ratings_)
lastModelInputId = _ratings_.lastModelInputId

_ratings_.usersPartialModel_swigconstant(_ratings_)
usersPartialModel = _ratings_.usersPartialModel

_ratings_.itemsPartialModel_swigconstant(_ratings_)
itemsPartialModel = _ratings_.itemsPartialModel

_ratings_.lastPartialModelInputId_swigconstant(_ratings_)
lastPartialModelInputId = _ratings_.lastPartialModelInputId

_ratings_.finalResult_swigconstant(_ratings_)
finalResult = _ratings_.finalResult

_ratings_.lastPartialResultId_swigconstant(_ratings_)
lastPartialResultId = _ratings_.lastPartialResultId

_ratings_.prediction_swigconstant(_ratings_)
prediction = _ratings_.prediction

_ratings_.lastResultId_swigconstant(_ratings_)
lastResultId = _ratings_.lastResultId
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
    __swig_destroy__ = _ratings_.delete_InputIface
    __del__ = lambda self: None

    def getNumberOfUsers(self):
        return _ratings_.InputIface_getNumberOfUsers(self)

    def getNumberOfItems(self):
        return _ratings_.InputIface_getNumberOfItems(self)
InputIface_swigregister = _ratings_.InputIface_swigregister
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
        this = _ratings_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _ratings_.Input_get(self, id)

    def set(self, id, ptr):
        return _ratings_.Input_set(self, id, ptr)

    def getNumberOfUsers(self):
        return _ratings_.Input_getNumberOfUsers(self)

    def getNumberOfItems(self):
        return _ratings_.Input_getNumberOfItems(self)

    def check(self, parameter, method):
        return _ratings_.Input_check(self, parameter, method)
Input_swigregister = _ratings_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _ratings_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_ratings_.Result_serializationTag)

    def getSerializationTag(self):
        return _ratings_.Result_getSerializationTag(self)

    def __init__(self):
        this = _ratings_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _ratings_.Result_get(self, id)

    def set(self, id, ptr):
        return _ratings_.Result_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _ratings_.Result_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _ratings_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _ratings_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _ratings_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _ratings_.Result_serializationTag()
Result_serializationTag = _ratings_.Result_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _ratings_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_ratings_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _ratings_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _ratings_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_PartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _ratings_.PartialResult_get(self, id)

    def set(self, id, ptr):
        return _ratings_.PartialResult_set(self, id, ptr)

    def check(self, input, parameter, method):
        return _ratings_.PartialResult_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _ratings_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _ratings_.PartialResult_allocate_Float32(self, input, parameter, method)

PartialResult_swigregister = _ratings_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _ratings_.PartialResult_serializationTag()
PartialResult_serializationTag = _ratings_.PartialResult_serializationTag

class DistributedInput_Step1Local(InputIface):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step1Local, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step1Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _ratings_.new_DistributedInput_Step1Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None

    def get(self, id):
        return _ratings_.DistributedInput_Step1Local_get(self, id)

    def set(self, id, ptr):
        return _ratings_.DistributedInput_Step1Local_set(self, id, ptr)

    def getNumberOfUsers(self):
        return _ratings_.DistributedInput_Step1Local_getNumberOfUsers(self)

    def getNumberOfItems(self):
        return _ratings_.DistributedInput_Step1Local_getNumberOfItems(self)

    def check(self, parameter, method):
        return _ratings_.DistributedInput_Step1Local_check(self, parameter, method)
DistributedInput_Step1Local_swigregister = _ratings_.DistributedInput_Step1Local_swigregister
DistributedInput_Step1Local_swigregister(DistributedInput_Step1Local)

class Batch_Float64AllUsersAllItems(daal.algorithms.Prediction):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64AllUsersAllItems, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64AllUsersAllItems, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _ratings_.Batch_Float64AllUsersAllItems_input_set
    __swig_getmethods__["input"] = _ratings_.Batch_Float64AllUsersAllItems_input_get
    if _newclass:
        input = _swig_property(_ratings_.Batch_Float64AllUsersAllItems_input_get, _ratings_.Batch_Float64AllUsersAllItems_input_set)
    __swig_setmethods__["parameter"] = _ratings_.Batch_Float64AllUsersAllItems_parameter_set
    __swig_getmethods__["parameter"] = _ratings_.Batch_Float64AllUsersAllItems_parameter_get
    if _newclass:
        parameter = _swig_property(_ratings_.Batch_Float64AllUsersAllItems_parameter_get, _ratings_.Batch_Float64AllUsersAllItems_parameter_set)

    def __init__(self, *args):
        this = _ratings_.new_Batch_Float64AllUsersAllItems(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Batch_Float64AllUsersAllItems
    __del__ = lambda self: None

    def getResult(self):
        return _ratings_.Batch_Float64AllUsersAllItems_getResult(self)

    def setResult(self, result):
        return _ratings_.Batch_Float64AllUsersAllItems_setResult(self, result)

    def getMethod(self):
        return _ratings_.Batch_Float64AllUsersAllItems_getMethod(self)

    def clone(self):
        return _ratings_.Batch_Float64AllUsersAllItems_clone(self)

    def compute(self):
        return _ratings_.Batch_Float64AllUsersAllItems_compute(self)
Batch_Float64AllUsersAllItems_swigregister = _ratings_.Batch_Float64AllUsersAllItems_swigregister
Batch_Float64AllUsersAllItems_swigregister(Batch_Float64AllUsersAllItems)

class Batch_Float32AllUsersAllItems(daal.algorithms.Prediction):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32AllUsersAllItems, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Prediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32AllUsersAllItems, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _ratings_.Batch_Float32AllUsersAllItems_input_set
    __swig_getmethods__["input"] = _ratings_.Batch_Float32AllUsersAllItems_input_get
    if _newclass:
        input = _swig_property(_ratings_.Batch_Float32AllUsersAllItems_input_get, _ratings_.Batch_Float32AllUsersAllItems_input_set)
    __swig_setmethods__["parameter"] = _ratings_.Batch_Float32AllUsersAllItems_parameter_set
    __swig_getmethods__["parameter"] = _ratings_.Batch_Float32AllUsersAllItems_parameter_get
    if _newclass:
        parameter = _swig_property(_ratings_.Batch_Float32AllUsersAllItems_parameter_get, _ratings_.Batch_Float32AllUsersAllItems_parameter_set)

    def __init__(self, *args):
        this = _ratings_.new_Batch_Float32AllUsersAllItems(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Batch_Float32AllUsersAllItems
    __del__ = lambda self: None

    def getResult(self):
        return _ratings_.Batch_Float32AllUsersAllItems_getResult(self)

    def setResult(self, result):
        return _ratings_.Batch_Float32AllUsersAllItems_setResult(self, result)

    def getMethod(self):
        return _ratings_.Batch_Float32AllUsersAllItems_getMethod(self)

    def clone(self):
        return _ratings_.Batch_Float32AllUsersAllItems_clone(self)

    def compute(self):
        return _ratings_.Batch_Float32AllUsersAllItems_compute(self)
Batch_Float32AllUsersAllItems_swigregister = _ratings_.Batch_Float32AllUsersAllItems_swigregister
Batch_Float32AllUsersAllItems_swigregister(Batch_Float32AllUsersAllItems)

class Distributed_Step1LocalFloat64AllUsersAllItems(daal.algorithms.DistributedPrediction):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.DistributedPrediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64AllUsersAllItems, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.DistributedPrediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64AllUsersAllItems, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_input_set
    __swig_getmethods__["input"] = _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_input_get
    if _newclass:
        input = _swig_property(_ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_input_get, _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_input_set)
    __swig_setmethods__["parameter"] = _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_parameter_set
    __swig_getmethods__["parameter"] = _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_parameter_get
    if _newclass:
        parameter = _swig_property(_ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_parameter_get, _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_parameter_set)

    def __init__(self, *args):
        this = _ratings_.new_Distributed_Step1LocalFloat64AllUsersAllItems(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Distributed_Step1LocalFloat64AllUsersAllItems
    __del__ = lambda self: None

    def getResult(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_getResult(self)

    def getPartialResult(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_getPartialResult(self)

    def setResult(self, result):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_setResult(self, result)

    def setPartialResult(self, partialResult, initFlag=False):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_setPartialResult(self, partialResult, initFlag)

    def getMethod(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_getMethod(self)

    def clone(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_clone(self)

    def compute(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_compute(self)

    def finalizeCompute(self):
        return _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_finalizeCompute(self)
Distributed_Step1LocalFloat64AllUsersAllItems_swigregister = _ratings_.Distributed_Step1LocalFloat64AllUsersAllItems_swigregister
Distributed_Step1LocalFloat64AllUsersAllItems_swigregister(Distributed_Step1LocalFloat64AllUsersAllItems)

class Distributed_Step1LocalFloat32AllUsersAllItems(daal.algorithms.DistributedPrediction):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.DistributedPrediction]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32AllUsersAllItems, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.DistributedPrediction]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32AllUsersAllItems, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_input_set
    __swig_getmethods__["input"] = _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_input_get
    if _newclass:
        input = _swig_property(_ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_input_get, _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_input_set)
    __swig_setmethods__["parameter"] = _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_parameter_set
    __swig_getmethods__["parameter"] = _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_parameter_get
    if _newclass:
        parameter = _swig_property(_ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_parameter_get, _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_parameter_set)

    def __init__(self, *args):
        this = _ratings_.new_Distributed_Step1LocalFloat32AllUsersAllItems(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _ratings_.delete_Distributed_Step1LocalFloat32AllUsersAllItems
    __del__ = lambda self: None

    def getResult(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_getResult(self)

    def getPartialResult(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_getPartialResult(self)

    def setResult(self, result):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_setResult(self, result)

    def setPartialResult(self, partialResult, initFlag=False):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_setPartialResult(self, partialResult, initFlag)

    def getMethod(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_getMethod(self)

    def clone(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_clone(self)

    def compute(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_compute(self)

    def finalizeCompute(self):
        return _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_finalizeCompute(self)
Distributed_Step1LocalFloat32AllUsersAllItems_swigregister = _ratings_.Distributed_Step1LocalFloat32AllUsersAllItems_swigregister
Distributed_Step1LocalFloat32AllUsersAllItems_swigregister(Distributed_Step1LocalFloat32AllUsersAllItems)

from numpy import float64, float32, intc

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            return DistributedInput_Step1Local(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == allUsersAllItems:
                        return Distributed_Step1LocalFloat64AllUsersAllItems(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == allUsersAllItems:
                        return Distributed_Step1LocalFloat32AllUsersAllItems(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == allUsersAllItems:
                return Batch_Float64AllUsersAllItems(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == allUsersAllItems:
                return Batch_Float32AllUsersAllItems(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


