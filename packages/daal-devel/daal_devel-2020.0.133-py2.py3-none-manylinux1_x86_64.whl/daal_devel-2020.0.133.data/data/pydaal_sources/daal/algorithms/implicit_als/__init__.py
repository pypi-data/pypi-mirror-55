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
            fp, pathname, description = imp.find_module('_implicit_als_', [dirname(__file__)])
        except ImportError:
            import _implicit_als_
            return _implicit_als_
        if fp is not None:
            try:
                _mod = imp.load_module('_implicit_als_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _implicit_als_ = swig_import_helper()
    del swig_import_helper
else:
    import _implicit_als_
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


import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
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

    def __init__(self, nFactors=10, maxIterations=5, alpha=40.0, arg5=0.01, preferenceThreshold=0.0):
        this = _implicit_als_.new_Parameter(nFactors, maxIterations, alpha, arg5, preferenceThreshold)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nFactors"] = _implicit_als_.Parameter_nFactors_set
    __swig_getmethods__["nFactors"] = _implicit_als_.Parameter_nFactors_get
    if _newclass:
        nFactors = _swig_property(_implicit_als_.Parameter_nFactors_get, _implicit_als_.Parameter_nFactors_set)
    __swig_setmethods__["maxIterations"] = _implicit_als_.Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _implicit_als_.Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_implicit_als_.Parameter_maxIterations_get, _implicit_als_.Parameter_maxIterations_set)
    __swig_setmethods__["alpha"] = _implicit_als_.Parameter_alpha_set
    __swig_getmethods__["alpha"] = _implicit_als_.Parameter_alpha_get
    if _newclass:
        alpha = _swig_property(_implicit_als_.Parameter_alpha_get, _implicit_als_.Parameter_alpha_set)
    __swig_setmethods__["_lambda"] = _implicit_als_.Parameter__lambda_set
    __swig_getmethods__["_lambda"] = _implicit_als_.Parameter__lambda_get
    if _newclass:
        _lambda = _swig_property(_implicit_als_.Parameter__lambda_get, _implicit_als_.Parameter__lambda_set)
    __swig_setmethods__["preferenceThreshold"] = _implicit_als_.Parameter_preferenceThreshold_set
    __swig_getmethods__["preferenceThreshold"] = _implicit_als_.Parameter_preferenceThreshold_get
    if _newclass:
        preferenceThreshold = _swig_property(_implicit_als_.Parameter_preferenceThreshold_get, _implicit_als_.Parameter_preferenceThreshold_set)

    def check(self):
        return _implicit_als_.Parameter_check(self)
    __swig_destroy__ = _implicit_als_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _implicit_als_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Model(daal.algorithms.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _implicit_als_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_implicit_als_.Model_serializationTag)

    def getSerializationTag(self):
        return _implicit_als_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _implicit_als_.Model_downCast
    if _newclass:
        downCast = staticmethod(_implicit_als_.Model_downCast)
    __swig_destroy__ = _implicit_als_.delete_Model
    __del__ = lambda self: None

    def getUsersFactors(self):
        return _implicit_als_.Model_getUsersFactors(self)

    def getItemsFactors(self):
        return _implicit_als_.Model_getItemsFactors(self)

    def __init__(self, *args):
        this = _implicit_als_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
Model_swigregister = _implicit_als_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _implicit_als_.Model_serializationTag()
Model_serializationTag = _implicit_als_.Model_serializationTag

def Model_downCast(r):
    return _implicit_als_.Model_downCast(r)
Model_downCast = _implicit_als_.Model_downCast

class PartialModel(daal.algorithms.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialModel, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialModel, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _implicit_als_.PartialModel_serializationTag
    if _newclass:
        serializationTag = staticmethod(_implicit_als_.PartialModel_serializationTag)

    def getSerializationTag(self):
        return _implicit_als_.PartialModel_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _implicit_als_.PartialModel_create
    if _newclass:
        create = staticmethod(_implicit_als_.PartialModel_create)
    __swig_destroy__ = _implicit_als_.delete_PartialModel
    __del__ = lambda self: None

    def getFactors(self):
        return _implicit_als_.PartialModel_getFactors(self)

    def getIndices(self):
        return _implicit_als_.PartialModel_getIndices(self)

    def __init__(self, *args):
        this = _implicit_als_.new_PartialModel(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
PartialModel_swigregister = _implicit_als_.PartialModel_swigregister
PartialModel_swigregister(PartialModel)

def PartialModel_serializationTag():
    return _implicit_als_.PartialModel_serializationTag()
PartialModel_serializationTag = _implicit_als_.PartialModel_serializationTag

def PartialModel_create(factors, indices, stat=None):
    return _implicit_als_.PartialModel_create(factors, indices, stat)
PartialModel_create = _implicit_als_.PartialModel_create

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


