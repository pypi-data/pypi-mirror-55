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
            fp, pathname, description = imp.find_module('_low_order_moments_', [dirname(__file__)])
        except ImportError:
            import _low_order_moments_
            return _low_order_moments_
        if fp is not None:
            try:
                _mod = imp.load_module('_low_order_moments_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _low_order_moments_ = swig_import_helper()
    del swig_import_helper
else:
    import _low_order_moments_
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

_low_order_moments_.defaultDense_swigconstant(_low_order_moments_)
defaultDense = _low_order_moments_.defaultDense

_low_order_moments_.singlePassDense_swigconstant(_low_order_moments_)
singlePassDense = _low_order_moments_.singlePassDense

_low_order_moments_.sumDense_swigconstant(_low_order_moments_)
sumDense = _low_order_moments_.sumDense

_low_order_moments_.fastCSR_swigconstant(_low_order_moments_)
fastCSR = _low_order_moments_.fastCSR

_low_order_moments_.singlePassCSR_swigconstant(_low_order_moments_)
singlePassCSR = _low_order_moments_.singlePassCSR

_low_order_moments_.sumCSR_swigconstant(_low_order_moments_)
sumCSR = _low_order_moments_.sumCSR

_low_order_moments_.estimatesAll_swigconstant(_low_order_moments_)
estimatesAll = _low_order_moments_.estimatesAll

_low_order_moments_.estimatesMinMax_swigconstant(_low_order_moments_)
estimatesMinMax = _low_order_moments_.estimatesMinMax

_low_order_moments_.estimatesMeanVariance_swigconstant(_low_order_moments_)
estimatesMeanVariance = _low_order_moments_.estimatesMeanVariance

_low_order_moments_.data_swigconstant(_low_order_moments_)
data = _low_order_moments_.data

_low_order_moments_.lastInputId_swigconstant(_low_order_moments_)
lastInputId = _low_order_moments_.lastInputId

_low_order_moments_.minimum_swigconstant(_low_order_moments_)
minimum = _low_order_moments_.minimum

_low_order_moments_.maximum_swigconstant(_low_order_moments_)
maximum = _low_order_moments_.maximum

_low_order_moments_.sum_swigconstant(_low_order_moments_)
sum = _low_order_moments_.sum

_low_order_moments_.sumSquares_swigconstant(_low_order_moments_)
sumSquares = _low_order_moments_.sumSquares

_low_order_moments_.sumSquaresCentered_swigconstant(_low_order_moments_)
sumSquaresCentered = _low_order_moments_.sumSquaresCentered

_low_order_moments_.mean_swigconstant(_low_order_moments_)
mean = _low_order_moments_.mean

_low_order_moments_.secondOrderRawMoment_swigconstant(_low_order_moments_)
secondOrderRawMoment = _low_order_moments_.secondOrderRawMoment

_low_order_moments_.variance_swigconstant(_low_order_moments_)
variance = _low_order_moments_.variance

_low_order_moments_.standardDeviation_swigconstant(_low_order_moments_)
standardDeviation = _low_order_moments_.standardDeviation

_low_order_moments_.variation_swigconstant(_low_order_moments_)
variation = _low_order_moments_.variation

_low_order_moments_.lastResultId_swigconstant(_low_order_moments_)
lastResultId = _low_order_moments_.lastResultId

_low_order_moments_.nObservations_swigconstant(_low_order_moments_)
nObservations = _low_order_moments_.nObservations

_low_order_moments_.partialMinimum_swigconstant(_low_order_moments_)
partialMinimum = _low_order_moments_.partialMinimum

_low_order_moments_.partialMaximum_swigconstant(_low_order_moments_)
partialMaximum = _low_order_moments_.partialMaximum

_low_order_moments_.partialSum_swigconstant(_low_order_moments_)
partialSum = _low_order_moments_.partialSum

_low_order_moments_.partialSumSquares_swigconstant(_low_order_moments_)
partialSumSquares = _low_order_moments_.partialSumSquares

_low_order_moments_.partialSumSquaresCentered_swigconstant(_low_order_moments_)
partialSumSquaresCentered = _low_order_moments_.partialSumSquaresCentered

_low_order_moments_.lastPartialResultId_swigconstant(_low_order_moments_)
lastPartialResultId = _low_order_moments_.lastPartialResultId

_low_order_moments_.partialResults_swigconstant(_low_order_moments_)
partialResults = _low_order_moments_.partialResults

_low_order_moments_.lastMasterInputId_swigconstant(_low_order_moments_)
lastMasterInputId = _low_order_moments_.lastMasterInputId
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

    def getNumberOfColumns(self, nCols):
        return _low_order_moments_.InputIface_getNumberOfColumns(self, nCols)
    __swig_destroy__ = _low_order_moments_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _low_order_moments_.InputIface_swigregister
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
        this = _low_order_moments_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Input
    __del__ = lambda self: None

    def getNumberOfColumns(self, nCols):
        return _low_order_moments_.Input_getNumberOfColumns(self, nCols)

    def get(self, id):
        return _low_order_moments_.Input_get(self, id)

    def set(self, id, ptr):
        return _low_order_moments_.Input_set(self, id, ptr)

    def check(self, parameter, method):
        return _low_order_moments_.Input_check(self, parameter, method)
Input_swigregister = _low_order_moments_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _low_order_moments_.PartialResult_serializationTag
    if _newclass:
        serializationTag = staticmethod(_low_order_moments_.PartialResult_serializationTag)

    def getSerializationTag(self):
        return _low_order_moments_.PartialResult_getSerializationTag(self)

    def __init__(self):
        this = _low_order_moments_.new_PartialResult()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_PartialResult
    __del__ = lambda self: None

    def getNumberOfColumns(self, nCols):
        return _low_order_moments_.PartialResult_getNumberOfColumns(self, nCols)

    def get(self, id):
        return _low_order_moments_.PartialResult_get(self, id)

    def set(self, id, ptr):
        return _low_order_moments_.PartialResult_set(self, id, ptr)

    def check(self, *args):
        return _low_order_moments_.PartialResult_check(self, *args)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _low_order_moments_.PartialResult_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _low_order_moments_.PartialResult_allocate_Float32(self, input, parameter, method)


    def initialize_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _low_order_moments_.PartialResult_initialize_Float64(self, input, parameter, method)


    def initialize_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _low_order_moments_.PartialResult_initialize_Float32(self, input, parameter, method)

PartialResult_swigregister = _low_order_moments_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

def PartialResult_serializationTag():
    return _low_order_moments_.PartialResult_serializationTag()
PartialResult_serializationTag = _low_order_moments_.PartialResult_serializationTag

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

    def __init__(self, *args):
        this = _low_order_moments_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["estimatesToCompute"] = _low_order_moments_.Parameter_estimatesToCompute_set
    __swig_getmethods__["estimatesToCompute"] = _low_order_moments_.Parameter_estimatesToCompute_get
    if _newclass:
        estimatesToCompute = _swig_property(_low_order_moments_.Parameter_estimatesToCompute_get, _low_order_moments_.Parameter_estimatesToCompute_set)

    def check(self):
        return _low_order_moments_.Parameter_check(self)
    __swig_destroy__ = _low_order_moments_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _low_order_moments_.Parameter_swigregister
Parameter_swigregister(Parameter)

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
    __swig_getmethods__["serializationTag"] = lambda x: _low_order_moments_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_low_order_moments_.Result_serializationTag)

    def getSerializationTag(self):
        return _low_order_moments_.Result_getSerializationTag(self)

    def __init__(self):
        this = _low_order_moments_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _low_order_moments_.Result_get(self, id)

    def set(self, id, value):
        return _low_order_moments_.Result_set(self, id, value)

    def check(self, *args):
        return _low_order_moments_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _low_order_moments_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _low_order_moments_.Result_allocate_Float32(self, *args)

