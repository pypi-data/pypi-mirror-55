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
            fp, pathname, description = imp.find_module('_training9_', [dirname(__file__)])
        except ImportError:
            import _training9_
            return _training9_
        if fp is not None:
            try:
                _mod = imp.load_module('_training9_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training9_ = swig_import_helper()
    del swig_import_helper
else:
    import _training9_
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


import daal.algorithms.gbt.classification
import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.gbt
import daal.algorithms.gbt.training
import daal.algorithms.engines.mt19937
import daal.algorithms.engines
import daal.algorithms.classifier.training

_training9_.xboost_swigconstant(_training9_)
xboost = _training9_.xboost

_training9_.defaultDense_swigconstant(_training9_)
defaultDense = _training9_.defaultDense

_training9_.crossEntropy_swigconstant(_training9_)
crossEntropy = _training9_.crossEntropy

_training9_.custom_swigconstant(_training9_)
custom = _training9_.custom

_training9_.variableImportanceWeight_swigconstant(_training9_)
variableImportanceWeight = _training9_.variableImportanceWeight

_training9_.variableImportanceTotalCover_swigconstant(_training9_)
variableImportanceTotalCover = _training9_.variableImportanceTotalCover

_training9_.variableImportanceCover_swigconstant(_training9_)
variableImportanceCover = _training9_.variableImportanceCover

_training9_.variableImportanceTotalGain_swigconstant(_training9_)
variableImportanceTotalGain = _training9_.variableImportanceTotalGain

_training9_.variableImportanceGain_swigconstant(_training9_)
variableImportanceGain = _training9_.variableImportanceGain

_training9_.lastOptionalResultNumericTableId_swigconstant(_training9_)
lastOptionalResultNumericTableId = _training9_.lastOptionalResultNumericTableId
class Parameter(daal.algorithms.classifier.Parameter, daal.algorithms.gbt.training.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter, daal.algorithms.gbt.training.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.Parameter, daal.algorithms.gbt.training.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses):
        this = _training9_.new_Parameter(nClasses)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _training9_.Parameter_check(self)
    __swig_setmethods__["loss"] = _training9_.Parameter_loss_set
    __swig_getmethods__["loss"] = _training9_.Parameter_loss_get
    if _newclass:
        loss = _swig_property(_training9_.Parameter_loss_get, _training9_.Parameter_loss_set)
    __swig_destroy__ = _training9_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _training9_.Parameter_swigregister
Parameter_swigregister(Parameter)

class interface2_Parameter(daal.algorithms.classifier.interface2_Parameter, daal.algorithms.gbt.training.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter, daal.algorithms.gbt.training.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.interface2_Parameter, daal.algorithms.gbt.training.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, nClasses):
        this = _training9_.new_interface2_Parameter(nClasses)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _training9_.interface2_Parameter_check(self)
    __swig_setmethods__["loss"] = _training9_.interface2_Parameter_loss_set
    __swig_getmethods__["loss"] = _training9_.interface2_Parameter_loss_get
    if _newclass:
        loss = _swig_property(_training9_.interface2_Parameter_loss_get, _training9_.interface2_Parameter_loss_set)
    __swig_destroy__ = _training9_.delete_interface2_Parameter
    __del__ = lambda self: None
interface2_Parameter_swigregister = _training9_.interface2_Parameter_swigregister
interface2_Parameter_swigregister(interface2_Parameter)

class Result(daal.algorithms.classifier.training.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training9_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training9_.Result_serializationTag)

    def getSerializationTag(self):
        return _training9_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training9_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training9_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _training9_.Result_get(self, id)

    def getOptionalData(self, id):
        return _training9_.Result_getOptionalData(self, id)

    def set(self, *args):
        return _training9_.Result_set(self, *args)

    def check(self, input, par, method):
        return _training9_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training9_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training9_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _training9_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training9_.Result_serializationTag()
Result_serializationTag = _training9_.Result_serializationTag

class Batch_Float64Xboost(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Xboost, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Xboost, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training9_.Batch_Float64Xboost_input_set
    __swig_getmethods__["input"] = _training9_.Batch_Float64Xboost_input_get
    if _newclass:
        input = _swig_property(_training9_.Batch_Float64Xboost_input_get, _training9_.Batch_Float64Xboost_input_set)

    def __init__(self, *args):
        this = _training9_.new_Batch_Float64Xboost(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training9_.delete_Batch_Float64Xboost
    __del__ = lambda self: None

    def parameter(self, *args):
        return _training9_.Batch_Float64Xboost_parameter(self, *args)

    def getInput(self):
        return _training9_.Batch_Float64Xboost_getInput(self)

    def getMethod(self):
        return _training9_.Batch_Float64Xboost_getMethod(self)

    def getResult(self):
        return _training9_.Batch_Float64Xboost_getResult(self)

    def resetResult(self):
        return _training9_.Batch_Float64Xboost_resetResult(self)

    def clone(self):
        return _training9_.Batch_Float64Xboost_clone(self)

    def checkComputeParams(self):
        return _training9_.Batch_Float64Xboost_checkComputeParams(self)

    def compute(self):
        return _training9_.Batch_Float64Xboost_compute(self)
Batch_Float64Xboost_swigregister = _training9_.Batch_Float64Xboost_swigregister
Batch_Float64Xboost_swigregister(Batch_Float64Xboost)

class Batch_Float32Xboost(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Xboost, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Xboost, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _training9_.Batch_Float32Xboost_input_set
    __swig_getmethods__["input"] = _training9_.Batch_Float32Xboost_input_get
    if _newclass:
        input = _swig_property(_training9_.Batch_Float32Xboost_input_get, _training9_.Batch_Float32Xboost_input_set)

    def __init__(self, *args):
        this = _training9_.new_Batch_Float32Xboost(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training9_.delete_Batch_Float32Xboost
    __del__ = lambda self: None

    def parameter(self, *args):
        return _training9_.Batch_Float32Xboost_parameter(self, *args)

    def getInput(self):
        return _training9_.Batch_Float32Xboost_getInput(self)

    def getMethod(self):
        return _training9_.Batch_Float32Xboost_getMethod(self)

    def getResult(self):
        return _training9_.Batch_Float32Xboost_getResult(self)

    def resetResult(self):
        return _training9_.Batch_Float32Xboost_resetResult(self)

    def clone(self):
        return _training9_.Batch_Float32Xboost_clone(self)

    def checkComputeParams(self):
        return _training9_.Batch_Float32Xboost_checkComputeParams(self)

    def compute(self):
        return _training9_.Batch_Float32Xboost_compute(self)
Batch_Float32Xboost_swigregister = _training9_.Batch_Float32Xboost_swigregister
Batch_Float32Xboost_swigregister(Batch_Float32Xboost)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == xboost:
                return Batch_Float64Xboost(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == xboost:
                return Batch_Float32Xboost(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


