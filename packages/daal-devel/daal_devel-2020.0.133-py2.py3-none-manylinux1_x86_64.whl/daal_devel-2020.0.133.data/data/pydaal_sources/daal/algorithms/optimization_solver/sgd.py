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
            fp, pathname, description = imp.find_module('_sgd_', [dirname(__file__)])
        except ImportError:
            import _sgd_
            return _sgd_
        if fp is not None:
            try:
                _mod = imp.load_module('_sgd_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _sgd_ = swig_import_helper()
    del swig_import_helper
else:
    import _sgd_
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

_sgd_.defaultDense_swigconstant(_sgd_)
defaultDense = _sgd_.defaultDense

_sgd_.miniBatch_swigconstant(_sgd_)
miniBatch = _sgd_.miniBatch

_sgd_.momentum_swigconstant(_sgd_)
momentum = _sgd_.momentum

_sgd_.pastUpdateVector_swigconstant(_sgd_)
pastUpdateVector = _sgd_.pastUpdateVector

_sgd_.pastWorkValue_swigconstant(_sgd_)
pastWorkValue = _sgd_.pastWorkValue

_sgd_.lastOptionalData_swigconstant(_sgd_)
lastOptionalData = _sgd_.lastOptionalData
class interface1_BaseParameter(daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_BaseParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.interface1_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_BaseParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sgd_.new_interface1_BaseParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _sgd_.delete_interface1_BaseParameter
    __del__ = lambda self: None

    def check(self):
        return _sgd_.interface1_BaseParameter_check(self)
    __swig_setmethods__["batchIndices"] = _sgd_.interface1_BaseParameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _sgd_.interface1_BaseParameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_sgd_.interface1_BaseParameter_batchIndices_get, _sgd_.interface1_BaseParameter_batchIndices_set)
    __swig_setmethods__["learningRateSequence"] = _sgd_.interface1_BaseParameter_learningRateSequence_set
    __swig_getmethods__["learningRateSequence"] = _sgd_.interface1_BaseParameter_learningRateSequence_get
    if _newclass:
        learningRateSequence = _swig_property(_sgd_.interface1_BaseParameter_learningRateSequence_get, _sgd_.interface1_BaseParameter_learningRateSequence_set)
    __swig_setmethods__["seed"] = _sgd_.interface1_BaseParameter_seed_set
    __swig_getmethods__["seed"] = _sgd_.interface1_BaseParameter_seed_get
    if _newclass:
        seed = _swig_property(_sgd_.interface1_BaseParameter_seed_get, _sgd_.interface1_BaseParameter_seed_set)
    __swig_setmethods__["engine"] = _sgd_.interface1_BaseParameter_engine_set
    __swig_getmethods__["engine"] = _sgd_.interface1_BaseParameter_engine_get
    if _newclass:
        engine = _swig_property(_sgd_.interface1_BaseParameter_engine_get, _sgd_.interface1_BaseParameter_engine_set)
interface1_BaseParameter_swigregister = _sgd_.interface1_BaseParameter_swigregister
interface1_BaseParameter_swigregister(interface1_BaseParameter)

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
        this = _sgd_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _sgd_.interface1_Input_set(self, id, ptr)

    def get(self, id):
        return _sgd_.interface1_Input_get(self, id)

    def interface1_getOptionalData(self, id):
        return _sgd_.interface1_Input_interface1_getOptionalData(self, id)

    def interface1_setOptionalData(self, id, ptr):
        return _sgd_.interface1_Input_interface1_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _sgd_.interface1_Input_check(self, par, method)
    __swig_destroy__ = _sgd_.delete_interface1_Input
    __del__ = lambda self: None
interface1_Input_swigregister = _sgd_.interface1_Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _sgd_.interface1_Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_sgd_.interface1_Result_serializationTag)

    def getSerializationTag(self):
        return _sgd_.interface1_Result_getSerializationTag(self)

    def __init__(self):
        this = _sgd_.new_interface1_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _sgd_.interface1_Result_set(self, id, ptr)

    def get(self, id):
        return _sgd_.interface1_Result_get(self, id)

    def interface1_getOptionalData(self, id):
        return _sgd_.interface1_Result_interface1_getOptionalData(self, id)

    def interface1_setOptionalData(self, id, ptr):
        return _sgd_.interface1_Result_interface1_setOptionalData(self, id, ptr)

    def check(self, input, par, method):
        return _sgd_.interface1_Result_check(self, input, par, method)
    __swig_destroy__ = _sgd_.delete_interface1_Result
    __del__ = lambda self: None
