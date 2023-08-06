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
            fp, pathname, description = imp.find_module('_multi_class_classifier_', [dirname(__file__)])
        except ImportError:
            import _multi_class_classifier_
            return _multi_class_classifier_
        if fp is not None:
            try:
                _mod = imp.load_module('_multi_class_classifier_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _multi_class_classifier_ = swig_import_helper()
    del swig_import_helper
else:
    import _multi_class_classifier_
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
import daal.algorithms.classifier.training
import daal.algorithms.classifier.prediction
class ParameterBase(daal.algorithms.classifier.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ParameterBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ParameterBase, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses):
        this = _multi_class_classifier_.new_ParameterBase(nClasses)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["training"] = _multi_class_classifier_.ParameterBase_training_set
    __swig_getmethods__["training"] = _multi_class_classifier_.ParameterBase_training_get
    if _newclass:
        training = _swig_property(_multi_class_classifier_.ParameterBase_training_get, _multi_class_classifier_.ParameterBase_training_set)
    __swig_setmethods__["prediction"] = _multi_class_classifier_.ParameterBase_prediction_set
    __swig_getmethods__["prediction"] = _multi_class_classifier_.ParameterBase_prediction_get
    if _newclass:
        prediction = _swig_property(_multi_class_classifier_.ParameterBase_prediction_get, _multi_class_classifier_.ParameterBase_prediction_set)
    __swig_destroy__ = _multi_class_classifier_.delete_ParameterBase
    __del__ = lambda self: None
ParameterBase_swigregister = _multi_class_classifier_.ParameterBase_swigregister
ParameterBase_swigregister(ParameterBase)

class Parameter(ParameterBase):
    __swig_setmethods__ = {}
    for _s in [ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses, maxIterations=100, accuracyThreshold=1.0e-12):
        this = _multi_class_classifier_.new_Parameter(nClasses, maxIterations, accuracyThreshold)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["maxIterations"] = _multi_class_classifier_.Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _multi_class_classifier_.Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_multi_class_classifier_.Parameter_maxIterations_get, _multi_class_classifier_.Parameter_maxIterations_set)
    __swig_setmethods__["accuracyThreshold"] = _multi_class_classifier_.Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _multi_class_classifier_.Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_multi_class_classifier_.Parameter_accuracyThreshold_get, _multi_class_classifier_.Parameter_accuracyThreshold_set)

    def check(self):
        return _multi_class_classifier_.Parameter_check(self)
    __swig_destroy__ = _multi_class_classifier_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _multi_class_classifier_.Parameter_swigregister
Parameter_swigregister(Parameter)

class interface2_ParameterBase(daal.algorithms.classifier.interface2_Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_ParameterBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_ParameterBase, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses):
        this = _multi_class_classifier_.new_interface2_ParameterBase(nClasses)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["training"] = _multi_class_classifier_.interface2_ParameterBase_training_set
    __swig_getmethods__["training"] = _multi_class_classifier_.interface2_ParameterBase_training_get
    if _newclass:
        training = _swig_property(_multi_class_classifier_.interface2_ParameterBase_training_get, _multi_class_classifier_.interface2_ParameterBase_training_set)
    __swig_setmethods__["prediction"] = _multi_class_classifier_.interface2_ParameterBase_prediction_set
    __swig_getmethods__["prediction"] = _multi_class_classifier_.interface2_ParameterBase_prediction_get
    if _newclass:
        prediction = _swig_property(_multi_class_classifier_.interface2_ParameterBase_prediction_get, _multi_class_classifier_.interface2_ParameterBase_prediction_set)
    __swig_destroy__ = _multi_class_classifier_.delete_interface2_ParameterBase
    __del__ = lambda self: None
interface2_ParameterBase_swigregister = _multi_class_classifier_.interface2_ParameterBase_swigregister
interface2_ParameterBase_swigregister(interface2_ParameterBase)

class interface2_Parameter(interface2_ParameterBase):
    __swig_setmethods__ = {}
    for _s in [interface2_ParameterBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [interface2_ParameterBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses, maxIterations=100, accuracyThreshold=1.0e-12):
        this = _multi_class_classifier_.new_interface2_Parameter(nClasses, maxIterations, accuracyThreshold)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["maxIterations"] = _multi_class_classifier_.interface2_Parameter_maxIterations_set
    __swig_getmethods__["maxIterations"] = _multi_class_classifier_.interface2_Parameter_maxIterations_get
    if _newclass:
        maxIterations = _swig_property(_multi_class_classifier_.interface2_Parameter_maxIterations_get, _multi_class_classifier_.interface2_Parameter_maxIterations_set)
    __swig_setmethods__["accuracyThreshold"] = _multi_class_classifier_.interface2_Parameter_accuracyThreshold_set
    __swig_getmethods__["accuracyThreshold"] = _multi_class_classifier_.interface2_Parameter_accuracyThreshold_get
    if _newclass:
        accuracyThreshold = _swig_property(_multi_class_classifier_.interface2_Parameter_accuracyThreshold_get, _multi_class_classifier_.interface2_Parameter_accuracyThreshold_set)

    def check(self):
        return _multi_class_classifier_.interface2_Parameter_check(self)
    __swig_destroy__ = _multi_class_classifier_.delete_interface2_Parameter
    __del__ = lambda self: None
interface2_Parameter_swigregister = _multi_class_classifier_.interface2_Parameter_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _multi_class_classifier_.Model_serializationTag
    if _newclass:
        serializationTag = staticmethod(_multi_class_classifier_.Model_serializationTag)

    def getSerializationTag(self):
        return _multi_class_classifier_.Model_getSerializationTag(self)
    __swig_getmethods__["downCast"] = lambda x: _multi_class_classifier_.Model_downCast
    if _newclass:
        downCast = staticmethod(_multi_class_classifier_.Model_downCast)

    def __init__(self, *args):
        this = _multi_class_classifier_.new_Model(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_getmethods__["create"] = lambda x: _multi_class_classifier_.Model_create
    if _newclass:
        create = staticmethod(_multi_class_classifier_.Model_create)
    __swig_destroy__ = _multi_class_classifier_.delete_Model
    __del__ = lambda self: None

    def getMultiClassClassifierModel(self):
        return _multi_class_classifier_.Model_getMultiClassClassifierModel(self)

    def getTwoClassClassifierModels(self):
        return _multi_class_classifier_.Model_getTwoClassClassifierModels(self)

    def setTwoClassClassifierModel(self, idx, model):
        return _multi_class_classifier_.Model_setTwoClassClassifierModel(self, idx, model)

    def getTwoClassClassifierModel(self, idx):
        return _multi_class_classifier_.Model_getTwoClassClassifierModel(self, idx)

    def getNumberOfTwoClassClassifierModels(self):
        return _multi_class_classifier_.Model_getNumberOfTwoClassClassifierModels(self)

    def getNumberOfFeatures(self):
        return _multi_class_classifier_.Model_getNumberOfFeatures(self)
Model_swigregister = _multi_class_classifier_.Model_swigregister
Model_swigregister(Model)

def Model_serializationTag():
    return _multi_class_classifier_.Model_serializationTag()
Model_serializationTag = _multi_class_classifier_.Model_serializationTag

def Model_downCast(r):
    return _multi_class_classifier_.Model_downCast(r)
Model_downCast = _multi_class_classifier_.Model_downCast

def Model_create(*args):
    return _multi_class_classifier_.Model_create(*args)
Model_create = _multi_class_classifier_.Model_create

from numpy import float64, float32, intc


from . import prediction
from . import quality_metric_set
from . import training

# This file is compatible with both classic and new-style classes.


