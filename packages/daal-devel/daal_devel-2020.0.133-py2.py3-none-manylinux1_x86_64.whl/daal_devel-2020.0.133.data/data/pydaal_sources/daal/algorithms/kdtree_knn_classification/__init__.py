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
            fp, pathname, description = imp.find_module('_kdtree_knn_classification_', [dirname(__file__)])
        except ImportError:
            import _kdtree_knn_classification_
            return _kdtree_knn_classification_
        if fp is not None:
            try:
                _mod = imp.load_module('_kdtree_knn_classification_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _kdtree_knn_classification_ = swig_import_helper()
    del swig_import_helper
else:
    import _kdtree_knn_classification_
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


import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_kdtree_knn_classification_.doNotUse_swigconstant(_kdtree_knn_classification_)
doNotUse = _kdtree_knn_classification_.doNotUse

_kdtree_knn_classification_.doUse_swigconstant(_kdtree_knn_classification_)
doUse = _kdtree_knn_classification_.doUse
class Parameter(daal.algorithms.classifier.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kdtree_knn_classification_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _kdtree_knn_classification_.Parameter_check(self)
    __swig_setmethods__["k"] = _kdtree_knn_classification_.Parameter_k_set
    __swig_getmethods__["k"] = _kdtree_knn_classification_.Parameter_k_get
    if _newclass:
        k = _swig_property(_kdtree_knn_classification_.Parameter_k_get, _kdtree_knn_classification_.Parameter_k_set)
    __swig_setmethods__["seed"] = _kdtree_knn_classification_.Parameter_seed_set
    __swig_getmethods__["seed"] = _kdtree_knn_classification_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_kdtree_knn_classification_.Parameter_seed_get, _kdtree_knn_classification_.Parameter_seed_set)
    __swig_setmethods__["dataUseInModel"] = _kdtree_knn_classification_.Parameter_dataUseInModel_set
    __swig_getmethods__["dataUseInModel"] = _kdtree_knn_classification_.Parameter_dataUseInModel_get
    if _newclass:
        dataUseInModel = _swig_property(_kdtree_knn_classification_.Parameter_dataUseInModel_get, _kdtree_knn_classification_.Parameter_dataUseInModel_set)
    __swig_setmethods__["engine"] = _kdtree_knn_classification_.Parameter_engine_set
    __swig_getmethods__["engine"] = _kdtree_knn_classification_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_kdtree_knn_classification_.Parameter_engine_get, _kdtree_knn_classification_.Parameter_engine_set)
    __swig_destroy__ = _kdtree_knn_classification_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _kdtree_knn_classification_.Parameter_swigregister
Parameter_swigregister(Parameter)

class interface2_Parameter(daal.algorithms.classifier.interface2_Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kdtree_knn_classification_.new_interface2_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _kdtree_knn_classification_.interface2_Parameter_check(self)
    __swig_setmethods__["k"] = _kdtree_knn_classification_.interface2_Parameter_k_set
    __swig_getmethods__["k"] = _kdtree_knn_classification_.interface2_Parameter_k_get
    if _newclass:
        k = _swig_property(_kdtree_knn_classification_.interface2_Parameter_k_get, _kdtree_knn_classification_.interface2_Parameter_k_set)
    __swig_setmethods__["seed"] = _kdtree_knn_classification_.interface2_Parameter_seed_set
    __swig_getmethods__["seed"] = _kdtree_knn_classification_.interface2_Parameter_seed_get
    if _newclass:
        seed = _swig_property(_kdtree_knn_classification_.interface2_Parameter_seed_get, _kdtree_knn_classification_.interface2_Parameter_seed_set)
    __swig_setmethods__["dataUseInModel"] = _kdtree_knn_classification_.interface2_Parameter_dataUseInModel_set
    __swig_getmethods__["dataUseInModel"] = _kdtree_knn_classification_.interface2_Parameter_dataUseInModel_get
    if _newclass:
        dataUseInModel = _swig_property(_kdtree_knn_classification_.interface2_Parameter_dataUseInModel_get, _kdtree_knn_classification_.interface2_Parameter_dataUseInModel_set)
    __swig_setmethods__["engine"] = _kdtree_knn_classification_.interface2_Parameter_engine_set
    __swig_getmethods__["engine"] = _kdtree_knn_classification_.interface2_Parameter_engine_get
    if _newclass:
        engine = _swig_property(_kdtree_knn_classification_.interface2_Parameter_engine_get, _kdtree_knn_classification_.interface2_Parameter_engine_set)
    __swig_destroy__ = _kdtree_knn_classification_.delete_interface2_Parameter
    __del__ = lambda self: None
interface2_Parameter_swigregister = _kdtree_knn_classification_.interface2_Parameter_swigregister
interface2_Parameter_swigregister(interface2_Parameter)

class Model(daal.algorithms.classifier.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _kdtree_knn_classification_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_kdtree_knn_classification_.Model_serializationTag)

    def getSerializationTag(self):
        return _kdtree_knn_classification_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _kdtree_knn_classification_.Model_downCast
    if _newclass:
        downCast = staticmethod(_kdtree_knn_classification_.Model_downCast)

    def __init__(self, nFeatures=0):
        this = _kdtree_knn_classification_.new_Model(nFeatures)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_getmethods__["create"] = lambda x: _kdtree_knn_classification_.Model_create
    if _newclass:
        create = staticmethod(_kdtree_knn_classification_.Model_create)
    __swig_destroy__ = _kdtree_knn_classification_.delete_Model
    __del__ = lambda self: None

    def impl(self, *args):
        return _kdtree_knn_classification_.Model_impl(self, *args)

    def getNumberOfFeatures(self):
        return _kdtree_knn_classification_.Model_getNumberOfFeatures(self)
Model_swigregister = _kdtree_knn_classification_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _kdtree_knn_classification_.Model_serializationTag()
Model_serializationTag = _kdtree_knn_classification_.Model_serializationTag

def Model_downCast(r):
    return _kdtree_knn_classification_.Model_downCast(r)
Model_downCast = _kdtree_knn_classification_.Model_downCast

def Model_create(nFeatures=0, stat=None):
    return _kdtree_knn_classification_.Model_create(nFeatures, stat)
Model_create = _kdtree_knn_classification_.Model_create

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


