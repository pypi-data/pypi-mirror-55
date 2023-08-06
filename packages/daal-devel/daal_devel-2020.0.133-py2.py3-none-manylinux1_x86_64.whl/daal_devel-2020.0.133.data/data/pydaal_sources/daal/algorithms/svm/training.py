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
            fp, pathname, description = imp.find_module('_training24_', [dirname(__file__)])
        except ImportError:
            import _training24_
            return _training24_
        if fp is not None:
            try:
                _mod = imp.load_module('_training24_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training24_ = swig_import_helper()
    del swig_import_helper
else:
    import _training24_
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
import daal.algorithms.classifier.training

_training24_.boser_swigconstant(_training24_)
boser = _training24_.boser

_training24_.defaultDense_swigconstant(_training24_)
defaultDense = _training24_.defaultDense
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
    __swig_getmethods__["serializationTag"] = lambda x: _training24_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training24_.Result_serializationTag)

    def getSerializationTag(self):
        return _training24_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training24_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training24_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _training24_.Result_get(self, id)

    def check(self, input, parameter, method):
        return _training24_.Result_check(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training24_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training24_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _training24_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training24_.Result_serializationTag()
Result_serializationTag = _training24_.Result_serializationTag

class Batch_Float64Boser(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Boser, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Boser, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training24_.Batch_Float64Boser_parameter_set
    __swig_getmethods__["parameter"] = _training24_.Batch_Float64Boser_parameter_get
    if _newclass:
        parameter = _swig_property(_training24_.Batch_Float64Boser_parameter_get, _training24_.Batch_Float64Boser_parameter_set)
    __swig_setmethods__["input"] = _training24_.Batch_Float64Boser_input_set
    __swig_getmethods__["input"] = _training24_.Batch_Float64Boser_input_get
    if _newclass:
        input = _swig_property(_training24_.Batch_Float64Boser_input_get, _training24_.Batch_Float64Boser_input_set)

    def __init__(self, *args):
        this = _training24_.new_Batch_Float64Boser(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training24_.delete_Batch_Float64Boser
    __del__ = lambda self: None

    def getInput(self):
        return _training24_.Batch_Float64Boser_getInput(self)

    def getMethod(self):
        return _training24_.Batch_Float64Boser_getMethod(self)

    def getResult(self):
        return _training24_.Batch_Float64Boser_getResult(self)

    def resetResult(self):
        return _training24_.Batch_Float64Boser_resetResult(self)

    def clone(self):
        return _training24_.Batch_Float64Boser_clone(self)

    def compute(self):
        return _training24_.Batch_Float64Boser_compute(self)
Batch_Float64Boser_swigregister = _training24_.Batch_Float64Boser_swigregister
Batch_Float64Boser_swigregister(Batch_Float64Boser)

class Batch_Float32Boser(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Boser, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Boser, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training24_.Batch_Float32Boser_parameter_set
    __swig_getmethods__["parameter"] = _training24_.Batch_Float32Boser_parameter_get
    if _newclass:
        parameter = _swig_property(_training24_.Batch_Float32Boser_parameter_get, _training24_.Batch_Float32Boser_parameter_set)
    __swig_setmethods__["input"] = _training24_.Batch_Float32Boser_input_set
    __swig_getmethods__["input"] = _training24_.Batch_Float32Boser_input_get
    if _newclass:
        input = _swig_property(_training24_.Batch_Float32Boser_input_get, _training24_.Batch_Float32Boser_input_set)

    def __init__(self, *args):
        this = _training24_.new_Batch_Float32Boser(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training24_.delete_Batch_Float32Boser
    __del__ = lambda self: None

    def getInput(self):
        return _training24_.Batch_Float32Boser_getInput(self)

    def getMethod(self):
        return _training24_.Batch_Float32Boser_getMethod(self)

    def getResult(self):
        return _training24_.Batch_Float32Boser_getResult(self)

    def resetResult(self):
        return _training24_.Batch_Float32Boser_resetResult(self)

    def clone(self):
        return _training24_.Batch_Float32Boser_clone(self)

    def compute(self):
        return _training24_.Batch_Float32Boser_compute(self)
Batch_Float32Boser_swigregister = _training24_.Batch_Float32Boser_swigregister
Batch_Float32Boser_swigregister(Batch_Float32Boser)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == boser:
                return Batch_Float64Boser(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == boser:
                return Batch_Float32Boser(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


