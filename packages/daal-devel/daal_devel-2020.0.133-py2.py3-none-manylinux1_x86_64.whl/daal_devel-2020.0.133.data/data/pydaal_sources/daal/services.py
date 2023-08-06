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
            fp, pathname, description = imp.find_module('_services_', [dirname(__file__)])
        except ImportError:
            import _services_
            return _services_
        if fp is not None:
            try:
                _mod = imp.load_module('_services_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _services_ = swig_import_helper()
    del swig_import_helper
else:
    import _services_
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


import daal

_services_.__INTEL_DAAL_BUILD_DATE_swigconstant(_services_)
__INTEL_DAAL_BUILD_DATE = _services_.__INTEL_DAAL_BUILD_DATE

_services_.__INTEL_DAAL___swigconstant(_services_)
__INTEL_DAAL__ = _services_.__INTEL_DAAL__

_services_.__INTEL_DAAL_MINOR___swigconstant(_services_)
__INTEL_DAAL_MINOR__ = _services_.__INTEL_DAAL_MINOR__

_services_.__INTEL_DAAL_UPDATE___swigconstant(_services_)
__INTEL_DAAL_UPDATE__ = _services_.__INTEL_DAAL_UPDATE__

_services_.INTEL_DAAL_VERSION_swigconstant(_services_)
INTEL_DAAL_VERSION = _services_.INTEL_DAAL_VERSION
class LibraryVersionInfo(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LibraryVersionInfo, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LibraryVersionInfo, name)
    __repr__ = _swig_repr
    __swig_getmethods__["majorVersion"] = _services_.LibraryVersionInfo_majorVersion_get
    if _newclass:
        majorVersion = _swig_property(_services_.LibraryVersionInfo_majorVersion_get)
    __swig_getmethods__["minorVersion"] = _services_.LibraryVersionInfo_minorVersion_get
    if _newclass:
        minorVersion = _swig_property(_services_.LibraryVersionInfo_minorVersion_get)
    __swig_getmethods__["updateVersion"] = _services_.LibraryVersionInfo_updateVersion_get
    if _newclass:
        updateVersion = _swig_property(_services_.LibraryVersionInfo_updateVersion_get)
    __swig_getmethods__["productStatus"] = _services_.LibraryVersionInfo_productStatus_get
    if _newclass:
        productStatus = _swig_property(_services_.LibraryVersionInfo_productStatus_get)
    __swig_getmethods__["build"] = _services_.LibraryVersionInfo_build_get
    if _newclass:
        build = _swig_property(_services_.LibraryVersionInfo_build_get)
    __swig_getmethods__["build_rev"] = _services_.LibraryVersionInfo_build_rev_get
    if _newclass:
        build_rev = _swig_property(_services_.LibraryVersionInfo_build_rev_get)
    __swig_getmethods__["name"] = _services_.LibraryVersionInfo_name_get
    if _newclass:
        name = _swig_property(_services_.LibraryVersionInfo_name_get)
    __swig_getmethods__["processor"] = _services_.LibraryVersionInfo_processor_get
    if _newclass:
        processor = _swig_property(_services_.LibraryVersionInfo_processor_get)

    def __init__(self):
        this = _services_.new_LibraryVersionInfo()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _services_.delete_LibraryVersionInfo
    __del__ = lambda self: None
LibraryVersionInfo_swigregister = _services_.LibraryVersionInfo_swigregister
LibraryVersionInfo_swigregister(LibraryVersionInfo)


_services_.NoErrorMessageDetailFound_swigconstant(_services_)
NoErrorMessageDetailFound = _services_.NoErrorMessageDetailFound

_services_.Row_swigconstant(_services_)
Row = _services_.Row

_services_.Column_swigconstant(_services_)
Column = _services_.Column

_services_.Rank_swigconstant(_services_)
Rank = _services_.Rank

_services_.StatisticsName_swigconstant(_services_)
StatisticsName = _services_.StatisticsName

_services_.Method_swigconstant(_services_)
Method = _services_.Method

_services_.Iteration_swigconstant(_services_)
Iteration = _services_.Iteration

_services_.Component_swigconstant(_services_)
Component = _services_.Component

_services_.Minor_swigconstant(_services_)
Minor = _services_.Minor

_services_.ArgumentName_swigconstant(_services_)
ArgumentName = _services_.ArgumentName

_services_.ElementInCollection_swigconstant(_services_)
ElementInCollection = _services_.ElementInCollection

_services_.Dimension_swigconstant(_services_)
Dimension = _services_.Dimension

_services_.ParameterName_swigconstant(_services_)
ParameterName = _services_.ParameterName

_services_.OptionalInput_swigconstant(_services_)
OptionalInput = _services_.OptionalInput

_services_.OptionalResult_swigconstant(_services_)
OptionalResult = _services_.OptionalResult

_services_.Layer_swigconstant(_services_)
Layer = _services_.Layer

_services_.SerializationTag_swigconstant(_services_)
SerializationTag = _services_.SerializationTag

_services_.ExpectedValue_swigconstant(_services_)
ExpectedValue = _services_.ExpectedValue

_services_.ActualValue_swigconstant(_services_)
ActualValue = _services_.ActualValue

_services_.ErrorMethodNotSupported_swigconstant(_services_)
ErrorMethodNotSupported = _services_.ErrorMethodNotSupported

_services_.ErrorIncorrectNumberOfFeatures_swigconstant(_services_)
ErrorIncorrectNumberOfFeatures = _services_.ErrorIncorrectNumberOfFeatures

_services_.ErrorIncorrectNumberOfObservations_swigconstant(_services_)
ErrorIncorrectNumberOfObservations = _services_.ErrorIncorrectNumberOfObservations

_services_.ErrorIncorrectSizeOfArray_swigconstant(_services_)
ErrorIncorrectSizeOfArray = _services_.ErrorIncorrectSizeOfArray

_services_.ErrorNullParameterNotSupported_swigconstant(_services_)
ErrorNullParameterNotSupported = _services_.ErrorNullParameterNotSupported

_services_.ErrorIncorrectNumberOfArguments_swigconstant(_services_)
ErrorIncorrectNumberOfArguments = _services_.ErrorIncorrectNumberOfArguments

_services_.ErrorIncorrectInputNumericTable_swigconstant(_services_)
ErrorIncorrectInputNumericTable = _services_.ErrorIncorrectInputNumericTable

_services_.ErrorEmptyInputNumericTable_swigconstant(_services_)
ErrorEmptyInputNumericTable = _services_.ErrorEmptyInputNumericTable

_services_.ErrorIncorrectDataRange_swigconstant(_services_)
ErrorIncorrectDataRange = _services_.ErrorIncorrectDataRange

_services_.ErrorPrecomputedStatisticsIndexOutOfRange_swigconstant(_services_)
ErrorPrecomputedStatisticsIndexOutOfRange = _services_.ErrorPrecomputedStatisticsIndexOutOfRange

_services_.ErrorIncorrectNumberOfInputNumericTables_swigconstant(_services_)
ErrorIncorrectNumberOfInputNumericTables = _services_.ErrorIncorrectNumberOfInputNumericTables

_services_.ErrorIncorrectNumberOfOutputNumericTables_swigconstant(_services_)
ErrorIncorrectNumberOfOutputNumericTables = _services_.ErrorIncorrectNumberOfOutputNumericTables

_services_.ErrorNullInputNumericTable_swigconstant(_services_)
ErrorNullInputNumericTable = _services_.ErrorNullInputNumericTable

_services_.ErrorNullOutputNumericTable_swigconstant(_services_)
ErrorNullOutputNumericTable = _services_.ErrorNullOutputNumericTable

_services_.ErrorNullModel_swigconstant(_services_)
ErrorNullModel = _services_.ErrorNullModel

_services_.ErrorInconsistentNumberOfRows_swigconstant(_services_)
ErrorInconsistentNumberOfRows = _services_.ErrorInconsistentNumberOfRows

_services_.ErrorIncorrectSizeOfInputNumericTable_swigconstant(_services_)
ErrorIncorrectSizeOfInputNumericTable = _services_.ErrorIncorrectSizeOfInputNumericTable

_services_.ErrorIncorrectSizeOfOutputNumericTable_swigconstant(_services_)
ErrorIncorrectSizeOfOutputNumericTable = _services_.ErrorIncorrectSizeOfOutputNumericTable

_services_.ErrorIncorrectNumberOfRowsInInputNumericTable_swigconstant(_services_)
ErrorIncorrectNumberOfRowsInInputNumericTable = _services_.ErrorIncorrectNumberOfRowsInInputNumericTable

_services_.ErrorIncorrectNumberOfColumnsInInputNumericTable_swigconstant(_services_)
ErrorIncorrectNumberOfColumnsInInputNumericTable = _services_.ErrorIncorrectNumberOfColumnsInInputNumericTable

_services_.ErrorIncorrectNumberOfRowsInOutputNumericTable_swigconstant(_services_)
ErrorIncorrectNumberOfRowsInOutputNumericTable = _services_.ErrorIncorrectNumberOfRowsInOutputNumericTable

_services_.ErrorIncorrectNumberOfColumnsInOutputNumericTable_swigconstant(_services_)
ErrorIncorrectNumberOfColumnsInOutputNumericTable = _services_.ErrorIncorrectNumberOfColumnsInOutputNumericTable

_services_.ErrorIncorrectTypeOfInputNumericTable_swigconstant(_services_)
ErrorIncorrectTypeOfInputNumericTable = _services_.ErrorIncorrectTypeOfInputNumericTable

_services_.ErrorIncorrectTypeOfOutputNumericTable_swigconstant(_services_)
ErrorIncorrectTypeOfOutputNumericTable = _services_.ErrorIncorrectTypeOfOutputNumericTable

_services_.ErrorIncorrectNumberOfElementsInInputCollection_swigconstant(_services_)
ErrorIncorrectNumberOfElementsInInputCollection = _services_.ErrorIncorrectNumberOfElementsInInputCollection

_services_.ErrorIncorrectNumberOfElementsInResultCollection_swigconstant(_services_)
ErrorIncorrectNumberOfElementsInResultCollection = _services_.ErrorIncorrectNumberOfElementsInResultCollection

_services_.ErrorNullInput_swigconstant(_services_)
ErrorNullInput = _services_.ErrorNullInput

_services_.ErrorNullResult_swigconstant(_services_)
ErrorNullResult = _services_.ErrorNullResult

_services_.ErrorIncorrectParameter_swigconstant(_services_)
ErrorIncorrectParameter = _services_.ErrorIncorrectParameter

_services_.ErrorModelNotFullInitialized_swigconstant(_services_)
ErrorModelNotFullInitialized = _services_.ErrorModelNotFullInitialized

_services_.ErrorInconsistentNumberOfColumns_swigconstant(_services_)
ErrorInconsistentNumberOfColumns = _services_.ErrorInconsistentNumberOfColumns

_services_.ErrorIncorrectIndex_swigconstant(_services_)
ErrorIncorrectIndex = _services_.ErrorIncorrectIndex

_services_.ErrorDataArchiveInternal_swigconstant(_services_)
ErrorDataArchiveInternal = _services_.ErrorDataArchiveInternal

_services_.ErrorNullPartialModel_swigconstant(_services_)
ErrorNullPartialModel = _services_.ErrorNullPartialModel

_services_.ErrorNullInputDataCollection_swigconstant(_services_)
ErrorNullInputDataCollection = _services_.ErrorNullInputDataCollection

_services_.ErrorNullOutputDataCollection_swigconstant(_services_)
ErrorNullOutputDataCollection = _services_.ErrorNullOutputDataCollection

_services_.ErrorNullPartialResult_swigconstant(_services_)
ErrorNullPartialResult = _services_.ErrorNullPartialResult

_services_.ErrorIncorrectNumberOfInputNumericTensors_swigconstant(_services_)
ErrorIncorrectNumberOfInputNumericTensors = _services_.ErrorIncorrectNumberOfInputNumericTensors

_services_.ErrorIncorrectNumberOfOutputNumericTensors_swigconstant(_services_)
ErrorIncorrectNumberOfOutputNumericTensors = _services_.ErrorIncorrectNumberOfOutputNumericTensors

_services_.ErrorNullTensor_swigconstant(_services_)
ErrorNullTensor = _services_.ErrorNullTensor

_services_.ErrorIncorrectNumberOfDimensionsInTensor_swigconstant(_services_)
ErrorIncorrectNumberOfDimensionsInTensor = _services_.ErrorIncorrectNumberOfDimensionsInTensor

_services_.ErrorIncorrectSizeOfDimensionInTensor_swigconstant(_services_)
ErrorIncorrectSizeOfDimensionInTensor = _services_.ErrorIncorrectSizeOfDimensionInTensor

_services_.ErrorNullLayerData_swigconstant(_services_)
ErrorNullLayerData = _services_.ErrorNullLayerData

_services_.ErrorIncorrectSizeOfLayerData_swigconstant(_services_)
ErrorIncorrectSizeOfLayerData = _services_.ErrorIncorrectSizeOfLayerData

_services_.ErrorNullNumericTable_swigconstant(_services_)
ErrorNullNumericTable = _services_.ErrorNullNumericTable

_services_.ErrorIncorrectNumberOfColumns_swigconstant(_services_)
ErrorIncorrectNumberOfColumns = _services_.ErrorIncorrectNumberOfColumns

_services_.ErrorIncorrectNumberOfRows_swigconstant(_services_)
ErrorIncorrectNumberOfRows = _services_.ErrorIncorrectNumberOfRows

_services_.ErrorIncorrectTypeOfNumericTable_swigconstant(_services_)
ErrorIncorrectTypeOfNumericTable = _services_.ErrorIncorrectTypeOfNumericTable

_services_.ErrorUnsupportedCSRIndexing_swigconstant(_services_)
ErrorUnsupportedCSRIndexing = _services_.ErrorUnsupportedCSRIndexing

_services_.ErrorSignificanceLevel_swigconstant(_services_)
ErrorSignificanceLevel = _services_.ErrorSignificanceLevel

_services_.ErrorAccuracyThreshold_swigconstant(_services_)
ErrorAccuracyThreshold = _services_.ErrorAccuracyThreshold

_services_.ErrorIncorrectNumberOfBetas_swigconstant(_services_)
ErrorIncorrectNumberOfBetas = _services_.ErrorIncorrectNumberOfBetas

_services_.ErrorIncorrectNumberOfBetasInReducedModel_swigconstant(_services_)
ErrorIncorrectNumberOfBetasInReducedModel = _services_.ErrorIncorrectNumberOfBetasInReducedModel

_services_.ErrorNumericTableIsNotSquare_swigconstant(_services_)
ErrorNumericTableIsNotSquare = _services_.ErrorNumericTableIsNotSquare

_services_.ErrorNullAuxiliaryAlgorithm_swigconstant(_services_)
ErrorNullAuxiliaryAlgorithm = _services_.ErrorNullAuxiliaryAlgorithm

_services_.ErrorNullInitializationProcedure_swigconstant(_services_)
ErrorNullInitializationProcedure = _services_.ErrorNullInitializationProcedure

_services_.ErrorNullAuxiliaryDataCollection_swigconstant(_services_)
ErrorNullAuxiliaryDataCollection = _services_.ErrorNullAuxiliaryDataCollection

_services_.ErrorEmptyAuxiliaryDataCollection_swigconstant(_services_)
ErrorEmptyAuxiliaryDataCollection = _services_.ErrorEmptyAuxiliaryDataCollection

_services_.ErrorIncorrectElementInCollection_swigconstant(_services_)
ErrorIncorrectElementInCollection = _services_.ErrorIncorrectElementInCollection

_services_.ErrorNullPartialResultDataCollection_swigconstant(_services_)
ErrorNullPartialResultDataCollection = _services_.ErrorNullPartialResultDataCollection

_services_.ErrorIncorrectElementInPartialResultCollection_swigconstant(_services_)
ErrorIncorrectElementInPartialResultCollection = _services_.ErrorIncorrectElementInPartialResultCollection

_services_.ErrorIncorrectElementInNumericTableCollection_swigconstant(_services_)
ErrorIncorrectElementInNumericTableCollection = _services_.ErrorIncorrectElementInNumericTableCollection

_services_.ErrorNullOptionalResult_swigconstant(_services_)
ErrorNullOptionalResult = _services_.ErrorNullOptionalResult

_services_.ErrorIncorrectOptionalResult_swigconstant(_services_)
ErrorIncorrectOptionalResult = _services_.ErrorIncorrectOptionalResult

_services_.ErrorIncorrectOptionalInput_swigconstant(_services_)
ErrorIncorrectOptionalInput = _services_.ErrorIncorrectOptionalInput

_services_.ErrorIncorrectNumberOfPartialClusters_swigconstant(_services_)
ErrorIncorrectNumberOfPartialClusters = _services_.ErrorIncorrectNumberOfPartialClusters

_services_.ErrorIncorrectTotalNumberOfPartialClusters_swigconstant(_services_)
ErrorIncorrectTotalNumberOfPartialClusters = _services_.ErrorIncorrectTotalNumberOfPartialClusters

_services_.ErrorIncorrectDataCollectionSize_swigconstant(_services_)
ErrorIncorrectDataCollectionSize = _services_.ErrorIncorrectDataCollectionSize

_services_.ErrorIncorrectValueInTheNumericTable_swigconstant(_services_)
ErrorIncorrectValueInTheNumericTable = _services_.ErrorIncorrectValueInTheNumericTable

_services_.ErrorIncorrectItemInDataCollection_swigconstant(_services_)
ErrorIncorrectItemInDataCollection = _services_.ErrorIncorrectItemInDataCollection

_services_.ErrorNullPtr_swigconstant(_services_)
ErrorNullPtr = _services_.ErrorNullPtr

_services_.ErrorUndefinedFeature_swigconstant(_services_)
ErrorUndefinedFeature = _services_.ErrorUndefinedFeature

_services_.ErrorCloneMethodFailed_swigconstant(_services_)
ErrorCloneMethodFailed = _services_.ErrorCloneMethodFailed

_services_.ErrorDataTypeNotSupported_swigconstant(_services_)
ErrorDataTypeNotSupported = _services_.ErrorDataTypeNotSupported

_services_.ErrorCpuIsInvalid_swigconstant(_services_)
ErrorCpuIsInvalid = _services_.ErrorCpuIsInvalid

_services_.ErrorCpuNotSupported_swigconstant(_services_)
ErrorCpuNotSupported = _services_.ErrorCpuNotSupported

_services_.ErrorMemoryAllocationFailed_swigconstant(_services_)
ErrorMemoryAllocationFailed = _services_.ErrorMemoryAllocationFailed

_services_.ErrorEmptyDataBlock_swigconstant(_services_)
ErrorEmptyDataBlock = _services_.ErrorEmptyDataBlock

_services_.ErrorIncorrectCombinationOfComputationModeAndStep_swigconstant(_services_)
ErrorIncorrectCombinationOfComputationModeAndStep = _services_.ErrorIncorrectCombinationOfComputationModeAndStep

_services_.ErrorDictionaryAlreadyAvailable_swigconstant(_services_)
ErrorDictionaryAlreadyAvailable = _services_.ErrorDictionaryAlreadyAvailable

_services_.ErrorDictionaryNotAvailable_swigconstant(_services_)
ErrorDictionaryNotAvailable = _services_.ErrorDictionaryNotAvailable

_services_.ErrorNumericTableNotAvailable_swigconstant(_services_)
ErrorNumericTableNotAvailable = _services_.ErrorNumericTableNotAvailable

_services_.ErrorNumericTableAlreadyAllocated_swigconstant(_services_)
ErrorNumericTableAlreadyAllocated = _services_.ErrorNumericTableAlreadyAllocated

_services_.ErrorNumericTableNotAllocated_swigconstant(_services_)
ErrorNumericTableNotAllocated = _services_.ErrorNumericTableNotAllocated

_services_.ErrorPrecomputedSumNotAvailable_swigconstant(_services_)
ErrorPrecomputedSumNotAvailable = _services_.ErrorPrecomputedSumNotAvailable

_services_.ErrorPrecomputedMinNotAvailable_swigconstant(_services_)
ErrorPrecomputedMinNotAvailable = _services_.ErrorPrecomputedMinNotAvailable

_services_.ErrorPrecomputedMaxNotAvailable_swigconstant(_services_)
ErrorPrecomputedMaxNotAvailable = _services_.ErrorPrecomputedMaxNotAvailable

_services_.ErrorServiceMicroTableInternal_swigconstant(_services_)
ErrorServiceMicroTableInternal = _services_.ErrorServiceMicroTableInternal

_services_.ErrorEmptyCSRNumericTable_swigconstant(_services_)
ErrorEmptyCSRNumericTable = _services_.ErrorEmptyCSRNumericTable

_services_.ErrorEmptyHomogenNumericTable_swigconstant(_services_)
ErrorEmptyHomogenNumericTable = _services_.ErrorEmptyHomogenNumericTable

_services_.ErrorSourceDataNotAvailable_swigconstant(_services_)
ErrorSourceDataNotAvailable = _services_.ErrorSourceDataNotAvailable

_services_.ErrorEmptyDataSource_swigconstant(_services_)
ErrorEmptyDataSource = _services_.ErrorEmptyDataSource

_services_.ErrorIncorrectClassLabels_swigconstant(_services_)
ErrorIncorrectClassLabels = _services_.ErrorIncorrectClassLabels

_services_.ErrorIncorrectSizeOfModel_swigconstant(_services_)
ErrorIncorrectSizeOfModel = _services_.ErrorIncorrectSizeOfModel

_services_.ErrorIncorrectTypeOfModel_swigconstant(_services_)
ErrorIncorrectTypeOfModel = _services_.ErrorIncorrectTypeOfModel

_services_.ErrorIncorrectErrorcodeFromGenerator_swigconstant(_services_)
ErrorIncorrectErrorcodeFromGenerator = _services_.ErrorIncorrectErrorcodeFromGenerator

_services_.ErrorLeapfrogUnsupported_swigconstant(_services_)
ErrorLeapfrogUnsupported = _services_.ErrorLeapfrogUnsupported

_services_.ErrorSkipAheadUnsupported_swigconstant(_services_)
ErrorSkipAheadUnsupported = _services_.ErrorSkipAheadUnsupported

_services_.ErrorFeatureNamesNotAvailable_swigconstant(_services_)
ErrorFeatureNamesNotAvailable = _services_.ErrorFeatureNamesNotAvailable

_services_.ErrorEngineNotSupported_swigconstant(_services_)
ErrorEngineNotSupported = _services_.ErrorEngineNotSupported

_services_.ErrorInputSigmaMatrixHasNonPositiveMinor_swigconstant(_services_)
ErrorInputSigmaMatrixHasNonPositiveMinor = _services_.ErrorInputSigmaMatrixHasNonPositiveMinor

_services_.ErrorInputSigmaMatrixHasIllegalValue_swigconstant(_services_)
ErrorInputSigmaMatrixHasIllegalValue = _services_.ErrorInputSigmaMatrixHasIllegalValue

_services_.ErrorIncorrectInternalFunctionParameter_swigconstant(_services_)
ErrorIncorrectInternalFunctionParameter = _services_.ErrorIncorrectInternalFunctionParameter

_services_.ErrorUserCancelled_swigconstant(_services_)
ErrorUserCancelled = _services_.ErrorUserCancelled

_services_.ErrorAprioriIncorrectItemsetTableSize_swigconstant(_services_)
ErrorAprioriIncorrectItemsetTableSize = _services_.ErrorAprioriIncorrectItemsetTableSize

_services_.ErrorAprioriIncorrectSupportTableSize_swigconstant(_services_)
ErrorAprioriIncorrectSupportTableSize = _services_.ErrorAprioriIncorrectSupportTableSize

_services_.ErrorAprioriIncorrectLeftRuleTableSize_swigconstant(_services_)
ErrorAprioriIncorrectLeftRuleTableSize = _services_.ErrorAprioriIncorrectLeftRuleTableSize

_services_.ErrorAprioriIncorrectRightRuleTableSize_swigconstant(_services_)
ErrorAprioriIncorrectRightRuleTableSize = _services_.ErrorAprioriIncorrectRightRuleTableSize

_services_.ErrorAprioriIncorrectConfidenceTableSize_swigconstant(_services_)
ErrorAprioriIncorrectConfidenceTableSize = _services_.ErrorAprioriIncorrectConfidenceTableSize

_services_.ErrorAprioriIncorrectInputData_swigconstant(_services_)
ErrorAprioriIncorrectInputData = _services_.ErrorAprioriIncorrectInputData

_services_.ErrorInconsistentNumberOfClasses_swigconstant(_services_)
ErrorInconsistentNumberOfClasses = _services_.ErrorInconsistentNumberOfClasses

_services_.ErrorCholeskyInternal_swigconstant(_services_)
ErrorCholeskyInternal = _services_.ErrorCholeskyInternal

_services_.ErrorInputMatrixHasNonPositiveMinor_swigconstant(_services_)
ErrorInputMatrixHasNonPositiveMinor = _services_.ErrorInputMatrixHasNonPositiveMinor

_services_.ErrorCovarianceInternal_swigconstant(_services_)
ErrorCovarianceInternal = _services_.ErrorCovarianceInternal

_services_.ErrorEMMatrixInverse_swigconstant(_services_)
ErrorEMMatrixInverse = _services_.ErrorEMMatrixInverse

_services_.ErrorEMIncorrectToleranceToConverge_swigconstant(_services_)
ErrorEMIncorrectToleranceToConverge = _services_.ErrorEMIncorrectToleranceToConverge

_services_.ErrorEMIllConditionedCovarianceMatrix_swigconstant(_services_)
ErrorEMIllConditionedCovarianceMatrix = _services_.ErrorEMIllConditionedCovarianceMatrix

_services_.ErrorEMIncorrectMaxNumberOfIterations_swigconstant(_services_)
ErrorEMIncorrectMaxNumberOfIterations = _services_.ErrorEMIncorrectMaxNumberOfIterations

_services_.ErrorEMNegativeDefinedCovarianceMartix_swigconstant(_services_)
ErrorEMNegativeDefinedCovarianceMartix = _services_.ErrorEMNegativeDefinedCovarianceMartix

_services_.ErrorEMEmptyComponent_swigconstant(_services_)
ErrorEMEmptyComponent = _services_.ErrorEMEmptyComponent

_services_.ErrorEMCovariance_swigconstant(_services_)
ErrorEMCovariance = _services_.ErrorEMCovariance

_services_.ErrorEMIncorrectNumberOfComponents_swigconstant(_services_)
ErrorEMIncorrectNumberOfComponents = _services_.ErrorEMIncorrectNumberOfComponents

_services_.ErrorEMInitNoTrialConverges_swigconstant(_services_)
ErrorEMInitNoTrialConverges = _services_.ErrorEMInitNoTrialConverges

_services_.ErrorEMInitIncorrectToleranceToConverge_swigconstant(_services_)
ErrorEMInitIncorrectToleranceToConverge = _services_.ErrorEMInitIncorrectToleranceToConverge

_services_.ErrorEMInitIncorrectDepthNumberIterations_swigconstant(_services_)
ErrorEMInitIncorrectDepthNumberIterations = _services_.ErrorEMInitIncorrectDepthNumberIterations

_services_.ErrorEMInitIncorrectNumberOfTrials_swigconstant(_services_)
ErrorEMInitIncorrectNumberOfTrials = _services_.ErrorEMInitIncorrectNumberOfTrials

_services_.ErrorEMInitIncorrectNumberOfComponents_swigconstant(_services_)
ErrorEMInitIncorrectNumberOfComponents = _services_.ErrorEMInitIncorrectNumberOfComponents

_services_.ErrorEMInitInconsistentNumberOfComponents_swigconstant(_services_)
ErrorEMInitInconsistentNumberOfComponents = _services_.ErrorEMInitInconsistentNumberOfComponents

_services_.ErrorVarianceComputation_swigconstant(_services_)
ErrorVarianceComputation = _services_.ErrorVarianceComputation

_services_.ErrorKMeansNumberOfClustersIsTooLarge_swigconstant(_services_)
ErrorKMeansNumberOfClustersIsTooLarge = _services_.ErrorKMeansNumberOfClustersIsTooLarge

_services_.ErrorLinearRegressionInternal_swigconstant(_services_)
ErrorLinearRegressionInternal = _services_.ErrorLinearRegressionInternal

_services_.ErrorNormEqSystemSolutionFailed_swigconstant(_services_)
ErrorNormEqSystemSolutionFailed = _services_.ErrorNormEqSystemSolutionFailed

_services_.ErrorLinRegXtXInvFailed_swigconstant(_services_)
ErrorLinRegXtXInvFailed = _services_.ErrorLinRegXtXInvFailed

_services_.ErrorLowOrderMomentsInternal_swigconstant(_services_)
ErrorLowOrderMomentsInternal = _services_.ErrorLowOrderMomentsInternal

_services_.ErrorIncorrectNumberOfClasses_swigconstant(_services_)
ErrorIncorrectNumberOfClasses = _services_.ErrorIncorrectNumberOfClasses

_services_.ErrorMultiClassNullTwoClassTraining_swigconstant(_services_)
ErrorMultiClassNullTwoClassTraining = _services_.ErrorMultiClassNullTwoClassTraining

_services_.ErrorMultiClassFailedToTrainTwoClassClassifier_swigconstant(_services_)
ErrorMultiClassFailedToTrainTwoClassClassifier = _services_.ErrorMultiClassFailedToTrainTwoClassClassifier

_services_.ErrorMultiClassFailedToComputeTwoClassPrediction_swigconstant(_services_)
ErrorMultiClassFailedToComputeTwoClassPrediction = _services_.ErrorMultiClassFailedToComputeTwoClassPrediction

_services_.ErrorEmptyInputCollection_swigconstant(_services_)
ErrorEmptyInputCollection = _services_.ErrorEmptyInputCollection

_services_.ErrorNaiveBayesIncorrectModel_swigconstant(_services_)
ErrorNaiveBayesIncorrectModel = _services_.ErrorNaiveBayesIncorrectModel

_services_.ErrorOutlierDetectionInternal_swigconstant(_services_)
ErrorOutlierDetectionInternal = _services_.ErrorOutlierDetectionInternal

_services_.ErrorPCAFailedToComputeCorrelationEigenvalues_swigconstant(_services_)
ErrorPCAFailedToComputeCorrelationEigenvalues = _services_.ErrorPCAFailedToComputeCorrelationEigenvalues

_services_.ErrorPCACorrelationInputDataTypeSupportsOfflineModeOnly_swigconstant(_services_)
ErrorPCACorrelationInputDataTypeSupportsOfflineModeOnly = _services_.ErrorPCACorrelationInputDataTypeSupportsOfflineModeOnly

_services_.ErrorIncorrectCrossProductTableSize_swigconstant(_services_)
ErrorIncorrectCrossProductTableSize = _services_.ErrorIncorrectCrossProductTableSize

_services_.ErrorCrossProductTableIsNotSquare_swigconstant(_services_)
ErrorCrossProductTableIsNotSquare = _services_.ErrorCrossProductTableIsNotSquare

_services_.ErrorInputCorrelationNotSupportedInOnlineAndDistributed_swigconstant(_services_)
ErrorInputCorrelationNotSupportedInOnlineAndDistributed = _services_.ErrorInputCorrelationNotSupportedInOnlineAndDistributed

_services_.ErrorIncorrectNComponents_swigconstant(_services_)
ErrorIncorrectNComponents = _services_.ErrorIncorrectNComponents

_services_.ErrorQRInternal_swigconstant(_services_)
ErrorQRInternal = _services_.ErrorQRInternal

_services_.ErrorQrIthParamIllegalValue_swigconstant(_services_)
ErrorQrIthParamIllegalValue = _services_.ErrorQrIthParamIllegalValue

_services_.ErrorQrXBDSQRDidNotConverge_swigconstant(_services_)
ErrorQrXBDSQRDidNotConverge = _services_.ErrorQrXBDSQRDidNotConverge

_services_.ErrorStumpIncorrectSplitFeature_swigconstant(_services_)
ErrorStumpIncorrectSplitFeature = _services_.ErrorStumpIncorrectSplitFeature

_services_.ErrorStumpInvalidInputCategoricalData_swigconstant(_services_)
ErrorStumpInvalidInputCategoricalData = _services_.ErrorStumpInvalidInputCategoricalData

_services_.ErrorSvdIthParamIllegalValue_swigconstant(_services_)
ErrorSvdIthParamIllegalValue = _services_.ErrorSvdIthParamIllegalValue

_services_.ErrorSvdXBDSQRDidNotConverge_swigconstant(_services_)
ErrorSvdXBDSQRDidNotConverge = _services_.ErrorSvdXBDSQRDidNotConverge

_services_.ErrorLCNinnerConvolution_swigconstant(_services_)
ErrorLCNinnerConvolution = _services_.ErrorLCNinnerConvolution

_services_.ErrorSVMPredictKernerFunctionCall_swigconstant(_services_)
ErrorSVMPredictKernerFunctionCall = _services_.ErrorSVMPredictKernerFunctionCall

_services_.ErrorIncorrectWeakLearnerClassificationAlgorithm_swigconstant(_services_)
ErrorIncorrectWeakLearnerClassificationAlgorithm = _services_.ErrorIncorrectWeakLearnerClassificationAlgorithm

_services_.ErrorIncorrectWeakLearnerRegressionAlgorithm_swigconstant(_services_)
ErrorIncorrectWeakLearnerRegressionAlgorithm = _services_.ErrorIncorrectWeakLearnerRegressionAlgorithm

_services_.ErrorIncorrectWeakLearnerClassificationModel_swigconstant(_services_)
ErrorIncorrectWeakLearnerClassificationModel = _services_.ErrorIncorrectWeakLearnerClassificationModel

_services_.ErrorIncorrectWeakLearnerRegressionModel_swigconstant(_services_)
ErrorIncorrectWeakLearnerRegressionModel = _services_.ErrorIncorrectWeakLearnerRegressionModel

_services_.ErrorCompressionNullInputStream_swigconstant(_services_)
ErrorCompressionNullInputStream = _services_.ErrorCompressionNullInputStream

_services_.ErrorCompressionNullOutputStream_swigconstant(_services_)
ErrorCompressionNullOutputStream = _services_.ErrorCompressionNullOutputStream

_services_.ErrorCompressionEmptyInputStream_swigconstant(_services_)
ErrorCompressionEmptyInputStream = _services_.ErrorCompressionEmptyInputStream

_services_.ErrorCompressionEmptyOutputStream_swigconstant(_services_)
ErrorCompressionEmptyOutputStream = _services_.ErrorCompressionEmptyOutputStream

_services_.ErrorZlibInternal_swigconstant(_services_)
ErrorZlibInternal = _services_.ErrorZlibInternal

_services_.ErrorZlibDataFormat_swigconstant(_services_)
ErrorZlibDataFormat = _services_.ErrorZlibDataFormat

_services_.ErrorZlibParameters_swigconstant(_services_)
ErrorZlibParameters = _services_.ErrorZlibParameters

_services_.ErrorZlibMemoryAllocationFailed_swigconstant(_services_)
ErrorZlibMemoryAllocationFailed = _services_.ErrorZlibMemoryAllocationFailed

_services_.ErrorZlibNeedDictionary_swigconstant(_services_)
ErrorZlibNeedDictionary = _services_.ErrorZlibNeedDictionary

_services_.ErrorBzip2Internal_swigconstant(_services_)
ErrorBzip2Internal = _services_.ErrorBzip2Internal

_services_.ErrorBzip2DataFormat_swigconstant(_services_)
ErrorBzip2DataFormat = _services_.ErrorBzip2DataFormat

_services_.ErrorBzip2Parameters_swigconstant(_services_)
ErrorBzip2Parameters = _services_.ErrorBzip2Parameters

_services_.ErrorBzip2MemoryAllocationFailed_swigconstant(_services_)
ErrorBzip2MemoryAllocationFailed = _services_.ErrorBzip2MemoryAllocationFailed

_services_.ErrorLzoInternal_swigconstant(_services_)
ErrorLzoInternal = _services_.ErrorLzoInternal

_services_.ErrorLzoOutputStreamSizeIsNotEnough_swigconstant(_services_)
ErrorLzoOutputStreamSizeIsNotEnough = _services_.ErrorLzoOutputStreamSizeIsNotEnough

_services_.ErrorLzoDataFormat_swigconstant(_services_)
ErrorLzoDataFormat = _services_.ErrorLzoDataFormat

_services_.ErrorLzoDataFormatLessThenHeader_swigconstant(_services_)
ErrorLzoDataFormatLessThenHeader = _services_.ErrorLzoDataFormatLessThenHeader

_services_.ErrorLzoDataFormatNotFullBlock_swigconstant(_services_)
ErrorLzoDataFormatNotFullBlock = _services_.ErrorLzoDataFormatNotFullBlock

_services_.ErrorRleInternal_swigconstant(_services_)
ErrorRleInternal = _services_.ErrorRleInternal

_services_.ErrorRleOutputStreamSizeIsNotEnough_swigconstant(_services_)
ErrorRleOutputStreamSizeIsNotEnough = _services_.ErrorRleOutputStreamSizeIsNotEnough

_services_.ErrorRleDataFormat_swigconstant(_services_)
ErrorRleDataFormat = _services_.ErrorRleDataFormat

_services_.ErrorRleDataFormatLessThenHeader_swigconstant(_services_)
ErrorRleDataFormatLessThenHeader = _services_.ErrorRleDataFormatLessThenHeader

_services_.ErrorRleDataFormatNotFullBlock_swigconstant(_services_)
ErrorRleDataFormatNotFullBlock = _services_.ErrorRleDataFormatNotFullBlock

_services_.ErrorLowerBoundGreaterThanOrEqualToUpperBound_swigconstant(_services_)
ErrorLowerBoundGreaterThanOrEqualToUpperBound = _services_.ErrorLowerBoundGreaterThanOrEqualToUpperBound

_services_.ErrorQuantileOrderValueIsInvalid_swigconstant(_services_)
ErrorQuantileOrderValueIsInvalid = _services_.ErrorQuantileOrderValueIsInvalid

_services_.ErrorQuantilesInternal_swigconstant(_services_)
ErrorQuantilesInternal = _services_.ErrorQuantilesInternal

_services_.ErrorALSInternal_swigconstant(_services_)
ErrorALSInternal = _services_.ErrorALSInternal

_services_.ErrorALSInconsistentSparseDataBlocks_swigconstant(_services_)
ErrorALSInconsistentSparseDataBlocks = _services_.ErrorALSInconsistentSparseDataBlocks

_services_.ErrorSorting_swigconstant(_services_)
ErrorSorting = _services_.ErrorSorting

_services_.ErrorNegativeLearningRate_swigconstant(_services_)
ErrorNegativeLearningRate = _services_.ErrorNegativeLearningRate

_services_.ErrorMeanAndStandardDeviationComputing_swigconstant(_services_)
ErrorMeanAndStandardDeviationComputing = _services_.ErrorMeanAndStandardDeviationComputing

_services_.ErrorNullVariance_swigconstant(_services_)
ErrorNullVariance = _services_.ErrorNullVariance

_services_.ErrorMinAndMaxComputing_swigconstant(_services_)
ErrorMinAndMaxComputing = _services_.ErrorMinAndMaxComputing

_services_.ErrorZeroNumberOfTerms_swigconstant(_services_)
ErrorZeroNumberOfTerms = _services_.ErrorZeroNumberOfTerms

_services_.ErrorConvolutionInternal_swigconstant(_services_)
ErrorConvolutionInternal = _services_.ErrorConvolutionInternal

_services_.ErrorIncorrectKernelSise1_swigconstant(_services_)
ErrorIncorrectKernelSise1 = _services_.ErrorIncorrectKernelSise1

_services_.ErrorIncorrectKernelSise2_swigconstant(_services_)
ErrorIncorrectKernelSise2 = _services_.ErrorIncorrectKernelSise2

_services_.ErrorRidgeRegressionInternal_swigconstant(_services_)
ErrorRidgeRegressionInternal = _services_.ErrorRidgeRegressionInternal

_services_.ErrorRidgeRegressionNormEqSystemSolutionFailed_swigconstant(_services_)
ErrorRidgeRegressionNormEqSystemSolutionFailed = _services_.ErrorRidgeRegressionNormEqSystemSolutionFailed

_services_.ErrorRidgeRegressionInvertFailed_swigconstant(_services_)
ErrorRidgeRegressionInvertFailed = _services_.ErrorRidgeRegressionInvertFailed

_services_.ErrorInconsistenceModelAndBatchSizeInParameter_swigconstant(_services_)
ErrorInconsistenceModelAndBatchSizeInParameter = _services_.ErrorInconsistenceModelAndBatchSizeInParameter

_services_.ErrorNeuralNetworkLayerCall_swigconstant(_services_)
ErrorNeuralNetworkLayerCall = _services_.ErrorNeuralNetworkLayerCall

_services_.ErrorSplitLayerBackward_swigconstant(_services_)
ErrorSplitLayerBackward = _services_.ErrorSplitLayerBackward

_services_.ErrorPivotedQRInternal_swigconstant(_services_)
ErrorPivotedQRInternal = _services_.ErrorPivotedQRInternal

_services_.ErrorDFBootstrapVarImportanceIncompatible_swigconstant(_services_)
ErrorDFBootstrapVarImportanceIncompatible = _services_.ErrorDFBootstrapVarImportanceIncompatible

_services_.ErrorDFBootstrapOOBIncompatible_swigconstant(_services_)
ErrorDFBootstrapOOBIncompatible = _services_.ErrorDFBootstrapOOBIncompatible

_services_.ErrorGbtIncorrectNumberOfTrees_swigconstant(_services_)
ErrorGbtIncorrectNumberOfTrees = _services_.ErrorGbtIncorrectNumberOfTrees

_services_.ErrorGbtPredictIncorrectNumberOfIterations_swigconstant(_services_)
ErrorGbtPredictIncorrectNumberOfIterations = _services_.ErrorGbtPredictIncorrectNumberOfIterations

_services_.ErrorUserAllocatedMemory_swigconstant(_services_)
ErrorUserAllocatedMemory = _services_.ErrorUserAllocatedMemory

_services_.ErrorDataSourseNotAvailable_swigconstant(_services_)
ErrorDataSourseNotAvailable = _services_.ErrorDataSourseNotAvailable

_services_.ErrorHandlesSQL_swigconstant(_services_)
ErrorHandlesSQL = _services_.ErrorHandlesSQL

_services_.ErrorODBC_swigconstant(_services_)
ErrorODBC = _services_.ErrorODBC

_services_.ErrorSQLstmtHandle_swigconstant(_services_)
ErrorSQLstmtHandle = _services_.ErrorSQLstmtHandle

_services_.ErrorOnFileOpen_swigconstant(_services_)
ErrorOnFileOpen = _services_.ErrorOnFileOpen

_services_.ErrorOnFileRead_swigconstant(_services_)
ErrorOnFileRead = _services_.ErrorOnFileRead

_services_.ErrorNullByteInjection_swigconstant(_services_)
ErrorNullByteInjection = _services_.ErrorNullByteInjection

_services_.ErrorKDBNoConnection_swigconstant(_services_)
ErrorKDBNoConnection = _services_.ErrorKDBNoConnection

_services_.ErrorKDBWrongCredentials_swigconstant(_services_)
ErrorKDBWrongCredentials = _services_.ErrorKDBWrongCredentials

_services_.ErrorKDBNetworkError_swigconstant(_services_)
ErrorKDBNetworkError = _services_.ErrorKDBNetworkError

_services_.ErrorKDBServerError_swigconstant(_services_)
ErrorKDBServerError = _services_.ErrorKDBServerError

_services_.ErrorKDBTypeUnsupported_swigconstant(_services_)
ErrorKDBTypeUnsupported = _services_.ErrorKDBTypeUnsupported

_services_.ErrorKDBWrongTypeOfOutput_swigconstant(_services_)
ErrorKDBWrongTypeOfOutput = _services_.ErrorKDBWrongTypeOfOutput

_services_.ErrorIncorrectEngineParameter_swigconstant(_services_)
ErrorIncorrectEngineParameter = _services_.ErrorIncorrectEngineParameter

_services_.ErrorEmptyInputAlgorithmsCollection_swigconstant(_services_)
ErrorEmptyInputAlgorithmsCollection = _services_.ErrorEmptyInputAlgorithmsCollection

_services_.ErrorObjectDoesNotSupportSerialization_swigconstant(_services_)
ErrorObjectDoesNotSupportSerialization = _services_.ErrorObjectDoesNotSupportSerialization

_services_.ErrorCouldntAttachCurrentThreadToJavaVM_swigconstant(_services_)
ErrorCouldntAttachCurrentThreadToJavaVM = _services_.ErrorCouldntAttachCurrentThreadToJavaVM

_services_.ErrorCouldntCreateGlobalReferenceToJavaObject_swigconstant(_services_)
ErrorCouldntCreateGlobalReferenceToJavaObject = _services_.ErrorCouldntCreateGlobalReferenceToJavaObject

_services_.ErrorCouldntFindJavaMethod_swigconstant(_services_)
ErrorCouldntFindJavaMethod = _services_.ErrorCouldntFindJavaMethod

_services_.ErrorCouldntFindClassForJavaObject_swigconstant(_services_)
ErrorCouldntFindClassForJavaObject = _services_.ErrorCouldntFindClassForJavaObject

_services_.ErrorCouldntDetachCurrentThreadFromJavaVM_swigconstant(_services_)
ErrorCouldntDetachCurrentThreadFromJavaVM = _services_.ErrorCouldntDetachCurrentThreadFromJavaVM

_services_.UnknownError_swigconstant(_services_)
UnknownError = _services_.UnknownError

_services_.NoErrorMessageFound_swigconstant(_services_)
NoErrorMessageFound = _services_.NoErrorMessageFound

_services_.ErrorMethodNotImplemented_swigconstant(_services_)
ErrorMethodNotImplemented = _services_.ErrorMethodNotImplemented
class Exception(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Exception, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Exception, name)
    __repr__ = _swig_repr

    def __init__(self, description):
        this = _services_.new_Exception(description)
        try:
            self.this.append(this)
        except:
            self.this = this

    def what(self):
        return _services_.Exception_what(self)
    __swig_destroy__ = _services_.delete_Exception
    __del__ = lambda self: None
    __swig_getmethods__["getException"] = lambda x: _services_.Exception_getException
    if _newclass:
        getException = staticmethod(_services_.Exception_getException)
Exception_swigregister = _services_.Exception_swigregister
Exception_swigregister(Exception)

def Exception_getException(*args):
    return _services_.Exception_getException(*args)
Exception_getException = _services_.Exception_getException

class Error(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Error, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Error, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _services_.new_Error(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _services_.delete_Error
    __del__ = lambda self: None

    def id(self):
        return _services_.Error_id(self)

    def setId(self, id):
        return _services_.Error_setId(self, id)

    def description(self):
        return _services_.Error_description(self)

    def addIntDetail(self, id, value):
        return _services_.Error_addIntDetail(self, id, value)

    def addDoubleDetail(self, id, value):
        return _services_.Error_addDoubleDetail(self, id, value)

    def addStringDetail(self, id, value):
        return _services_.Error_addStringDetail(self, id, value)

    def details(self):
        return _services_.Error_details(self)
    __swig_getmethods__["create"] = lambda x: _services_.Error_create
    if _newclass:
        create = staticmethod(_services_.Error_create)
Error_swigregister = _services_.Error_swigregister
Error_swigregister(Error)

def Error_create(*args):
    return _services_.Error_create(*args)
Error_create = _services_.Error_create

class KernelErrorCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KernelErrorCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KernelErrorCollection, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _services_.new_KernelErrorCollection(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def add(self, *args):
        return _services_.KernelErrorCollection_add(self, *args)

    def isEmpty(self):
        return _services_.KernelErrorCollection_isEmpty(self)

    def size(self):
        return _services_.KernelErrorCollection_size(self)

    def at(self, *args):
        return _services_.KernelErrorCollection_at(self, *args)
    __swig_destroy__ = _services_.delete_KernelErrorCollection
    __del__ = lambda self: None

    def getDescription(self):
        return _services_.KernelErrorCollection_getDescription(self)
KernelErrorCollection_swigregister = _services_.KernelErrorCollection_swigregister
KernelErrorCollection_swigregister(KernelErrorCollection)

class Status(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Status, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Status, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _services_.delete_Status
    __del__ = lambda self: None

    def ok(self):
        return _services_.Status_ok(self)
    def __nonzero__(self):
        return _services_.Status___nonzero__(self)
    __bool__ = __nonzero__



    def add(self, *args):
        return _services_.Status_add(self, *args)

    def __ior__(self, other):
        return _services_.Status___ior__(self, other)

    def getDescription(self):
        return _services_.Status_getDescription(self)

    def clear(self):
        return _services_.Status_clear(self)

    def __init__(self, *args):
        this = _services_.new_Status(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getCollection(self):
        return _services_.Status_getCollection(self)
Status_swigregister = _services_.Status_swigregister
Status_swigregister(Status)


def throwIfPossible(s):
    return _services_.throwIfPossible(s)
throwIfPossible = _services_.throwIfPossible

def checkForNullByteInjection(begin, end):
    return _services_.checkForNullByteInjection(begin, end)
checkForNullByteInjection = _services_.checkForNullByteInjection

_services_.sse2_swigconstant(_services_)
sse2 = _services_.sse2

_services_.ssse3_swigconstant(_services_)
ssse3 = _services_.ssse3

_services_.sse42_swigconstant(_services_)
sse42 = _services_.sse42

_services_.avx_swigconstant(_services_)
avx = _services_.avx

_services_.avx2_swigconstant(_services_)
avx2 = _services_.avx2

_services_.avx512_mic_swigconstant(_services_)
avx512_mic = _services_.avx512_mic

_services_.avx512_swigconstant(_services_)
avx512 = _services_.avx512

_services_.avx512_mic_e1_swigconstant(_services_)
avx512_mic_e1 = _services_.avx512_mic_e1

_services_.lastCpuType_swigconstant(_services_)
lastCpuType = _services_.lastCpuType
class Environment(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Environment, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Environment, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["getInstance"] = lambda x: _services_.Environment_getInstance
    if _newclass:
        getInstance = staticmethod(_services_.Environment_getInstance)
    __swig_getmethods__["freeInstance"] = lambda x: _services_.Environment_freeInstance
    if _newclass:
        freeInstance = staticmethod(_services_.Environment_freeInstance)
    cpu_default = _services_.Environment_cpu_default
    avx512_mic = _services_.Environment_avx512_mic
    avx512 = _services_.Environment_avx512
    avx512_mic_e1 = _services_.Environment_avx512_mic_e1

    def getCpuId(self, *args):
        return _services_.Environment_getCpuId(self, *args)

    def setCpuId(self, cpuid):
        return _services_.Environment_setCpuId(self, cpuid)

    def enableInstructionsSet(self, enable):
        return _services_.Environment_enableInstructionsSet(self, enable)
    MultiThreaded = _services_.Environment_MultiThreaded
    SingleThreaded = _services_.Environment_SingleThreaded

    def setDynamicLibraryThreadingTypeOnWindows(self, type):
        return _services_.Environment_setDynamicLibraryThreadingTypeOnWindows(self, type)

    def setNumberOfThreads(self, numThreads):
        return _services_.Environment_setNumberOfThreads(self, numThreads)

    def enableThreadPinning(self, enableThreadPinningFlag=True):
        return _services_.Environment_enableThreadPinning(self, enableThreadPinningFlag)

    def getNumberOfThreads(self):
        return _services_.Environment_getNumberOfThreads(self)

    def setMemoryLimit(self, type, limit):
        return _services_.Environment_setMemoryLimit(self, type, limit)
    __swig_destroy__ = _services_.delete_Environment
    __del__ = lambda self: None
Environment_swigregister = _services_.Environment_swigregister
Environment_swigregister(Environment)

def Environment_getInstance():
    return _services_.Environment_getInstance()
Environment_getInstance = _services_.Environment_getInstance

def Environment_freeInstance():
    return _services_.Environment_freeInstance()
Environment_freeInstance = _services_.Environment_freeInstance

class Collection_SerializationIfacePtr(_object):
    r"""
    This class is an alias of Collection()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Collection_SerializationIfacePtr, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Collection_SerializationIfacePtr, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _services_.new_Collection_SerializationIfacePtr(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _services_.delete_Collection_SerializationIfacePtr
    __del__ = lambda self: None

    def size(self):
        return _services_.Collection_SerializationIfacePtr_size(self)

    def capacity(self):
        return _services_.Collection_SerializationIfacePtr_capacity(self)

    def get(self, *args):
        return _services_.Collection_SerializationIfacePtr_get(self, *args)

    def data(self, *args):
        return _services_.Collection_SerializationIfacePtr_data(self, *args)

    def push_back(self, x):
        return _services_.Collection_SerializationIfacePtr_push_back(self, x)

    def safe_push_back(self, x):
        return _services_.Collection_SerializationIfacePtr_safe_push_back(self, x)

    def __lshift__(self, x):
        return _services_.Collection_SerializationIfacePtr___lshift__(self, x)

    def resize(self, newCapacity):
        return _services_.Collection_SerializationIfacePtr_resize(self, newCapacity)

    def clear(self):
        return _services_.Collection_SerializationIfacePtr_clear(self)

    def insert(self, *args):
        return _services_.Collection_SerializationIfacePtr_insert(self, *args)

    def erase(self, pos):
        return _services_.Collection_SerializationIfacePtr_erase(self, pos)

    def __getitem__(self, i):
        return _services_.Collection_SerializationIfacePtr___getitem__(self, i)

    def __setitem__(self, i, v):
        return _services_.Collection_SerializationIfacePtr___setitem__(self, i, v)
Collection_SerializationIfacePtr_swigregister = _services_.Collection_SerializationIfacePtr_swigregister
Collection_SerializationIfacePtr_swigregister(Collection_SerializationIfacePtr)

class Collection_DataBlock(_object):
    r"""
    This class is an alias of Collection()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Collection_DataBlock, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Collection_DataBlock, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _services_.new_Collection_DataBlock(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _services_.delete_Collection_DataBlock
    __del__ = lambda self: None

    def size(self):
        return _services_.Collection_DataBlock_size(self)

    def capacity(self):
        return _services_.Collection_DataBlock_capacity(self)

    def get(self, *args):
        return _services_.Collection_DataBlock_get(self, *args)

    def data(self, *args):
        return _services_.Collection_DataBlock_data(self, *args)

    def push_back(self, x):
        return _services_.Collection_DataBlock_push_back(self, x)

    def safe_push_back(self, x):
        return _services_.Collection_DataBlock_safe_push_back(self, x)

    def __lshift__(self, x):
        return _services_.Collection_DataBlock___lshift__(self, x)

    def resize(self, newCapacity):
        return _services_.Collection_DataBlock_resize(self, newCapacity)

    def clear(self):
        return _services_.Collection_DataBlock_clear(self)

    def insert(self, *args):
        return _services_.Collection_DataBlock_insert(self, *args)

    def erase(self, pos):
        return _services_.Collection_DataBlock_erase(self, pos)

    def __getitem__(self, i):
        return _services_.Collection_DataBlock___getitem__(self, i)

    def __setitem__(self, i, v):
        return _services_.Collection_DataBlock___setitem__(self, i, v)
Collection_DataBlock_swigregister = _services_.Collection_DataBlock_swigregister
Collection_DataBlock_swigregister(Collection_DataBlock)

from numpy import float64, float32, intc

class Collection(object):
    r"""Factory class for different types of Collection."""
    def __new__(cls,
                DataType,
                *args, **kwargs):
        if DataType == daal.data_management.SerializationIfacePtr:
            return Collection_SerializationIfacePtr(*args)
        if DataType == daal.services.SharedPtr__daal.data_management.DataBlock:
            return Collection_DataBlock(*args)

        raise RuntimeError("No appropriate constructor found for Collection")


# This file is compatible with both classic and new-style classes.


