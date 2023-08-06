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
            fp, pathname, description = imp.find_module('_iterative_solver_', [dirname(__file__)])
        except ImportError:
            import _iterative_solver_
            return _iterative_solver_
        if fp is not None:
            try:
                _mod = imp.load_module('_iterative_solver_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _iterative_solver_ = swig_import_helper()
    del swig_import_helper
else:
    import _iterative_solver_
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


import daal.algorithms.optimization_solver
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import sys
daal.algorithms.optimization_solver = sys.modules[__package__]
del sys


_iterative_solver_.inputArgument_swigconstant(_iterative_solver_)
inputArgument = _iterative_solver_.inputArgument

_iterative_solver_.lastInputId_swigconstant(_iterative_solver_)
lastInputId = _iterative_solver_.lastInputId

_iterative_solver_.optionalArgument_swigconstant(_iterative_solver_)
optionalArgument = _iterative_solver_.optionalArgument

_iterative_solver_.lastOptionalInputId_swigconstant(_iterative_solver_)
lastOptionalInputId = _iterative_solver_.lastOptionalInputId

_iterative_solver_.minimum_swigconstant(_iterative_solver_)
minimum = _iterative_solver_.minimum

_iterative_solver_.nIterations_swigconstant(_iterative_solver_)
nIterations = _iterative_solver_.nIterations

_iterative_solver_.lastResultId_swigconstant(_iterative_solver_)
lastResultId = _iterative_solver_.lastResultId

_iterative_solver_.optionalResult_swigconstant(_iterative_solver_)
optionalResult = _iterative_solver_.optionalResult

_iterative_solver_.lastOptionalResultId_swigconstant(_iterative_solver_)
lastOptionalResultId = _iterative_solver_.lastOptionalResultId

_iterative_solver_.lastIteration_swigconstant(_iterative_solver_)
lastIteration = _iterative_solver_.lastIteration

_iterative_solver_.lastOptionalData_swigconstant(_iterative_solver_)
lastOptionalData = _iterative_solver_.lastOptionalData
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
        this = _iterative_solver_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_interface1_Parameter
    __del__ = lambda self: None

    def check(self):
        return _iterative_solver_.interface1_Parameter_check(self)
    __swig_setmethods__["function"] = _iterative_solver_.interface1_Parameter_function_set
    __swig_getmethods__["function"] = _iterative_solver_.interface1_Parameter_function_get
    if _newclass:
        function = _swig_property(_iterative_solver_.interface1_Parameter_function_get, _iterative_solver_.interface1_Parameter_function_set)
    __swig_setmethods__["nIterations"] = _iterative_solver_.interface1_Parameter_nIterations_set
    __swig_getmethods__["nIterations"] = _iterative_solver_.interface1_Parameter_nIterations_get
    if _newclass:
        nIterations = _swig_property(_iterative_solver_.interface1_Parameter_nIterations_get, _iterative_solver_.interface1_Parameter_nIterations_set)
    __swig_setmethods__["accuracyThreshold"] = _iterative_solver_.interface1_Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _iterative_solver_.interface1_Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_iterative_solver_.interface1_Parameter_accuracyThreshold_get, _iterative_solver_.interface1_Parameter_accuracyThreshold_set)
    __swig_setmethods__["optionalResultRequired"] = _iterative_solver_.interface1_Parameter_optionalResultRequired_set
    __swig_getmethods__["optionalResultRequired"] = _iterative_solver_.interface1_Parameter_optionalResultRequired_get
    if _newclass:
        optionalResultRequired = _swig_property(_iterative_solver_.interface1_Parameter_optionalResultRequired_get, _iterative_solver_.interface1_Parameter_optionalResultRequired_set)
    __swig_setmethods__["batchSize"] = _iterative_solver_.interface1_Parameter_batchSize_set
    __swig_getmethods__["batchSize"] = _iterative_solver_.interface1_Parameter_batchSize_get
    if _newclass:
        batchSize = _swig_property(_iterative_solver_.interface1_Parameter_batchSize_get, _iterative_solver_.interface1_Parameter_batchSize_set)
