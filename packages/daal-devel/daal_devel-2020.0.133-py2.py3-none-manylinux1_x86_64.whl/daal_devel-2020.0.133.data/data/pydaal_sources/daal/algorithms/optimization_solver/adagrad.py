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
            fp, pathname, description = imp.find_module('_adagrad_', [dirname(__file__)])
        except ImportError:
            import _adagrad_
            return _adagrad_
        if fp is not None:
            try:
                _mod = imp.load_module('_adagrad_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _adagrad_ = swig_import_helper()
    del swig_import_helper
else:
    import _adagrad_
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


import daal.algorithms.optimization_solver.iterative_solver
import daal.algorithms.optimization_solver
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.optimization_solver.sum_of_functions
import daal.algorithms.optimization_solver.objective_function
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_adagrad_.defaultDense_swigconstant(_adagrad_)
defaultDense = _adagrad_.defaultDense

_adagrad_.gradientSquareSum_swigconstant(_adagrad_)
gradientSquareSum = _adagrad_.gradientSquareSum

_adagrad_.lastOptionalData_swigconstant(_adagrad_)
lastOptionalData = _adagrad_.lastOptionalData
class interface1_Parameter(daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _adagrad_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _adagrad_.delete_interface1_Parameter
    __del__ = lambda self: None

    def check(self):
        return _adagrad_.interface1_Parameter_check(self)
    __swig_setmethods__["batchIndices"] = _adagrad_.interface1_Parameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _adagrad_.interface1_Parameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_adagrad_.interface1_Parameter_batchIndices_get, _adagrad_.interface1_Parameter_batchIndices_set)
    __swig_setmethods__["learningRate"] = _adagrad_.interface1_Parameter_learningRate_set
    __swig_getmethods__["learningRate"] = _adagrad_.interface1_Parameter_learningRate_get
    if _newclass:
        learningRate = _swig_property(_adagrad_.interface1_Parameter_learningRate_get, _adagrad_.interface1_Parameter_learningRate_set)
    __swig_setmethods__["degenerateCasesThreshold"] = _adagrad_.interface1_Parameter_degenerateCasesThreshold_set
    __swig_getmethods__["degenerateCasesThreshold"] = _adagrad_.interface1_Parameter_degenerateCasesThreshold_get
    if _newclass:
        degenerateCasesThreshold = _swig_property(_adagrad_.interface1_Parameter_degenerateCasesThreshold_get, _adagrad_.interface1_Parameter_degenerateCasesThreshold_set)
    __swig_setmethods__["seed"] = _adagrad_.interface1_Parameter_seed_set
    __swig_getmethods__["seed"] = _adagrad_.interface1_Parameter_seed_get
    if _newclass:
        seed = _swig_property(_adagrad_.interface1_Parameter_seed_get, _adagrad_.interface1_Parameter_seed_set)
    __swig_setmethods__["engine"] = _adagrad_.interface1_Parameter_engine_set
    __swig_getmethods__["engine"] = _adagrad_.interface1_Parameter_engine_get
    if _newclass:
        engine = _swig_property(_adagrad_.interface1_Parameter_engine_get, _adagrad_.interface1_Parameter_engine_set)
interface1_Parameter_swigregister = _adagrad_.interface1_Parameter_swigregister
interface1_Parameter_swigregister(interface1_Parameter)

class interface1_Input(daal.algorithms.optimization_solver.iterative_solver.interface1_Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _adagrad_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _adagrad_.interface1_Input_set(self, id, ptr)

    def get(self, id):
        return _adagrad_.interface1_Input_get(self, id)

    def interface1_getOptionalData(self, id):
        return _adagrad_.interface1_Input_interface1_getOptionalData(self, id)

    def interface1_setOptionalData(self, id, ptr):
        return _adagrad_.interface1_Input_interface1_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _adagrad_.interface1_Input_check(self, par, method)
    __swig_destroy__ = _adagrad_.delete_interface1_Input
    __del__ = lambda self: None
interface1_Input_swigregister = _adagrad_.interface1_Input_swigregister
interface1_Input_swigregister(interface1_Input)

class interface1_Result(daal.algorithms.optimization_solver.iterative_solver.interface1_Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _adagrad_.interface1_Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_adagrad_.interface1_Result_serializationTag)

    def getSerializationTag(self):
        return _adagrad_.interface1_Result_getSerializationTag(self)

    def __init__(self):
        this = _adagrad_.new_interface1_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _adagrad_.interface1_Result_set(self, id, ptr)

    def get(self, id):
        return _adagrad_.interface1_Result_get(self, id)

    def interface1_getOptionalData(self, id):
        return _adagrad_.interface1_Result_interface1_getOptionalData(self, id)

    def interface1_setOptionalData(self, id, ptr):
        return _adagrad_.interface1_Result_interface1_setOptionalData(self, id, ptr)

    def check(self, input, par, method):
        return _adagrad_.interface1_Result_check(self, input, par, method)
    __swig_destroy__ = _adagrad_.delete_interface1_Result
    __del__ = lambda self: None
interface1_Result_swigregister = _adagrad_.interface1_Result_swigregister
interface1_Result_swigregister(interface1_Result)

def interface1_Result_serializationTag():
    return _adagrad_.interface1_Result_serializationTag()
interface1_Result_serializationTag = _adagrad_.interface1_Result_serializationTag

class Parameter(daal.algorithms.optimization_solver.iterative_solver.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _adagrad_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _adagrad_.delete_Parameter
    __del__ = lambda self: None

    def check(self):
        return _adagrad_.Parameter_check(self)
    __swig_setmethods__["batchIndices"] = _adagrad_.Parameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _adagrad_.Parameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_adagrad_.Parameter_batchIndices_get, _adagrad_.Parameter_batchIndices_set)
    __swig_setmethods__["learningRate"] = _adagrad_.Parameter_learningRate_set
    __swig_getmethods__["learningRate"] = _adagrad_.Parameter_learningRate_get
    if _newclass:
        learningRate = _swig_property(_adagrad_.Parameter_learningRate_get, _adagrad_.Parameter_learningRate_set)
    __swig_setmethods__["degenerateCasesThreshold"] = _adagrad_.Parameter_degenerateCasesThreshold_set
    __swig_getmethods__["degenerateCasesThreshold"] = _adagrad_.Parameter_degenerateCasesThreshold_get
    if _newclass:
        degenerateCasesThreshold = _swig_property(_adagrad_.Parameter_degenerateCasesThreshold_get, _adagrad_.Parameter_degenerateCasesThreshold_set)
    __swig_setmethods__["seed"] = _adagrad_.Parameter_seed_set
    __swig_getmethods__["seed"] = _adagrad_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_adagrad_.Parameter_seed_get, _adagrad_.Parameter_seed_set)
    __swig_setmethods__["engine"] = _adagrad_.Parameter_engine_set
    __swig_getmethods__["engine"] = _adagrad_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_adagrad_.Parameter_engine_get, _adagrad_.Parameter_engine_set)
