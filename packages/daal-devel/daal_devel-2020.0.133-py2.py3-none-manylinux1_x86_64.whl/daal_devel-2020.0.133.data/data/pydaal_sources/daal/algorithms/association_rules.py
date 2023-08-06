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
            fp, pathname, description = imp.find_module('_association_rules_', [dirname(__file__)])
        except ImportError:
            import _association_rules_
            return _association_rules_
        if fp is not None:
            try:
                _mod = imp.load_module('_association_rules_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _association_rules_ = swig_import_helper()
    del swig_import_helper
else:
    import _association_rules_
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

_association_rules_.apriori_swigconstant(_association_rules_)
apriori = _association_rules_.apriori

_association_rules_.defaultDense_swigconstant(_association_rules_)
defaultDense = _association_rules_.defaultDense

_association_rules_.itemsetsUnsorted_swigconstant(_association_rules_)
itemsetsUnsorted = _association_rules_.itemsetsUnsorted

_association_rules_.itemsetsSortedBySupport_swigconstant(_association_rules_)
itemsetsSortedBySupport = _association_rules_.itemsetsSortedBySupport

_association_rules_.rulesUnsorted_swigconstant(_association_rules_)
rulesUnsorted = _association_rules_.rulesUnsorted

_association_rules_.rulesSortedByConfidence_swigconstant(_association_rules_)
rulesSortedByConfidence = _association_rules_.rulesSortedByConfidence

_association_rules_.data_swigconstant(_association_rules_)
data = _association_rules_.data

_association_rules_.lastInputId_swigconstant(_association_rules_)
lastInputId = _association_rules_.lastInputId

_association_rules_.largeItemsets_swigconstant(_association_rules_)
largeItemsets = _association_rules_.largeItemsets

_association_rules_.largeItemsetsSupport_swigconstant(_association_rules_)
largeItemsetsSupport = _association_rules_.largeItemsetsSupport

_association_rules_.antecedentItemsets_swigconstant(_association_rules_)
antecedentItemsets = _association_rules_.antecedentItemsets

_association_rules_.consequentItemsets_swigconstant(_association_rules_)
consequentItemsets = _association_rules_.consequentItemsets

_association_rules_.confidence_swigconstant(_association_rules_)
confidence = _association_rules_.confidence

_association_rules_.lastResultId_swigconstant(_association_rules_)
lastResultId = _association_rules_.lastResultId
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
        this = _association_rules_.new_Parameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["minSupport"] = _association_rules_.Parameter_minSupport_set
    __swig_getmethods__["minSupport"] = _association_rules_.Parameter_minSupport_get
    if _newclass:
        minSupport = _swig_property(_association_rules_.Parameter_minSupport_get, _association_rules_.Parameter_minSupport_set)
    __swig_setmethods__["minConfidence"] = _association_rules_.Parameter_minConfidence_set
    __swig_getmethods__["minConfidence"] = _association_rules_.Parameter_minConfidence_get
    if _newclass:
        minConfidence = _swig_property(_association_rules_.Parameter_minConfidence_get, _association_rules_.Parameter_minConfidence_set)
    __swig_setmethods__["nUniqueItems"] = _association_rules_.Parameter_nUniqueItems_set
    __swig_getmethods__["nUniqueItems"] = _association_rules_.Parameter_nUniqueItems_get
    if _newclass:
        nUniqueItems = _swig_property(_association_rules_.Parameter_nUniqueItems_get, _association_rules_.Parameter_nUniqueItems_set)
    __swig_setmethods__["nTransactions"] = _association_rules_.Parameter_nTransactions_set
    __swig_getmethods__["nTransactions"] = _association_rules_.Parameter_nTransactions_get
    if _newclass:
        nTransactions = _swig_property(_association_rules_.Parameter_nTransactions_get, _association_rules_.Parameter_nTransactions_set)
    __swig_setmethods__["discoverRules"] = _association_rules_.Parameter_discoverRules_set
    __swig_getmethods__["discoverRules"] = _association_rules_.Parameter_discoverRules_get
    if _newclass:
        discoverRules = _swig_property(_association_rules_.Parameter_discoverRules_get, _association_rules_.Parameter_discoverRules_set)
    __swig_setmethods__["itemsetsOrder"] = _association_rules_.Parameter_itemsetsOrder_set
    __swig_getmethods__["itemsetsOrder"] = _association_rules_.Parameter_itemsetsOrder_get
    if _newclass:
        itemsetsOrder = _swig_property(_association_rules_.Parameter_itemsetsOrder_get, _association_rules_.Parameter_itemsetsOrder_set)
    __swig_setmethods__["rulesOrder"] = _association_rules_.Parameter_rulesOrder_set
    __swig_getmethods__["rulesOrder"] = _association_rules_.Parameter_rulesOrder_get
    if _newclass:
        rulesOrder = _swig_property(_association_rules_.Parameter_rulesOrder_get, _association_rules_.Parameter_rulesOrder_set)
    __swig_setmethods__["minItemsetSize"] = _association_rules_.Parameter_minItemsetSize_set
    __swig_getmethods__["minItemsetSize"] = _association_rules_.Parameter_minItemsetSize_get
    if _newclass:
        minItemsetSize = _swig_property(_association_rules_.Parameter_minItemsetSize_get, _association_rules_.Parameter_minItemsetSize_set)
    __swig_setmethods__["maxItemsetSize"] = _association_rules_.Parameter_maxItemsetSize_set
    __swig_getmethods__["maxItemsetSize"] = _association_rules_.Parameter_maxItemsetSize_get
    if _newclass:
        maxItemsetSize = _swig_property(_association_rules_.Parameter_maxItemsetSize_get, _association_rules_.Parameter_maxItemsetSize_set)

    def check(self):
        return _association_rules_.Parameter_check(self)
    __swig_destroy__ = _association_rules_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _association_rules_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Input(daal.algorithms.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _association_rules_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _association_rules_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _association_rules_.Input_get(self, id)

    def set(self, id, ptr):
        return _association_rules_.Input_set(self, id, ptr)

    def check(self, par, method):
        return _association_rules_.Input_check(self, par, method)
Input_swigregister = _association_rules_.Input_swigregister
Input_swigregister(Input)

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
    __swig_getmethods__["serializationTag"] = lambda x: _association_rules_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_association_rules_.Result_serializationTag)

    def getSerializationTag(self):
        return _association_rules_.Result_getSerializationTag(self)

    def __init__(self):
        this = _association_rules_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _association_rules_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _association_rules_.Result_get(self, id)

    def set(self, id, ptr):
        return _association_rules_.Result_set(self, id, ptr)

    def check(self, input, par, method):
        return _association_rules_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _association_rules_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _association_rules_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _association_rules_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _association_rules_.Result_serializationTag()
Result_serializationTag = _association_rules_.Result_serializationTag

class Batch_Float64Apriori(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float64Apriori, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float64Apriori, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _association_rules_.new_Batch_Float64Apriori(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _association_rules_.Batch_Float64Apriori_getMethod(self)

    def getResult(self):
        return _association_rules_.Batch_Float64Apriori_getResult(self)

    def setResult(self, res):
        return _association_rules_.Batch_Float64Apriori_setResult(self, res)

    def clone(self):
        return _association_rules_.Batch_Float64Apriori_clone(self)
    __swig_setmethods__["input"] = _association_rules_.Batch_Float64Apriori_input_set
    __swig_getmethods__["input"] = _association_rules_.Batch_Float64Apriori_input_get
    if _newclass:
        input = _swig_property(_association_rules_.Batch_Float64Apriori_input_get, _association_rules_.Batch_Float64Apriori_input_set)
    __swig_setmethods__["parameter"] = _association_rules_.Batch_Float64Apriori_parameter_set
    __swig_getmethods__["parameter"] = _association_rules_.Batch_Float64Apriori_parameter_get
    if _newclass:
        parameter = _swig_property(_association_rules_.Batch_Float64Apriori_parameter_get, _association_rules_.Batch_Float64Apriori_parameter_set)

    def compute(self):
        return _association_rules_.Batch_Float64Apriori_compute(self)
    __swig_destroy__ = _association_rules_.delete_Batch_Float64Apriori
    __del__ = lambda self: None
Batch_Float64Apriori_swigregister = _association_rules_.Batch_Float64Apriori_swigregister
Batch_Float64Apriori_swigregister(Batch_Float64Apriori)

class Batch_Float32Apriori(daal.algorithms.Analysis_Batch):
    r"""
    This class is an alias of Batch()
    """
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Batch_Float32Apriori, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Batch_Float32Apriori, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _association_rules_.new_Batch_Float32Apriori(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getMethod(self):
        return _association_rules_.Batch_Float32Apriori_getMethod(self)

    def getResult(self):
        return _association_rules_.Batch_Float32Apriori_getResult(self)

    def setResult(self, res):
        return _association_rules_.Batch_Float32Apriori_setResult(self, res)

    def clone(self):
        return _association_rules_.Batch_Float32Apriori_clone(self)
    __swig_setmethods__["input"] = _association_rules_.Batch_Float32Apriori_input_set
    __swig_getmethods__["input"] = _association_rules_.Batch_Float32Apriori_input_get
    if _newclass:
        input = _swig_property(_association_rules_.Batch_Float32Apriori_input_get, _association_rules_.Batch_Float32Apriori_input_set)
    __swig_setmethods__["parameter"] = _association_rules_.Batch_Float32Apriori_parameter_set
    __swig_getmethods__["parameter"] = _association_rules_.Batch_Float32Apriori_parameter_get
    if _newclass:
        parameter = _swig_property(_association_rules_.Batch_Float32Apriori_parameter_get, _association_rules_.Batch_Float32Apriori_parameter_set)

    def compute(self):
        return _association_rules_.Batch_Float32Apriori_compute(self)
    __swig_destroy__ = _association_rules_.delete_Batch_Float32Apriori
    __del__ = lambda self: None
Batch_Float32Apriori_swigregister = _association_rules_.Batch_Float32Apriori_swigregister
Batch_Float32Apriori_swigregister(Batch_Float32Apriori)

from numpy import float64, float32, intc

class Batch(object):
    r"""Factory class for different types of Batch."""
    def __new__(cls,
                *args, **kwargs):
        if 'fptype' not in kwargs or kwargs['fptype'] == float64:
            if 'method' not in kwargs or kwargs['method'] == apriori:
                return Batch_Float64Apriori(*args)
        if 'fptype' in kwargs and kwargs['fptype'] == float32:
            if 'method' not in kwargs or kwargs['method'] == apriori:
                return Batch_Float32Apriori(*args)

        raise RuntimeError("No appropriate constructor found for Batch")


# This file is compatible with both classic and new-style classes.