interface1_Parameter_swigregister = _iterative_solver_.interface1_Parameter_swigregister
interface1_Parameter_swigregister(interface1_Parameter)

class interface1_Input(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _iterative_solver_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_interface1_Input
    __del__ = lambda self: None

    def interface1_getInput(self, id):
        return _iterative_solver_.interface1_Input_interface1_getInput(self, id)

    def interface1_getOptionalInput(self, id):
        return _iterative_solver_.interface1_Input_interface1_getOptionalInput(self, id)

    def get(self, id):
        return _iterative_solver_.interface1_Input_get(self, id)

    def interface1_setInput(self, id, ptr):
        return _iterative_solver_.interface1_Input_interface1_setInput(self, id, ptr)

    def interface1_setOptionalInput(self, id, ptr):
        return _iterative_solver_.interface1_Input_interface1_setOptionalInput(self, id, ptr)

    def set(self, id, ptr):
        return _iterative_solver_.interface1_Input_set(self, id, ptr)

    def check(self, par, method):
        return _iterative_solver_.interface1_Input_check(self, par, method)
interface1_Input_swigregister = _iterative_solver_.interface1_Input_swigregister
interface1_Input_swigregister(interface1_Input)

class interface1_Result(daal.algorithms.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _iterative_solver_.interface1_Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_iterative_solver_.interface1_Result_serializationTag)

    def getSerializationTag(self):
        return _iterative_solver_.interface1_Result_getSerializationTag(self)

    def __init__(self):
        this = _iterative_solver_.new_interface1_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_interface1_Result
    __del__ = lambda self: None

    def interface1_getResult(self, id):
        return _iterative_solver_.interface1_Result_interface1_getResult(self, id)

    def interface1_getOptionalResult(self, id):
        return _iterative_solver_.interface1_Result_interface1_getOptionalResult(self, id)

    def get(self, id):
        return _iterative_solver_.interface1_Result_get(self, id)

    def interface1_setResult(self, id, ptr):
        return _iterative_solver_.interface1_Result_interface1_setResult(self, id, ptr)

    def interface1_setOptionalResult(self, id, ptr):
        return _iterative_solver_.interface1_Result_interface1_setOptionalResult(self, id, ptr)

    def set(self, id, ptr):
        return _iterative_solver_.interface1_Result_set(self, id, ptr)

    def check(self, input, par, method):
        return _iterative_solver_.interface1_Result_check(self, input, par, method)
interface1_Result_swigregister = _iterative_solver_.interface1_Result_swigregister
interface1_Result_swigregister(interface1_Result)

def interface1_Result_serializationTag():
    return _iterative_solver_.interface1_Result_serializationTag()
interface1_Result_serializationTag = _iterative_solver_.interface1_Result_serializationTag

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
        this = _iterative_solver_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_Parameter
    __del__ = lambda self: None

    def check(self):
        return _iterative_solver_.Parameter_check(self)
    __swig_setmethods__["function"] = _iterative_solver_.Parameter_function_set
    __swig_getmethods__["function"] = _iterative_solver_.Parameter_function_get
    if _newclass:
        function = _swig_property(_iterative_solver_.Parameter_function_get, _iterative_solver_.Parameter_function_set)
    __swig_setmethods__["nIterations"] = _iterative_solver_.Parameter_nIterations_set
    __swig_getmethods__["nIterations"] = _iterative_solver_.Parameter_nIterations_get
    if _newclass:
        nIterations = _swig_property(_iterative_solver_.Parameter_nIterations_get, _iterative_solver_.Parameter_nIterations_set)
    __swig_setmethods__["accuracyThreshold"] = _iterative_solver_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _iterative_solver_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_iterative_solver_.Parameter_accuracyThreshold_get, _iterative_solver_.Parameter_accuracyThreshold_set)
    __swig_setmethods__["optionalResultRequired"] = _iterative_solver_.Parameter_optionalResultRequired_set
    __swig_getmethods__["optionalResultRequired"] = _iterative_solver_.Parameter_optionalResultRequired_get
    if _newclass:
        optionalResultRequired = _swig_property(_iterative_solver_.Parameter_optionalResultRequired_get, _iterative_solver_.Parameter_optionalResultRequired_set)
    __swig_setmethods__["batchSize"] = _iterative_solver_.Parameter_batchSize_set
    __swig_getmethods__["batchSize"] = _iterative_solver_.Parameter_batchSize_get
    if _newclass:
        batchSize = _swig_property(_iterative_solver_.Parameter_batchSize_get, _iterative_solver_.Parameter_batchSize_set)
