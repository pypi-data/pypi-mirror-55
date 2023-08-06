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
            fp, pathname, description = imp.find_module('_svm_', [dirname(__file__)])
        except ImportError:
            import _svm_
            return _svm_
        if fp is not None:
            try:
                _mod = imp.load_module('_svm_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _svm_ = swig_import_helper()
    del swig_import_helper
else:
    import _svm_
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
import daal.algorithms.kernel_function
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
        this = _svm_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["C"] = _svm_.Parameter_C_set
    __swig_getmethods__["C"] = _svm_.Parameter_C_get
    if _newclass:
        C = _swig_property(_svm_.Parameter_C_get, _svm_.Parameter_C_set)
    __swig_setmethods__["accuracyThreshold"] = _svm_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _svm_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_svm_.Parameter_accuracyThreshold_get, _svm_.Parameter_accuracyThreshold_set)
    __swig_setmethods__["tau"] = _svm_.Parameter_tau_set
    __swig_getmethods__["tau"] = _svm_.Parameter_tau_get
    if _newclass:
        tau = _swig_property(_svm_.Parameter_tau_get, _svm_.Parameter_tau_set)
    __swig_setmethods__["maxIterations"] = _svm_.Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _svm_.Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_svm_.Parameter_maxIterations_get, _svm_.Parameter_maxIterations_set)
    __swig_setmethods__["cacheSize"] = _svm_.Parameter_cacheSize_set
    __swig_getmethods__["cacheSize"] = _svm_.Parameter_cacheSize_get
    if _newclass:
        cacheSize = _swig_property(_svm_.Parameter_cacheSize_get, _svm_.Parameter_cacheSize_set)
    __swig_setmethods__["doShrinking"] = _svm_.Parameter_doShrinking_set
    __swig_getmethods__["doShrinking"] = _svm_.Parameter_doShrinking_get
    if _newclass:
        doShrinking = _swig_property(_svm_.Parameter_doShrinking_get, _svm_.Parameter_doShrinking_set)
    __swig_setmethods__["shrinkingStep"] = _svm_.Parameter_shrinkingStep_set
    __swig_getmethods__["shrinkingStep"] = _svm_.Parameter_shrinkingStep_get
    if _newclass:
        shrinkingStep = _swig_property(_svm_.Parameter_shrinkingStep_get, _svm_.Parameter_shrinkingStep_set)
    __swig_setmethods__["kernel"] = _svm_.Parameter_kernel_set
    __swig_getmethods__["kernel"] = _svm_.Parameter_kernel_get
    if _newclass:
        kernel = _swig_property(_svm_.Parameter_kernel_get, _svm_.Parameter_kernel_set)

    def check(self):
        return _svm_.Parameter_check(self)
    __swig_destroy__ = _svm_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _svm_.Parameter_swigregister
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
        this = _svm_.new_interface2_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["C"] = _svm_.interface2_Parameter_C_set
    __swig_getmethods__["C"] = _svm_.interface2_Parameter_C_get
    if _newclass:
        C = _swig_property(_svm_.interface2_Parameter_C_get, _svm_.interface2_Parameter_C_set)
    __swig_setmethods__["accuracyThreshold"] = _svm_.interface2_Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _svm_.interface2_Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_svm_.interface2_Parameter_accuracyThreshold_get, _svm_.interface2_Parameter_accuracyThreshold_set)
    __swig_setmethods__["tau"] = _svm_.interface2_Parameter_tau_set
    __swig_getmethods__["tau"] = _svm_.interface2_Parameter_tau_get
    if _newclass:
        tau = _swig_property(_svm_.interface2_Parameter_tau_get, _svm_.interface2_Parameter_tau_set)
    __swig_setmethods__["maxIterations"] = _svm_.interface2_Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _svm_.interface2_Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_svm_.interface2_Parameter_maxIterations_get, _svm_.interface2_Parameter_maxIterations_set)
    __swig_setmethods__["cacheSize"] = _svm_.interface2_Parameter_cacheSize_set
    __swig_getmethods__["cacheSize"] = _svm_.interface2_Parameter_cacheSize_get
    if _newclass:
        cacheSize = _swig_property(_svm_.interface2_Parameter_cacheSize_get, _svm_.interface2_Parameter_cacheSize_set)
    __swig_setmethods__["doShrinking"] = _svm_.interface2_Parameter_doShrinking_set
    __swig_getmethods__["doShrinking"] = _svm_.interface2_Parameter_doShrinking_get
    if _newclass:
        doShrinking = _swig_property(_svm_.interface2_Parameter_doShrinking_get, _svm_.interface2_Parameter_doShrinking_set)
    __swig_setmethods__["shrinkingStep"] = _svm_.interface2_Parameter_shrinkingStep_set
    __swig_getmethods__["shrinkingStep"] = _svm_.interface2_Parameter_shrinkingStep_get
    if _newclass:
        shrinkingStep = _swig_property(_svm_.interface2_Parameter_shrinkingStep_get, _svm_.interface2_Parameter_shrinkingStep_set)
    __swig_setmethods__["kernel"] = _svm_.interface2_Parameter_kernel_set
    __swig_getmethods__["kernel"] = _svm_.interface2_Parameter_kernel_get
    if _newclass:
        kernel = _swig_property(_svm_.interface2_Parameter_kernel_get, _svm_.interface2_Parameter_kernel_set)

    def check(self):
        return _svm_.interface2_Parameter_check(self)
    __swig_destroy__ = _svm_.delete_interface2_Parameter
    __del__ = lambda self: None
interface2_Parameter_swigregister = _svm_.interface2_Parameter_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _svm_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_svm_.Model_serializationTag)

    def getSerializationTag(self):
        return _svm_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _svm_.Model_downCast
    if _newclass:
        downCast = staticmethod(_svm_.Model_downCast)
    __swig_getmethods__["create"] = lambda x: _svm_.Model_create
    if _newclass:
        create = staticmethod(_svm_.Model_create)
    __swig_destroy__ = _svm_.delete_Model
    __del__ = lambda self: None

    def getSupportVectors(self):
        return _svm_.Model_getSupportVectors(self)

    def getSupportIndices(self):
        return _svm_.Model_getSupportIndices(self)

    def getClassificationCoefficients(self):
        return _svm_.Model_getClassificationCoefficients(self)

    def getBias(self):
        return _svm_.Model_getBias(self)

    def setBias(self, bias):
        return _svm_.Model_setBias(self, bias)

    def getNumberOfFeatures(self):
        return _svm_.Model_getNumberOfFeatures(self)

    def __init__(self, *args):
        this = _svm_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
Model_swigregister = _svm_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _svm_.Model_serializationTag()
Model_serializationTag = _svm_.Model_serializationTag

def Model_downCast(r):
    return _svm_.Model_downCast(r)
Model_downCast = _svm_.Model_downCast

def Model_create(stat=None):
    return _svm_.Model_create(stat)
Model_create = _svm_.Model_create

from numpy import float64, float32, intc


from . import prediction
from . import quality_metric_set
from . import training

# This file is compatible with both classic and new-style classes.


