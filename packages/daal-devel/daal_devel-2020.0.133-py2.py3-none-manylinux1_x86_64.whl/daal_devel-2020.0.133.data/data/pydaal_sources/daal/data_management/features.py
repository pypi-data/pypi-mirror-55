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
            fp, pathname, description = imp.find_module('_features_', [dirname(__file__)])
        except ImportError:
            import _features_
            return _features_
        if fp is not None:
            try:
                _mod = imp.load_module('_features_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _features_ = swig_import_helper()
    del swig_import_helper
else:
    import _features_
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


import daal

_features_.DAAL_FLOAT32_swigconstant(_features_)
DAAL_FLOAT32 = _features_.DAAL_FLOAT32

_features_.DAAL_FLOAT64_swigconstant(_features_)
DAAL_FLOAT64 = _features_.DAAL_FLOAT64

_features_.DAAL_INT32_S_swigconstant(_features_)
DAAL_INT32_S = _features_.DAAL_INT32_S

_features_.DAAL_INT32_U_swigconstant(_features_)
DAAL_INT32_U = _features_.DAAL_INT32_U

_features_.DAAL_INT64_S_swigconstant(_features_)
DAAL_INT64_S = _features_.DAAL_INT64_S

_features_.DAAL_INT64_U_swigconstant(_features_)
DAAL_INT64_U = _features_.DAAL_INT64_U

_features_.DAAL_INT8_S_swigconstant(_features_)
DAAL_INT8_S = _features_.DAAL_INT8_S

_features_.DAAL_INT8_U_swigconstant(_features_)
DAAL_INT8_U = _features_.DAAL_INT8_U

_features_.DAAL_INT16_S_swigconstant(_features_)
DAAL_INT16_S = _features_.DAAL_INT16_S

_features_.DAAL_INT16_U_swigconstant(_features_)
DAAL_INT16_U = _features_.DAAL_INT16_U

_features_.DAAL_OTHER_T_swigconstant(_features_)
DAAL_OTHER_T = _features_.DAAL_OTHER_T

_features_.DAAL_GEN_FLOAT_swigconstant(_features_)
DAAL_GEN_FLOAT = _features_.DAAL_GEN_FLOAT

_features_.DAAL_GEN_DOUBLE_swigconstant(_features_)
DAAL_GEN_DOUBLE = _features_.DAAL_GEN_DOUBLE

_features_.DAAL_GEN_INTEGER_swigconstant(_features_)
DAAL_GEN_INTEGER = _features_.DAAL_GEN_INTEGER

_features_.DAAL_GEN_BOOLEAN_swigconstant(_features_)
DAAL_GEN_BOOLEAN = _features_.DAAL_GEN_BOOLEAN

_features_.DAAL_GEN_STRING_swigconstant(_features_)
DAAL_GEN_STRING = _features_.DAAL_GEN_STRING

_features_.DAAL_GEN_UNKNOWN_swigconstant(_features_)
DAAL_GEN_UNKNOWN = _features_.DAAL_GEN_UNKNOWN

_features_.DAAL_CATEGORICAL_swigconstant(_features_)
DAAL_CATEGORICAL = _features_.DAAL_CATEGORICAL

_features_.DAAL_ORDINAL_swigconstant(_features_)
DAAL_ORDINAL = _features_.DAAL_ORDINAL

_features_.DAAL_CONTINUOUS_swigconstant(_features_)
DAAL_CONTINUOUS = _features_.DAAL_CONTINUOUS
from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


