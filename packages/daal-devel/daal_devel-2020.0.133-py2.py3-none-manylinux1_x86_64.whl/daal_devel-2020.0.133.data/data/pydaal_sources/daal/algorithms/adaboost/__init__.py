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
            fp, pathname, description = imp.find_module('_adaboost_', [dirname(__file__)])
        except ImportError:
            import _adaboost_
            return _adaboost_
        if fp is not None:
            try:
                _mod = imp.load_module('_adaboost_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _adaboost_ = swig_import_helper()
    del swig_import_helper
else:
    import _adaboost_
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
import daal.algorithms.boosting
class Parameter(daal.algorithms.boosting.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.boosting.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.boosting.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _adaboost_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["accuracyThreshold"] = _adaboost_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _adaboost_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_adaboost_.Parameter_accuracyThreshold_get, _adaboost_.Parameter_accuracyThreshold_set)
    __swig_setmethods__["maxIterations"] = _adaboost_.Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _adaboost_.Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_adaboost_.Parameter_maxIterations_get, _adaboost_.Parameter_maxIterations_set)

    def check(self):
        return _adaboost_.Parameter_check(self)
    __swig_destroy__ = _adaboost_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _adaboost_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Model(daal.algorithms.boosting.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.boosting.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.boosting.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _adaboost_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_adaboost_.Model_serializationTag)

    def getSerializationTag(self):
        return _adaboost_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _adaboost_.Model_downCast
    if _newclass:
        downCast = staticmethod(_adaboost_.Model_downCast)
    __swig_destroy__ = _adaboost_.delete_Model
    __del__ = lambda self: None

    def getAlpha(self):
        return _adaboost_.Model_getAlpha(self)

    def __init__(self, *args):
        this = _adaboost_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
Model_swigregister = _adaboost_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _adaboost_.Model_serializationTag()
Model_serializationTag = _adaboost_.Model_serializationTag

def Model_downCast(r):
    return _adaboost_.Model_downCast(r)
Model_downCast = _adaboost_.Model_downCast


_adaboost_.computeWeakLearnersErrors_swigconstant(_adaboost_)
computeWeakLearnersErrors = _adaboost_.computeWeakLearnersErrors
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
        this = _adaboost_.new_interface2_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["weakLearnerTraining"] = _adaboost_.interface2_Parameter_weakLearnerTraining_set
    __swig_getmethods__["weakLearnerTraining"] = _adaboost_.interface2_Parameter_weakLearnerTraining_get
    if _newclass:
        weakLearnerTraining = _swig_property(_adaboost_.interface2_Parameter_weakLearnerTraining_get, _adaboost_.interface2_Parameter_weakLearnerTraining_set)
    __swig_setmethods__["weakLearnerPrediction"] = _adaboost_.interface2_Parameter_weakLearnerPrediction_set
    __swig_getmethods__["weakLearnerPrediction"] = _adaboost_.interface2_Parameter_weakLearnerPrediction_get
    if _newclass:
        weakLearnerPrediction = _swig_property(_adaboost_.interface2_Parameter_weakLearnerPrediction_get, _adaboost_.interface2_Parameter_weakLearnerPrediction_set)
    __swig_setmethods__["accuracyThreshold"] = _adaboost_.interface2_Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _adaboost_.interface2_Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_adaboost_.interface2_Parameter_accuracyThreshold_get, _adaboost_.interface2_Parameter_accuracyThreshold_set)
    __swig_setmethods__["maxIterations"] = _adaboost_.interface2_Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _adaboost_.interface2_Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_adaboost_.interface2_Parameter_maxIterations_get, _adaboost_.interface2_Parameter_maxIterations_set)
    __swig_setmethods__["learningRate"] = _adaboost_.interface2_Parameter_learningRate_set
    __swig_getmethods__["learningRate"] = _adaboost_.interface2_Parameter_learningRate_get
    if _newclass:
        learningRate = _swig_property(_adaboost_.interface2_Parameter_learningRate_get, _adaboost_.interface2_Parameter_learningRate_set)
    __swig_setmethods__["resultsToCompute"] = _adaboost_.interface2_Parameter_resultsToCompute_set
    __swig_getmethods__["resultsToCompute"] = _adaboost_.interface2_Parameter_resultsToCompute_get
    if _newclass:
        resultsToCompute = _swig_property(_adaboost_.interface2_Parameter_resultsToCompute_get, _adaboost_.interface2_Parameter_resultsToCompute_set)

    def check(self):
        return _adaboost_.interface2_Parameter_check(self)
    __swig_destroy__ = _adaboost_.delete_interface2_Parameter
    __del__ = lambda self: None
interface2_Parameter_swigregister = _adaboost_.interface2_Parameter_swigregister
interface2_Parameter_swigregister(interface2_Parameter)

class interface2_Model(daal.algorithms.classifier.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Model, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _adaboost_.interface2_Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_adaboost_.interface2_Model_serializationTag)

    def getSerializationTag(self):
        return _adaboost_.interface2_Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _adaboost_.interface2_Model_downCast
    if _newclass:
        downCast = staticmethod(_adaboost_.interface2_Model_downCast)

    def __init__(self, nFeatures=0):
        this = _adaboost_.new_interface2_Model(nFeatures)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _adaboost_.delete_interface2_Model
    __del__ = lambda self: None

    def getNumberOfWeakLearners(self):
        return _adaboost_.interface2_Model_getNumberOfWeakLearners(self)

    def getWeakLearnerModel(self, idx):
        return _adaboost_.interface2_Model_getWeakLearnerModel(self, idx)

    def addWeakLearnerModel(self, model):
        return _adaboost_.interface2_Model_addWeakLearnerModel(self, model)

    def clearWeakLearnerModels(self):
        return _adaboost_.interface2_Model_clearWeakLearnerModels(self)

    def getNumberOfFeatures(self):
        return _adaboost_.interface2_Model_getNumberOfFeatures(self)

    def getAlpha(self):
        return _adaboost_.interface2_Model_getAlpha(self)
interface2_Model_swigregister = _adaboost_.interface2_Model_swigregister
interface2_Model_swigregister(interface2_Model)

def interface2_Model_serializationTag():
    return _adaboost_.interface2_Model_serializationTag()
interface2_Model_serializationTag = _adaboost_.interface2_Model_serializationTag

def interface2_Model_downCast(r):
    return _adaboost_.interface2_Model_downCast(r)
interface2_Model_downCast = _adaboost_.interface2_Model_downCast

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