interface1_Result_swigregister = _sgd_.interface1_Result_swigregister
interface1_Result_swigregister(interface1_Result)

def interface1_Result_serializationTag():
    return _sgd_.interface1_Result_serializationTag()
interface1_Result_serializationTag = _sgd_.interface1_Result_serializationTag

class BaseParameter(daal.algorithms.optimization_solver.iterative_solver.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BaseParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BaseParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sgd_.new_BaseParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _sgd_.delete_BaseParameter
    __del__ = lambda self: None

    def check(self):
        return _sgd_.BaseParameter_check(self)
    __swig_setmethods__["batchIndices"] = _sgd_.BaseParameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _sgd_.BaseParameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_sgd_.BaseParameter_batchIndices_get, _sgd_.BaseParameter_batchIndices_set)
    __swig_setmethods__["learningRateSequence"] = _sgd_.BaseParameter_learningRateSequence_set
    __swig_getmethods__["learningRateSequence"] = _sgd_.BaseParameter_learningRateSequence_get
    if _newclass:
        learningRateSequence = _swig_property(_sgd_.BaseParameter_learningRateSequence_get, _sgd_.BaseParameter_learningRateSequence_set)
    __swig_setmethods__["seed"] = _sgd_.BaseParameter_seed_set
    __swig_getmethods__["seed"] = _sgd_.BaseParameter_seed_get
    if _newclass:
        seed = _swig_property(_sgd_.BaseParameter_seed_get, _sgd_.BaseParameter_seed_set)
    __swig_setmethods__["engine"] = _sgd_.BaseParameter_engine_set
    __swig_getmethods__["engine"] = _sgd_.BaseParameter_engine_get
    if _newclass:
        engine = _swig_property(_sgd_.BaseParameter_engine_get, _sgd_.BaseParameter_engine_set)
BaseParameter_swigregister = _sgd_.BaseParameter_swigregister
BaseParameter_swigregister(BaseParameter)

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
        this = _sgd_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _sgd_.Input_set(self, id, ptr)

    def get(self, id):
        return _sgd_.Input_get(self, id)

    def getOptionalData(self, id):
        return _sgd_.Input_getOptionalData(self, id)

    def setOptionalData(self, id, ptr):
        return _sgd_.Input_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _sgd_.Input_check(self, par, method)
    __swig_destroy__ = _sgd_.delete_Input
    __del__ = lambda self: None
Input_swigregister = _sgd_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _sgd_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_sgd_.Result_serializationTag)

    def getSerializationTag(self):
        return _sgd_.Result_getSerializationTag(self)

    def __init__(self):
        this = _sgd_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _sgd_.Result_set(self, id, ptr)

    def get(self, id):
        return _sgd_.Result_get(self, id)

    def getOptionalData(self, id):
        return _sgd_.Result_getOptionalData(self, id)

    def setOptionalData(self, id, ptr):
        return _sgd_.Result_setOptionalData(self, id, ptr)

    def check(self, input, par, method):
        return _sgd_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _sgd_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _sgd_.Result_allocate_Float32(self, input, par, method)

    __swig_destroy__ = _sgd_.delete_Result
    __del__ = lambda self: None
Result_swigregister = _sgd_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _sgd_.Result_serializationTag()
Result_serializationTag = _sgd_.Result_serializationTag

