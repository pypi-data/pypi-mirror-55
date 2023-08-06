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
            fp, pathname, description = imp.find_module('_csv_', [dirname(__file__)])
        except ImportError:
            import _csv_
            return _csv_
        if fp is not None:
            try:
                _mod = imp.load_module('_csv_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _csv_ = swig_import_helper()
    del swig_import_helper
else:
    import _csv_
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


import daal.data_management.modifiers
import daal.data_management
import daal
import daal.services
import daal.data_management.features
class FeatureModifierIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FeatureModifierIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FeatureModifierIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_destroy__ = _csv_.delete_FeatureModifierIface
    __del__ = lambda self: None
FeatureModifierIface_swigregister = _csv_.FeatureModifierIface_swigregister
FeatureModifierIface_swigregister(FeatureModifierIface)

class FeatureModifier(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FeatureModifier, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FeatureModifier, name)
    __repr__ = _swig_repr

    def __init__(self, noof=0, nor=1):
        if self.__class__ == FeatureModifier:
            _self = None
        else:
            _self = self
        this = _csv_.new_FeatureModifier(_self, noof, nor)
        try:
            self.this.append(this)
        except:
            self.this = this
        self.__disown__()



    __swig_destroy__ = _csv_.delete_FeatureModifier
    __del__ = lambda self: None

    def getNumberOfOutputFeatures(self):
        return _csv_.FeatureModifier_getNumberOfOutputFeatures(self)

    def apply(self, tokens):
        return _csv_.FeatureModifier_apply(self, tokens)
    def __disown__(self):
        self.this.disown()
        _csv_.disown_FeatureModifier(self)
        return weakref_proxy(self)
FeatureModifier_swigregister = _csv_.FeatureModifier_swigregister
FeatureModifier_swigregister(FeatureModifier)


def continuous():
    return _csv_.continuous()
continuous = _csv_.continuous

def categorical():
    return _csv_.categorical()
categorical = _csv_.categorical

def automatic():
    return _csv_.automatic()
automatic = _csv_.automatic
from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