Result_swigregister = _low_order_moments_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _low_order_moments_.Result_serializationTag()
Result_serializationTag = _low_order_moments_.Result_serializationTag

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
        return _low_order_moments_.BatchImpl_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.BatchImpl_setResult(self, result)

    def clone(self):
        return _low_order_moments_.BatchImpl_clone(self)
    __swig_destroy__ = _low_order_moments_.delete_BatchImpl
    __del__ = lambda self: None
    __swig_setmethods__["input"] = _low_order_moments_.BatchImpl_input_set
    __swig_getmethods__["input"] = _low_order_moments_.BatchImpl_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.BatchImpl_input_get, _low_order_moments_.BatchImpl_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.BatchImpl_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.BatchImpl_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.BatchImpl_parameter_get, _low_order_moments_.BatchImpl_parameter_set)
BatchImpl_swigregister = _low_order_moments_.BatchImpl_swigregister
BatchImpl_swigregister(BatchImpl)

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
        this = _low_order_moments_.new_DistributedInput_Step2Master(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_DistributedInput_Step2Master
    __del__ = lambda self: None

    def getNumberOfColumns(self, nCols):
        return _low_order_moments_.DistributedInput_Step2Master_getNumberOfColumns(self, nCols)

    def add(self, id, partialResult):
        return _low_order_moments_.DistributedInput_Step2Master_add(self, id, partialResult)

    def set(self, id, ptr):
        return _low_order_moments_.DistributedInput_Step2Master_set(self, id, ptr)

    def get(self, id):
        return _low_order_moments_.DistributedInput_Step2Master_get(self, id)

    def check(self, parameter, method):
        return _low_order_moments_.DistributedInput_Step2Master_check(self, parameter, method)
DistributedInput_Step2Master_swigregister = _low_order_moments_.DistributedInput_Step2Master_swigregister
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
        this = _low_order_moments_.new_Batch_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64DefaultDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64DefaultDense_compute(self)
Batch_Float64DefaultDense_swigregister = _low_order_moments_.Batch_Float64DefaultDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64SinglePassDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64SinglePassDense_compute(self)
Batch_Float64SinglePassDense_swigregister = _low_order_moments_.Batch_Float64SinglePassDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64SumDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64SumDense_compute(self)
Batch_Float64SumDense_swigregister = _low_order_moments_.Batch_Float64SumDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64FastCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64FastCSR_compute(self)
Batch_Float64FastCSR_swigregister = _low_order_moments_.Batch_Float64FastCSR_swigregister
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
        this = _low_order_moments_.new_Batch_Float64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64SinglePassCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64SinglePassCSR_compute(self)
Batch_Float64SinglePassCSR_swigregister = _low_order_moments_.Batch_Float64SinglePassCSR_swigregister
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
        this = _low_order_moments_.new_Batch_Float64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float64SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float64SumCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float64SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float64SumCSR_compute(self)
Batch_Float64SumCSR_swigregister = _low_order_moments_.Batch_Float64SumCSR_swigregister
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
        this = _low_order_moments_.new_Batch_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32DefaultDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32DefaultDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32DefaultDense_compute(self)
Batch_Float32DefaultDense_swigregister = _low_order_moments_.Batch_Float32DefaultDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32SinglePassDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32SinglePassDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32SinglePassDense_compute(self)
Batch_Float32SinglePassDense_swigregister = _low_order_moments_.Batch_Float32SinglePassDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32SumDense
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32SumDense_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32SumDense_compute(self)
Batch_Float32SumDense_swigregister = _low_order_moments_.Batch_Float32SumDense_swigregister
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
        this = _low_order_moments_.new_Batch_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32FastCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32FastCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32FastCSR_compute(self)
Batch_Float32FastCSR_swigregister = _low_order_moments_.Batch_Float32FastCSR_swigregister
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
        this = _low_order_moments_.new_Batch_Float32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32SinglePassCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32SinglePassCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32SinglePassCSR_compute(self)
Batch_Float32SinglePassCSR_swigregister = _low_order_moments_.Batch_Float32SinglePassCSR_swigregister
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
        this = _low_order_moments_.new_Batch_Float32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _low_order_moments_.delete_Batch_Float32SumCSR
    __del__ = lambda self: None

    def getMethod(self):
        return _low_order_moments_.Batch_Float32SumCSR_getMethod(self)

    def clone(self):
        return _low_order_moments_.Batch_Float32SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Batch_Float32SumCSR_compute(self)
Batch_Float32SumCSR_swigregister = _low_order_moments_.Batch_Float32SumCSR_swigregister
Batch_Float32SumCSR_swigregister(Batch_Float32SumCSR)

class Online_Float64DefaultDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64DefaultDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64DefaultDense_input_get, _low_order_moments_.Online_Float64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64DefaultDense_parameter_get, _low_order_moments_.Online_Float64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64DefaultDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64DefaultDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64DefaultDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64DefaultDense
    __del__ = lambda self: None
Online_Float64DefaultDense_swigregister = _low_order_moments_.Online_Float64DefaultDense_swigregister
Online_Float64DefaultDense_swigregister(Online_Float64DefaultDense)

class Online_Float64SinglePassDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SinglePassDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64SinglePassDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64SinglePassDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64SinglePassDense_input_get, _low_order_moments_.Online_Float64SinglePassDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64SinglePassDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64SinglePassDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64SinglePassDense_parameter_get, _low_order_moments_.Online_Float64SinglePassDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64SinglePassDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64SinglePassDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64SinglePassDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64SinglePassDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64SinglePassDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64SinglePassDense
    __del__ = lambda self: None
Online_Float64SinglePassDense_swigregister = _low_order_moments_.Online_Float64SinglePassDense_swigregister
Online_Float64SinglePassDense_swigregister(Online_Float64SinglePassDense)

class Online_Float64SumDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SumDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64SumDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64SumDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64SumDense_input_get, _low_order_moments_.Online_Float64SumDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64SumDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64SumDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64SumDense_parameter_get, _low_order_moments_.Online_Float64SumDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64SumDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64SumDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64SumDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64SumDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64SumDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64SumDense
    __del__ = lambda self: None
Online_Float64SumDense_swigregister = _low_order_moments_.Online_Float64SumDense_swigregister
Online_Float64SumDense_swigregister(Online_Float64SumDense)

class Online_Float64FastCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64FastCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64FastCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64FastCSR_input_get, _low_order_moments_.Online_Float64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64FastCSR_parameter_get, _low_order_moments_.Online_Float64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64FastCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64FastCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64FastCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64FastCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64FastCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64FastCSR
    __del__ = lambda self: None
Online_Float64FastCSR_swigregister = _low_order_moments_.Online_Float64FastCSR_swigregister
Online_Float64FastCSR_swigregister(Online_Float64FastCSR)

class Online_Float64SinglePassCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SinglePassCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64SinglePassCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64SinglePassCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64SinglePassCSR_input_get, _low_order_moments_.Online_Float64SinglePassCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64SinglePassCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64SinglePassCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64SinglePassCSR_parameter_get, _low_order_moments_.Online_Float64SinglePassCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64SinglePassCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64SinglePassCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64SinglePassCSR
    __del__ = lambda self: None
Online_Float64SinglePassCSR_swigregister = _low_order_moments_.Online_Float64SinglePassCSR_swigregister
Online_Float64SinglePassCSR_swigregister(Online_Float64SinglePassCSR)

class Online_Float64SumCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SumCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float64SumCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float64SumCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float64SumCSR_input_get, _low_order_moments_.Online_Float64SumCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float64SumCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float64SumCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float64SumCSR_parameter_get, _low_order_moments_.Online_Float64SumCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float64SumCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float64SumCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float64SumCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float64SumCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float64SumCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float64SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float64SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float64SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float64SumCSR
    __del__ = lambda self: None
Online_Float64SumCSR_swigregister = _low_order_moments_.Online_Float64SumCSR_swigregister
Online_Float64SumCSR_swigregister(Online_Float64SumCSR)

class Online_Float32DefaultDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32DefaultDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32DefaultDense_input_get, _low_order_moments_.Online_Float32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32DefaultDense_parameter_get, _low_order_moments_.Online_Float32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32DefaultDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32DefaultDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32DefaultDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32DefaultDense
    __del__ = lambda self: None
Online_Float32DefaultDense_swigregister = _low_order_moments_.Online_Float32DefaultDense_swigregister
Online_Float32DefaultDense_swigregister(Online_Float32DefaultDense)

class Online_Float32SinglePassDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SinglePassDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32SinglePassDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32SinglePassDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32SinglePassDense_input_get, _low_order_moments_.Online_Float32SinglePassDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32SinglePassDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32SinglePassDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32SinglePassDense_parameter_get, _low_order_moments_.Online_Float32SinglePassDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32SinglePassDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32SinglePassDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32SinglePassDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32SinglePassDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32SinglePassDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32SinglePassDense
    __del__ = lambda self: None
Online_Float32SinglePassDense_swigregister = _low_order_moments_.Online_Float32SinglePassDense_swigregister
Online_Float32SinglePassDense_swigregister(Online_Float32SinglePassDense)

class Online_Float32SumDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SumDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32SumDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32SumDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32SumDense_input_get, _low_order_moments_.Online_Float32SumDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32SumDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32SumDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32SumDense_parameter_get, _low_order_moments_.Online_Float32SumDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32SumDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32SumDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32SumDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32SumDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32SumDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32SumDense
    __del__ = lambda self: None
Online_Float32SumDense_swigregister = _low_order_moments_.Online_Float32SumDense_swigregister
Online_Float32SumDense_swigregister(Online_Float32SumDense)

class Online_Float32FastCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32FastCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32FastCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32FastCSR_input_get, _low_order_moments_.Online_Float32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32FastCSR_parameter_get, _low_order_moments_.Online_Float32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32FastCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32FastCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32FastCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32FastCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32FastCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32FastCSR
    __del__ = lambda self: None
Online_Float32FastCSR_swigregister = _low_order_moments_.Online_Float32FastCSR_swigregister
Online_Float32FastCSR_swigregister(Online_Float32FastCSR)

class Online_Float32SinglePassCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SinglePassCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32SinglePassCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32SinglePassCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32SinglePassCSR_input_get, _low_order_moments_.Online_Float32SinglePassCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32SinglePassCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32SinglePassCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32SinglePassCSR_parameter_get, _low_order_moments_.Online_Float32SinglePassCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32SinglePassCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32SinglePassCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32SinglePassCSR
    __del__ = lambda self: None
Online_Float32SinglePassCSR_swigregister = _low_order_moments_.Online_Float32SinglePassCSR_swigregister
Online_Float32SinglePassCSR_swigregister(Online_Float32SinglePassCSR)

class Online_Float32SumCSR(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SumCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Online_Float32SumCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Online_Float32SumCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Online_Float32SumCSR_input_get, _low_order_moments_.Online_Float32SumCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Online_Float32SumCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Online_Float32SumCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Online_Float32SumCSR_parameter_get, _low_order_moments_.Online_Float32SumCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Online_Float32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Online_Float32SumCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Online_Float32SumCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Online_Float32SumCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Online_Float32SumCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Online_Float32SumCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Online_Float32SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Online_Float32SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Online_Float32SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Online_Float32SumCSR
    __del__ = lambda self: None
Online_Float32SumCSR_swigregister = _low_order_moments_.Online_Float32SumCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64DefaultDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64DefaultDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64SinglePassDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SinglePassDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64SinglePassDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64SumDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SumDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64SumDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64FastCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64FastCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64SinglePassCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SinglePassCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64SinglePassCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat64SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat64SumCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SumCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat64SumCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32DefaultDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32DefaultDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32SinglePassDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SinglePassDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32SinglePassDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32SumDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SumDense_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32SumDense_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32FastCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32FastCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32SinglePassCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SinglePassCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32SinglePassCSR_swigregister
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
        this = _low_order_moments_.new_Distributed_Step1LocalFloat32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step1LocalFloat32SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step1LocalFloat32SumCSR
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SumCSR_swigregister = _low_order_moments_.Distributed_Step1LocalFloat32SumCSR_swigregister
Distributed_Step1LocalFloat32SumCSR_swigregister(Distributed_Step1LocalFloat32SumCSR)

class Distributed_Step2MasterFloat64DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64DefaultDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64DefaultDense_swigregister
Distributed_Step2MasterFloat64DefaultDense_swigregister(Distributed_Step2MasterFloat64DefaultDense)

class Distributed_Step2MasterFloat64SinglePassDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SinglePassDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64SinglePassDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64SinglePassDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassDense_swigregister
Distributed_Step2MasterFloat64SinglePassDense_swigregister(Distributed_Step2MasterFloat64SinglePassDense)

class Distributed_Step2MasterFloat64SumDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SumDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SumDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SumDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SumDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat64SumDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SumDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SumDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SumDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64SumDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64SumDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat64SumDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64SumDense_swigregister
Distributed_Step2MasterFloat64SumDense_swigregister(Distributed_Step2MasterFloat64SumDense)

class Distributed_Step2MasterFloat64FastCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64FastCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64FastCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64FastCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64FastCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64FastCSR_swigregister
Distributed_Step2MasterFloat64FastCSR_swigregister(Distributed_Step2MasterFloat64FastCSR)

class Distributed_Step2MasterFloat64SinglePassCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SinglePassCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64SinglePassCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64SinglePassCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64SinglePassCSR_swigregister
Distributed_Step2MasterFloat64SinglePassCSR_swigregister(Distributed_Step2MasterFloat64SinglePassCSR)

class Distributed_Step2MasterFloat64SumCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SumCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SumCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat64SumCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat64SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat64SumCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat64SumCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat64SumCSR_swigregister
Distributed_Step2MasterFloat64SumCSR_swigregister(Distributed_Step2MasterFloat64SumCSR)

class Distributed_Step2MasterFloat32DefaultDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32DefaultDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32DefaultDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32DefaultDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32DefaultDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32DefaultDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32DefaultDense_swigregister
Distributed_Step2MasterFloat32DefaultDense_swigregister(Distributed_Step2MasterFloat32DefaultDense)

class Distributed_Step2MasterFloat32SinglePassDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SinglePassDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SinglePassDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32SinglePassDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32SinglePassDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32SinglePassDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassDense_swigregister
Distributed_Step2MasterFloat32SinglePassDense_swigregister(Distributed_Step2MasterFloat32SinglePassDense)

class Distributed_Step2MasterFloat32SumDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SumDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SumDense, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SumDense_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SumDense_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SumDense_input_get, _low_order_moments_.Distributed_Step2MasterFloat32SumDense_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SumDense_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SumDense_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SumDense_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32SumDense_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32SumDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumDense_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32SumDense
    __del__ = lambda self: None
Distributed_Step2MasterFloat32SumDense_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32SumDense_swigregister
Distributed_Step2MasterFloat32SumDense_swigregister(Distributed_Step2MasterFloat32SumDense)

class Distributed_Step2MasterFloat32FastCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32FastCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32FastCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32FastCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32FastCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32FastCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32FastCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32FastCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32FastCSR_swigregister
Distributed_Step2MasterFloat32FastCSR_swigregister(Distributed_Step2MasterFloat32FastCSR)

class Distributed_Step2MasterFloat32SinglePassCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SinglePassCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SinglePassCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32SinglePassCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32SinglePassCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32SinglePassCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32SinglePassCSR_swigregister
Distributed_Step2MasterFloat32SinglePassCSR_swigregister(Distributed_Step2MasterFloat32SinglePassCSR)

class Distributed_Step2MasterFloat32SumCSR(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SumCSR, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SumCSR, name)
    __repr__ = _swig_repr
    __swig_setmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_input_set
    __swig_getmethods__["input"] = _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_input_get
    if _newclass:
        input = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SumCSR_input_get, _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_input_set)
    __swig_setmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_parameter_set
    __swig_getmethods__["parameter"] = _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_parameter_get
    if _newclass:
        parameter = _swig_property(_low_order_moments_.Distributed_Step2MasterFloat32SumCSR_parameter_get, _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_parameter_set)

    def __init__(self, *args):
        this = _low_order_moments_.new_Distributed_Step2MasterFloat32SumCSR(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_getMethod(self)

    def getResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_getResult(self)

    def setResult(self, result):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_setResult(self, result)

    def getPartialResult(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_getPartialResult(self)

    def setPartialResult(self, partialResult, initFlag=False):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_setPartialResult(self, partialResult, initFlag)

    def clone(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_clone(self)

    def compute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_compute(self)

    def finalizeCompute(self):
        return _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_finalizeCompute(self)
    __swig_destroy__ = _low_order_moments_.delete_Distributed_Step2MasterFloat32SumCSR
    __del__ = lambda self: None
Distributed_Step2MasterFloat32SumCSR_swigregister = _low_order_moments_.Distributed_Step2MasterFloat32SumCSR_swigregister
Distributed_Step2MasterFloat32SumCSR_swigregister(Distributed_Step2MasterFloat32SumCSR)

from numpy import float64, float32, intc

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step2Master:
            return DistributedInput_Step2Master(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

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


# This file is compatible with both classic and new-style classes.


