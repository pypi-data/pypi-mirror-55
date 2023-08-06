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
            fp, pathname, description = imp.find_module('_objective_function_', [dirname(__file__)])
        except ImportError:
            import _objective_function_
            return _objective_function_
        if fp is not None:
            try:
                _mod = imp.load_module('_objective_function_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _objective_function_ = swig_import_helper()
    del swig_import_helper
else:
    import _objective_function_
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

_objective_function_.argument_swigconstant(_objective_function_)
argument = _objective_function_.argument

_objective_function_.lastInputId_swigconstant(_objective_function_)
lastInputId = _objective_function_.lastInputId

_objective_function_.gradient_swigconstant(_objective_function_)
gradient = _objective_function_.gradient

_objective_function_.value_swigconstant(_objective_function_)
value = _objective_function_.value

_objective_function_.hessian_swigconstant(_objective_function_)
hessian = _objective_function_.hessian

_objective_function_.nonSmoothTermValue_swigconstant(_objective_function_)
nonSmoothTermValue = _objective_function_.nonSmoothTermValue

_objective_function_.proximalProjection_swigconstant(_objective_function_)
proximalProjection = _objective_function_.proximalProjection

_objective_function_.lipschitzConstant_swigconstant(_objective_function_)
lipschitzConstant = _objective_function_.lipschitzConstant

_objective_function_.componentOfGradient_swigconstant(_objective_function_)
componentOfGradient = _objective_function_.componentOfGradient

_objective_function_.componentOfHessianDiagonal_swigconstant(_objective_function_)
componentOfHessianDiagonal = _objective_function_.componentOfHessianDiagonal

_objective_function_.componentOfProximalProjection_swigconstant(_objective_function_)
componentOfProximalProjection = _objective_function_.componentOfProximalProjection

_objective_function_.gradientIdx_swigconstant(_objective_function_)
gradientIdx = _objective_function_.gradientIdx

_objective_function_.valueIdx_swigconstant(_objective_function_)
valueIdx = _objective_function_.valueIdx

_objective_function_.hessianIdx_swigconstant(_objective_function_)
hessianIdx = _objective_function_.hessianIdx

_objective_function_.nonSmoothTermValueIdx_swigconstant(_objective_function_)
nonSmoothTermValueIdx = _objective_function_.nonSmoothTermValueIdx

_objective_function_.proximalProjectionIdx_swigconstant(_objective_function_)
proximalProjectionIdx = _objective_function_.proximalProjectionIdx

_objective_function_.lipschitzConstantIdx_swigconstant(_objective_function_)
lipschitzConstantIdx = _objective_function_.lipschitzConstantIdx

_objective_function_.componentOfGradientIdx_swigconstant(_objective_function_)
componentOfGradientIdx = _objective_function_.componentOfGradientIdx

_objective_function_.componentOfHessianDiagonalIdx_swigconstant(_objective_function_)
componentOfHessianDiagonalIdx = _objective_function_.componentOfHessianDiagonalIdx

_objective_function_.componentOfProximalProjectionIdx_swigconstant(_objective_function_)
componentOfProximalProjectionIdx = _objective_function_.componentOfProximalProjectionIdx

_objective_function_.lastResultId_swigconstant(_objective_function_)
lastResultId = _objective_function_.lastResultId
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
        this = _objective_function_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _objective_function_.delete_Parameter
    __del__ = lambda self: None
    __swig_setmethods__["resultsToCompute"] = _objective_function_.Parameter_resultsToCompute_set
    __swig_getmethods__["resultsToCompute"] = _objective_function_.Parameter_resultsToCompute_get
    if _newclass:
        resultsToCompute = _swig_property(_objective_function_.Parameter_resultsToCompute_get, _objective_function_.Parameter_resultsToCompute_set)
Parameter_swigregister = _objective_function_.Parameter_swigregister
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
        this = _objective_function_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _objective_function_.delete_Input
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _objective_function_.Input_set(self, id, ptr)

    def get(self, id):
        return _objective_function_.Input_get(self, id)

    def check(self, par, method):
        return _objective_function_.Input_check(self, par, method)
Input_swigregister = _objective_function_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _objective_function_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_objective_function_.Result_serializationTag)

    def getSerializationTag(self):
        return _objective_function_.Result_getSerializationTag(self)

    def __init__(self):
        this = _objective_function_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _objective_function_.delete_Result
    __del__ = lambda self: None

    def set(self, id, ptr):
        return _objective_function_.Result_set(self, id, ptr)

    def get(self, id):
        return _objective_function_.Result_get(self, id)

    def check(self, input, par, method):
        return _objective_function_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _objective_function_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _objective_function_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _objective_function_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _objective_function_.Result_serializationTag()
Result_serializationTag = _objective_function_.Result_serializationTag

class Batch(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _objective_function_.delete_Batch
    __del__ = lambda self: None

    def getResult(self):
        return _objective_function_.Batch_getResult(self)

    def setResult(self, result):
        return _objective_function_.Batch_setResult(self, result)

    def clone(self):
        return _objective_function_.Batch_clone(self)

    def compute(self):
        return _objective_function_.Batch_compute(self)
Batch_swigregister = _objective_function_.Batch_swigregister
Batch_swigregister(Batch)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


