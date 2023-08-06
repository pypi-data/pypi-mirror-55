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
            fp, pathname, description = imp.find_module('_training19_', [dirname(__file__)])
        except ImportError:
            import _training19_
            return _training19_
        if fp is not None:
            try:
                _mod = imp.load_module('_training19_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _training19_ = swig_import_helper()
    del swig_import_helper
else:
    import _training19_
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


import daal.algorithms.multinomial_naive_bayes
import daal.algorithms.classifier
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.classifier.training

_training19_.defaultDense_swigconstant(_training19_)
defaultDense = _training19_.defaultDense

_training19_.fastCSR_swigconstant(_training19_)
fastCSR = _training19_.fastCSR

_training19_.partialModels_swigconstant(_training19_)
partialModels = _training19_.partialModels

_training19_.lastStep2MasterInputId_swigconstant(_training19_)
lastStep2MasterInputId = _training19_.lastStep2MasterInputId
class PartialResult(daal.algorithms.classifier.training.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _training19_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training19_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _training19_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _training19_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_PartialResult
    __del__ = lambda self: None

    def get(self, id):
        return _training19_.PartialResult_get(self, id)

    def getNumberOfFeatures(self):
        return _training19_.PartialResult_getNumberOfFeatures(self)

    def check(self, *args):
        return _training19_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training19_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training19_.PartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _training19_.PartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _training19_.PartialResult_initialize_Float32(self, input, parameter, method)

PartialResult_swigregister = _training19_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _training19_.PartialResult_serializationTag()
PartialResult_serializationTag = _training19_.PartialResult_serializationTag

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
    __swig_getmethods__["serializationTag"] = lambda x: _training19_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_training19_.Result_serializationTag)

    def getSerializationTag(self):
        return _training19_.Result_getSerializationTag(self)

    def __init__(self):
        this = _training19_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _training19_.Result_get(self, id)

    def check(self, *args):
        return _training19_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _training19_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _training19_.Result_allocate_Float32(self, *args)

Result_swigregister = _training19_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _training19_.Result_serializationTag()
Result_serializationTag = _training19_.Result_serializationTag

class DistributedInput(daal.algorithms.classifier.training.InputIface):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_DistributedInput(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_DistributedInput
    __del__ = lambda self: None

    def getNumberOfFeatures(self):
        return _training19_.DistributedInput_getNumberOfFeatures(self)

    def get(self, id):
        return _training19_.DistributedInput_get(self, id)

    def add(self, id, partialResult):
        return _training19_.DistributedInput_add(self, id, partialResult)

    def set(self, id, value):
        return _training19_.DistributedInput_set(self, id, value)

    def check(self, parameter, method):
        return _training19_.DistributedInput_check(self, parameter, method)
DistributedInput_swigregister = _training19_.DistributedInput_swigregister
DistributedInput_swigregister(DistributedInput)

class Batch_Float64DefaultDense(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Batch_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Batch_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Batch_Float64DefaultDense_parameter_get, _training19_.Batch_Float64DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _training19_.Batch_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _training19_.Batch_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training19_.Batch_Float64DefaultDense_input_get, _training19_.Batch_Float64DefaultDense_input_set)

    def __init__(self, *args):
        this = _training19_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def getInput(self):
        return _training19_.Batch_Float64DefaultDense_getInput(self)

    def getMethod(self):
        return _training19_.Batch_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _training19_.Batch_Float64DefaultDense_getResult(self)

    def resetResult(self):
        return _training19_.Batch_Float64DefaultDense_resetResult(self)

    def clone(self):
        return _training19_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _training19_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _training19_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float64FastCSR(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Batch_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Batch_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Batch_Float64FastCSR_parameter_get, _training19_.Batch_Float64FastCSR_parameter_set)
    __swig_setmethods__["input"] = _training19_.Batch_Float64FastCSR_input_set
    __swig_getmethods__["input"] = _training19_.Batch_Float64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training19_.Batch_Float64FastCSR_input_get, _training19_.Batch_Float64FastCSR_input_set)

    def __init__(self, *args):
        this = _training19_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None

    def getInput(self):
        return _training19_.Batch_Float64FastCSR_getInput(self)

    def getMethod(self):
        return _training19_.Batch_Float64FastCSR_getMethod(self)

    def getResult(self):
        return _training19_.Batch_Float64FastCSR_getResult(self)

    def resetResult(self):
        return _training19_.Batch_Float64FastCSR_resetResult(self)

    def clone(self):
        return _training19_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _training19_.Batch_Float64FastCSR_compute(self)
Batch_Float64FastCSR_swigregister = _training19_.Batch_Float64FastCSR_swigregister
Batch_Float64FastCSR_swigregister(Batch_Float64FastCSR)

class Batch_Float32DefaultDense(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Batch_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Batch_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Batch_Float32DefaultDense_parameter_get, _training19_.Batch_Float32DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _training19_.Batch_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _training19_.Batch_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training19_.Batch_Float32DefaultDense_input_get, _training19_.Batch_Float32DefaultDense_input_set)

    def __init__(self, *args):
        this = _training19_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def getInput(self):
        return _training19_.Batch_Float32DefaultDense_getInput(self)

    def getMethod(self):
        return _training19_.Batch_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _training19_.Batch_Float32DefaultDense_getResult(self)

    def resetResult(self):
        return _training19_.Batch_Float32DefaultDense_resetResult(self)

    def clone(self):
        return _training19_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _training19_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _training19_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Batch_Float32FastCSR(daal.algorithms.classifier.training.Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Batch_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Batch_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Batch_Float32FastCSR_parameter_get, _training19_.Batch_Float32FastCSR_parameter_set)
    __swig_setmethods__["input"] = _training19_.Batch_Float32FastCSR_input_set
    __swig_getmethods__["input"] = _training19_.Batch_Float32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training19_.Batch_Float32FastCSR_input_get, _training19_.Batch_Float32FastCSR_input_set)

    def __init__(self, *args):
        this = _training19_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None

    def getInput(self):
        return _training19_.Batch_Float32FastCSR_getInput(self)

    def getMethod(self):
        return _training19_.Batch_Float32FastCSR_getMethod(self)

    def getResult(self):
        return _training19_.Batch_Float32FastCSR_getResult(self)

    def resetResult(self):
        return _training19_.Batch_Float32FastCSR_resetResult(self)

    def clone(self):
        return _training19_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _training19_.Batch_Float32FastCSR_compute(self)
