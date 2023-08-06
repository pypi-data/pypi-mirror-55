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
            fp, pathname, description = imp.find_module('_training17_', [dirname(__file__)])
        except ImportError:
            import _training17_
            return _training17_
        if fp is not None:
            try:
                _mod = imp.load_module('_training17_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training17_ = swig_import_helper()
    del swig_import_helper
else:
    import _training17_
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


import daal.algorithms.logitboost
import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.boosting
import daal.algorithms.boosting.training
import daal.algorithms.classifier.training

_training17_.friedman_swigconstant(_training17_)
friedman = _training17_.friedman

_training17_.defaultDense_swigconstant(_training17_)
defaultDense = _training17_.defaultDense
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
    __swig_getmethods__["serializationTag"] = lambda x: _training17_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training17_.Result_serializationTag)

    def getSerializationTag(self):
        return _training17_.Result_getSerializationTag(self)
    __swig_destroy__ = _training17_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _training17_.Result_get(self, id)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training17_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training17_.Result_allocate_Float32(self, input, parameter, method)


    def __init__(self):
        this = _training17_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
Result_swigregister = _training17_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training17_.Result_serializationTag()
Result_serializationTag = _training17_.Result_serializationTag

class interface2_Result(daal.algorithms.classifier.training.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, interface2_Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, interface2_Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training17_.interface2_Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training17_.interface2_Result_serializationTag)

    def getSerializationTag(self):
        return _training17_.interface2_Result_getSerializationTag(self)
    __swig_destroy__ = _training17_.delete_interface2_Result
    __del__ = lambda self: None

    def get(self, id):
        return _training17_.interface2_Result_get(self, id)

    def __init__(self):
        this = _training17_.new_interface2_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
interface2_Result_swigregister = _training17_.interface2_Result_swigregister
interface2_Result_swigregister(interface2_Result)

def interface2_Result_serializationTag():
    return _training17_.interface2_Result_serializationTag()
interface2_Result_serializationTag = _training17_.interface2_Result_serializationTag

class Batch_Float64Friedman(daal.algorithms.boosting.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.boosting.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Friedman, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.boosting.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Friedman, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training17_.Batch_Float64Friedman_parameter_set
    __swig_getmethods__["parameter"] = _training17_.Batch_Float64Friedman_parameter_get
    if _newclass:
        parameter = _swig_property(_training17_.Batch_Float64Friedman_parameter_get, _training17_.Batch_Float64Friedman_parameter_set)
    __swig_setmethods__["input"] = _training17_.Batch_Float64Friedman_input_set
    __swig_getmethods__["input"] = _training17_.Batch_Float64Friedman_input_get
    if _newclass:
        input = _swig_property(_training17_.Batch_Float64Friedman_input_get, _training17_.Batch_Float64Friedman_input_set)

    def __init__(self, *args):
        this = _training17_.new_Batch_Float64Friedman(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training17_.delete_Batch_Float64Friedman
    __del__ = lambda self: None

    def getInput(self):
        return _training17_.Batch_Float64Friedman_getInput(self)

    def getMethod(self):
        return _training17_.Batch_Float64Friedman_getMethod(self)

    def getResult(self):
        return _training17_.Batch_Float64Friedman_getResult(self)

    def resetResult(self):
        return _training17_.Batch_Float64Friedman_resetResult(self)

    def clone(self):
        return _training17_.Batch_Float64Friedman_clone(self)

    def compute(self):
        return _training17_.Batch_Float64Friedman_compute(self)
Batch_Float64Friedman_swigregister = _training17_.Batch_Float64Friedman_swigregister
Batch_Float64Friedman_swigregister(Batch_Float64Friedman)

class Batch_Float32Friedman(daal.algorithms.boosting.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.boosting.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Friedman, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.boosting.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Friedman, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training17_.Batch_Float32Friedman_parameter_set
    __swig_getmethods__["parameter"] = _training17_.Batch_Float32Friedman_parameter_get
    if _newclass:
        parameter = _swig_property(_training17_.Batch_Float32Friedman_parameter_get, _training17_.Batch_Float32Friedman_parameter_set)
    __swig_setmethods__["input"] = _training17_.Batch_Float32Friedman_input_set
    __swig_getmethods__["input"] = _training17_.Batch_Float32Friedman_input_get
    if _newclass:
        input = _swig_property(_training17_.Batch_Float32Friedman_input_get, _training17_.Batch_Float32Friedman_input_set)

    def __init__(self, *args):
        this = _training17_.new_Batch_Float32Friedman(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training17_.delete_Batch_Float32Friedman
    __del__ = lambda self: None

    def getInput(self):
        return _training17_.Batch_Float32Friedman_getInput(self)

    def getMethod(self):
        return _training17_.Batch_Float32Friedman_getMethod(self)

    def getResult(self):
        return _training17_.Batch_Float32Friedman_getResult(self)

    def resetResult(self):
        return _training17_.Batch_Float32Friedman_resetResult(self)

    def clone(self):
        return _training17_.Batch_Float32Friedman_clone(self)

    def compute(self):
        return _training17_.Batch_Float32Friedman_compute(self)
Batch_Float32Friedman_swigregister = _training17_.Batch_Float32Friedman_swigregister
Batch_Float32Friedman_swigregister(Batch_Float32Friedman)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == friedman:
                return Batch_Float64Friedman(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == friedman:
                return Batch_Float32Friedman(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


