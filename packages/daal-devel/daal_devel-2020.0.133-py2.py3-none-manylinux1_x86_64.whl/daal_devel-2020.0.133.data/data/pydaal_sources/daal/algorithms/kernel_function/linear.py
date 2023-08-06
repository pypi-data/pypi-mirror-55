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
            fp, pathname, description = imp.find_module('_linear_', [dirname(__file__)])
        except ImportError:
            import _linear_
            return _linear_
        if fp is not None:
            try:
                _mod = imp.load_module('_linear_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _linear_ = swig_import_helper()
    del swig_import_helper
else:
    import _linear_
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


import daal.algorithms.kernel_function
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_linear_.defaultDense_swigconstant(_linear_)
defaultDense = _linear_.defaultDense

_linear_.fastCSR_swigconstant(_linear_)
fastCSR = _linear_.fastCSR
class Parameter(daal.algorithms.kernel_function.ParameterBase):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, k=1.0, b=0.0):
        this = _linear_.new_Parameter(k, b)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["k"] = _linear_.Parameter_k_set
    __swig_getmethods__["k"] = _linear_.Parameter_k_get
    if _newclass:
        k = _swig_property(_linear_.Parameter_k_get, _linear_.Parameter_k_set)
    __swig_setmethods__["b"] = _linear_.Parameter_b_set
    __swig_getmethods__["b"] = _linear_.Parameter_b_get
    if _newclass:
        b = _swig_property(_linear_.Parameter_b_get, _linear_.Parameter_b_set)
    __swig_destroy__ = _linear_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _linear_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Input(daal.algorithms.kernel_function.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _linear_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _linear_.delete_Input
    __del__ = lambda self: None

    def check(self, par, method):
        return _linear_.Input_check(self, par, method)
Input_swigregister = _linear_.Input_swigregister
Input_swigregister(Input)

class Batch_Float64DefaultDense(daal.algorithms.kernel_function.KernelIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _linear_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _linear_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_linear_.Batch_Float64DefaultDense_parameter_get, _linear_.Batch_Float64DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _linear_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _linear_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_linear_.Batch_Float64DefaultDense_input_get, _linear_.Batch_Float64DefaultDense_input_set)

    def __init__(self, *args):
        this = _linear_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _linear_.Batch_Float64DefaultDense_getMethod(self)

    def getInput(self):
        return _linear_.Batch_Float64DefaultDense_getInput(self)

    def getParameter(self):
        return _linear_.Batch_Float64DefaultDense_getParameter(self)

    def clone(self):
        return _linear_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _linear_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _linear_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _linear_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float64FastCSR(daal.algorithms.kernel_function.KernelIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _linear_.Batch_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _linear_.Batch_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_linear_.Batch_Float64FastCSR_parameter_get, _linear_.Batch_Float64FastCSR_parameter_set)
    __swig_setmethods__["input"] = _linear_.Batch_Float64FastCSR_input_set
    __swig_getmethods__["input"] = _linear_.Batch_Float64FastCSR_input_get
    if _newclass:
        input = _swig_property(_linear_.Batch_Float64FastCSR_input_get, _linear_.Batch_Float64FastCSR_input_set)

    def __init__(self, *args):
        this = _linear_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _linear_.Batch_Float64FastCSR_getMethod(self)

    def getInput(self):
        return _linear_.Batch_Float64FastCSR_getInput(self)

    def getParameter(self):
        return _linear_.Batch_Float64FastCSR_getParameter(self)

    def clone(self):
        return _linear_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _linear_.Batch_Float64FastCSR_compute(self)
    __swig_destroy__ = _linear_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None
Batch_Float64FastCSR_swigregister = _linear_.Batch_Float64FastCSR_swigregister
Batch_Float64FastCSR_swigregister(Batch_Float64FastCSR)

class Batch_Float32DefaultDense(daal.algorithms.kernel_function.KernelIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _linear_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _linear_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_linear_.Batch_Float32DefaultDense_parameter_get, _linear_.Batch_Float32DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _linear_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _linear_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_linear_.Batch_Float32DefaultDense_input_get, _linear_.Batch_Float32DefaultDense_input_set)

    def __init__(self, *args):
        this = _linear_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _linear_.Batch_Float32DefaultDense_getMethod(self)

    def getInput(self):
        return _linear_.Batch_Float32DefaultDense_getInput(self)

    def getParameter(self):
        return _linear_.Batch_Float32DefaultDense_getParameter(self)

    def clone(self):
        return _linear_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _linear_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _linear_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _linear_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Batch_Float32FastCSR(daal.algorithms.kernel_function.KernelIface):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.kernel_function.KernelIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _linear_.Batch_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _linear_.Batch_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_linear_.Batch_Float32FastCSR_parameter_get, _linear_.Batch_Float32FastCSR_parameter_set)
    __swig_setmethods__["input"] = _linear_.Batch_Float32FastCSR_input_set
    __swig_getmethods__["input"] = _linear_.Batch_Float32FastCSR_input_get
    if _newclass:
        input = _swig_property(_linear_.Batch_Float32FastCSR_input_get, _linear_.Batch_Float32FastCSR_input_set)

    def __init__(self, *args):
        this = _linear_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _linear_.Batch_Float32FastCSR_getMethod(self)

    def getInput(self):
        return _linear_.Batch_Float32FastCSR_getInput(self)

    def getParameter(self):
        return _linear_.Batch_Float32FastCSR_getParameter(self)

    def clone(self):
        return _linear_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _linear_.Batch_Float32FastCSR_compute(self)
    __swig_destroy__ = _linear_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None
Batch_Float32FastCSR_swigregister = _linear_.Batch_Float32FastCSR_swigregister
Batch_Float32FastCSR_swigregister(Batch_Float32FastCSR)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float64FastCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


