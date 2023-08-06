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
            fp, pathname, description = imp.find_module('_mse_', [dirname(__file__)])
        except ImportError:
            import _mse_
            return _mse_
        if fp is not None:
            try:
                _mod = imp.load_module('_mse_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _mse_ = swig_import_helper()
    del swig_import_helper
else:
    import _mse_
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


import daal.algorithms.optimization_solver.sum_of_functions
import daal.algorithms.optimization_solver.objective_function
import daal.algorithms.optimization_solver
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_mse_.argument_swigconstant(_mse_)
argument = _mse_.argument

_mse_.data_swigconstant(_mse_)
data = _mse_.data

_mse_.dependentVariables_swigconstant(_mse_)
dependentVariables = _mse_.dependentVariables

_mse_.lastInputId_swigconstant(_mse_)
lastInputId = _mse_.lastInputId

_mse_.optionalArgument_swigconstant(_mse_)
optionalArgument = _mse_.optionalArgument

_mse_.lastOptionalInputId_swigconstant(_mse_)
lastOptionalInputId = _mse_.lastOptionalInputId

_mse_.weights_swigconstant(_mse_)
weights = _mse_.weights

_mse_.gramMatrix_swigconstant(_mse_)
gramMatrix = _mse_.gramMatrix

_mse_.lastOptionalData_swigconstant(_mse_)
lastOptionalData = _mse_.lastOptionalData

_mse_.defaultDense_swigconstant(_mse_)
defaultDense = _mse_.defaultDense
class interface1_Parameter(daal.algorithms.optimization_solver.sum_of_functions.interface1_Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.interface1_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.interface1_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _mse_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _mse_.interface1_Parameter_check(self)
    __swig_destroy__ = _mse_.delete_interface1_Parameter
    __del__ = lambda self: None
interface1_Parameter_swigregister = _mse_.interface1_Parameter_swigregister
interface1_Parameter_swigregister(interface1_Parameter)

class interface1_Input(daal.algorithms.optimization_solver.sum_of_functions.interface1_Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.interface1_Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.interface1_Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _mse_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _mse_.delete_interface1_Input
    __del__ = lambda self: None

    def interface1_setInput(self, id, ptr):
        return _mse_.interface1_Input_interface1_setInput(self, id, ptr)

    def interface1_getInput(self, id):
        return _mse_.interface1_Input_interface1_getInput(self, id)

    def interface1_getOptionalInput(self, id):
        return _mse_.interface1_Input_interface1_getOptionalInput(self, id)

    def interface1_setOptionalInput(self, id, ptr):
        return _mse_.interface1_Input_interface1_setOptionalInput(self, id, ptr)

    def interface1_getOptionalData(self, id):
        return _mse_.interface1_Input_interface1_getOptionalData(self, id)

    def interface1_setOptionalData(self, id, ptr):
        return _mse_.interface1_Input_interface1_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _mse_.interface1_Input_check(self, par, method)
interface1_Input_swigregister = _mse_.interface1_Input_swigregister
interface1_Input_swigregister(interface1_Input)

class Parameter(daal.algorithms.optimization_solver.sum_of_functions.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _mse_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _mse_.Parameter_check(self)
    __swig_destroy__ = _mse_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["interceptFlag"] = _mse_.Parameter_interceptFlag_set
    __swig_getmethods__["interceptFlag"] = _mse_.Parameter_interceptFlag_get
    if _newclass:
        interceptFlag = _swig_property(_mse_.Parameter_interceptFlag_get, _mse_.Parameter_interceptFlag_set)
    __swig_setmethods__["penaltyL1"] = _mse_.Parameter_penaltyL1_set
    __swig_getmethods__["penaltyL1"] = _mse_.Parameter_penaltyL1_get
    if _newclass:
        penaltyL1 = _swig_property(_mse_.Parameter_penaltyL1_get, _mse_.Parameter_penaltyL1_set)
    __swig_setmethods__["penaltyL2"] = _mse_.Parameter_penaltyL2_set
    __swig_getmethods__["penaltyL2"] = _mse_.Parameter_penaltyL2_get
    if _newclass:
        penaltyL2 = _swig_property(_mse_.Parameter_penaltyL2_get, _mse_.Parameter_penaltyL2_set)
Parameter_swigregister = _mse_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Input(daal.algorithms.optimization_solver.sum_of_functions.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _mse_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _mse_.delete_Input
    __del__ = lambda self: None

    def setInput(self, id, ptr):
        return _mse_.Input_setInput(self, id, ptr)

    def getInput(self, id):
        return _mse_.Input_getInput(self, id)

    def getOptionalInput(self, id):
        return _mse_.Input_getOptionalInput(self, id)

    def setOptionalInput(self, id, ptr):
        return _mse_.Input_setOptionalInput(self, id, ptr)

    def getOptionalData(self, id):
        return _mse_.Input_getOptionalData(self, id)

    def setOptionalData(self, id, ptr):
        return _mse_.Input_setOptionalData(self, id, ptr)

    def check(self, par, method):
        return _mse_.Input_check(self, par, method)
Input_swigregister = _mse_.Input_swigregister
Input_swigregister(Input)

class Batch_Float64DefaultDense(daal.algorithms.optimization_solver.sum_of_functions.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _mse_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def __init__(self, *args):
        this = _mse_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def parameter(self, *args):
        return _mse_.Batch_Float64DefaultDense_parameter(self, *args)

    def getMethod(self):
        return _mse_.Batch_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _mse_.Batch_Float64DefaultDense_clone(self)

    def allocate(self):
        return _mse_.Batch_Float64DefaultDense_allocate(self)
    __swig_setmethods__["input"] = _mse_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _mse_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_mse_.Batch_Float64DefaultDense_input_get, _mse_.Batch_Float64DefaultDense_input_set)

    def compute(self):
        return _mse_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _mse_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.optimization_solver.sum_of_functions.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.sum_of_functions.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _mse_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def __init__(self, *args):
        this = _mse_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def parameter(self, *args):
        return _mse_.Batch_Float32DefaultDense_parameter(self, *args)

    def getMethod(self):
        return _mse_.Batch_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _mse_.Batch_Float32DefaultDense_clone(self)

    def allocate(self):
        return _mse_.Batch_Float32DefaultDense_allocate(self)
    __swig_setmethods__["input"] = _mse_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _mse_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_mse_.Batch_Float32DefaultDense_input_get, _mse_.Batch_Float32DefaultDense_input_set)

    def compute(self):
        return _mse_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _mse_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

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


