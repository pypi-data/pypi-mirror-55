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
            fp, pathname, description = imp.find_module('_normal_', [dirname(__file__)])
        except ImportError:
            import _normal_
            return _normal_
        if fp is not None:
            try:
                _mod = imp.load_module('_normal_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _normal_ = swig_import_helper()
    del swig_import_helper
else:
    import _normal_
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

_normal_.icdf_swigconstant(_normal_)
icdf = _normal_.icdf

_normal_.defaultDense_swigconstant(_normal_)
defaultDense = _normal_.defaultDense
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

    def __init__(self, _a=0.0, _sigma=1.0):
        this = _normal_.new_Parameter_Float64(_a, _sigma)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["a"] = _normal_.Parameter_Float64_a_set
    __swig_getmethods__["a"] = _normal_.Parameter_Float64_a_get
    if _newclass:
        a = _swig_property(_normal_.Parameter_Float64_a_get, _normal_.Parameter_Float64_a_set)
    __swig_setmethods__["sigma"] = _normal_.Parameter_Float64_sigma_set
    __swig_getmethods__["sigma"] = _normal_.Parameter_Float64_sigma_get
    if _newclass:
        sigma = _swig_property(_normal_.Parameter_Float64_sigma_get, _normal_.Parameter_Float64_sigma_set)

    def check(self):
        return _normal_.Parameter_Float64_check(self)
    __swig_destroy__ = _normal_.delete_Parameter_Float64
    __del__ = lambda self: None
Parameter_Float64_swigregister = _normal_.Parameter_Float64_swigregister
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

    def __init__(self, _a=0.0, _sigma=1.0):
        this = _normal_.new_Parameter_Float32(_a, _sigma)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["a"] = _normal_.Parameter_Float32_a_set
    __swig_getmethods__["a"] = _normal_.Parameter_Float32_a_get
    if _newclass:
        a = _swig_property(_normal_.Parameter_Float32_a_get, _normal_.Parameter_Float32_a_set)
    __swig_setmethods__["sigma"] = _normal_.Parameter_Float32_sigma_set
    __swig_getmethods__["sigma"] = _normal_.Parameter_Float32_sigma_get
    if _newclass:
        sigma = _swig_property(_normal_.Parameter_Float32_sigma_get, _normal_.Parameter_Float32_sigma_set)

    def check(self):
        return _normal_.Parameter_Float32_check(self)
    __swig_destroy__ = _normal_.delete_Parameter_Float32
    __del__ = lambda self: None
Parameter_Float32_swigregister = _normal_.Parameter_Float32_swigregister
Parameter_Float32_swigregister(Parameter_Float32)

class Batch_Float64Icdf(daal.algorithms.distributions.BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Icdf, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Icdf, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _normal_.new_Batch_Float64Icdf(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _normal_.Batch_Float64Icdf_getMethod(self)

    def getResult(self):
        return _normal_.Batch_Float64Icdf_getResult(self)

    def setResult(self, result):
        return _normal_.Batch_Float64Icdf_setResult(self, result)

    def clone(self):
        return _normal_.Batch_Float64Icdf_clone(self)

    def allocateResult(self):
        return _normal_.Batch_Float64Icdf_allocateResult(self)
    __swig_setmethods__["parameter"] = _normal_.Batch_Float64Icdf_parameter_set
    __swig_getmethods__["parameter"] = _normal_.Batch_Float64Icdf_parameter_get
    if _newclass:
        parameter = _swig_property(_normal_.Batch_Float64Icdf_parameter_get, _normal_.Batch_Float64Icdf_parameter_set)

    def compute(self):
        return _normal_.Batch_Float64Icdf_compute(self)
    __swig_destroy__ = _normal_.delete_Batch_Float64Icdf
    __del__ = lambda self: None
Batch_Float64Icdf_swigregister = _normal_.Batch_Float64Icdf_swigregister
Batch_Float64Icdf_swigregister(Batch_Float64Icdf)

class Batch_Float32Icdf(daal.algorithms.distributions.BatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Icdf, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.distributions.BatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Icdf, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _normal_.new_Batch_Float32Icdf(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _normal_.Batch_Float32Icdf_getMethod(self)

    def getResult(self):
        return _normal_.Batch_Float32Icdf_getResult(self)

    def setResult(self, result):
        return _normal_.Batch_Float32Icdf_setResult(self, result)

    def clone(self):
        return _normal_.Batch_Float32Icdf_clone(self)

    def allocateResult(self):
        return _normal_.Batch_Float32Icdf_allocateResult(self)
    __swig_setmethods__["parameter"] = _normal_.Batch_Float32Icdf_parameter_set
    __swig_getmethods__["parameter"] = _normal_.Batch_Float32Icdf_parameter_get
    if _newclass:
        parameter = _swig_property(_normal_.Batch_Float32Icdf_parameter_get, _normal_.Batch_Float32Icdf_parameter_set)

    def compute(self):
        return _normal_.Batch_Float32Icdf_compute(self)
    __swig_destroy__ = _normal_.delete_Batch_Float32Icdf
    __del__ = lambda self: None
Batch_Float32Icdf_swigregister = _normal_.Batch_Float32Icdf_swigregister
Batch_Float32Icdf_swigregister(Batch_Float32Icdf)

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
            if 'method' not in kwargs or kwargs['method'] == icdf:
                return Batch_Float64Icdf(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == icdf:
                return Batch_Float32Icdf(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