Parameter_swigregister = _adagrad_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Input(daal.algorithms.optimization_solver.iterative_solver.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _adagrad_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _adagrad_.Input_set(self, id, ptr)

    def get(self, id):
        return _adagrad_.Input_get(self, id)

    def getOptionalData(self, id):
        return _adagrad_.Input_getOptionalData(self, id)

    def setOptionalData(self, id, ptr):
        return _adagrad_.Input_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _adagrad_.Input_check(self, par, method)
    __swig_destroy__ = _adagrad_.delete_Input
    __del__ = lambda self: None
Input_swigregister = _adagrad_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.optimization_solver.iterative_solver.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _adagrad_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_adagrad_.Result_serializationTag)

    def getSerializationTag(self):
        return _adagrad_.Result_getSerializationTag(self)

    def __init__(self):
        this = _adagrad_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _adagrad_.Result_set(self, id, ptr)

    def get(self, id):
        return _adagrad_.Result_get(self, id)

    def getOptionalData(self, id):
        return _adagrad_.Result_getOptionalData(self, id)

    def setOptionalData(self, id, ptr):
        return _adagrad_.Result_setOptionalData(self, id, ptr)

    def check(self, input, par, method):
        return _adagrad_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _adagrad_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _adagrad_.Result_allocate_Float32(self, input, par, method)

    __swig_destroy__ = _adagrad_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _adagrad_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _adagrad_.Result_serializationTag()
Result_serializationTag = _adagrad_.Result_serializationTag

class Batch_Float64DefaultDense(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _adagrad_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _adagrad_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_adagrad_.Batch_Float64DefaultDense_input_get, _adagrad_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _adagrad_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _adagrad_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_adagrad_.Batch_Float64DefaultDense_parameter_get, _adagrad_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _adagrad_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _adagrad_.Batch_Float64DefaultDense_getMethod(self)

    def getInput(self):
        return _adagrad_.Batch_Float64DefaultDense_getInput(self)

    def getParameter(self):
        return _adagrad_.Batch_Float64DefaultDense_getParameter(self)

    def createResult(self):
        return _adagrad_.Batch_Float64DefaultDense_createResult(self)

    def clone(self):
        return _adagrad_.Batch_Float64DefaultDense_clone(self)
    __swig_getmethods__["create"] = lambda x: _adagrad_.Batch_Float64DefaultDense_create
    if _newclass:
        create = staticmethod(_adagrad_.Batch_Float64DefaultDense_create)

    def compute(self):
        return _adagrad_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _adagrad_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _adagrad_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

def Batch_Float64DefaultDense_create():
    return _adagrad_.Batch_Float64DefaultDense_create()
Batch_Float64DefaultDense_create = _adagrad_.Batch_Float64DefaultDense_create

class Batch_Float32DefaultDense(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _adagrad_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _adagrad_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_adagrad_.Batch_Float32DefaultDense_input_get, _adagrad_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _adagrad_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _adagrad_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_adagrad_.Batch_Float32DefaultDense_parameter_get, _adagrad_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _adagrad_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _adagrad_.Batch_Float32DefaultDense_getMethod(self)

    def getInput(self):
        return _adagrad_.Batch_Float32DefaultDense_getInput(self)

    def getParameter(self):
        return _adagrad_.Batch_Float32DefaultDense_getParameter(self)

    def createResult(self):
        return _adagrad_.Batch_Float32DefaultDense_createResult(self)

    def clone(self):
        return _adagrad_.Batch_Float32DefaultDense_clone(self)
    __swig_getmethods__["create"] = lambda x: _adagrad_.Batch_Float32DefaultDense_create
    if _newclass:
        create = staticmethod(_adagrad_.Batch_Float32DefaultDense_create)

    def compute(self):
        return _adagrad_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _adagrad_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _adagrad_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

def Batch_Float32DefaultDense_create():
    return _adagrad_.Batch_Float32DefaultDense_create()
Batch_Float32DefaultDense_create = _adagrad_.Batch_Float32DefaultDense_create

from numpy import float64, float32, intc

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


