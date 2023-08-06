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
            fp, pathname, description = imp.find_module('_cross_entropy_loss_', [dirname(__file__)])
        except ImportError:
            import _cross_entropy_loss_
            return _cross_entropy_loss_
        if fp is not None:
            try:
                _mod = imp.load_module('_cross_entropy_loss_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _cross_entropy_loss_ = swig_import_helper()
    del swig_import_helper
else:
    import _cross_entropy_loss_
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

_cross_entropy_loss_.argument_swigconstant(_cross_entropy_loss_)
argument = _cross_entropy_loss_.argument

_cross_entropy_loss_.data_swigconstant(_cross_entropy_loss_)
data = _cross_entropy_loss_.data

_cross_entropy_loss_.dependentVariables_swigconstant(_cross_entropy_loss_)
dependentVariables = _cross_entropy_loss_.dependentVariables

_cross_entropy_loss_.lastInputId_swigconstant(_cross_entropy_loss_)
lastInputId = _cross_entropy_loss_.lastInputId

_cross_entropy_loss_.defaultDense_swigconstant(_cross_entropy_loss_)
defaultDense = _cross_entropy_loss_.defaultDense
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
        this = _cross_entropy_loss_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _cross_entropy_loss_.interface1_Parameter_check(self)
    __swig_destroy__ = _cross_entropy_loss_.delete_interface1_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["interceptFlag"] = _cross_entropy_loss_.interface1_Parameter_interceptFlag_set
    __swig_getmethods__["interceptFlag"] = _cross_entropy_loss_.interface1_Parameter_interceptFlag_get
    if _newclass:
        interceptFlag = _swig_property(_cross_entropy_loss_.interface1_Parameter_interceptFlag_get, _cross_entropy_loss_.interface1_Parameter_interceptFlag_set)
    __swig_setmethods__["penaltyL1"] = _cross_entropy_loss_.interface1_Parameter_penaltyL1_set
    __swig_getmethods__["penaltyL1"] = _cross_entropy_loss_.interface1_Parameter_penaltyL1_get
    if _newclass:
        penaltyL1 = _swig_property(_cross_entropy_loss_.interface1_Parameter_penaltyL1_get, _cross_entropy_loss_.interface1_Parameter_penaltyL1_set)
    __swig_setmethods__["penaltyL2"] = _cross_entropy_loss_.interface1_Parameter_penaltyL2_set
    __swig_getmethods__["penaltyL2"] = _cross_entropy_loss_.interface1_Parameter_penaltyL2_get
    if _newclass:
        penaltyL2 = _swig_property(_cross_entropy_loss_.interface1_Parameter_penaltyL2_get, _cross_entropy_loss_.interface1_Parameter_penaltyL2_set)
    __swig_setmethods__["nClasses"] = _cross_entropy_loss_.interface1_Parameter_nClasses_set
    __swig_getmethods__["nClasses"] = _cross_entropy_loss_.interface1_Parameter_nClasses_get
    if _newclass:
        nClasses = _swig_property(_cross_entropy_loss_.interface1_Parameter_nClasses_get, _cross_entropy_loss_.interface1_Parameter_nClasses_set)
interface1_Parameter_swigregister = _cross_entropy_loss_.interface1_Parameter_swigregister
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
        this = _cross_entropy_loss_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _cross_entropy_loss_.delete_interface1_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _cross_entropy_loss_.interface1_Input_set(self, id, ptr)

    def get(self, id):
        return _cross_entropy_loss_.interface1_Input_get(self, id)

    def check(self, par, method):
        return _cross_entropy_loss_.interface1_Input_check(self, par, method)
interface1_Input_swigregister = _cross_entropy_loss_.interface1_Input_swigregister
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
        this = _cross_entropy_loss_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _cross_entropy_loss_.Parameter_check(self)
    __swig_destroy__ = _cross_entropy_loss_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["interceptFlag"] = _cross_entropy_loss_.Parameter_interceptFlag_set
    __swig_getmethods__["interceptFlag"] = _cross_entropy_loss_.Parameter_interceptFlag_get
    if _newclass:
        interceptFlag = _swig_property(_cross_entropy_loss_.Parameter_interceptFlag_get, _cross_entropy_loss_.Parameter_interceptFlag_set)
    __swig_setmethods__["penaltyL1"] = _cross_entropy_loss_.Parameter_penaltyL1_set
    __swig_getmethods__["penaltyL1"] = _cross_entropy_loss_.Parameter_penaltyL1_get
    if _newclass:
        penaltyL1 = _swig_property(_cross_entropy_loss_.Parameter_penaltyL1_get, _cross_entropy_loss_.Parameter_penaltyL1_set)
    __swig_setmethods__["penaltyL2"] = _cross_entropy_loss_.Parameter_penaltyL2_set
    __swig_getmethods__["penaltyL2"] = _cross_entropy_loss_.Parameter_penaltyL2_get
    if _newclass:
        penaltyL2 = _swig_property(_cross_entropy_loss_.Parameter_penaltyL2_get, _cross_entropy_loss_.Parameter_penaltyL2_set)
    __swig_setmethods__["nClasses"] = _cross_entropy_loss_.Parameter_nClasses_set
    __swig_getmethods__["nClasses"] = _cross_entropy_loss_.Parameter_nClasses_get
    if _newclass:
        nClasses = _swig_property(_cross_entropy_loss_.Parameter_nClasses_get, _cross_entropy_loss_.Parameter_nClasses_set)
Parameter_swigregister = _cross_entropy_loss_.Parameter_swigregister
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
        this = _cross_entropy_loss_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _cross_entropy_loss_.delete_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _cross_entropy_loss_.Input_set(self, id, ptr)

    def get(self, id):
        return _cross_entropy_loss_.Input_get(self, id)

    def check(self, par, method):
        return _cross_entropy_loss_.Input_check(self, par, method)
Input_swigregister = _cross_entropy_loss_.Input_swigregister
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
    __swig_destroy__ = _cross_entropy_loss_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def __init__(self, *args):
        this = _cross_entropy_loss_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _cross_entropy_loss_.Batch_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _cross_entropy_loss_.Batch_Float64DefaultDense_clone(self)

    def allocate(self):
        return _cross_entropy_loss_.Batch_Float64DefaultDense_allocate(self)

    def parameter(self, *args):
        return _cross_entropy_loss_.Batch_Float64DefaultDense_parameter(self, *args)
    __swig_getmethods__["create"] = lambda x: _cross_entropy_loss_.Batch_Float64DefaultDense_create
    if _newclass:
        create = staticmethod(_cross_entropy_loss_.Batch_Float64DefaultDense_create)
    __swig_setmethods__["input"] = _cross_entropy_loss_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _cross_entropy_loss_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_cross_entropy_loss_.Batch_Float64DefaultDense_input_get, _cross_entropy_loss_.Batch_Float64DefaultDense_input_set)

    def compute(self):
        return _cross_entropy_loss_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _cross_entropy_loss_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