Batch_Float32FastCSR_swigregister = _training19_.Batch_Float32FastCSR_swigregister
Batch_Float32FastCSR_swigregister(Batch_Float32FastCSR)

class Online_Float64DefaultDense(daal.algorithms.classifier.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Online_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Online_Float64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Online_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _training19_.Online_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _training19_.Online_Float64DefaultDense_setResult(self, result)

    def resetResult(self):
        return _training19_.Online_Float64DefaultDense_resetResult(self)

    def getPartialResult(self):
        return _training19_.Online_Float64DefaultDense_getPartialResult(self)

    def clone(self):
        return _training19_.Online_Float64DefaultDense_clone(self)
    __swig_setmethods__["parameter"] = _training19_.Online_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Online_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Online_Float64DefaultDense_parameter_get, _training19_.Online_Float64DefaultDense_parameter_set)

    def compute(self):
        return _training19_.Online_Float64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Online_Float64DefaultDense_finalizeCompute(self)
Online_Float64DefaultDense_swigregister = _training19_.Online_Float64DefaultDense_swigregister
Online_Float64DefaultDense_swigregister(Online_Float64DefaultDense)

class Online_Float64FastCSR(daal.algorithms.classifier.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Online_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Online_Float64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Online_Float64FastCSR_getMethod(self)

    def getResult(self):
        return _training19_.Online_Float64FastCSR_getResult(self)

    def setResult(self, result):
        return _training19_.Online_Float64FastCSR_setResult(self, result)

    def resetResult(self):
        return _training19_.Online_Float64FastCSR_resetResult(self)

    def getPartialResult(self):
        return _training19_.Online_Float64FastCSR_getPartialResult(self)

    def clone(self):
        return _training19_.Online_Float64FastCSR_clone(self)
    __swig_setmethods__["parameter"] = _training19_.Online_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Online_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Online_Float64FastCSR_parameter_get, _training19_.Online_Float64FastCSR_parameter_set)

    def compute(self):
        return _training19_.Online_Float64FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Online_Float64FastCSR_finalizeCompute(self)
Online_Float64FastCSR_swigregister = _training19_.Online_Float64FastCSR_swigregister
Online_Float64FastCSR_swigregister(Online_Float64FastCSR)

