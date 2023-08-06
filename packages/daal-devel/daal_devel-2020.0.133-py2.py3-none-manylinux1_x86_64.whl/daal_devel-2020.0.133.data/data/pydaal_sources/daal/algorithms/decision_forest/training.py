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
            fp, pathname, description = imp.find_module('_training6_', [dirname(__file__)])
        except ImportError:
            import _training6_
            return _training6_
        if fp is not None:
            try:
                _mod = imp.load_module('_training6_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training6_ = swig_import_helper()
    del swig_import_helper
else:
    import _training6_
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


import daal.algorithms.decision_forest
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.engines.mt19937
import daal.algorithms.engines

_training6_.none_swigconstant(_training6_)
none = _training6_.none

_training6_.MDI_swigconstant(_training6_)
MDI = _training6_.MDI

_training6_.MDA_Raw_swigconstant(_training6_)
MDA_Raw = _training6_.MDA_Raw

_training6_.MDA_Scaled_swigconstant(_training6_)
MDA_Scaled = _training6_.MDA_Scaled

_training6_.computeOutOfBagError_swigconstant(_training6_)
computeOutOfBagError = _training6_.computeOutOfBagError

_training6_.computeOutOfBagErrorPerObservation_swigconstant(_training6_)
computeOutOfBagErrorPerObservation = _training6_.computeOutOfBagErrorPerObservation
class Parameter(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _training6_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["nTrees"] = _training6_.Parameter_nTrees_set
    __swig_getmethods__["nTrees"] = _training6_.Parameter_nTrees_get
    if _newclass:
        nTrees = _swig_property(_training6_.Parameter_nTrees_get, _training6_.Parameter_nTrees_set)
    __swig_setmethods__["observationsPerTreeFraction"] = _training6_.Parameter_observationsPerTreeFraction_set
    __swig_getmethods__["observationsPerTreeFraction"] = _training6_.Parameter_observationsPerTreeFraction_get
    if _newclass:
        observationsPerTreeFraction = _swig_property(_training6_.Parameter_observationsPerTreeFraction_get, _training6_.Parameter_observationsPerTreeFraction_set)
    __swig_setmethods__["featuresPerNode"] = _training6_.Parameter_featuresPerNode_set
    __swig_getmethods__["featuresPerNode"] = _training6_.Parameter_featuresPerNode_get
    if _newclass:
        featuresPerNode = _swig_property(_training6_.Parameter_featuresPerNode_get, _training6_.Parameter_featuresPerNode_set)
    __swig_setmethods__["maxTreeDepth"] = _training6_.Parameter_maxTreeDepth_set
    __swig_getmethods__["maxTreeDepth"] = _training6_.Parameter_maxTreeDepth_get
    if _newclass:
        maxTreeDepth = _swig_property(_training6_.Parameter_maxTreeDepth_get, _training6_.Parameter_maxTreeDepth_set)
    __swig_setmethods__["minObservationsInLeafNode"] = _training6_.Parameter_minObservationsInLeafNode_set
    __swig_getmethods__["minObservationsInLeafNode"] = _training6_.Parameter_minObservationsInLeafNode_get
    if _newclass:
        minObservationsInLeafNode = _swig_property(_training6_.Parameter_minObservationsInLeafNode_get, _training6_.Parameter_minObservationsInLeafNode_set)
    __swig_setmethods__["seed"] = _training6_.Parameter_seed_set
    __swig_getmethods__["seed"] = _training6_.Parameter_seed_get
    if _newclass:
        seed = _swig_property(_training6_.Parameter_seed_get, _training6_.Parameter_seed_set)
    __swig_setmethods__["engine"] = _training6_.Parameter_engine_set
    __swig_getmethods__["engine"] = _training6_.Parameter_engine_get
    if _newclass:
        engine = _swig_property(_training6_.Parameter_engine_get, _training6_.Parameter_engine_set)
    __swig_setmethods__["impurityThreshold"] = _training6_.Parameter_impurityThreshold_set
    __swig_getmethods__["impurityThreshold"] = _training6_.Parameter_impurityThreshold_get
    if _newclass:
        impurityThreshold = _swig_property(_training6_.Parameter_impurityThreshold_get, _training6_.Parameter_impurityThreshold_set)
    __swig_setmethods__["varImportance"] = _training6_.Parameter_varImportance_set
    __swig_getmethods__["varImportance"] = _training6_.Parameter_varImportance_get
    if _newclass:
        varImportance = _swig_property(_training6_.Parameter_varImportance_get, _training6_.Parameter_varImportance_set)
    __swig_setmethods__["resultsToCompute"] = _training6_.Parameter_resultsToCompute_set
    __swig_getmethods__["resultsToCompute"] = _training6_.Parameter_resultsToCompute_get
    if _newclass:
        resultsToCompute = _swig_property(_training6_.Parameter_resultsToCompute_get, _training6_.Parameter_resultsToCompute_set)
    __swig_setmethods__["memorySavingMode"] = _training6_.Parameter_memorySavingMode_set
    __swig_getmethods__["memorySavingMode"] = _training6_.Parameter_memorySavingMode_get
    if _newclass:
        memorySavingMode = _swig_property(_training6_.Parameter_memorySavingMode_get, _training6_.Parameter_memorySavingMode_set)
    __swig_setmethods__["bootstrap"] = _training6_.Parameter_bootstrap_set
    __swig_getmethods__["bootstrap"] = _training6_.Parameter_bootstrap_get
    if _newclass:
        bootstrap = _swig_property(_training6_.Parameter_bootstrap_get, _training6_.Parameter_bootstrap_set)
    __swig_destroy__ = _training6_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _training6_.Parameter_swigregister
Parameter_swigregister(Parameter)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


