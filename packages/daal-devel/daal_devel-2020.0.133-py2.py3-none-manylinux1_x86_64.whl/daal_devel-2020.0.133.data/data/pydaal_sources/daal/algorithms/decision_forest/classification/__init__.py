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
            fp, pathname, description = imp.find_module('_classification_', [dirname(__file__)])
        except ImportError:
            import _classification_
            return _classification_
        if fp is not None:
            try:
                _mod = imp.load_module('_classification_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _classification_ = swig_import_helper()
    del swig_import_helper
else:
    import _classification_
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
import daal.algorithms.decision_forest
class Model(daal.algorithms.classifier.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _classification_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_classification_.Model_serializationTag)

    def getSerializationTag(self):
        return _classification_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _classification_.Model_downCast
    if _newclass:
        downCast = staticmethod(_classification_.Model_downCast)

    def numberOfTrees(self):
        return _classification_.Model_numberOfTrees(self)

    def traverseDF(self, iTree, visitor):
        return _classification_.Model_traverseDF(self, iTree, visitor)

    def traverseBF(self, iTree, visitor):
        return _classification_.Model_traverseBF(self, iTree, visitor)

    def clear(self):
        return _classification_.Model_clear(self)

    def traverseDFS(self, iTree, visitor):
        return _classification_.Model_traverseDFS(self, iTree, visitor)

    def traverseBFS(self, iTree, visitor):
        return _classification_.Model_traverseBFS(self, iTree, visitor)

    def getNumberOfTrees(self):
        return _classification_.Model_getNumberOfTrees(self)
    __swig_destroy__ = _classification_.delete_Model
    __del__ = lambda self: None
Model_swigregister = _classification_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _classification_.Model_serializationTag()
Model_serializationTag = _classification_.Model_serializationTag

def Model_downCast(r):
    return _classification_.Model_downCast(r)
Model_downCast = _classification_.Model_downCast

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