class Online_Float32DefaultDense(daal.algorithms.classifier.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Online_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Online_Float32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Online_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _training19_.Online_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _training19_.Online_Float32DefaultDense_setResult(self, result)

    def resetResult(self):
        return _training19_.Online_Float32DefaultDense_resetResult(self)

    def getPartialResult(self):
        return _training19_.Online_Float32DefaultDense_getPartialResult(self)

    def clone(self):
        return _training19_.Online_Float32DefaultDense_clone(self)
    __swig_setmethods__["parameter"] = _training19_.Online_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Online_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Online_Float32DefaultDense_parameter_get, _training19_.Online_Float32DefaultDense_parameter_set)

    def compute(self):
        return _training19_.Online_Float32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Online_Float32DefaultDense_finalizeCompute(self)
Online_Float32DefaultDense_swigregister = _training19_.Online_Float32DefaultDense_swigregister
Online_Float32DefaultDense_swigregister(Online_Float32DefaultDense)

class Online_Float32FastCSR(daal.algorithms.classifier.training.Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.classifier.training.Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Online_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Online_Float32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Online_Float32FastCSR_getMethod(self)

    def getResult(self):
        return _training19_.Online_Float32FastCSR_getResult(self)

    def setResult(self, result):
        return _training19_.Online_Float32FastCSR_setResult(self, result)

    def resetResult(self):
        return _training19_.Online_Float32FastCSR_resetResult(self)

    def getPartialResult(self):
        return _training19_.Online_Float32FastCSR_getPartialResult(self)

    def clone(self):
        return _training19_.Online_Float32FastCSR_clone(self)
    __swig_setmethods__["parameter"] = _training19_.Online_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Online_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Online_Float32FastCSR_parameter_get, _training19_.Online_Float32FastCSR_parameter_set)

    def compute(self):
        return _training19_.Online_Float32FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Online_Float32FastCSR_finalizeCompute(self)
Online_Float32FastCSR_swigregister = _training19_.Online_Float32FastCSR_swigregister
Online_Float32FastCSR_swigregister(Online_Float32FastCSR)