Parameter_swigregister = _iterative_solver_.Parameter_swigregister
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
        this = _iterative_solver_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_Input
    __del__ = lambda self: None

    def getInput(self, id):
        return _iterative_solver_.Input_getInput(self, id)

    def getOptionalInput(self, id):
        return _iterative_solver_.Input_getOptionalInput(self, id)

    def get(self, id):
        return _iterative_solver_.Input_get(self, id)

    def setInput(self, id, ptr):
        return _iterative_solver_.Input_setInput(self, id, ptr)

    def setOptionalInput(self, id, ptr):
        return _iterative_solver_.Input_setOptionalInput(self, id, ptr)

    def set(self, id, ptr):
        return _iterative_solver_.Input_set(self, id, ptr)

    def check(self, par, method):
        return _iterative_solver_.Input_check(self, par, method)
Input_swigregister = _iterative_solver_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _iterative_solver_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_iterative_solver_.Result_serializationTag)

    def getSerializationTag(self):
        return _iterative_solver_.Result_getSerializationTag(self)

    def __init__(self):
        this = _iterative_solver_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _iterative_solver_.delete_Result
    __del__ = lambda self: None

    def getResult(self, id):
        return _iterative_solver_.Result_getResult(self, id)

    def getOptionalResult(self, id):
        return _iterative_solver_.Result_getOptionalResult(self, id)

    def get(self, id):
        return _iterative_solver_.Result_get(self, id)

    def setResult(self, id, ptr):
        return _iterative_solver_.Result_setResult(self, id, ptr)

    def setOptionalResult(self, id, ptr):
        return _iterative_solver_.Result_setOptionalResult(self, id, ptr)

    def set(self, id, ptr):
        return _iterative_solver_.Result_set(self, id, ptr)

    def check(self, input, par, method):
        return _iterative_solver_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _iterative_solver_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _iterative_solver_.Result_allocate_Float32(self, input, par, method)

Result_swigregister = _iterative_solver_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _iterative_solver_.Result_serializationTag()
Result_serializationTag = _iterative_solver_.Result_serializationTag

class interface1_Batch(daal.algorithms.optimization_solver.BatchIface):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.BatchIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.BatchIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _iterative_solver_.delete_interface1_Batch
    __del__ = lambda self: None

    def getInput(self):
        return _iterative_solver_.interface1_Batch_getInput(self)

    def getParameter(self):
        return _iterative_solver_.interface1_Batch_getParameter(self)

    def getResult(self):
        return _iterative_solver_.interface1_Batch_getResult(self)

    def createResult(self):
        return _iterative_solver_.interface1_Batch_createResult(self)

    def clone(self):
        return _iterative_solver_.interface1_Batch_clone(self)
interface1_Batch_swigregister = _iterative_solver_.interface1_Batch_swigregister
interface1_Batch_swigregister(interface1_Batch)

class Batch(daal.algorithms.optimization_solver.BatchIface):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.BatchIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.BatchIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _iterative_solver_.delete_Batch
    __del__ = lambda self: None

    def getInput(self):
        return _iterative_solver_.Batch_getInput(self)

    def getParameter(self):
        return _iterative_solver_.Batch_getParameter(self)

    def getResult(self):
        return _iterative_solver_.Batch_getResult(self)

    def createResult(self):
        return _iterative_solver_.Batch_createResult(self)

    def clone(self):
        return _iterative_solver_.Batch_clone(self)

    def compute(self):
        return _iterative_solver_.Batch_compute(self)
Batch_swigregister = _iterative_solver_.Batch_swigregister
Batch_swigregister(Batch)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


