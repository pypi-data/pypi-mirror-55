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
            fp, pathname, description = imp.find_module('_linear_regression_', [dirname(__file__)])
        except ImportError:
            import _linear_regression_
            return _linear_regression_
        if fp is not None:
            try:
                _mod = imp.load_module('_linear_regression_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _linear_regression_ = swig_import_helper()
    del swig_import_helper
else:
    import _linear_regression_
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
import daal.algorithms.linear_model
import daal.algorithms.regression
class ModelQR(daal.algorithms.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModelQR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ModelQR, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _linear_regression_.ModelQR_serializationTag
    if _newclass:
        serializationTag = staticmethod(_linear_regression_.ModelQR_serializationTag)

    def getSerializationTag(self):
        return _linear_regression_.ModelQR_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _linear_regression_.ModelQR_downCast
    if _newclass:
        downCast = staticmethod(_linear_regression_.ModelQR_downCast)
    __swig_destroy__ = _linear_regression_.delete_ModelQR
    __del__ = lambda self: None

    def getRTable(self):
        return _linear_regression_.ModelQR_getRTable(self)

    def getQTYTable(self):
        return _linear_regression_.ModelQR_getQTYTable(self)
ModelQR_swigregister = _linear_regression_.ModelQR_swigregister
ModelQR_swigregister(ModelQR)

def ModelQR_serializationTag():
    return _linear_regression_.ModelQR_serializationTag()
ModelQR_serializationTag = _linear_regression_.ModelQR_serializationTag

def ModelQR_downCast(r):
    return _linear_regression_.ModelQR_downCast(r)
ModelQR_downCast = _linear_regression_.ModelQR_downCast

class Parameter(daal.algorithms.linear_model.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _linear_regression_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _linear_regression_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _linear_regression_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Model(daal.algorithms.linear_model.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.linear_model.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.linear_model.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _linear_regression_.delete_Model
    __del__ = lambda self: None
Model_swigregister = _linear_regression_.Model_swigregister
Model_swigregister(Model)


def checkModel(model, par, nBeta, nResponses, method):
    return _linear_regression_.checkModel(model, par, nBeta, nResponses, method)
checkModel = _linear_regression_.checkModel
class ModelNormEq(Model):
    __swig_setmethods__ = {}
    for _s in [Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModelNormEq, name, value)
    __swig_getmethods__ = {}
    for _s in [Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ModelNormEq, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _linear_regression_.ModelNormEq_serializationTag
    if _newclass:
        serializationTag = staticmethod(_linear_regression_.ModelNormEq_serializationTag)

    def getSerializationTag(self):
        return _linear_regression_.ModelNormEq_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _linear_regression_.ModelNormEq_downCast
    if _newclass:
        downCast = staticmethod(_linear_regression_.ModelNormEq_downCast)
    __swig_destroy__ = _linear_regression_.delete_ModelNormEq
    __del__ = lambda self: None

    def getXTXTable(self):
        return _linear_regression_.ModelNormEq_getXTXTable(self)

    def getXTYTable(self):
        return _linear_regression_.ModelNormEq_getXTYTable(self)
ModelNormEq_swigregister = _linear_regression_.ModelNormEq_swigregister
ModelNormEq_swigregister(ModelNormEq)

def ModelNormEq_serializationTag():
    return _linear_regression_.ModelNormEq_serializationTag()
ModelNormEq_serializationTag = _linear_regression_.ModelNormEq_serializationTag

def ModelNormEq_downCast(r):
    return _linear_regression_.ModelNormEq_downCast(r)
ModelNormEq_downCast = _linear_regression_.ModelNormEq_downCast

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