class Parameter_DefaultDense(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sgd_.new_Parameter_DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _sgd_.Parameter_DefaultDense_check(self)
    __swig_destroy__ = _sgd_.delete_Parameter_DefaultDense
    __del__ = lambda self: None
Parameter_DefaultDense_swigregister = _sgd_.Parameter_DefaultDense_swigregister
Parameter_DefaultDense_swigregister(Parameter_DefaultDense)

class Parameter_MiniBatch(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_MiniBatch, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_MiniBatch, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sgd_.new_Parameter_MiniBatch(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _sgd_.Parameter_MiniBatch_check(self)
    __swig_destroy__ = _sgd_.delete_Parameter_MiniBatch
    __del__ = lambda self: None
    __swig_setmethods__["conservativeSequence"] = _sgd_.Parameter_MiniBatch_conservativeSequence_set
    __swig_getmethods__["conservativeSequence"] = _sgd_.Parameter_MiniBatch_conservativeSequence_get
    if _newclass:
        conservativeSequence = _swig_property(_sgd_.Parameter_MiniBatch_conservativeSequence_get, _sgd_.Parameter_MiniBatch_conservativeSequence_set)
    __swig_setmethods__["innerNIterations"] = _sgd_.Parameter_MiniBatch_innerNIterations_set
    __swig_getmethods__["innerNIterations"] = _sgd_.Parameter_MiniBatch_innerNIterations_get
    if _newclass:
        innerNIterations = _swig_property(_sgd_.Parameter_MiniBatch_innerNIterations_get, _sgd_.Parameter_MiniBatch_innerNIterations_set)
Parameter_MiniBatch_swigregister = _sgd_.Parameter_MiniBatch_swigregister
Parameter_MiniBatch_swigregister(Parameter_MiniBatch)

class Parameter_Momentum(BaseParameter):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Momentum, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Momentum, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sgd_.new_Parameter_Momentum(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _sgd_.Parameter_Momentum_check(self)
    __swig_destroy__ = _sgd_.delete_Parameter_Momentum
    __del__ = lambda self: None
    __swig_setmethods__["momentum"] = _sgd_.Parameter_Momentum_momentum_set
    __swig_getmethods__["momentum"] = _sgd_.Parameter_Momentum_momentum_get
    if _newclass:
        momentum = _swig_property(_sgd_.Parameter_Momentum_momentum_get, _sgd_.Parameter_Momentum_momentum_set)
Parameter_Momentum_swigregister = _sgd_.Parameter_Momentum_swigregister
Parameter_Momentum_swigregister(Parameter_Momentum)

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
    __swig_setmethods__["input"] = _sgd_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float64DefaultDense_input_get, _sgd_.Batch_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float64DefaultDense_parameter_get, _sgd_.Batch_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float64DefaultDense_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float64DefaultDense_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float64DefaultDense_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float64DefaultDense_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float64DefaultDense_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float64DefaultDense_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float64DefaultDense_create)

    def compute(self):
        return _sgd_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _sgd_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

def Batch_Float64DefaultDense_create():
    return _sgd_.Batch_Float64DefaultDense_create()
Batch_Float64DefaultDense_create = _sgd_.Batch_Float64DefaultDense_create

class Batch_Float64MiniBatch(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64MiniBatch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64MiniBatch, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _sgd_.Batch_Float64MiniBatch_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float64MiniBatch_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float64MiniBatch_input_get, _sgd_.Batch_Float64MiniBatch_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float64MiniBatch_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float64MiniBatch_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float64MiniBatch_parameter_get, _sgd_.Batch_Float64MiniBatch_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float64MiniBatch(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float64MiniBatch_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float64MiniBatch_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float64MiniBatch_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float64MiniBatch_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float64MiniBatch_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float64MiniBatch_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float64MiniBatch_create)

    def compute(self):
        return _sgd_.Batch_Float64MiniBatch_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float64MiniBatch
    __del__ = lambda self: None
Batch_Float64MiniBatch_swigregister = _sgd_.Batch_Float64MiniBatch_swigregister
Batch_Float64MiniBatch_swigregister(Batch_Float64MiniBatch)

def Batch_Float64MiniBatch_create():
    return _sgd_.Batch_Float64MiniBatch_create()
Batch_Float64MiniBatch_create = _sgd_.Batch_Float64MiniBatch_create

class Batch_Float64Momentum(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Momentum, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Momentum, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _sgd_.Batch_Float64Momentum_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float64Momentum_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float64Momentum_input_get, _sgd_.Batch_Float64Momentum_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float64Momentum_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float64Momentum_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float64Momentum_parameter_get, _sgd_.Batch_Float64Momentum_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float64Momentum(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float64Momentum_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float64Momentum_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float64Momentum_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float64Momentum_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float64Momentum_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float64Momentum_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float64Momentum_create)

    def compute(self):
        return _sgd_.Batch_Float64Momentum_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float64Momentum
    __del__ = lambda self: None
Batch_Float64Momentum_swigregister = _sgd_.Batch_Float64Momentum_swigregister
Batch_Float64Momentum_swigregister(Batch_Float64Momentum)

def Batch_Float64Momentum_create():
    return _sgd_.Batch_Float64Momentum_create()
Batch_Float64Momentum_create = _sgd_.Batch_Float64Momentum_create

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
    __swig_setmethods__["input"] = _sgd_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float32DefaultDense_input_get, _sgd_.Batch_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float32DefaultDense_parameter_get, _sgd_.Batch_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float32DefaultDense_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float32DefaultDense_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float32DefaultDense_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float32DefaultDense_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float32DefaultDense_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float32DefaultDense_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float32DefaultDense_create)

    def compute(self):
        return _sgd_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _sgd_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

def Batch_Float32DefaultDense_create():
    return _sgd_.Batch_Float32DefaultDense_create()
Batch_Float32DefaultDense_create = _sgd_.Batch_Float32DefaultDense_create

class Batch_Float32MiniBatch(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32MiniBatch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32MiniBatch, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _sgd_.Batch_Float32MiniBatch_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float32MiniBatch_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float32MiniBatch_input_get, _sgd_.Batch_Float32MiniBatch_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float32MiniBatch_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float32MiniBatch_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float32MiniBatch_parameter_get, _sgd_.Batch_Float32MiniBatch_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float32MiniBatch(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float32MiniBatch_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float32MiniBatch_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float32MiniBatch_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float32MiniBatch_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float32MiniBatch_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float32MiniBatch_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float32MiniBatch_create)

    def compute(self):
        return _sgd_.Batch_Float32MiniBatch_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float32MiniBatch
    __del__ = lambda self: None
Batch_Float32MiniBatch_swigregister = _sgd_.Batch_Float32MiniBatch_swigregister
Batch_Float32MiniBatch_swigregister(Batch_Float32MiniBatch)

def Batch_Float32MiniBatch_create():
    return _sgd_.Batch_Float32MiniBatch_create()
Batch_Float32MiniBatch_create = _sgd_.Batch_Float32MiniBatch_create

class Batch_Float32Momentum(daal.algorithms.optimization_solver.iterative_solver.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Momentum, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.iterative_solver.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Momentum, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _sgd_.Batch_Float32Momentum_input_set
    __swig_getmethods__["input"] = _sgd_.Batch_Float32Momentum_input_get
    if _newclass:
        input = _swig_property(_sgd_.Batch_Float32Momentum_input_get, _sgd_.Batch_Float32Momentum_input_set)
    __swig_setmethods__["parameter"] = _sgd_.Batch_Float32Momentum_parameter_set
    __swig_getmethods__["parameter"] = _sgd_.Batch_Float32Momentum_parameter_get
    if _newclass:
        parameter = _swig_property(_sgd_.Batch_Float32Momentum_parameter_get, _sgd_.Batch_Float32Momentum_parameter_set)

    def __init__(self, *args):
        this = _sgd_.new_Batch_Float32Momentum(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _sgd_.Batch_Float32Momentum_getMethod(self)

    def getInput(self):
        return _sgd_.Batch_Float32Momentum_getInput(self)

    def getParameter(self):
        return _sgd_.Batch_Float32Momentum_getParameter(self)

    def createResult(self):
        return _sgd_.Batch_Float32Momentum_createResult(self)

    def clone(self):
        return _sgd_.Batch_Float32Momentum_clone(self)
    __swig_getmethods__["create"] = lambda x: _sgd_.Batch_Float32Momentum_create
    if _newclass:
        create = staticmethod(_sgd_.Batch_Float32Momentum_create)

    def compute(self):
        return _sgd_.Batch_Float32Momentum_compute(self)
    __swig_destroy__ = _sgd_.delete_Batch_Float32Momentum
    __del__ = lambda self: None
Batch_Float32Momentum_swigregister = _sgd_.Batch_Float32Momentum_swigregister
Batch_Float32Momentum_swigregister(Batch_Float32Momentum)

def Batch_Float32Momentum_create():
    return _sgd_.Batch_Float32Momentum_create()
Batch_Float32Momentum_create = _sgd_.Batch_Float32Momentum_create

from numpy import float64, float32, intc

class Parameter(object):
    r"""Factory class for different types of Parameter."""
    def __new__(cls,
                method,
                *args, **kwargs):
        if method == defaultDense:
            return Parameter_DefaultDense(*args)
        if method == miniBatch:
            return Parameter_MiniBatch(*args)
        if method == momentum:
            return Parameter_Momentum(*args)

        raise RuntimeError("No appropriate constructor found for Parameter")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == miniBatch:
                return Batch_Float64MiniBatch(*args)
            if 'method' in kwargs and kwargs['method'] == momentum:
                return Batch_Float64Momentum(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == miniBatch:
                return Batch_Float32MiniBatch(*args)
            if 'method' in kwargs and kwargs['method'] == momentum:
                return Batch_Float32Momentum(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


