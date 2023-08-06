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
            fp, pathname, description = imp.find_module('_mt2203_', [dirname(__file__)])
        except ImportError:
            import _mt2203_
            return _mt2203_
        if fp is not None:
            try:
                _mod = imp.load_module('_mt2203_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _mt2203_ = swig_import_helper()
    del swig_import_helper
else:
    import _mt2203_
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


import daal.algorithms.engines
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_mt2203_.defaultDense_swigconstant(_mt2203_)
defaultDense = _mt2203_.defaultDense
class Batch_Float64DefaultDense(daal.algorithms.engines.FamilyBatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.engines.FamilyBatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.engines.FamilyBatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["create"] = lambda x: _mt2203_.Batch_Float64DefaultDense_create
    if _newclass:
        create = staticmethod(_mt2203_.Batch_Float64DefaultDense_create)

    def getMethod(self):
        return _mt2203_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _mt2203_.Batch_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _mt2203_.Batch_Float64DefaultDense_setResult(self, result)

    def clone(self):
        return _mt2203_.Batch_Float64DefaultDense_clone(self)

    def allocateResult(self):
        return _mt2203_.Batch_Float64DefaultDense_allocateResult(self)

    def compute(self):
        return _mt2203_.Batch_Float64DefaultDense_compute(self)
    __swig_destroy__ = _mt2203_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None
Batch_Float64DefaultDense_swigregister = _mt2203_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

def Batch_Float64DefaultDense_create(seed=777, st=None):
    return _mt2203_.Batch_Float64DefaultDense_create(seed, st)
Batch_Float64DefaultDense_create = _mt2203_.Batch_Float64DefaultDense_create

class Batch_Float32DefaultDense(daal.algorithms.engines.FamilyBatchBase):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.engines.FamilyBatchBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.engines.FamilyBatchBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["create"] = lambda x: _mt2203_.Batch_Float32DefaultDense_create
    if _newclass:
        create = staticmethod(_mt2203_.Batch_Float32DefaultDense_create)

    def getMethod(self):
        return _mt2203_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _mt2203_.Batch_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _mt2203_.Batch_Float32DefaultDense_setResult(self, result)

    def clone(self):
        return _mt2203_.Batch_Float32DefaultDense_clone(self)

    def allocateResult(self):
        return _mt2203_.Batch_Float32DefaultDense_allocateResult(self)

    def compute(self):
        return _mt2203_.Batch_Float32DefaultDense_compute(self)
    __swig_destroy__ = _mt2203_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None
Batch_Float32DefaultDense_swigregister = _mt2203_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

def Batch_Float32DefaultDense_create(seed=777, st=None):
    return _mt2203_.Batch_Float32DefaultDense_create(seed, st)
Batch_Float32DefaultDense_create = _mt2203_.Batch_Float32DefaultDense_create

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


