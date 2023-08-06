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
            fp, pathname, description = imp.find_module('_pca_', [dirname(__file__)])
        except ImportError:
            import _pca_
            return _pca_
        if fp is not None:
            try:
                _mod = imp.load_module('_pca_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pca_ = swig_import_helper()
    del swig_import_helper
else:
    import _pca_
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
import daal.algorithms.covariance

_pca_.correlationDense_swigconstant(_pca_)
correlationDense = _pca_.correlationDense

_pca_.defaultDense_swigconstant(_pca_)
defaultDense = _pca_.defaultDense

_pca_.svdDense_swigconstant(_pca_)
svdDense = _pca_.svdDense

_pca_.data_swigconstant(_pca_)
data = _pca_.data

_pca_.lastInputDatasetId_swigconstant(_pca_)
lastInputDatasetId = _pca_.lastInputDatasetId

_pca_.correlation_swigconstant(_pca_)
correlation = _pca_.correlation

_pca_.lastInputCorrelationId_swigconstant(_pca_)
lastInputCorrelationId = _pca_.lastInputCorrelationId

_pca_.partialResults_swigconstant(_pca_)
partialResults = _pca_.partialResults

_pca_.lastStep2MasterInputId_swigconstant(_pca_)
lastStep2MasterInputId = _pca_.lastStep2MasterInputId

_pca_.nObservationsCorrelation_swigconstant(_pca_)
nObservationsCorrelation = _pca_.nObservationsCorrelation

_pca_.crossProductCorrelation_swigconstant(_pca_)
crossProductCorrelation = _pca_.crossProductCorrelation

_pca_.sumCorrelation_swigconstant(_pca_)
sumCorrelation = _pca_.sumCorrelation

_pca_.lastPartialCorrelationResultId_swigconstant(_pca_)
lastPartialCorrelationResultId = _pca_.lastPartialCorrelationResultId

_pca_.nObservationsSVD_swigconstant(_pca_)
nObservationsSVD = _pca_.nObservationsSVD

_pca_.sumSVD_swigconstant(_pca_)
sumSVD = _pca_.sumSVD

_pca_.sumSquaresSVD_swigconstant(_pca_)
sumSquaresSVD = _pca_.sumSquaresSVD

_pca_.lastPartialSVDTableResultId_swigconstant(_pca_)
lastPartialSVDTableResultId = _pca_.lastPartialSVDTableResultId

_pca_.auxiliaryData_swigconstant(_pca_)
auxiliaryData = _pca_.auxiliaryData

_pca_.distributedInputs_swigconstant(_pca_)
distributedInputs = _pca_.distributedInputs

_pca_.lastPartialSVDCollectionResultId_swigconstant(_pca_)
lastPartialSVDCollectionResultId = _pca_.lastPartialSVDCollectionResultId

_pca_.eigenvalues_swigconstant(_pca_)
eigenvalues = _pca_.eigenvalues

_pca_.eigenvectors_swigconstant(_pca_)
eigenvectors = _pca_.eigenvectors

_pca_.means_swigconstant(_pca_)
means = _pca_.means

_pca_.variances_swigconstant(_pca_)
variances = _pca_.variances

_pca_.lastResultId_swigconstant(_pca_)
lastResultId = _pca_.lastResultId

_pca_.dataForTransform_swigconstant(_pca_)
dataForTransform = _pca_.dataForTransform

_pca_.none_swigconstant(_pca_)
none = _pca_.none

_pca_.mean_swigconstant(_pca_)
mean = _pca_.mean

_pca_.variance_swigconstant(_pca_)
variance = _pca_.variance

_pca_.eigenvalue_swigconstant(_pca_)
eigenvalue = _pca_.eigenvalue
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

    def getNFeatures(self):
        return _pca_.InputIface_getNFeatures(self)

    def isCorrelation(self):
        return _pca_.InputIface_isCorrelation(self)
    __swig_destroy__ = _pca_.delete_InputIface
    __del__ = lambda self: None
InputIface_swigregister = _pca_.InputIface_swigregister
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
        this = _pca_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Input
    __del__ = lambda self: None

    def getDataset(self, id):
        return _pca_.Input_getDataset(self, id)

    def setDataset(self, id, value):
        return _pca_.Input_setDataset(self, id, value)

    def setCorrelation(self, id, value):
        return _pca_.Input_setCorrelation(self, id, value)

    def getNFeatures(self):
        return _pca_.Input_getNFeatures(self)

    def check(self, par, method):
        return _pca_.Input_check(self, par, method)
Input_swigregister = _pca_.Input_swigregister
Input_swigregister(Input)

class PartialResultBase(daal.algorithms.PartialResult):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResultBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.PartialResult]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResultBase, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getNFeatures(self):
        return _pca_.PartialResultBase_getNFeatures(self)
    __swig_destroy__ = _pca_.delete_PartialResultBase
    __del__ = lambda self: None
PartialResultBase_swigregister = _pca_.PartialResultBase_swigregister
PartialResultBase_swigregister(PartialResultBase)

