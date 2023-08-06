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
            fp, pathname, description = imp.find_module('_sum_of_functions_', [dirname(__file__)])
        except ImportError:
            import _sum_of_functions_
            return _sum_of_functions_
        if fp is not None:
            try:
                _mod = imp.load_module('_sum_of_functions_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _sum_of_functions_ = swig_import_helper()
    del swig_import_helper
else:
    import _sum_of_functions_
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


import daal.algorithms.optimization_solver.objective_function
import daal.algorithms.optimization_solver
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_sum_of_functions_.argument_swigconstant(_sum_of_functions_)
argument = _sum_of_functions_.argument
class interface1_Parameter(daal.algorithms.optimization_solver.objective_function.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sum_of_functions_.new_interface1_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _sum_of_functions_.interface1_Parameter_check(self)
    __swig_destroy__ = _sum_of_functions_.delete_interface1_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["numberOfTerms"] = _sum_of_functions_.interface1_Parameter_numberOfTerms_set
    __swig_getmethods__["numberOfTerms"] = _sum_of_functions_.interface1_Parameter_numberOfTerms_get
    if _newclass:
        numberOfTerms = _swig_property(_sum_of_functions_.interface1_Parameter_numberOfTerms_get, _sum_of_functions_.interface1_Parameter_numberOfTerms_set)
    __swig_setmethods__["batchIndices"] = _sum_of_functions_.interface1_Parameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _sum_of_functions_.interface1_Parameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_sum_of_functions_.interface1_Parameter_batchIndices_get, _sum_of_functions_.interface1_Parameter_batchIndices_set)
interface1_Parameter_swigregister = _sum_of_functions_.interface1_Parameter_swigregister
interface1_Parameter_swigregister(interface1_Parameter)

class interface1_Input(daal.algorithms.optimization_solver.objective_function.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sum_of_functions_.new_interface1_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _sum_of_functions_.delete_interface1_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _sum_of_functions_.interface1_Input_set(self, id, ptr)

    def get(self, id):
        return _sum_of_functions_.interface1_Input_get(self, id)

    def check(self, par, method):
        return _sum_of_functions_.interface1_Input_check(self, par, method)
interface1_Input_swigregister = _sum_of_functions_.interface1_Input_swigregister
interface1_Input_swigregister(interface1_Input)

class Parameter(daal.algorithms.optimization_solver.objective_function.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sum_of_functions_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _sum_of_functions_.Parameter_check(self)
    __swig_destroy__ = _sum_of_functions_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["numberOfTerms"] = _sum_of_functions_.Parameter_numberOfTerms_set
    __swig_getmethods__["numberOfTerms"] = _sum_of_functions_.Parameter_numberOfTerms_get
    if _newclass:
        numberOfTerms = _swig_property(_sum_of_functions_.Parameter_numberOfTerms_get, _sum_of_functions_.Parameter_numberOfTerms_set)
    __swig_setmethods__["batchIndices"] = _sum_of_functions_.Parameter_batchIndices_set
    __swig_getmethods__["batchIndices"] = _sum_of_functions_.Parameter_batchIndices_get
    if _newclass:
        batchIndices = _swig_property(_sum_of_functions_.Parameter_batchIndices_get, _sum_of_functions_.Parameter_batchIndices_set)
    __swig_setmethods__["featureId"] = _sum_of_functions_.Parameter_featureId_set
    __swig_getmethods__["featureId"] = _sum_of_functions_.Parameter_featureId_get
    if _newclass:
        featureId = _swig_property(_sum_of_functions_.Parameter_featureId_get, _sum_of_functions_.Parameter_featureId_set)
Parameter_swigregister = _sum_of_functions_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Input(daal.algorithms.optimization_solver.objective_function.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _sum_of_functions_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _sum_of_functions_.delete_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _sum_of_functions_.Input_set(self, id, ptr)

    def get(self, id):
        return _sum_of_functions_.Input_get(self, id)

    def check(self, par, method):
        return _sum_of_functions_.Input_check(self, par, method)
Input_swigregister = _sum_of_functions_.Input_swigregister
Input_swigregister(Input)

class interface1_Batch(daal.algorithms.optimization_solver.objective_function.Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface1_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface1_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _sum_of_functions_.delete_interface1_Batch
    __del__ = lambda self: None

    def clone(self):
        return _sum_of_functions_.interface1_Batch_clone(self)
    __swig_setmethods__["sumOfFunctionsParameter"] = _sum_of_functions_.interface1_Batch_sumOfFunctionsParameter_set
    __swig_getmethods__["sumOfFunctionsParameter"] = _sum_of_functions_.interface1_Batch_sumOfFunctionsParameter_get
    if _newclass:
        sumOfFunctionsParameter = _swig_property(_sum_of_functions_.interface1_Batch_sumOfFunctionsParameter_get, _sum_of_functions_.interface1_Batch_sumOfFunctionsParameter_set)
    __swig_setmethods__["sumOfFunctionsInput"] = _sum_of_functions_.interface1_Batch_sumOfFunctionsInput_set
    __swig_getmethods__["sumOfFunctionsInput"] = _sum_of_functions_.interface1_Batch_sumOfFunctionsInput_get
    if _newclass:
        sumOfFunctionsInput = _swig_property(_sum_of_functions_.interface1_Batch_sumOfFunctionsInput_get, _sum_of_functions_.interface1_Batch_sumOfFunctionsInput_set)
interface1_Batch_swigregister = _sum_of_functions_.interface1_Batch_swigregister
interface1_Batch_swigregister(interface1_Batch)

class Batch(daal.algorithms.optimization_solver.objective_function.Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.optimization_solver.objective_function.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _sum_of_functions_.delete_Batch
    __del__ = lambda self: None

    def clone(self):
        return _sum_of_functions_.Batch_clone(self)
    __swig_setmethods__["sumOfFunctionsParameter"] = _sum_of_functions_.Batch_sumOfFunctionsParameter_set
    __swig_getmethods__["sumOfFunctionsParameter"] = _sum_of_functions_.Batch_sumOfFunctionsParameter_get
    if _newclass:
        sumOfFunctionsParameter = _swig_property(_sum_of_functions_.Batch_sumOfFunctionsParameter_get, _sum_of_functions_.Batch_sumOfFunctionsParameter_set)
    __swig_setmethods__["sumOfFunctionsInput"] = _sum_of_functions_.Batch_sumOfFunctionsInput_set
    __swig_getmethods__["sumOfFunctionsInput"] = _sum_of_functions_.Batch_sumOfFunctionsInput_get
    if _newclass:
        sumOfFunctionsInput = _swig_property(_sum_of_functions_.Batch_sumOfFunctionsInput_get, _sum_of_functions_.Batch_sumOfFunctionsInput_set)

    def compute(self):
        return _sum_of_functions_.Batch_compute(self)
Batch_swigregister = _sum_of_functions_.Batch_swigregister
Batch_swigregister(Batch)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