def Batch_Float64DefaultDense_create(nClasses, numberOfTerms):
    return _cross_entropy_loss_.Batch_Float64DefaultDense_create(nClasses, numberOfTerms)
Batch_Float64DefaultDense_create = _cross_entropy_loss_.Batch_Float64DefaultDense_create

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
    __swig_destroy__ = _cross_entropy_loss_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def __init__(self, *args):
        this = _cross_entropy_loss_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _cross_entropy_loss_.Batch_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _cross_entropy_loss_.Batch_Float32DefaultDense_clone(self)

    def allocate(self):
        return _cross_entropy_loss_.Batch_Float32DefaultDense_allocate(self)

    def parameter(self, *args):
        return _cross_entropy_loss_.Batch_Float32DefaultDense_parameter(self, *args)
    __swig_getmethods__["create"] = lambda x: _cross_entropy_loss_.Batch_Float32DefaultDense_create
    if _newclass:
        create = staticmethod(_cross_entropy_loss_.Batch_Float32DefaultDense_create)
    __swig_setmethods__["input"] = _cross_entropy_loss_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _cross_entropy_loss_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_cross_entropy_loss_.Batch_Float32DefaultDense_input_get, _cross_entropy_loss_.Batch_Float32DefaultDense_input_set)

    def compute(self):
        return _cross_entropy_loss_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _cross_entropy_loss_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

def Batch_Float32DefaultDense_create(nClasses, numberOfTerms):
    return _cross_entropy_loss_.Batch_Float32DefaultDense_create(nClasses, numberOfTerms)
Batch_Float32DefaultDense_create = _cross_entropy_loss_.Batch_Float32DefaultDense_create

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