class BaseBatchParameter(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BaseBatchParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BaseBatchParameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _pca_.new_BaseBatchParameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["resultsToCompute"] = _pca_.BaseBatchParameter_resultsToCompute_set
    __swig_getmethods__["resultsToCompute"] = _pca_.BaseBatchParameter_resultsToCompute_get
    if _newclass:
        resultsToCompute = _swig_property(_pca_.BaseBatchParameter_resultsToCompute_get, _pca_.BaseBatchParameter_resultsToCompute_set)
    __swig_setmethods__["nComponents"] = _pca_.BaseBatchParameter_nComponents_set
    __swig_getmethods__["nComponents"] = _pca_.BaseBatchParameter_nComponents_get
    if _newclass:
        nComponents = _swig_property(_pca_.BaseBatchParameter_nComponents_get, _pca_.BaseBatchParameter_nComponents_set)
    __swig_setmethods__["isDeterministic"] = _pca_.BaseBatchParameter_isDeterministic_set
    __swig_getmethods__["isDeterministic"] = _pca_.BaseBatchParameter_isDeterministic_get
    if _newclass:
        isDeterministic = _swig_property(_pca_.BaseBatchParameter_isDeterministic_get, _pca_.BaseBatchParameter_isDeterministic_set)
    __swig_destroy__ = _pca_.delete_BaseBatchParameter
    __del__ = lambda self: None
BaseBatchParameter_swigregister = _pca_.BaseBatchParameter_swigregister
BaseBatchParameter_swigregister(BaseBatchParameter)

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
    __swig_getmethods__["serializationTag"] = lambda x: _pca_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_pca_.Result_serializationTag)

    def getSerializationTag(self):
        return _pca_.Result_getSerializationTag(self)

    def __init__(self, *args):
        this = _pca_.new_Result(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _pca_.Result_get(self, id)

    def getCollection(self, id):
        return _pca_.Result_getCollection(self, id)

    def set(self, *args):
        return _pca_.Result_set(self, *args)

    def check(self, *args):
        return _pca_.Result_check(self, *args)

    def allocate_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _pca_.Result_allocate_Float64(self, *args)


    def allocate_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _pca_.Result_allocate_Float32(self, *args)

Result_swigregister = _pca_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _pca_.Result_serializationTag()
Result_serializationTag = _pca_.Result_serializationTag

class PartialResult_SvdDense(PartialResultBase):
    r"""
    This class is an alias of PartialResult()
    """
    __swig_setmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult_SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult_SvdDense, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _pca_.PartialResult_SvdDense_serializationTag
    if _newclass:
        serializationTag = staticmethod(_pca_.PartialResult_SvdDense_serializationTag)

    def getSerializationTag(self):
        return _pca_.PartialResult_SvdDense_getSerializationTag(self)

    def __init__(self):
        this = _pca_.new_PartialResult_SvdDense()
        try:
            self.this.append(this)
        except:
            self.this = this

    def getSVDTable(self, id):
        return _pca_.PartialResult_SvdDense_getSVDTable(self, id)

    def getNFeatures(self):
        return _pca_.PartialResult_SvdDense_getNFeatures(self)

    def getSVDCollection(self, *args):
        return _pca_.PartialResult_SvdDense_getSVDCollection(self, *args)

    def setSVDTable(self, id, value):
        return _pca_.PartialResult_SvdDense_setSVDTable(self, id, value)

    def setSVDCollection(self, id, value):
        return _pca_.PartialResult_SvdDense_setSVDCollection(self, id, value)

    def add(self, id, value):
        return _pca_.PartialResult_SvdDense_add(self, id, value)

    def check(self, *args):
        return _pca_.PartialResult_SvdDense_check(self, *args)
    __swig_destroy__ = _pca_.delete_PartialResult_SvdDense
    __del__ = lambda self: None

    def initialize_Float32(self, input, parameter, method):
        return _pca_.PartialResult_SvdDense_initialize_Float32(self, input, parameter, method)

    def initialize_Float64(self, input, parameter, method):
        return _pca_.PartialResult_SvdDense_initialize_Float64(self, input, parameter, method)

    def allocate_Float32(self, input, parameter, method):
        return _pca_.PartialResult_SvdDense_allocate_Float32(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        return _pca_.PartialResult_SvdDense_allocate_Float64(self, input, parameter, method)
PartialResult_SvdDense_swigregister = _pca_.PartialResult_SvdDense_swigregister
PartialResult_SvdDense_swigregister(PartialResult_SvdDense)

def PartialResult_SvdDense_serializationTag():
    return _pca_.PartialResult_SvdDense_serializationTag()
PartialResult_SvdDense_serializationTag = _pca_.PartialResult_SvdDense_serializationTag

class PartialResult_CorrelationDense(PartialResultBase):
    r"""
    This class is an alias of PartialResult()
    """
    __swig_setmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult_CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [PartialResultBase]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult_CorrelationDense, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _pca_.PartialResult_CorrelationDense_serializationTag
    if _newclass:
        serializationTag = staticmethod(_pca_.PartialResult_CorrelationDense_serializationTag)

    def getSerializationTag(self):
        return _pca_.PartialResult_CorrelationDense_getSerializationTag(self)

    def __init__(self):
        this = _pca_.new_PartialResult_CorrelationDense()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _pca_.PartialResult_CorrelationDense_get(self, id)

    def getNFeatures(self):
        return _pca_.PartialResult_CorrelationDense_getNFeatures(self)

    def set(self, id, value):
        return _pca_.PartialResult_CorrelationDense_set(self, id, value)
    __swig_destroy__ = _pca_.delete_PartialResult_CorrelationDense
    __del__ = lambda self: None

    def check(self, *args):
        return _pca_.PartialResult_CorrelationDense_check(self, *args)

    def initialize_Float32(self, input, parameter, method):
        return _pca_.PartialResult_CorrelationDense_initialize_Float32(self, input, parameter, method)

    def initialize_Float64(self, input, parameter, method):
        return _pca_.PartialResult_CorrelationDense_initialize_Float64(self, input, parameter, method)

    def allocate_Float32(self, input, parameter, method):
        return _pca_.PartialResult_CorrelationDense_allocate_Float32(self, input, parameter, method)

    def allocate_Float64(self, input, parameter, method):
        return _pca_.PartialResult_CorrelationDense_allocate_Float64(self, input, parameter, method)
PartialResult_CorrelationDense_swigregister = _pca_.PartialResult_CorrelationDense_swigregister
PartialResult_CorrelationDense_swigregister(PartialResult_CorrelationDense)

def PartialResult_CorrelationDense_serializationTag():
    return _pca_.PartialResult_CorrelationDense_serializationTag()
PartialResult_CorrelationDense_serializationTag = _pca_.PartialResult_CorrelationDense_serializationTag

class DistributedInput_SvdDense(InputIface):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedInput_SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _pca_.DistributedInput_SvdDense_set(self, id, ptr)

    def get(self, id):
        return _pca_.DistributedInput_SvdDense_get(self, id)

    def add(self, id, value):
        return _pca_.DistributedInput_SvdDense_add(self, id, value)

    def getPartialResult(self, id):
        return _pca_.DistributedInput_SvdDense_getPartialResult(self, id)

    def check(self, parameter, method):
        return _pca_.DistributedInput_SvdDense_check(self, parameter, method)

    def getNFeatures(self):
        return _pca_.DistributedInput_SvdDense_getNFeatures(self)
    __swig_destroy__ = _pca_.delete_DistributedInput_SvdDense
    __del__ = lambda self: None
DistributedInput_SvdDense_swigregister = _pca_.DistributedInput_SvdDense_swigregister
DistributedInput_SvdDense_swigregister(DistributedInput_SvdDense)

class DistributedInput_CorrelationDense(InputIface):
    r"""
    This class is an alias of DistributedInput()
    """
    __swig_setmethods__ = {}
    for _s in [InputIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedInput_CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [InputIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedInput_CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedInput_CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def set(self, id, ptr):
        return _pca_.DistributedInput_CorrelationDense_set(self, id, ptr)

    def get(self, id):
        return _pca_.DistributedInput_CorrelationDense_get(self, id)

    def getPartialResult(self, id):
        return _pca_.DistributedInput_CorrelationDense_getPartialResult(self, id)

    def add(self, id, value):
        return _pca_.DistributedInput_CorrelationDense_add(self, id, value)

    def getNFeatures(self):
        return _pca_.DistributedInput_CorrelationDense_getNFeatures(self)

    def check(self, parameter, method):
        return _pca_.DistributedInput_CorrelationDense_check(self, parameter, method)
    __swig_destroy__ = _pca_.delete_DistributedInput_CorrelationDense
    __del__ = lambda self: None
DistributedInput_CorrelationDense_swigregister = _pca_.DistributedInput_CorrelationDense_swigregister
DistributedInput_CorrelationDense_swigregister(DistributedInput_CorrelationDense)

class Batch_Float64SvdDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Batch_Float64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Batch_Float64SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Batch_Float64SvdDense_getMethod(self)

    def setResult(self, res):
        return _pca_.Batch_Float64SvdDense_setResult(self, res)

    def getResult(self):
        return _pca_.Batch_Float64SvdDense_getResult(self)

    def clone(self):
        return _pca_.Batch_Float64SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Batch_Float64SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Batch_Float64SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Batch_Float64SvdDense_input_get, _pca_.Batch_Float64SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Batch_Float64SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Batch_Float64SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Batch_Float64SvdDense_parameter_get, _pca_.Batch_Float64SvdDense_parameter_set)

    def compute(self):
        return _pca_.Batch_Float64SvdDense_compute(self)
Batch_Float64SvdDense_swigregister = _pca_.Batch_Float64SvdDense_swigregister
Batch_Float64SvdDense_swigregister(Batch_Float64SvdDense)

class Batch_Float64CorrelationDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Batch_Float64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Batch_Float64CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Batch_Float64CorrelationDense_getMethod(self)

    def setResult(self, res):
        return _pca_.Batch_Float64CorrelationDense_setResult(self, res)

    def getResult(self):
        return _pca_.Batch_Float64CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Batch_Float64CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Batch_Float64CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Batch_Float64CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Batch_Float64CorrelationDense_input_get, _pca_.Batch_Float64CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Batch_Float64CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Batch_Float64CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Batch_Float64CorrelationDense_parameter_get, _pca_.Batch_Float64CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Batch_Float64CorrelationDense_compute(self)
Batch_Float64CorrelationDense_swigregister = _pca_.Batch_Float64CorrelationDense_swigregister
Batch_Float64CorrelationDense_swigregister(Batch_Float64CorrelationDense)

class Batch_Float32SvdDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Batch_Float32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Batch_Float32SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Batch_Float32SvdDense_getMethod(self)

    def setResult(self, res):
        return _pca_.Batch_Float32SvdDense_setResult(self, res)

    def getResult(self):
        return _pca_.Batch_Float32SvdDense_getResult(self)

    def clone(self):
        return _pca_.Batch_Float32SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Batch_Float32SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Batch_Float32SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Batch_Float32SvdDense_input_get, _pca_.Batch_Float32SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Batch_Float32SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Batch_Float32SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Batch_Float32SvdDense_parameter_get, _pca_.Batch_Float32SvdDense_parameter_set)

    def compute(self):
        return _pca_.Batch_Float32SvdDense_compute(self)
Batch_Float32SvdDense_swigregister = _pca_.Batch_Float32SvdDense_swigregister
Batch_Float32SvdDense_swigregister(Batch_Float32SvdDense)

class Batch_Float32CorrelationDense(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Batch_Float32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Batch_Float32CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Batch_Float32CorrelationDense_getMethod(self)

    def setResult(self, res):
        return _pca_.Batch_Float32CorrelationDense_setResult(self, res)

    def getResult(self):
        return _pca_.Batch_Float32CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Batch_Float32CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Batch_Float32CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Batch_Float32CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Batch_Float32CorrelationDense_input_get, _pca_.Batch_Float32CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Batch_Float32CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Batch_Float32CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Batch_Float32CorrelationDense_parameter_get, _pca_.Batch_Float32CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Batch_Float32CorrelationDense_compute(self)
Batch_Float32CorrelationDense_swigregister = _pca_.Batch_Float32CorrelationDense_swigregister
Batch_Float32CorrelationDense_swigregister(Batch_Float32CorrelationDense)

class BatchParameter_Float64SvdDense(BaseBatchParameter):
    r"""
    This class is an alias of BatchParameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchParameter_Float64SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchParameter_Float64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_BatchParameter_Float64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["normalization"] = _pca_.BatchParameter_Float64SvdDense_normalization_set
    __swig_getmethods__["normalization"] = _pca_.BatchParameter_Float64SvdDense_normalization_get
    if _newclass:
        normalization = _swig_property(_pca_.BatchParameter_Float64SvdDense_normalization_get, _pca_.BatchParameter_Float64SvdDense_normalization_set)

    def check(self):
        return _pca_.BatchParameter_Float64SvdDense_check(self)
    __swig_destroy__ = _pca_.delete_BatchParameter_Float64SvdDense
    __del__ = lambda self: None
BatchParameter_Float64SvdDense_swigregister = _pca_.BatchParameter_Float64SvdDense_swigregister
BatchParameter_Float64SvdDense_swigregister(BatchParameter_Float64SvdDense)

class BatchParameter_Float64CorrelationDense(BaseBatchParameter):
    r"""
    This class is an alias of BatchParameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchParameter_Float64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchParameter_Float64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_BatchParameter_Float64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.BatchParameter_Float64CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.BatchParameter_Float64CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.BatchParameter_Float64CorrelationDense_covariance_get, _pca_.BatchParameter_Float64CorrelationDense_covariance_set)

    def check(self):
        return _pca_.BatchParameter_Float64CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_BatchParameter_Float64CorrelationDense
    __del__ = lambda self: None
BatchParameter_Float64CorrelationDense_swigregister = _pca_.BatchParameter_Float64CorrelationDense_swigregister
BatchParameter_Float64CorrelationDense_swigregister(BatchParameter_Float64CorrelationDense)

class BatchParameter_Float32SvdDense(BaseBatchParameter):
    r"""
    This class is an alias of BatchParameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchParameter_Float32SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchParameter_Float32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_BatchParameter_Float32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["normalization"] = _pca_.BatchParameter_Float32SvdDense_normalization_set
    __swig_getmethods__["normalization"] = _pca_.BatchParameter_Float32SvdDense_normalization_get
    if _newclass:
        normalization = _swig_property(_pca_.BatchParameter_Float32SvdDense_normalization_get, _pca_.BatchParameter_Float32SvdDense_normalization_set)

    def check(self):
        return _pca_.BatchParameter_Float32SvdDense_check(self)
    __swig_destroy__ = _pca_.delete_BatchParameter_Float32SvdDense
    __del__ = lambda self: None
BatchParameter_Float32SvdDense_swigregister = _pca_.BatchParameter_Float32SvdDense_swigregister
BatchParameter_Float32SvdDense_swigregister(BatchParameter_Float32SvdDense)

class BatchParameter_Float32CorrelationDense(BaseBatchParameter):
    r"""
    This class is an alias of BatchParameter()
    """
    __swig_setmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, BatchParameter_Float32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [BaseBatchParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, BatchParameter_Float32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_BatchParameter_Float32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.BatchParameter_Float32CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.BatchParameter_Float32CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.BatchParameter_Float32CorrelationDense_covariance_get, _pca_.BatchParameter_Float32CorrelationDense_covariance_set)

    def check(self):
        return _pca_.BatchParameter_Float32CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_BatchParameter_Float32CorrelationDense
    __del__ = lambda self: None
BatchParameter_Float32CorrelationDense_swigregister = _pca_.BatchParameter_Float32CorrelationDense_swigregister
BatchParameter_Float32CorrelationDense_swigregister(BatchParameter_Float32CorrelationDense)

class Online_Float64SvdDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Online_Float64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Online_Float64SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Online_Float64SvdDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Online_Float64SvdDense_setPartialResult(self, partialResult)

    def setResult(self, res):
        return _pca_.Online_Float64SvdDense_setResult(self, res)

    def getPartialResult(self):
        return _pca_.Online_Float64SvdDense_getPartialResult(self)

    def getResult(self):
        return _pca_.Online_Float64SvdDense_getResult(self)

    def clone(self):
        return _pca_.Online_Float64SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Online_Float64SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Online_Float64SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Online_Float64SvdDense_input_get, _pca_.Online_Float64SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Online_Float64SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Online_Float64SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Online_Float64SvdDense_parameter_get, _pca_.Online_Float64SvdDense_parameter_set)

    def compute(self):
        return _pca_.Online_Float64SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Online_Float64SvdDense_finalizeCompute(self)
Online_Float64SvdDense_swigregister = _pca_.Online_Float64SvdDense_swigregister
Online_Float64SvdDense_swigregister(Online_Float64SvdDense)

class Online_Float64CorrelationDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Online_Float64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Online_Float64CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Online_Float64CorrelationDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Online_Float64CorrelationDense_setPartialResult(self, partialResult)

    def setResult(self, res):
        return _pca_.Online_Float64CorrelationDense_setResult(self, res)

    def getPartialResult(self):
        return _pca_.Online_Float64CorrelationDense_getPartialResult(self)

    def getResult(self):
        return _pca_.Online_Float64CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Online_Float64CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Online_Float64CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Online_Float64CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Online_Float64CorrelationDense_input_get, _pca_.Online_Float64CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Online_Float64CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Online_Float64CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Online_Float64CorrelationDense_parameter_get, _pca_.Online_Float64CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Online_Float64CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Online_Float64CorrelationDense_finalizeCompute(self)
Online_Float64CorrelationDense_swigregister = _pca_.Online_Float64CorrelationDense_swigregister
Online_Float64CorrelationDense_swigregister(Online_Float64CorrelationDense)

class Online_Float32SvdDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Online_Float32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Online_Float32SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Online_Float32SvdDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Online_Float32SvdDense_setPartialResult(self, partialResult)

    def setResult(self, res):
        return _pca_.Online_Float32SvdDense_setResult(self, res)

    def getPartialResult(self):
        return _pca_.Online_Float32SvdDense_getPartialResult(self)

    def getResult(self):
        return _pca_.Online_Float32SvdDense_getResult(self)

    def clone(self):
        return _pca_.Online_Float32SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Online_Float32SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Online_Float32SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Online_Float32SvdDense_input_get, _pca_.Online_Float32SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Online_Float32SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Online_Float32SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Online_Float32SvdDense_parameter_get, _pca_.Online_Float32SvdDense_parameter_set)

    def compute(self):
        return _pca_.Online_Float32SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Online_Float32SvdDense_finalizeCompute(self)
Online_Float32SvdDense_swigregister = _pca_.Online_Float32SvdDense_swigregister
Online_Float32SvdDense_swigregister(Online_Float32SvdDense)

class Online_Float32CorrelationDense(daal.algorithms.Analysis_Online):
    r"""
    This class is an alias of Online()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Online_Float32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Online_Float32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Online_Float32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Online_Float32CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Online_Float32CorrelationDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Online_Float32CorrelationDense_setPartialResult(self, partialResult)

    def setResult(self, res):
        return _pca_.Online_Float32CorrelationDense_setResult(self, res)

    def getPartialResult(self):
        return _pca_.Online_Float32CorrelationDense_getPartialResult(self)

    def getResult(self):
        return _pca_.Online_Float32CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Online_Float32CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Online_Float32CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Online_Float32CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Online_Float32CorrelationDense_input_get, _pca_.Online_Float32CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Online_Float32CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Online_Float32CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Online_Float32CorrelationDense_parameter_get, _pca_.Online_Float32CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Online_Float32CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Online_Float32CorrelationDense_finalizeCompute(self)
Online_Float32CorrelationDense_swigregister = _pca_.Online_Float32CorrelationDense_swigregister
Online_Float32CorrelationDense_swigregister(Online_Float32CorrelationDense)

class OnlineParameter_Float64SvdDense(_object):
    r"""
    This class is an alias of OnlineParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineParameter_Float64SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineParameter_Float64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_OnlineParameter_Float64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _pca_.OnlineParameter_Float64SvdDense_check(self)
    __swig_destroy__ = _pca_.delete_OnlineParameter_Float64SvdDense
    __del__ = lambda self: None
OnlineParameter_Float64SvdDense_swigregister = _pca_.OnlineParameter_Float64SvdDense_swigregister
OnlineParameter_Float64SvdDense_swigregister(OnlineParameter_Float64SvdDense)

class OnlineParameter_Float64CorrelationDense(_object):
    r"""
    This class is an alias of OnlineParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineParameter_Float64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineParameter_Float64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_OnlineParameter_Float64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.OnlineParameter_Float64CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.OnlineParameter_Float64CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.OnlineParameter_Float64CorrelationDense_covariance_get, _pca_.OnlineParameter_Float64CorrelationDense_covariance_set)

    def check(self):
        return _pca_.OnlineParameter_Float64CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_OnlineParameter_Float64CorrelationDense
    __del__ = lambda self: None
OnlineParameter_Float64CorrelationDense_swigregister = _pca_.OnlineParameter_Float64CorrelationDense_swigregister
OnlineParameter_Float64CorrelationDense_swigregister(OnlineParameter_Float64CorrelationDense)

class OnlineParameter_Float32SvdDense(_object):
    r"""
    This class is an alias of OnlineParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineParameter_Float32SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineParameter_Float32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_OnlineParameter_Float32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def check(self):
        return _pca_.OnlineParameter_Float32SvdDense_check(self)
    __swig_destroy__ = _pca_.delete_OnlineParameter_Float32SvdDense
    __del__ = lambda self: None
OnlineParameter_Float32SvdDense_swigregister = _pca_.OnlineParameter_Float32SvdDense_swigregister
OnlineParameter_Float32SvdDense_swigregister(OnlineParameter_Float32SvdDense)

class OnlineParameter_Float32CorrelationDense(_object):
    r"""
    This class is an alias of OnlineParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, OnlineParameter_Float32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, OnlineParameter_Float32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_OnlineParameter_Float32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.OnlineParameter_Float32CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.OnlineParameter_Float32CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.OnlineParameter_Float32CorrelationDense_covariance_get, _pca_.OnlineParameter_Float32CorrelationDense_covariance_set)

    def check(self):
        return _pca_.OnlineParameter_Float32CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_OnlineParameter_Float32CorrelationDense
    __del__ = lambda self: None
