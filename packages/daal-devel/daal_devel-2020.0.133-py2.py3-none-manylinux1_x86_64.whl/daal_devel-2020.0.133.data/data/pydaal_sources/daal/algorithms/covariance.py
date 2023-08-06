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
            fp, pathname, description = imp.find_module('_covariance_', [dirname(__file__)])
        except ImportError:
            import _covariance_
            return _covariance_
        if fp is not None:
            try:
                _mod = imp.load_module('_covariance_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _covariance_ = swig_import_helper()
    del swig_import_helper
else:
    import _covariance_
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


import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_covariance_.defaultDense_swigconstant(_covariance_)
defaultDense = _covariance_.defaultDense

_covariance_.singlePassDense_swigconstant(_covariance_)
singlePassDense = _covariance_.singlePassDense

_covariance_.sumDense_swigconstant(_covariance_)
sumDense = _covariance_.sumDense

_covariance_.fastCSR_swigconstant(_covariance_)
fastCSR = _covariance_.fastCSR

_covariance_.singlePassCSR_swigconstant(_covariance_)
singlePassCSR = _covariance_.singlePassCSR

_covariance_.sumCSR_swigconstant(_covariance_)
sumCSR = _covariance_.sumCSR

_covariance_.data_swigconstant(_covariance_)
data = _covariance_.data

_covariance_.lastInputId_swigconstant(_covariance_)
lastInputId = _covariance_.lastInputId

_covariance_.nObservations_swigconstant(_covariance_)
nObservations = _covariance_.nObservations

_covariance_.crossProduct_swigconstant(_covariance_)
crossProduct = _covariance_.crossProduct

_covariance_.sum_swigconstant(_covariance_)
sum = _covariance_.sum

_covariance_.lastPartialResultId_swigconstant(_covariance_)
lastPartialResultId = _covariance_.lastPartialResultId

_covariance_.covariance_swigconstant(_covariance_)
covariance = _covariance_.covariance

_covariance_.correlation_swigconstant(_covariance_)
correlation = _covariance_.correlation

_covariance_.mean_swigconstant(_covariance_)
mean = _covariance_.mean

_covariance_.lastResultId_swigconstant(_covariance_)
lastResultId = _covariance_.lastResultId

_covariance_.covarianceMatrix_swigconstant(_covariance_)
covarianceMatrix = _covariance_.covarianceMatrix

_covariance_.correlationMatrix_swigconstant(_covariance_)
correlationMatrix = _covariance_.correlationMatrix

_covariance_.partialResults_swigconstant(_covariance_)
partialResults = _covariance_.partialResults

_covariance_.lastMasterInputId_swigconstant(_covariance_)
lastMasterInputId = _covariance_.lastMasterInputId
class InputIface(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, InputIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getNumberOfFeatures(self):
        return _covariance_.InputIface_getNumberOfFeatures(self)
    __swig_destroy__ = _covariance_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _covariance_.InputIface_swigregister
InputIface_swigregister(InputIface)

class Input(InputIface):
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Input
    __del__ = lambda self: None

    def getNumberOfFeatures(self):
        return _covariance_.Input_getNumberOfFeatures(self)

    def get(self, id):
        return _covariance_.Input_get(self, id)

    def set(self, id, ptr):
        return _covariance_.Input_set(self, id, ptr)

    def check(self, parameter, method):
        return _covariance_.Input_check(self, parameter, method)
Input_swigregister = _covariance_.Input_swigregister
Input_swigregister(Input)

class PartialResult(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _covariance_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_covariance_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _covariance_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _covariance_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_PartialResult
    __del__ = lambda self: None

    def getNumberOfFeatures(self):
        return _covariance_.PartialResult_getNumberOfFeatures(self)

    def get(self, id):
        return _covariance_.PartialResult_get(self, id)

    def set(self, id, ptr):
        return _covariance_.PartialResult_set(self, id, ptr)

    def check(self, *args):
        return _covariance_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _covariance_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _covariance_.PartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _covariance_.PartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _covariance_.PartialResult_initialize_Float32(self, input, parameter, method)

PartialResult_swigregister = _covariance_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _covariance_.PartialResult_serializationTag()
PartialResult_serializationTag = _covariance_.PartialResult_serializationTag

class Parameter(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _covariance_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["outputMatrixType"] = _covariance_.Parameter_outputMatrixType_set
    __swig_getmethods__["outputMatrixType"] = _covariance_.Parameter_outputMatrixType_get
    if _newclass:
        outputMatrixType = _swig_property(_covariance_.Parameter_outputMatrixType_get, _covariance_.Parameter_outputMatrixType_set)
    __swig_destroy__ = _covariance_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _covariance_.Parameter_swigregister
Parameter_swigregister(Parameter)

class OnlineParameter(Parameter):
    __swig_setmethods__ = {}
    for _s in [Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_OnlineParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _covariance_.OnlineParameter_check(self)
    __swig_destroy__ = _covariance_.delete_OnlineParameter
    __del__ = lambda self: None
OnlineParameter_swigregister = _covariance_.OnlineParameter_swigregister
OnlineParameter_swigregister(OnlineParameter)

class Result(daal.algorithms.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _covariance_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_covariance_.Result_serializationTag)

    def getSerializationTag(self):
        return _covariance_.Result_getSerializationTag(self)

    def __init__(self):
        this = _covariance_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _covariance_.Result_get(self, id)

    def set(self, id, value):
        return _covariance_.Result_set(self, id, value)

    def check(self, *args):
        return _covariance_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _covariance_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _covariance_.Result_allocate_Float32(self, *args)

Result_swigregister = _covariance_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _covariance_.Result_serializationTag()
Result_serializationTag = _covariance_.Result_serializationTag

class BatchImpl(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getResult(self):
        return _covariance_.BatchImpl_getResult(self)

    def setResult(self, result):
        return _covariance_.BatchImpl_setResult(self, result)

    def clone(self):
        return _covariance_.BatchImpl_clone(self)
    __swig_destroy__ = _covariance_.delete_BatchImpl
    __del__ = lambda self: None
    __swig_setmethods__["input"] = _covariance_.BatchImpl_input_set
    __swig_getmethods__["input"] = _covariance_.BatchImpl_input_get
    if _newclass:
        input = _swig_property(_covariance_.BatchImpl_input_get, _covariance_.BatchImpl_input_set)
    __swig_setmethods__["parameter"] = _covariance_.BatchImpl_parameter_set
    __swig_getmethods__["parameter"] = _covariance_.BatchImpl_parameter_get
    if _newclass:
        parameter = _swig_property(_covariance_.BatchImpl_parameter_get, _covariance_.BatchImpl_parameter_set)
BatchImpl_swigregister = _covariance_.BatchImpl_swigregister
BatchImpl_swigregister(BatchImpl)

class OnlineImpl(daal.algorithms.Analysis_Online):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _covariance_.delete_OnlineImpl
    __del__ = lambda self: None

    def getResult(self):
        return _covariance_.OnlineImpl_getResult(self)

    def setResult(self, result):
        return _covariance_.OnlineImpl_setResult(self, result)

    def getPartialResult(self):
        return _covariance_.OnlineImpl_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _covariance_.OnlineImpl_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _covariance_.OnlineImpl_clone(self)
    __swig_setmethods__["input"] = _covariance_.OnlineImpl_input_set
    __swig_getmethods__["input"] = _covariance_.OnlineImpl_input_get
    if _newclass:
        input = _swig_property(_covariance_.OnlineImpl_input_get, _covariance_.OnlineImpl_input_set)
    __swig_setmethods__["parameter"] = _covariance_.OnlineImpl_parameter_set
    __swig_getmethods__["parameter"] = _covariance_.OnlineImpl_parameter_get
    if _newclass:
        parameter = _swig_property(_covariance_.OnlineImpl_parameter_get, _covariance_.OnlineImpl_parameter_set)
OnlineImpl_swigregister = _covariance_.OnlineImpl_swigregister
OnlineImpl_swigregister(OnlineImpl)

class DistributedIface_Step1Local(OnlineImpl):
    r"""
    This class is an alias of DistributedIface()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedIface_Step1Local, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedIface_Step1Local, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def clone(self):
        return _covariance_.DistributedIface_Step1Local_clone(self)
    __swig_destroy__ = _covariance_.delete_DistributedIface_Step1Local
    __del__ = lambda self: None
DistributedIface_Step1Local_swigregister = _covariance_.DistributedIface_Step1Local_swigregister
DistributedIface_Step1Local_swigregister(DistributedIface_Step1Local)

class DistributedIface_Step2Master(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of DistributedIface()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedIface_Step2Master, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedIface_Step2Master, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _covariance_.delete_DistributedIface_Step2Master
    __del__ = lambda self: None

    def getResult(self):
        return _covariance_.DistributedIface_Step2Master_getResult(self)

    def setResult(self, result):
        return _covariance_.DistributedIface_Step2Master_setResult(self, result)

    def getPartialResult(self):
        return _covariance_.DistributedIface_Step2Master_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _covariance_.DistributedIface_Step2Master_setPartialResult(self, partialResult, initFlag)

    def checkFinalizeComputeParams(self):
        return _covariance_.DistributedIface_Step2Master_checkFinalizeComputeParams(self)

    def clone(self):
        return _covariance_.DistributedIface_Step2Master_clone(self)
    __swig_setmethods__["input"] = _covariance_.DistributedIface_Step2Master_input_set
    __swig_getmethods__["input"] = _covariance_.DistributedIface_Step2Master_input_get
    if _newclass:
        input = _swig_property(_covariance_.DistributedIface_Step2Master_input_get, _covariance_.DistributedIface_Step2Master_input_set)
    __swig_setmethods__["parameter"] = _covariance_.DistributedIface_Step2Master_parameter_set
    __swig_getmethods__["parameter"] = _covariance_.DistributedIface_Step2Master_parameter_get
    if _newclass:
        parameter = _swig_property(_covariance_.DistributedIface_Step2Master_parameter_get, _covariance_.DistributedIface_Step2Master_parameter_set)
DistributedIface_Step2Master_swigregister = _covariance_.DistributedIface_Step2Master_swigregister
DistributedIface_Step2Master_swigregister(DistributedIface_Step2Master)

class DistributedInput_Step1Local(Input):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step1Local, name, value)
    __swig_getmethods__ = {}
    for _s in [Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step1Local, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_DistributedInput_Step1Local(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_DistributedInput_Step1Local
    __del__ = lambda self: None
DistributedInput_Step1Local_swigregister = _covariance_.DistributedInput_Step1Local_swigregister
DistributedInput_Step1Local_swigregister(DistributedInput_Step1Local)

class DistributedInput_Step2Master(InputIface):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_Step2Master, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_Step2Master, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_DistributedInput_Step2Master(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_DistributedInput_Step2Master
    __del__ = lambda self: None

    def getNumberOfFeatures(self):
        return _covariance_.DistributedInput_Step2Master_getNumberOfFeatures(self)

    def add(self, id, partialResult):
        return _covariance_.DistributedInput_Step2Master_add(self, id, partialResult)

    def get(self, id):
        return _covariance_.DistributedInput_Step2Master_get(self, id)

    def check(self, parameter, method):
        return _covariance_.DistributedInput_Step2Master_check(self, parameter, method)
DistributedInput_Step2Master_swigregister = _covariance_.DistributedInput_Step2Master_swigregister
DistributedInput_Step2Master_swigregister(DistributedInput_Step2Master)

class Batch_Float64DefaultDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _covariance_.Batch_Float64DefaultDense_swigregister
Batch_Float64DefaultDense_swigregister(Batch_Float64DefaultDense)

class Batch_Float64SinglePassDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64SinglePassDense_compute(self)
Batch_Float64SinglePassDense_swigregister = _covariance_.Batch_Float64SinglePassDense_swigregister
Batch_Float64SinglePassDense_swigregister(Batch_Float64SinglePassDense)

class Batch_Float64SumDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64SumDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64SumDense_compute(self)
Batch_Float64SumDense_swigregister = _covariance_.Batch_Float64SumDense_swigregister
Batch_Float64SumDense_swigregister(Batch_Float64SumDense)

class Batch_Float64FastCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64FastCSR_compute(self)
Batch_Float64FastCSR_swigregister = _covariance_.Batch_Float64FastCSR_swigregister
Batch_Float64FastCSR_swigregister(Batch_Float64FastCSR)

class Batch_Float64SinglePassCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64SinglePassCSR_compute(self)
Batch_Float64SinglePassCSR_swigregister = _covariance_.Batch_Float64SinglePassCSR_swigregister
Batch_Float64SinglePassCSR_swigregister(Batch_Float64SinglePassCSR)

class Batch_Float64SumCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float64SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float64SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float64SumCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float64SumCSR_compute(self)
Batch_Float64SumCSR_swigregister = _covariance_.Batch_Float64SumCSR_swigregister
Batch_Float64SumCSR_swigregister(Batch_Float64SumCSR)

class Batch_Float32DefaultDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _covariance_.Batch_Float32DefaultDense_swigregister
Batch_Float32DefaultDense_swigregister(Batch_Float32DefaultDense)

class Batch_Float32SinglePassDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32SinglePassDense_compute(self)
Batch_Float32SinglePassDense_swigregister = _covariance_.Batch_Float32SinglePassDense_swigregister
Batch_Float32SinglePassDense_swigregister(Batch_Float32SinglePassDense)

class Batch_Float32SumDense(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32SumDense_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32SumDense_compute(self)
Batch_Float32SumDense_swigregister = _covariance_.Batch_Float32SumDense_swigregister
Batch_Float32SumDense_swigregister(Batch_Float32SumDense)

class Batch_Float32FastCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32FastCSR_compute(self)
Batch_Float32FastCSR_swigregister = _covariance_.Batch_Float32FastCSR_swigregister
Batch_Float32FastCSR_swigregister(Batch_Float32FastCSR)

class Batch_Float32SinglePassCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32SinglePassCSR_compute(self)
Batch_Float32SinglePassCSR_swigregister = _covariance_.Batch_Float32SinglePassCSR_swigregister
Batch_Float32SinglePassCSR_swigregister(Batch_Float32SinglePassCSR)

class Batch_Float32SumCSR(BatchImpl):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [BatchImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [BatchImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Batch_Float32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Batch_Float32SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Batch_Float32SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Batch_Float32SumCSR_clone(self)

    def compute(self):
        return _covariance_.Batch_Float32SumCSR_compute(self)
Batch_Float32SumCSR_swigregister = _covariance_.Batch_Float32SumCSR_swigregister
Batch_Float32SumCSR_swigregister(Batch_Float32SumCSR)

class Online_Float64DefaultDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64DefaultDense_finalizeCompute(self)
Online_Float64DefaultDense_swigregister = _covariance_.Online_Float64DefaultDense_swigregister
Online_Float64DefaultDense_swigregister(Online_Float64DefaultDense)

class Online_Float64SinglePassDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64SinglePassDense_finalizeCompute(self)
Online_Float64SinglePassDense_swigregister = _covariance_.Online_Float64SinglePassDense_swigregister
Online_Float64SinglePassDense_swigregister(Online_Float64SinglePassDense)

class Online_Float64SumDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64SumDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float64SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64SumDense_finalizeCompute(self)
Online_Float64SumDense_swigregister = _covariance_.Online_Float64SumDense_swigregister
Online_Float64SumDense_swigregister(Online_Float64SumDense)

class Online_Float64FastCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64FastCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float64FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64FastCSR_finalizeCompute(self)
Online_Float64FastCSR_swigregister = _covariance_.Online_Float64FastCSR_swigregister
Online_Float64FastCSR_swigregister(Online_Float64FastCSR)

class Online_Float64SinglePassCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64SinglePassCSR_finalizeCompute(self)
Online_Float64SinglePassCSR_swigregister = _covariance_.Online_Float64SinglePassCSR_swigregister
Online_Float64SinglePassCSR_swigregister(Online_Float64SinglePassCSR)

class Online_Float64SumCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float64SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float64SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float64SumCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float64SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float64SumCSR_finalizeCompute(self)
Online_Float64SumCSR_swigregister = _covariance_.Online_Float64SumCSR_swigregister
Online_Float64SumCSR_swigregister(Online_Float64SumCSR)

class Online_Float32DefaultDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32DefaultDense_finalizeCompute(self)
Online_Float32DefaultDense_swigregister = _covariance_.Online_Float32DefaultDense_swigregister
Online_Float32DefaultDense_swigregister(Online_Float32DefaultDense)

class Online_Float32SinglePassDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32SinglePassDense_finalizeCompute(self)
Online_Float32SinglePassDense_swigregister = _covariance_.Online_Float32SinglePassDense_swigregister
Online_Float32SinglePassDense_swigregister(Online_Float32SinglePassDense)

class Online_Float32SumDense(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32SumDense_clone(self)

    def compute(self):
        return _covariance_.Online_Float32SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32SumDense_finalizeCompute(self)
Online_Float32SumDense_swigregister = _covariance_.Online_Float32SumDense_swigregister
Online_Float32SumDense_swigregister(Online_Float32SumDense)

class Online_Float32FastCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32FastCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float32FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32FastCSR_finalizeCompute(self)
Online_Float32FastCSR_swigregister = _covariance_.Online_Float32FastCSR_swigregister
Online_Float32FastCSR_swigregister(Online_Float32FastCSR)

class Online_Float32SinglePassCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32SinglePassCSR_finalizeCompute(self)
Online_Float32SinglePassCSR_swigregister = _covariance_.Online_Float32SinglePassCSR_swigregister
Online_Float32SinglePassCSR_swigregister(Online_Float32SinglePassCSR)

class Online_Float32SumCSR(OnlineImpl):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [OnlineImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Online_Float32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Online_Float32SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Online_Float32SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Online_Float32SumCSR_clone(self)

    def compute(self):
        return _covariance_.Online_Float32SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Online_Float32SumCSR_finalizeCompute(self)
Online_Float32SumCSR_swigregister = _covariance_.Online_Float32SumCSR_swigregister
Online_Float32SumCSR_swigregister(Online_Float32SumCSR)

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
        this = _covariance_.new_Distributed_Step1LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DefaultDense_swigregister = _covariance_.Distributed_Step1LocalFloat64DefaultDense_swigregister
Distributed_Step1LocalFloat64DefaultDense_swigregister(Distributed_Step1LocalFloat64DefaultDense)

class Distributed_Step1LocalFloat64SinglePassDense(Online_Float64SinglePassDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64SinglePassDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64SinglePassDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64SinglePassDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SinglePassDense_swigregister = _covariance_.Distributed_Step1LocalFloat64SinglePassDense_swigregister
Distributed_Step1LocalFloat64SinglePassDense_swigregister(Distributed_Step1LocalFloat64SinglePassDense)

class Distributed_Step1LocalFloat64SumDense(Online_Float64SumDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64SumDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64SumDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64SumDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64SumDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64SumDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SumDense_swigregister = _covariance_.Distributed_Step1LocalFloat64SumDense_swigregister
Distributed_Step1LocalFloat64SumDense_swigregister(Distributed_Step1LocalFloat64SumDense)

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
        this = _covariance_.new_Distributed_Step1LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64FastCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64FastCSR_swigregister = _covariance_.Distributed_Step1LocalFloat64FastCSR_swigregister
Distributed_Step1LocalFloat64FastCSR_swigregister(Distributed_Step1LocalFloat64FastCSR)

class Distributed_Step1LocalFloat64SinglePassCSR(Online_Float64SinglePassCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64SinglePassCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64SinglePassCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64SinglePassCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SinglePassCSR_swigregister = _covariance_.Distributed_Step1LocalFloat64SinglePassCSR_swigregister
Distributed_Step1LocalFloat64SinglePassCSR_swigregister(Distributed_Step1LocalFloat64SinglePassCSR)

class Distributed_Step1LocalFloat64SumCSR(Online_Float64SumCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64SumCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64SumCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat64SumCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat64SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat64SumCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat64SumCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SumCSR_swigregister = _covariance_.Distributed_Step1LocalFloat64SumCSR_swigregister
Distributed_Step1LocalFloat64SumCSR_swigregister(Distributed_Step1LocalFloat64SumCSR)

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
        this = _covariance_.new_Distributed_Step1LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DefaultDense_swigregister = _covariance_.Distributed_Step1LocalFloat32DefaultDense_swigregister
Distributed_Step1LocalFloat32DefaultDense_swigregister(Distributed_Step1LocalFloat32DefaultDense)

class Distributed_Step1LocalFloat32SinglePassDense(Online_Float32SinglePassDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32SinglePassDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32SinglePassDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32SinglePassDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SinglePassDense_swigregister = _covariance_.Distributed_Step1LocalFloat32SinglePassDense_swigregister
Distributed_Step1LocalFloat32SinglePassDense_swigregister(Distributed_Step1LocalFloat32SinglePassDense)

class Distributed_Step1LocalFloat32SumDense(Online_Float32SumDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32SumDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32SumDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32SumDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32SumDense_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32SumDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SumDense_swigregister = _covariance_.Distributed_Step1LocalFloat32SumDense_swigregister
Distributed_Step1LocalFloat32SumDense_swigregister(Distributed_Step1LocalFloat32SumDense)

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
        this = _covariance_.new_Distributed_Step1LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32FastCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32FastCSR_swigregister = _covariance_.Distributed_Step1LocalFloat32FastCSR_swigregister
Distributed_Step1LocalFloat32FastCSR_swigregister(Distributed_Step1LocalFloat32FastCSR)

class Distributed_Step1LocalFloat32SinglePassCSR(Online_Float32SinglePassCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32SinglePassCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32SinglePassCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32SinglePassCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SinglePassCSR_swigregister = _covariance_.Distributed_Step1LocalFloat32SinglePassCSR_swigregister
Distributed_Step1LocalFloat32SinglePassCSR_swigregister(Distributed_Step1LocalFloat32SinglePassCSR)

class Distributed_Step1LocalFloat32SumCSR(Online_Float32SumCSR):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32SumCSR]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32SumCSR]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step1LocalFloat32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _covariance_.Distributed_Step1LocalFloat32SumCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step1LocalFloat32SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step1LocalFloat32SumCSR_finalizeCompute(self)
    __swig_destroy__ = _covariance_.delete_Distributed_Step1LocalFloat32SumCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SumCSR_swigregister = _covariance_.Distributed_Step1LocalFloat32SumCSR_swigregister
Distributed_Step1LocalFloat32SumCSR_swigregister(Distributed_Step1LocalFloat32SumCSR)

class Distributed_Step2MasterFloat64DefaultDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64DefaultDense_finalizeCompute(self)
Distributed_Step2MasterFloat64DefaultDense_swigregister = _covariance_.Distributed_Step2MasterFloat64DefaultDense_swigregister
Distributed_Step2MasterFloat64DefaultDense_swigregister(Distributed_Step2MasterFloat64DefaultDense)

class Distributed_Step2MasterFloat64SinglePassDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassDense_finalizeCompute(self)
Distributed_Step2MasterFloat64SinglePassDense_swigregister = _covariance_.Distributed_Step2MasterFloat64SinglePassDense_swigregister
Distributed_Step2MasterFloat64SinglePassDense_swigregister(Distributed_Step2MasterFloat64SinglePassDense)

class Distributed_Step2MasterFloat64SumDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64SumDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64SumDense_finalizeCompute(self)
Distributed_Step2MasterFloat64SumDense_swigregister = _covariance_.Distributed_Step2MasterFloat64SumDense_swigregister
Distributed_Step2MasterFloat64SumDense_swigregister(Distributed_Step2MasterFloat64SumDense)

class Distributed_Step2MasterFloat64FastCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64FastCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64FastCSR_finalizeCompute(self)
Distributed_Step2MasterFloat64FastCSR_swigregister = _covariance_.Distributed_Step2MasterFloat64FastCSR_swigregister
Distributed_Step2MasterFloat64FastCSR_swigregister(Distributed_Step2MasterFloat64FastCSR)

class Distributed_Step2MasterFloat64SinglePassCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64SinglePassCSR_finalizeCompute(self)
Distributed_Step2MasterFloat64SinglePassCSR_swigregister = _covariance_.Distributed_Step2MasterFloat64SinglePassCSR_swigregister
Distributed_Step2MasterFloat64SinglePassCSR_swigregister(Distributed_Step2MasterFloat64SinglePassCSR)

class Distributed_Step2MasterFloat64SumCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat64SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat64SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat64SumCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat64SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat64SumCSR_finalizeCompute(self)
Distributed_Step2MasterFloat64SumCSR_swigregister = _covariance_.Distributed_Step2MasterFloat64SumCSR_swigregister
Distributed_Step2MasterFloat64SumCSR_swigregister(Distributed_Step2MasterFloat64SumCSR)

class Distributed_Step2MasterFloat32DefaultDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DefaultDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32DefaultDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32DefaultDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32DefaultDense_finalizeCompute(self)
Distributed_Step2MasterFloat32DefaultDense_swigregister = _covariance_.Distributed_Step2MasterFloat32DefaultDense_swigregister
Distributed_Step2MasterFloat32DefaultDense_swigregister(Distributed_Step2MasterFloat32DefaultDense)

class Distributed_Step2MasterFloat32SinglePassDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SinglePassDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassDense_finalizeCompute(self)
Distributed_Step2MasterFloat32SinglePassDense_swigregister = _covariance_.Distributed_Step2MasterFloat32SinglePassDense_swigregister
Distributed_Step2MasterFloat32SinglePassDense_swigregister(Distributed_Step2MasterFloat32SinglePassDense)

class Distributed_Step2MasterFloat32SumDense(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SumDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32SumDense_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32SumDense_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32SumDense_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32SumDense_finalizeCompute(self)
Distributed_Step2MasterFloat32SumDense_swigregister = _covariance_.Distributed_Step2MasterFloat32SumDense_swigregister
Distributed_Step2MasterFloat32SumDense_swigregister(Distributed_Step2MasterFloat32SumDense)

class Distributed_Step2MasterFloat32FastCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32FastCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32FastCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32FastCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32FastCSR_finalizeCompute(self)
Distributed_Step2MasterFloat32FastCSR_swigregister = _covariance_.Distributed_Step2MasterFloat32FastCSR_swigregister
Distributed_Step2MasterFloat32FastCSR_swigregister(Distributed_Step2MasterFloat32FastCSR)

class Distributed_Step2MasterFloat32SinglePassCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SinglePassCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32SinglePassCSR_finalizeCompute(self)
Distributed_Step2MasterFloat32SinglePassCSR_swigregister = _covariance_.Distributed_Step2MasterFloat32SinglePassCSR_swigregister
Distributed_Step2MasterFloat32SinglePassCSR_swigregister(Distributed_Step2MasterFloat32SinglePassCSR)

class Distributed_Step2MasterFloat32SumCSR(DistributedIface_Step2Master):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [DistributedIface_Step2Master]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SumCSR, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _covariance_.new_Distributed_Step2MasterFloat32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _covariance_.delete_Distributed_Step2MasterFloat32SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _covariance_.Distributed_Step2MasterFloat32SumCSR_getMethod(self)

    def clone(self):
        return _covariance_.Distributed_Step2MasterFloat32SumCSR_clone(self)

    def compute(self):
        return _covariance_.Distributed_Step2MasterFloat32SumCSR_compute(self)

    def finalizeCompute(self):
        return _covariance_.Distributed_Step2MasterFloat32SumCSR_finalizeCompute(self)
Distributed_Step2MasterFloat32SumCSR_swigregister = _covariance_.Distributed_Step2MasterFloat32SumCSR_swigregister
Distributed_Step2MasterFloat32SumCSR_swigregister(Distributed_Step2MasterFloat32SumCSR)

from numpy import float64, float32, intc

class DistributedIface(object):
    r"""Factory class for different types of DistributedIface."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            return DistributedIface_Step1Local(*args)
        if step == daal.step2Master:
            return DistributedIface_Step2Master(*args)

        raise RuntimeError("No appropriate constructor found for DistributedIface")

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            return DistributedInput_Step1Local(*args)
        if step == daal.step2Master:
            return DistributedInput_Step2Master(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

class Online(object):
    r"""Factory class for different types of Online."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassDense:
                return Online_Float64SinglePassDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Online_Float64SumDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Online_Float64FastCSR(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                return Online_Float64SinglePassCSR(*args)
            if 'method' in kwargs and kwargs['method'] == sumCSR:
                return Online_Float64SumCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Online_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassDense:
                return Online_Float32SinglePassDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Online_Float32SumDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Online_Float32FastCSR(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                return Online_Float32SinglePassCSR(*args)
            if 'method' in kwargs and kwargs['method'] == sumCSR:
                return Online_Float32SumCSR(*args)

        raise RuntimeError("No appropriate constructor found for Online")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat64DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassDense:
                        return Distributed_Step1LocalFloat64SinglePassDense(*args)
                    if 'method' in kwargs and kwargs['method'] == sumDense:
                        return Distributed_Step1LocalFloat64SumDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat64FastCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                        return Distributed_Step1LocalFloat64SinglePassCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == sumCSR:
                        return Distributed_Step1LocalFloat64SumCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step1LocalFloat32DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassDense:
                        return Distributed_Step1LocalFloat32SinglePassDense(*args)
                    if 'method' in kwargs and kwargs['method'] == sumDense:
                        return Distributed_Step1LocalFloat32SumDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step1LocalFloat32FastCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                        return Distributed_Step1LocalFloat32SinglePassCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == sumCSR:
                        return Distributed_Step1LocalFloat32SumCSR(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat64DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassDense:
                        return Distributed_Step2MasterFloat64SinglePassDense(*args)
                    if 'method' in kwargs and kwargs['method'] == sumDense:
                        return Distributed_Step2MasterFloat64SumDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat64FastCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                        return Distributed_Step2MasterFloat64SinglePassCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == sumCSR:
                        return Distributed_Step2MasterFloat64SumCSR(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' not in kwargs or kwargs['method'] == defaultDense:
                        return Distributed_Step2MasterFloat32DefaultDense(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassDense:
                        return Distributed_Step2MasterFloat32SinglePassDense(*args)
                    if 'method' in kwargs and kwargs['method'] == sumDense:
                        return Distributed_Step2MasterFloat32SumDense(*args)
                    if 'method' in kwargs and kwargs['method'] == fastCSR:
                        return Distributed_Step2MasterFloat32FastCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                        return Distributed_Step2MasterFloat32SinglePassCSR(*args)
                    if 'method' in kwargs and kwargs['method'] == sumCSR:
                        return Distributed_Step2MasterFloat32SumCSR(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float64DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassDense:
                return Batch_Float64SinglePassDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Batch_Float64SumDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float64FastCSR(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                return Batch_Float64SinglePassCSR(*args)
            if 'method' in kwargs and kwargs['method'] == sumCSR:
                return Batch_Float64SumCSR(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == defaultDense:
                return Batch_Float32DefaultDense(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassDense:
                return Batch_Float32SinglePassDense(*args)
            if 'method' in kwargs and kwargs['method'] == sumDense:
                return Batch_Float32SumDense(*args)
            if 'method' in kwargs and kwargs['method'] == fastCSR:
                return Batch_Float32FastCSR(*args)
            if 'method' in kwargs and kwargs['method'] == singlePassCSR:
                return Batch_Float32SinglePassCSR(*args)
            if 'method' in kwargs and kwargs['method'] == sumCSR:
                return Batch_Float32SumCSR(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


