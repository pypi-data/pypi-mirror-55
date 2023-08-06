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
            fp, pathname, description = imp.find_module('_uniform_', [dirname(__file__)])
        except ImportError:
            import _uniform_
            return _uniform_
        if fp is not None:
            try:
                _mod = imp.load_module('_uniform_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _uniform_ = swig_import_helper()
    del swig_import_helper
else:
    import _uniform_
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


import daal.algorithms.distributions
import daal.algorithms.engines
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_uniform_.defaultDense_swigconstant(_uniform_)
defaultDense = _uniform_.defaultDense
class Parameter_Float64(daal.algorithms.distributions.ParameterBase):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float64, name)
    __repr__ = _swig_repr

    def __init__(self, _a=0.0, _b=1.0):
        this = _uniform_.new_Parameter_Float64(_a, _b)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["a"] = _uniform_.Parameter_Float64_a_set
    __swig_getmethods__["a"] = _uniform_.Parameter_Float64_a_get
    if _newclass:
        a = _swig_property(_uniform_.Parameter_Float64_a_get, _uniform_.Parameter_Float64_a_set)
    __swig_setmethods__["b"] = _uniform_.Parameter_Float64_b_set
    __swig_getmethods__["b"] = _uniform_.Parameter_Float64_b_get
    if _newclass:
        b = _swig_property(_uniform_.Parameter_Float64_b_get, _uniform_.Parameter_Float64_b_set)

    def check(self):
        return _uniform_.Parameter_Float64_check(self)
    __swig_destroy__ = _uniform_.delete_Parameter_Float64
    __del__ = lambda self: None
Parameter_Float64_swigregister = _uniform_.Parameter_Float64_swigregister
Parameter_Float64_swigregister(Parameter_Float64)

class Parameter_Float32(daal.algorithms.distributions.ParameterBase):
    r"""
    This class is an alias of Parameter()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter_Float32, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter_Float32, name)
    __repr__ = _swig_repr

    def __init__(self, _a=0.0, _b=1.0):
        this = _uniform_.new_Parameter_Float32(_a, _b)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["a"] = _uniform_.Parameter_Float32_a_set
    __swig_getmethods__["a"] = _uniform_.Parameter_Float32_a_get
    if _newclass:
        a = _swig_property(_uniform_.Parameter_Float32_a_get, _uniform_.Parameter_Float32_a_set)
    __swig_setmethods__["b"] = _uniform_.Parameter_Float32_b_set
    __swig_getmethods__["b"] = _uniform_.Parameter_Float32_b_get
    if _newclass:
        b = _swig_property(_uniform_.Parameter_Float32_b_get, _uniform_.Parameter_Float32_b_set)

    def check(self):
        return _uniform_.Parameter_Float32_check(self)
    __swig_destroy__ = _uniform_.delete_Parameter_Float32
    __del__ = lambda self: None
Parameter_Float32_swigregister = _uniform_.Parameter_Float32_swigregister
Parameter_Float32_swigregister(Parameter_Float32)

class Batch_Float64DefaultDense(daal.algorithms.distributions.BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _uniform_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _uniform_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _uniform_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _uniform_.Batch_Float64DefaultDense_setResult(self, result)

    def clone(self):
        return _uniform_.Batch_Float64DefaultDense_clone(self)

    def allocateResult(self):
        return _uniform_.Batch_Float64DefaultDense_allocateResult(self)
    __swig_setmethods__["parameter"] = _uniform_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _uniform_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_uniform_.Batch_Float64DefaultDense_parameter_get, _uniform_.Batch_Float64DefaultDense_parameter_set)

    def compute(self):
        return _uniform_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _uniform_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _uniform_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float32DefaultDense(daal.algorithms.distributions.BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _uniform_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _uniform_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _uniform_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _uniform_.Batch_Float32DefaultDense_setResult(self, result)

    def clone(self):
        return _uniform_.Batch_Float32DefaultDense_clone(self)

    def allocateResult(self):
        return _uniform_.Batch_Float32DefaultDense_allocateResult(self)
    __swig_setmethods__["parameter"] = _uniform_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _uniform_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_uniform_.Batch_Float32DefaultDense_parameter_get, _uniform_.Batch_Float32DefaultDense_parameter_set)

    def compute(self):
        return _uniform_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _uniform_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _uniform_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

from numpy import float64, float32, intc

class Parameter(object):
    r"""Factory class for different types of Parameter."""
    def __new__(cls,
                fptype,
                *args, **kwargs):
        if fptype == float64:
            return Parameter_Float64(*args)
        if fptype == float32:
            return Parameter_Float32(*args)

        raise RuntimeError("No appropriate constructor found for Parameter")

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


