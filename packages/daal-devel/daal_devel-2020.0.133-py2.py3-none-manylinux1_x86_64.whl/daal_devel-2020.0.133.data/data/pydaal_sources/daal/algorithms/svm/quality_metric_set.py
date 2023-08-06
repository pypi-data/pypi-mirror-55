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
            fp, pathname, description = imp.find_module('_quality_metric_set8_', [dirname(__file__)])
        except ImportError:
            import _quality_metric_set8_
            return _quality_metric_set8_
        if fp is not None:
            try:
                _mod = imp.load_module('_quality_metric_set8_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _quality_metric_set8_ = swig_import_helper()
    del swig_import_helper
else:
    import _quality_metric_set8_
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


import daal.algorithms.svm
import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.kernel_function
import daal.algorithms.classifier.quality_metric.binary_confusion_matrix
import daal.algorithms.quality_metric
import daal.algorithms.quality_metric_set

_quality_metric_set8_.confusionMatrix_swigconstant(_quality_metric_set8_)
confusionMatrix = _quality_metric_set8_.confusionMatrix

_quality_metric_set8_.lastQualityMetricId_swigconstant(_quality_metric_set8_)
lastQualityMetricId = _quality_metric_set8_.lastQualityMetricId
class ResultCollection(daal.algorithms.quality_metric_set.ResultCollection):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.ResultCollection]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultCollection, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.ResultCollection]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ResultCollection, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _quality_metric_set8_.new_ResultCollection()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _quality_metric_set8_.delete_ResultCollection
    __del__ = lambda self: None

    def getResult(self, id):
        return _quality_metric_set8_.ResultCollection_getResult(self, id)
ResultCollection_swigregister = _quality_metric_set8_.ResultCollection_swigregister
ResultCollection_swigregister(ResultCollection)

class InputDataCollection(daal.algorithms.quality_metric_set.InputDataCollection):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.InputDataCollection]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputDataCollection, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.InputDataCollection]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, InputDataCollection, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _quality_metric_set8_.new_InputDataCollection()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _quality_metric_set8_.delete_InputDataCollection
    __del__ = lambda self: None

    def getInput(self, id):
        return _quality_metric_set8_.InputDataCollection_getInput(self, id)
InputDataCollection_swigregister = _quality_metric_set8_.InputDataCollection_swigregister
InputDataCollection_swigregister(InputDataCollection)

class Batch(daal.algorithms.quality_metric_set.Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.quality_metric_set.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch, name)
    __repr__ = _swig_repr

    def __init__(self, useDefaultMetrics=True):
        this = _quality_metric_set8_.new_Batch(useDefaultMetrics)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _quality_metric_set8_.delete_Batch
    __del__ = lambda self: None

    def getResultCollection(self):
        return _quality_metric_set8_.Batch_getResultCollection(self)

    def getInputDataCollection(self):
        return _quality_metric_set8_.Batch_getInputDataCollection(self)

    def compute(self):
        return _quality_metric_set8_.Batch_compute(self)
Batch_swigregister = _quality_metric_set8_.Batch_swigregister
Batch_swigregister(Batch)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