OnlineParameter_Float32CorrelationDense_swigregister = _pca_.OnlineParameter_Float32CorrelationDense_swigregister
OnlineParameter_Float32CorrelationDense_swigregister(OnlineParameter_Float32CorrelationDense)

class Distributed_Step1LocalFloat64SvdDense(Online_Float64SvdDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64SvdDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64SvdDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step1LocalFloat64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _pca_.Distributed_Step1LocalFloat64SvdDense_clone(self)

    def compute(self):
        return _pca_.Distributed_Step1LocalFloat64SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step1LocalFloat64SvdDense_finalizeCompute(self)
    __swig_destroy__ = _pca_.delete_Distributed_Step1LocalFloat64SvdDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64SvdDense_swigregister = _pca_.Distributed_Step1LocalFloat64SvdDense_swigregister
Distributed_Step1LocalFloat64SvdDense_swigregister(Distributed_Step1LocalFloat64SvdDense)

class Distributed_Step1LocalFloat64CorrelationDense(Online_Float64CorrelationDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float64CorrelationDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float64CorrelationDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step1LocalFloat64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _pca_.Distributed_Step1LocalFloat64CorrelationDense_clone(self)

    def compute(self):
        return _pca_.Distributed_Step1LocalFloat64CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step1LocalFloat64CorrelationDense_finalizeCompute(self)
    __swig_destroy__ = _pca_.delete_Distributed_Step1LocalFloat64CorrelationDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat64CorrelationDense_swigregister = _pca_.Distributed_Step1LocalFloat64CorrelationDense_swigregister
Distributed_Step1LocalFloat64CorrelationDense_swigregister(Distributed_Step1LocalFloat64CorrelationDense)

class Distributed_Step1LocalFloat32SvdDense(Online_Float32SvdDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32SvdDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32SvdDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step1LocalFloat32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _pca_.Distributed_Step1LocalFloat32SvdDense_clone(self)

    def compute(self):
        return _pca_.Distributed_Step1LocalFloat32SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step1LocalFloat32SvdDense_finalizeCompute(self)
    __swig_destroy__ = _pca_.delete_Distributed_Step1LocalFloat32SvdDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32SvdDense_swigregister = _pca_.Distributed_Step1LocalFloat32SvdDense_swigregister
Distributed_Step1LocalFloat32SvdDense_swigregister(Distributed_Step1LocalFloat32SvdDense)

class Distributed_Step1LocalFloat32CorrelationDense(Online_Float32CorrelationDense):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [Online_Float32CorrelationDense]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step1LocalFloat32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [Online_Float32CorrelationDense]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step1LocalFloat32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step1LocalFloat32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def clone(self):
        return _pca_.Distributed_Step1LocalFloat32CorrelationDense_clone(self)

    def compute(self):
        return _pca_.Distributed_Step1LocalFloat32CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step1LocalFloat32CorrelationDense_finalizeCompute(self)
    __swig_destroy__ = _pca_.delete_Distributed_Step1LocalFloat32CorrelationDense
    __del__ = lambda self: None
Distributed_Step1LocalFloat32CorrelationDense_swigregister = _pca_.Distributed_Step1LocalFloat32CorrelationDense_swigregister
Distributed_Step1LocalFloat32CorrelationDense_swigregister(Distributed_Step1LocalFloat32CorrelationDense)

class Distributed_Step2MasterFloat64SvdDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step2MasterFloat64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Distributed_Step2MasterFloat64SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_getPartialResult(self)

    def setResult(self, res):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_setResult(self, res)

    def getResult(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_getResult(self)

    def clone(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Distributed_Step2MasterFloat64SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Distributed_Step2MasterFloat64SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Distributed_Step2MasterFloat64SvdDense_input_get, _pca_.Distributed_Step2MasterFloat64SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat64SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat64SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Distributed_Step2MasterFloat64SvdDense_parameter_get, _pca_.Distributed_Step2MasterFloat64SvdDense_parameter_set)

    def compute(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step2MasterFloat64SvdDense_finalizeCompute(self)
Distributed_Step2MasterFloat64SvdDense_swigregister = _pca_.Distributed_Step2MasterFloat64SvdDense_swigregister
Distributed_Step2MasterFloat64SvdDense_swigregister(Distributed_Step2MasterFloat64SvdDense)

class Distributed_Step2MasterFloat64CorrelationDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step2MasterFloat64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Distributed_Step2MasterFloat64CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_getPartialResult(self)

    def setResult(self, res):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_setResult(self, res)

    def getResult(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Distributed_Step2MasterFloat64CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Distributed_Step2MasterFloat64CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Distributed_Step2MasterFloat64CorrelationDense_input_get, _pca_.Distributed_Step2MasterFloat64CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat64CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat64CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Distributed_Step2MasterFloat64CorrelationDense_parameter_get, _pca_.Distributed_Step2MasterFloat64CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step2MasterFloat64CorrelationDense_finalizeCompute(self)
Distributed_Step2MasterFloat64CorrelationDense_swigregister = _pca_.Distributed_Step2MasterFloat64CorrelationDense_swigregister
Distributed_Step2MasterFloat64CorrelationDense_swigregister(Distributed_Step2MasterFloat64CorrelationDense)

class Distributed_Step2MasterFloat32SvdDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32SvdDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step2MasterFloat32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Distributed_Step2MasterFloat32SvdDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_getPartialResult(self)

    def setResult(self, res):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_setResult(self, res)

    def getResult(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_getResult(self)

    def clone(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Distributed_Step2MasterFloat32SvdDense_input_set
    __swig_getmethods__["input"] = _pca_.Distributed_Step2MasterFloat32SvdDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Distributed_Step2MasterFloat32SvdDense_input_get, _pca_.Distributed_Step2MasterFloat32SvdDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat32SvdDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat32SvdDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Distributed_Step2MasterFloat32SvdDense_parameter_get, _pca_.Distributed_Step2MasterFloat32SvdDense_parameter_set)

    def compute(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step2MasterFloat32SvdDense_finalizeCompute(self)
Distributed_Step2MasterFloat32SvdDense_swigregister = _pca_.Distributed_Step2MasterFloat32SvdDense_swigregister
Distributed_Step2MasterFloat32SvdDense_swigregister(Distributed_Step2MasterFloat32SvdDense)

class Distributed_Step2MasterFloat32CorrelationDense(daal.algorithms.Analysis_Distributed):
    r"""
    This class is an alias of Distributed()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Distributed_Step2MasterFloat32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Distributed_Step2MasterFloat32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_Distributed_Step2MasterFloat32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_Distributed_Step2MasterFloat32CorrelationDense
    __del__ = lambda self: None

    def getMethod(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_getMethod(self)

    def setPartialResult(self, partialResult):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_setPartialResult(self, partialResult)

    def getPartialResult(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_getPartialResult(self)

    def setResult(self, res):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_setResult(self, res)

    def getResult(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_getResult(self)

    def clone(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_clone(self)
    __swig_setmethods__["input"] = _pca_.Distributed_Step2MasterFloat32CorrelationDense_input_set
    __swig_getmethods__["input"] = _pca_.Distributed_Step2MasterFloat32CorrelationDense_input_get
    if _newclass:
        input = _swig_property(_pca_.Distributed_Step2MasterFloat32CorrelationDense_input_get, _pca_.Distributed_Step2MasterFloat32CorrelationDense_input_set)
    __swig_setmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat32CorrelationDense_parameter_set
    __swig_getmethods__["parameter"] = _pca_.Distributed_Step2MasterFloat32CorrelationDense_parameter_get
    if _newclass:
        parameter = _swig_property(_pca_.Distributed_Step2MasterFloat32CorrelationDense_parameter_get, _pca_.Distributed_Step2MasterFloat32CorrelationDense_parameter_set)

    def compute(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_compute(self)

    def finalizeCompute(self):
        return _pca_.Distributed_Step2MasterFloat32CorrelationDense_finalizeCompute(self)
Distributed_Step2MasterFloat32CorrelationDense_swigregister = _pca_.Distributed_Step2MasterFloat32CorrelationDense_swigregister
Distributed_Step2MasterFloat32CorrelationDense_swigregister(Distributed_Step2MasterFloat32CorrelationDense)

class DistributedParameter_Step1LocalFloat64SvdDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step1LocalFloat64SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step1LocalFloat64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step1LocalFloat64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step1LocalFloat64SvdDense
    __del__ = lambda self: None
DistributedParameter_Step1LocalFloat64SvdDense_swigregister = _pca_.DistributedParameter_Step1LocalFloat64SvdDense_swigregister
DistributedParameter_Step1LocalFloat64SvdDense_swigregister(DistributedParameter_Step1LocalFloat64SvdDense)

class DistributedParameter_Step1LocalFloat64CorrelationDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step1LocalFloat64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step1LocalFloat64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step1LocalFloat64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step1LocalFloat64CorrelationDense
    __del__ = lambda self: None
DistributedParameter_Step1LocalFloat64CorrelationDense_swigregister = _pca_.DistributedParameter_Step1LocalFloat64CorrelationDense_swigregister
DistributedParameter_Step1LocalFloat64CorrelationDense_swigregister(DistributedParameter_Step1LocalFloat64CorrelationDense)

class DistributedParameter_Step1LocalFloat32SvdDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step1LocalFloat32SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step1LocalFloat32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step1LocalFloat32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step1LocalFloat32SvdDense
    __del__ = lambda self: None
DistributedParameter_Step1LocalFloat32SvdDense_swigregister = _pca_.DistributedParameter_Step1LocalFloat32SvdDense_swigregister
DistributedParameter_Step1LocalFloat32SvdDense_swigregister(DistributedParameter_Step1LocalFloat32SvdDense)

class DistributedParameter_Step1LocalFloat32CorrelationDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step1LocalFloat32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step1LocalFloat32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step1LocalFloat32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step1LocalFloat32CorrelationDense
    __del__ = lambda self: None
DistributedParameter_Step1LocalFloat32CorrelationDense_swigregister = _pca_.DistributedParameter_Step1LocalFloat32CorrelationDense_swigregister
DistributedParameter_Step1LocalFloat32CorrelationDense_swigregister(DistributedParameter_Step1LocalFloat32CorrelationDense)

class DistributedParameter_Step2MasterFloat64SvdDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step2MasterFloat64SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step2MasterFloat64SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step2MasterFloat64SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step2MasterFloat64SvdDense
    __del__ = lambda self: None
DistributedParameter_Step2MasterFloat64SvdDense_swigregister = _pca_.DistributedParameter_Step2MasterFloat64SvdDense_swigregister
DistributedParameter_Step2MasterFloat64SvdDense_swigregister(DistributedParameter_Step2MasterFloat64SvdDense)

class DistributedParameter_Step2MasterFloat64CorrelationDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step2MasterFloat64CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step2MasterFloat64CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step2MasterFloat64CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_covariance_get, _pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_covariance_set)

    def check(self):
        return _pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step2MasterFloat64CorrelationDense
    __del__ = lambda self: None
DistributedParameter_Step2MasterFloat64CorrelationDense_swigregister = _pca_.DistributedParameter_Step2MasterFloat64CorrelationDense_swigregister
DistributedParameter_Step2MasterFloat64CorrelationDense_swigregister(DistributedParameter_Step2MasterFloat64CorrelationDense)

class DistributedParameter_Step2MasterFloat32SvdDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step2MasterFloat32SvdDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step2MasterFloat32SvdDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step2MasterFloat32SvdDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step2MasterFloat32SvdDense
    __del__ = lambda self: None
DistributedParameter_Step2MasterFloat32SvdDense_swigregister = _pca_.DistributedParameter_Step2MasterFloat32SvdDense_swigregister
DistributedParameter_Step2MasterFloat32SvdDense_swigregister(DistributedParameter_Step2MasterFloat32SvdDense)

class DistributedParameter_Step2MasterFloat32CorrelationDense(_object):
    r"""
    This class is an alias of DistributedParameter()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedParameter_Step2MasterFloat32CorrelationDense, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedParameter_Step2MasterFloat32CorrelationDense, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _pca_.new_DistributedParameter_Step2MasterFloat32CorrelationDense(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["covariance"] = _pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_covariance_set
    __swig_getmethods__["covariance"] = _pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_covariance_get
    if _newclass:
        covariance = _swig_property(_pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_covariance_get, _pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_covariance_set)

    def check(self):
        return _pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_check(self)
    __swig_destroy__ = _pca_.delete_DistributedParameter_Step2MasterFloat32CorrelationDense
    __del__ = lambda self: None
DistributedParameter_Step2MasterFloat32CorrelationDense_swigregister = _pca_.DistributedParameter_Step2MasterFloat32CorrelationDense_swigregister
DistributedParameter_Step2MasterFloat32CorrelationDense_swigregister(DistributedParameter_Step2MasterFloat32CorrelationDense)

from numpy import float64, float32, intc

class OnlineParameter(object):
    r"""Factory class for different types of OnlineParameter."""
    def __new__(cls,
                fptype,
                method,
                *args, **kwargs):
        if fptype == float64:
            if method == svdDense:
                return OnlineParameter_Float64SvdDense(*args)
            if method == correlationDense:
                return OnlineParameter_Float64CorrelationDense(*args)
        if fptype == float32:
            if method == svdDense:
                return OnlineParameter_Float32SvdDense(*args)
            if method == correlationDense:
                return OnlineParameter_Float32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for OnlineParameter")

class BatchParameter(object):
    r"""Factory class for different types of BatchParameter."""
    def __new__(cls,
                fptype,
                method,
                *args, **kwargs):
        if fptype == float64:
            if method == svdDense:
                return BatchParameter_Float64SvdDense(*args)
            if method == correlationDense:
                return BatchParameter_Float64CorrelationDense(*args)
        if fptype == float32:
            if method == svdDense:
                return BatchParameter_Float32SvdDense(*args)
            if method == correlationDense:
                return BatchParameter_Float32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for BatchParameter")

class DistributedParameter(object):
    r"""Factory class for different types of DistributedParameter."""
    def __new__(cls,
                step,
                fptype,
                method,
                *args, **kwargs):
        if step == daal.step1Local:
            if fptype == float64:
                    if method == svdDense:
                        return DistributedParameter_Step1LocalFloat64SvdDense(*args)
                    if method == correlationDense:
                        return DistributedParameter_Step1LocalFloat64CorrelationDense(*args)
            if fptype == float32:
                    if method == svdDense:
                        return DistributedParameter_Step1LocalFloat32SvdDense(*args)
                    if method == correlationDense:
                        return DistributedParameter_Step1LocalFloat32CorrelationDense(*args)
        if step == daal.step2Master:
            if fptype == float64:
                    if method == svdDense:
                        return DistributedParameter_Step2MasterFloat64SvdDense(*args)
                    if method == correlationDense:
                        return DistributedParameter_Step2MasterFloat64CorrelationDense(*args)
            if fptype == float32:
                    if method == svdDense:
                        return DistributedParameter_Step2MasterFloat32SvdDense(*args)
                    if method == correlationDense:
                        return DistributedParameter_Step2MasterFloat32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for DistributedParameter")

class PartialResult(object):
    r"""Factory class for different types of PartialResult."""
    def __new__(cls,
                method,
                *args, **kwargs):
        if method == svdDense:
            return PartialResult_SvdDense(*args)
        if method == correlationDense:
            return PartialResult_CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for PartialResult")

class Online(object):
    r"""Factory class for different types of Online."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' in kwargs and kwargs['method'] == svdDense:
                return Online_Float64SvdDense(*args)
            if 'method' not in kwargs or kwargs['method'] == correlationDense:
                return Online_Float64CorrelationDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' in kwargs and kwargs['method'] == svdDense:
                return Online_Float32SvdDense(*args)
            if 'method' not in kwargs or kwargs['method'] == correlationDense:
                return Online_Float32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for Online")

class DistributedInput(object):
    r"""Factory class for different types of DistributedInput."""
    def __new__(cls,
                method,
                *args, **kwargs):
        if method == svdDense:
            return DistributedInput_SvdDense(*args)
        if method == correlationDense:
            return DistributedInput_CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for DistributedInput")

class Distributed(object):
    r"""Factory class for different types of Distributed."""
    def __new__(cls,
                step,
                *args, **kwargs):
        if step == daal.step1Local:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == svdDense:
                        return Distributed_Step1LocalFloat64SvdDense(*args)
                    if 'method' not in kwargs or kwargs['method'] == correlationDense:
                        return Distributed_Step1LocalFloat64CorrelationDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == svdDense:
                        return Distributed_Step1LocalFloat32SvdDense(*args)
                    if 'method' not in kwargs or kwargs['method'] == correlationDense:
                        return Distributed_Step1LocalFloat32CorrelationDense(*args)
        if step == daal.step2Master:
            if 'fptype' not in kwargs or kwargs['fptype'] == float64:
                    if 'method' in kwargs and kwargs['method'] == svdDense:
                        return Distributed_Step2MasterFloat64SvdDense(*args)
                    if 'method' not in kwargs or kwargs['method'] == correlationDense:
                        return Distributed_Step2MasterFloat64CorrelationDense(*args)
            if 'fptype' in kwargs and kwargs['fptype'] == float32:
                    if 'method' in kwargs and kwargs['method'] == svdDense:
                        return Distributed_Step2MasterFloat32SvdDense(*args)
                    if 'method' not in kwargs or kwargs['method'] == correlationDense:
                        return Distributed_Step2MasterFloat32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for Distributed")

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' in kwargs and kwargs['method'] == svdDense:
                return Batch_Float64SvdDense(*args)
            if 'method' not in kwargs or kwargs['method'] == correlationDense:
                return Batch_Float64CorrelationDense(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' in kwargs and kwargs['method'] == svdDense:
                return Batch_Float32SvdDense(*args)
            if 'method' not in kwargs or kwargs['method'] == correlationDense:
                return Batch_Float32CorrelationDense(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


