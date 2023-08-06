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
            fp, pathname, description = imp.find_module('_kernel_function_', [dirname(__file__)])
        except ImportError:
            import _kernel_function_
            return _kernel_function_
        if fp is not None:
            try:
                _mod = imp.load_module('_kernel_function_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _kernel_function_ = swig_import_helper()
    del swig_import_helper
else:
    import _kernel_function_
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
import sys
daal.algorithms.kernel_function = sys.modules[__package__]
del sys


_kernel_function_.vectorVector_swigconstant(_kernel_function_)
vectorVector = _kernel_function_.vectorVector

_kernel_function_.matrixVector_swigconstant(_kernel_function_)
matrixVector = _kernel_function_.matrixVector

_kernel_function_.matrixMatrix_swigconstant(_kernel_function_)
matrixMatrix = _kernel_function_.matrixMatrix

_kernel_function_.X_swigconstant(_kernel_function_)
X = _kernel_function_.X

_kernel_function_.Y_swigconstant(_kernel_function_)
Y = _kernel_function_.Y

_kernel_function_.lastInputId_swigconstant(_kernel_function_)
lastInputId = _kernel_function_.lastInputId

_kernel_function_.values_swigconstant(_kernel_function_)
values = _kernel_function_.values

_kernel_function_.lastResultId_swigconstant(_kernel_function_)
lastResultId = _kernel_function_.lastResultId
class ParameterBase(daal.algorithms.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ParameterBase, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ParameterBase, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _kernel_function_.new_ParameterBase(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["rowIndexX"] = _kernel_function_.ParameterBase_rowIndexX_set
    __swig_getmethods__["rowIndexX"] = _kernel_function_.ParameterBase_rowIndexX_get
    if _newclass:
        rowIndexX = _swig_property(_kernel_function_.ParameterBase_rowIndexX_get, _kernel_function_.ParameterBase_rowIndexX_set)
    __swig_setmethods__["rowIndexY"] = _kernel_function_.ParameterBase_rowIndexY_set
    __swig_getmethods__["rowIndexY"] = _kernel_function_.ParameterBase_rowIndexY_get
    if _newclass:
        rowIndexY = _swig_property(_kernel_function_.ParameterBase_rowIndexY_get, _kernel_function_.ParameterBase_rowIndexY_set)
    __swig_setmethods__["rowIndexResult"] = _kernel_function_.ParameterBase_rowIndexResult_set
    __swig_getmethods__["rowIndexResult"] = _kernel_function_.ParameterBase_rowIndexResult_get
    if _newclass:
        rowIndexResult = _swig_property(_kernel_function_.ParameterBase_rowIndexResult_get, _kernel_function_.ParameterBase_rowIndexResult_set)
    __swig_setmethods__["computationMode"] = _kernel_function_.ParameterBase_computationMode_set
    __swig_getmethods__["computationMode"] = _kernel_function_.ParameterBase_computationMode_get
    if _newclass:
        computationMode = _swig_property(_kernel_function_.ParameterBase_computationMode_get, _kernel_function_.ParameterBase_computationMode_set)
    __swig_destroy__ = _kernel_function_.delete_ParameterBase
    __del__ = lambda self: None
ParameterBase_swigregister = _kernel_function_.ParameterBase_swigregister
ParameterBase_swigregister(ParameterBase)

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
        this = _kernel_function_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kernel_function_.delete_Input
    __del__ = lambda self: None

    def get(self, id):
        return _kernel_function_.Input_get(self, id)

    def set(self, id, ptr):
        return _kernel_function_.Input_set(self, id, ptr)
Input_swigregister = _kernel_function_.Input_swigregister
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
    __swig_getmethods__["serializationTag"] = lambda x: _kernel_function_.Result_serializationTag
    if _newclass:
        serializationTag = staticmethod(_kernel_function_.Result_serializationTag)

    def getSerializationTag(self):
        return _kernel_function_.Result_getSerializationTag(self)

    def __init__(self):
        this = _kernel_function_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _kernel_function_.delete_Result
    __del__ = lambda self: None

    def get(self, id):
        return _kernel_function_.Result_get(self, id)

    def set(self, id, ptr):
        return _kernel_function_.Result_set(self, id, ptr)

    def check(self, input, par, method):
        return _kernel_function_.Result_check(self, input, par, method)

    def allocate_Float64(self, input, par, method):
        r"""
    This function is specialized for float64"""
        return _kernel_function_.Result_allocate_Float64(self, input, par, method)


    def allocate_Float32(self, input, par, method):
        r"""
    This function is specialized for float32"""
        return _kernel_function_.Result_allocate_Float32(self, input, par, method)

Result_swigregister = _kernel_function_.Result_swigregister
Result_swigregister(Result)

def Result_serializationTag():
    return _kernel_function_.Result_serializationTag()
Result_serializationTag = _kernel_function_.Result_serializationTag

class KernelIface(daal.algorithms.Analysis_Batch):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, KernelIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Analysis_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, KernelIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getInput(self):
        return _kernel_function_.KernelIface_getInput(self)

    def getParameter(self):
        return _kernel_function_.KernelIface_getParameter(self)
    __swig_destroy__ = _kernel_function_.delete_KernelIface
    __del__ = lambda self: None

    def getResult(self):
        return _kernel_function_.KernelIface_getResult(self)

    def setResult(self, res):
        return _kernel_function_.KernelIface_setResult(self, res)

    def clone(self):
        return _kernel_function_.KernelIface_clone(self)
KernelIface_swigregister = _kernel_function_.KernelIface_swigregister
KernelIface_swigregister(KernelIface)

from numpy import float64, float32, intc


from . import linear
from . import rbf

# This file is compatible with both classic and new-style classes.