class Distributed_Step1LocalFloat64DefaultDense(Online_Float64DefaultDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64DefaultDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64DefaultDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step1LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _training19_.Distributed_Step1LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _training19_.Distributed_Step1LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step1LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _training19_.delete_Distributed_Step1LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DefaultDense_swigregister = _training19_.Distributed_Step1LocalFloat64DefaultDense_swigregister
Distributed_Step1LocalFloat64DefaultDense_swigregister(Distributed_Step1LocalFloat64DefaultDense)

class Distributed_Step1LocalFloat64FastCSR(Online_Float64FastCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64FastCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64FastCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step1LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _training19_.Distributed_Step1LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _training19_.Distributed_Step1LocalFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step1LocalFloat64FastCSR_finalizeCompute(self)
    __swig_destroy__ = _training19_.delete_Distributed_Step1LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64FastCSR_swigregister = _training19_.Distributed_Step1LocalFloat64FastCSR_swigregister
Distributed_Step1LocalFloat64FastCSR_swigregister(Distributed_Step1LocalFloat64FastCSR)

class Distributed_Step1LocalFloat32DefaultDense(Online_Float32DefaultDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32DefaultDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32DefaultDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step1LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _training19_.Distributed_Step1LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _training19_.Distributed_Step1LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step1LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _training19_.delete_Distributed_Step1LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DefaultDense_swigregister = _training19_.Distributed_Step1LocalFloat32DefaultDense_swigregister
Distributed_Step1LocalFloat32DefaultDense_swigregister(Distributed_Step1LocalFloat32DefaultDense)

class Distributed_Step1LocalFloat32FastCSR(Online_Float32FastCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32FastCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32FastCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step1LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _training19_.Distributed_Step1LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _training19_.Distributed_Step1LocalFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step1LocalFloat32FastCSR_finalizeCompute(self)
    __swig_destroy__ = _training19_.delete_Distributed_Step1LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32FastCSR_swigregister = _training19_.Distributed_Step1LocalFloat32FastCSR_swigregister
Distributed_Step1LocalFloat32FastCSR_swigregister(Distributed_Step1LocalFloat32FastCSR)

class Distributed_Step2MasterFloat64DefaultDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Distributed_Step2MasterFloat64DefaultDense_parameter_get, _training19_.Distributed_Step2MasterFloat64DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _training19_.Distributed_Step2MasterFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _training19_.Distributed_Step2MasterFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training19_.Distributed_Step2MasterFloat64DefaultDense_input_get, _training19_.Distributed_Step2MasterFloat64DefaultDense_input_set)

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step2MasterFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Distributed_Step2MasterFloat64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_getPartialResult(self)

    def setResult(self, result):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_setResult(self, result)

    def getResult(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_getResult(self)

    def checkFinalizeComputeParams(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_clone(self)

    def compute(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step2MasterFloat64DefaultDense_finalizeCompute(self)
Distributed_Step2MasterFloat64DefaultDense_swigregister = _training19_.Distributed_Step2MasterFloat64DefaultDense_swigregister
Distributed_Step2MasterFloat64DefaultDense_swigregister(Distributed_Step2MasterFloat64DefaultDense)

class Distributed_Step2MasterFloat64FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Distributed_Step2MasterFloat64FastCSR_parameter_get, _training19_.Distributed_Step2MasterFloat64FastCSR_parameter_set)
    __swig_setmethods__["input"] = _training19_.Distributed_Step2MasterFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _training19_.Distributed_Step2MasterFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_training19_.Distributed_Step2MasterFloat64FastCSR_input_get, _training19_.Distributed_Step2MasterFloat64FastCSR_input_set)

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step2MasterFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Distributed_Step2MasterFloat64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_getPartialResult(self)

    def setResult(self, result):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_setResult(self, result)

    def getResult(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_getResult(self)

    def checkFinalizeComputeParams(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_clone(self)

    def compute(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step2MasterFloat64FastCSR_finalizeCompute(self)
Distributed_Step2MasterFloat64FastCSR_swigregister = _training19_.Distributed_Step2MasterFloat64FastCSR_swigregister
Distributed_Step2MasterFloat64FastCSR_swigregister(Distributed_Step2MasterFloat64FastCSR)

class Distributed_Step2MasterFloat32DefaultDense(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Distributed_Step2MasterFloat32DefaultDense_parameter_get, _training19_.Distributed_Step2MasterFloat32DefaultDense_parameter_set)
    __swig_setmethods__["input"] = _training19_.Distributed_Step2MasterFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _training19_.Distributed_Step2MasterFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_training19_.Distributed_Step2MasterFloat32DefaultDense_input_get, _training19_.Distributed_Step2MasterFloat32DefaultDense_input_set)

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step2MasterFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Distributed_Step2MasterFloat32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_getPartialResult(self)

    def setResult(self, result):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_setResult(self, result)

    def getResult(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_getResult(self)

    def checkFinalizeComputeParams(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_checkFinalizeComputeParams(self)

    def clone(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_clone(self)

    def compute(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step2MasterFloat32DefaultDense_finalizeCompute(self)
Distributed_Step2MasterFloat32DefaultDense_swigregister = _training19_.Distributed_Step2MasterFloat32DefaultDense_swigregister
Distributed_Step2MasterFloat32DefaultDense_swigregister(Distributed_Step2MasterFloat32DefaultDense)

class Distributed_Step2MasterFloat32FastCSR(daal.algorithms.Training_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Training_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _training19_.Distributed_Step2MasterFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_training19_.Distributed_Step2MasterFloat32FastCSR_parameter_get, _training19_.Distributed_Step2MasterFloat32FastCSR_parameter_set)
    __swig_setmethods__["input"] = _training19_.Distributed_Step2MasterFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _training19_.Distributed_Step2MasterFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_training19_.Distributed_Step2MasterFloat32FastCSR_input_get, _training19_.Distributed_Step2MasterFloat32FastCSR_input_set)

    def __init__(self, *args):
        this = _training19_.new_Distributed_Step2MasterFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _training19_.delete_Distributed_Step2MasterFloat32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_getMethod(self)

    def setPartialResult(self, partialResult):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_getPartialResult(self)

    def setResult(self, result):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_setResult(self, result)

    def getResult(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_getResult(self)

    def checkFinalizeComputeParams(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_checkFinalizeComputeParams(self)

    def clone(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_clone(self)

    def compute(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _training19_.Distributed_Step2MasterFloat32FastCSR_finalizeCompute(self)
Distributed_Step2MasterFloat32FastCSR_swigregister = _training19_.Distributed_Step2MasterFloat32FastCSR_swigregister
Distributed_Step2MasterFloat32FastCSR_swigregister(Distributed_Step2MasterFloat32FastCSR)

from numpy import float64, float32, intc

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat64DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat32DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat32FastCSR(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat64DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat64FastCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat32DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float64FastCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Batch")

class Online(object):
    r"""Factory class for different types of Online."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Online_Float64FastCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Online_Float32FastCSR(*args)

        raise RuntimeError("No appropriate constructor found for Online")


# This file is compatible with both classic and new-style classes.


