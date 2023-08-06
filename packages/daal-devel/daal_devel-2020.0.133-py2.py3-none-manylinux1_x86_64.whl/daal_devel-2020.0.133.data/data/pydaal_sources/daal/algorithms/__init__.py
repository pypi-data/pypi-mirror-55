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
            fp, pathname, description = imp.find_module('_algorithms_', [dirname(__file__)])
        except ImportError:
            import _algorithms_
            return _algorithms_
        if fp is not None:
            try:
                _mod = imp.load_module('_algorithms_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _algorithms_ = swig_import_helper()
    del swig_import_helper
else:
    import _algorithms_
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


import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
class Kernel(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Kernel, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Kernel, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _algorithms_.new_Kernel()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Kernel
    __del__ = lambda self: None
Kernel_swigregister = _algorithms_.Kernel_swigregister
Kernel_swigregister(Kernel)

class AlgorithmContainerIfaceImpl(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainerIfaceImpl, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainerIfaceImpl, name)
    __repr__ = _swig_repr

    def __init__(self, daalEnv):
        this = _algorithms_.new_AlgorithmContainerIfaceImpl(daalEnv)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainerIfaceImpl
    __del__ = lambda self: None

    def setEnvironment(self, daalEnv):
        return _algorithms_.AlgorithmContainerIfaceImpl_setEnvironment(self, daalEnv)
AlgorithmContainerIfaceImpl_swigregister = _algorithms_.AlgorithmContainerIfaceImpl_swigregister
AlgorithmContainerIfaceImpl_swigregister(AlgorithmContainerIfaceImpl)

class AlgorithmIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmIface
    __del__ = lambda self: None

    def checkComputeParams(self):
        return _algorithms_.AlgorithmIface_checkComputeParams(self)

    def checkResult(self):
        return _algorithms_.AlgorithmIface_checkResult(self)

    def getMethod(self):
        return _algorithms_.AlgorithmIface_getMethod(self)
AlgorithmIface_swigregister = _algorithms_.AlgorithmIface_swigregister
AlgorithmIface_swigregister(AlgorithmIface)

class AlgorithmIfaceImpl(AlgorithmIface):
    __swig_setmethods__ = {}
    for _s in [AlgorithmIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmIfaceImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmIfaceImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmIfaceImpl
    __del__ = lambda self: None

    def enableChecks(self, enableChecksFlag):
        return _algorithms_.AlgorithmIfaceImpl_enableChecks(self, enableChecksFlag)

    def isChecksEnabled(self):
        return _algorithms_.AlgorithmIfaceImpl_isChecksEnabled(self)
AlgorithmIfaceImpl_swigregister = _algorithms_.AlgorithmIfaceImpl_swigregister
AlgorithmIfaceImpl_swigregister(AlgorithmIfaceImpl)

class Parameter(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _algorithms_.new_Parameter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Parameter
    __del__ = lambda self: None

    def check(self):
        return _algorithms_.Parameter_check(self)
Parameter_swigregister = _algorithms_.Parameter_swigregister
Parameter_swigregister(Parameter)

class Argument(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Argument, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Argument, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _algorithms_.new_Argument(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Argument
    __del__ = lambda self: None

    def __lshift__(self, val):
        return _algorithms_.Argument___lshift__(self, val)

    def size(self):
        return _algorithms_.Argument_size(self)
Argument_swigregister = _algorithms_.Argument_swigregister
Argument_swigregister(Argument)

class SerializableArgument(daal.data_management.SerializationIface, Argument):
    __swig_setmethods__ = {}
    for _s in [daal.data_management.SerializationIface, Argument]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, SerializableArgument, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.data_management.SerializationIface, Argument]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, SerializableArgument, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_SerializableArgument
    __del__ = lambda self: None
SerializableArgument_swigregister = _algorithms_.SerializableArgument_swigregister
SerializableArgument_swigregister(SerializableArgument)

class Input(Argument):
    __swig_setmethods__ = {}
    for _s in [Argument]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [Argument]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _algorithms_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Input
    __del__ = lambda self: None

    def check(self, parameter, method):
        return _algorithms_.Input_check(self, parameter, method)
Input_swigregister = _algorithms_.Input_swigregister
Input_swigregister(Input)

class PartialResult(SerializableArgument):
    __swig_setmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PartialResult, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PartialResult, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _algorithms_.new_PartialResult(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_PartialResult
    __del__ = lambda self: None

    def getSerializationTag(self):
        return _algorithms_.PartialResult_getSerializationTag(self)

    def getInitFlag(self):
        return _algorithms_.PartialResult_getInitFlag(self)

    def setInitFlag(self, flag):
        return _algorithms_.PartialResult_setInitFlag(self, flag)

    def check(self, *args):
        return _algorithms_.PartialResult_check(self, *args)
PartialResult_swigregister = _algorithms_.PartialResult_swigregister
PartialResult_swigregister(PartialResult)

class Result(SerializableArgument):
    __swig_setmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _algorithms_.new_Result(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Result
    __del__ = lambda self: None

    def getSerializationTag(self):
        return _algorithms_.Result_getSerializationTag(self)

    def check(self, *args):
        return _algorithms_.Result_check(self, *args)
Result_swigregister = _algorithms_.Result_swigregister
Result_swigregister(Result)

class OptionalArgument(SerializableArgument):
    __swig_setmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OptionalArgument, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializableArgument]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OptionalArgument, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _algorithms_.OptionalArgument_serializationTag
    if _newclass:
        serializationTag = staticmethod(_algorithms_.OptionalArgument_serializationTag)

    def getSerializationTag(self):
        return _algorithms_.OptionalArgument_getSerializationTag(self)

    def __init__(self, *args):
        this = _algorithms_.new_OptionalArgument(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, index):
        return _algorithms_.OptionalArgument_get(self, index)

    def set(self, index, value):
        return _algorithms_.OptionalArgument_set(self, index, value)
    __swig_destroy__ = _algorithms_.delete_OptionalArgument
    __del__ = lambda self: None
OptionalArgument_swigregister = _algorithms_.OptionalArgument_swigregister
OptionalArgument_swigregister(OptionalArgument)

def OptionalArgument_serializationTag():
    return _algorithms_.OptionalArgument_serializationTag()
OptionalArgument_serializationTag = _algorithms_.OptionalArgument_serializationTag

class Algorithm_Batch(AlgorithmIfaceImpl):
    r"""
    This class is an alias of Algorithm()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Algorithm_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Algorithm_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Algorithm_Batch
    __del__ = lambda self: None

    def checkComputeParams(self):
        return _algorithms_.Algorithm_Batch_checkComputeParams(self)

    def getBaseParameter(self):
        return _algorithms_.Algorithm_Batch_getBaseParameter(self)
Algorithm_Batch_swigregister = _algorithms_.Algorithm_Batch_swigregister
Algorithm_Batch_swigregister(Algorithm_Batch)

class Algorithm_Online(AlgorithmIfaceImpl):
    r"""
    This class is an alias of Algorithm()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Algorithm_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Algorithm_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Algorithm_Online
    __del__ = lambda self: None

    def clean(self):
        return _algorithms_.Algorithm_Online_clean(self)

    def checkPartialResult(self):
        return _algorithms_.Algorithm_Online_checkPartialResult(self)

    def checkFinalizeComputeParams(self):
        return _algorithms_.Algorithm_Online_checkFinalizeComputeParams(self)
Algorithm_Online_swigregister = _algorithms_.Algorithm_Online_swigregister
Algorithm_Online_swigregister(Algorithm_Online)

class Algorithm_Distributed(AlgorithmIfaceImpl):
    r"""
    This class is an alias of Algorithm()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Algorithm_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Algorithm_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Algorithm_Distributed
    __del__ = lambda self: None

    def clean(self):
        return _algorithms_.Algorithm_Distributed_clean(self)

    def checkPartialResult(self):
        return _algorithms_.Algorithm_Distributed_checkPartialResult(self)

    def checkFinalizeComputeParams(self):
        return _algorithms_.Algorithm_Distributed_checkFinalizeComputeParams(self)
Algorithm_Distributed_swigregister = _algorithms_.Algorithm_Distributed_swigregister
Algorithm_Distributed_swigregister(Algorithm_Distributed)

class AlgorithmContainer_Batch(AlgorithmContainerIfaceImpl):
    r"""
    This class is an alias of AlgorithmContainer()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainer_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainer_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainer_Batch
    __del__ = lambda self: None

    def compute(self):
        return _algorithms_.AlgorithmContainer_Batch_compute(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainer_Batch_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainer_Batch_resetCompute(self)
AlgorithmContainer_Batch_swigregister = _algorithms_.AlgorithmContainer_Batch_swigregister
AlgorithmContainer_Batch_swigregister(AlgorithmContainer_Batch)

class AlgorithmContainer_Online(AlgorithmContainerIfaceImpl):
    r"""
    This class is an alias of AlgorithmContainer()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainer_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainer_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainer_Online
    __del__ = lambda self: None

    def compute(self):
        return _algorithms_.AlgorithmContainer_Online_compute(self)

    def finalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Online_finalizeCompute(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainer_Online_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainer_Online_resetCompute(self)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Online_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Online_resetFinalizeCompute(self)
AlgorithmContainer_Online_swigregister = _algorithms_.AlgorithmContainer_Online_swigregister
AlgorithmContainer_Online_swigregister(AlgorithmContainer_Online)

class AlgorithmContainer_Distributed(AlgorithmContainerIfaceImpl):
    r"""
    This class is an alias of AlgorithmContainer()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainer_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainerIfaceImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainer_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainer_Distributed
    __del__ = lambda self: None

    def compute(self):
        return _algorithms_.AlgorithmContainer_Distributed_compute(self)

    def finalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Distributed_finalizeCompute(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainer_Distributed_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainer_Distributed_resetCompute(self)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Distributed_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmContainer_Distributed_resetFinalizeCompute(self)
AlgorithmContainer_Distributed_swigregister = _algorithms_.AlgorithmContainer_Distributed_swigregister
AlgorithmContainer_Distributed_swigregister(AlgorithmContainer_Distributed)

class AlgorithmContainerImpl_Batch(AlgorithmContainer_Batch):
    r"""
    This class is an alias of AlgorithmContainerImpl()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainer_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainerImpl_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainer_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainerImpl_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainerImpl_Batch
    __del__ = lambda self: None

    def setArguments(self, arg2, res, par):
        return _algorithms_.AlgorithmContainerImpl_Batch_setArguments(self, arg2, res, par)

    def getResult(self):
        return _algorithms_.AlgorithmContainerImpl_Batch_getResult(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Batch_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Batch_resetCompute(self)
AlgorithmContainerImpl_Batch_swigregister = _algorithms_.AlgorithmContainerImpl_Batch_swigregister
AlgorithmContainerImpl_Batch_swigregister(AlgorithmContainerImpl_Batch)

class AlgorithmContainerImpl_Online(AlgorithmContainer_Online):
    r"""
    This class is an alias of AlgorithmContainerImpl()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainer_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainerImpl_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainer_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainerImpl_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainerImpl_Online
    __del__ = lambda self: None

    def setArguments(self, arg2, pres, par):
        return _algorithms_.AlgorithmContainerImpl_Online_setArguments(self, arg2, pres, par)

    def setPartialResult(self, pres):
        return _algorithms_.AlgorithmContainerImpl_Online_setPartialResult(self, pres)

    def setResult(self, res):
        return _algorithms_.AlgorithmContainerImpl_Online_setResult(self, res)

    def getResult(self):
        return _algorithms_.AlgorithmContainerImpl_Online_getResult(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Online_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Online_resetCompute(self)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Online_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Online_resetFinalizeCompute(self)
AlgorithmContainerImpl_Online_swigregister = _algorithms_.AlgorithmContainerImpl_Online_swigregister
AlgorithmContainerImpl_Online_swigregister(AlgorithmContainerImpl_Online)

class AlgorithmContainerImpl_Distributed(AlgorithmContainer_Distributed):
    r"""
    This class is an alias of AlgorithmContainerImpl()
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmContainer_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmContainerImpl_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmContainer_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmContainerImpl_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmContainerImpl_Distributed
    __del__ = lambda self: None

    def setArguments(self, arg2, pres, par):
        return _algorithms_.AlgorithmContainerImpl_Distributed_setArguments(self, arg2, pres, par)

    def setPartialResult(self, pres):
        return _algorithms_.AlgorithmContainerImpl_Distributed_setPartialResult(self, pres)

    def setResult(self, res):
        return _algorithms_.AlgorithmContainerImpl_Distributed_setResult(self, res)

    def getResult(self):
        return _algorithms_.AlgorithmContainerImpl_Distributed_getResult(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Distributed_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Distributed_resetCompute(self)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Distributed_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmContainerImpl_Distributed_resetFinalizeCompute(self)
AlgorithmContainerImpl_Distributed_swigregister = _algorithms_.AlgorithmContainerImpl_Distributed_swigregister
AlgorithmContainerImpl_Distributed_swigregister(AlgorithmContainerImpl_Distributed)

class AlgorithmImpl_Batch(Algorithm_Batch):
    r"""
    This class is an alias of AlgorithmImpl()
    """
    __swig_setmethods__ = {}
    for _s in [Algorithm_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmImpl_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [Algorithm_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmImpl_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmImpl_Batch
    __del__ = lambda self: None

    def computeNoThrow(self):
        return _algorithms_.AlgorithmImpl_Batch_computeNoThrow(self)

    def compute(self):
        return _algorithms_.AlgorithmImpl_Batch_compute(self)

    def checkComputeParams(self):
        return _algorithms_.AlgorithmImpl_Batch_checkComputeParams(self)

    def checkResult(self):
        return _algorithms_.AlgorithmImpl_Batch_checkResult(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmImpl_Batch_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmImpl_Batch_resetCompute(self)

    def enableResetOnCompute(self, flag):
        return _algorithms_.AlgorithmImpl_Batch_enableResetOnCompute(self, flag)

    def hostApp(self):
        return _algorithms_.AlgorithmImpl_Batch_hostApp(self)

    def setHostApp(self, pHost):
        return _algorithms_.AlgorithmImpl_Batch_setHostApp(self, pHost)
AlgorithmImpl_Batch_swigregister = _algorithms_.AlgorithmImpl_Batch_swigregister
AlgorithmImpl_Batch_swigregister(AlgorithmImpl_Batch)

class AlgorithmImpl_Online(Algorithm_Online):
    r"""
    This class is an alias of AlgorithmImpl()
    """
    __swig_setmethods__ = {}
    for _s in [Algorithm_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmImpl_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [Algorithm_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmImpl_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmImpl_Online
    __del__ = lambda self: None

    def computeNoThrow(self):
        return _algorithms_.AlgorithmImpl_Online_computeNoThrow(self)

    def compute(self):
        return _algorithms_.AlgorithmImpl_Online_compute(self)

    def finalizeComputeNoThrow(self):
        return _algorithms_.AlgorithmImpl_Online_finalizeComputeNoThrow(self)

    def finalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Online_finalizeCompute(self)

    def checkComputeParams(self):
        return _algorithms_.AlgorithmImpl_Online_checkComputeParams(self)

    def checkResult(self):
        return _algorithms_.AlgorithmImpl_Online_checkResult(self)

    def checkPartialResult(self):
        return _algorithms_.AlgorithmImpl_Online_checkPartialResult(self)

    def checkFinalizeComputeParams(self):
        return _algorithms_.AlgorithmImpl_Online_checkFinalizeComputeParams(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmImpl_Online_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmImpl_Online_resetCompute(self)

    def enableResetOnCompute(self, flag):
        return _algorithms_.AlgorithmImpl_Online_enableResetOnCompute(self, flag)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Online_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Online_resetFinalizeCompute(self)

    def enableResetOnFinalizeCompute(self, flag):
        return _algorithms_.AlgorithmImpl_Online_enableResetOnFinalizeCompute(self, flag)

    def hostApp(self):
        return _algorithms_.AlgorithmImpl_Online_hostApp(self)

    def setHostApp(self, pHost):
        return _algorithms_.AlgorithmImpl_Online_setHostApp(self, pHost)
AlgorithmImpl_Online_swigregister = _algorithms_.AlgorithmImpl_Online_swigregister
AlgorithmImpl_Online_swigregister(AlgorithmImpl_Online)

class AlgorithmImpl_Distributed(Algorithm_Distributed):
    r"""
    This class is an alias of AlgorithmImpl()
    """
    __swig_setmethods__ = {}
    for _s in [Algorithm_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AlgorithmImpl_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [Algorithm_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AlgorithmImpl_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_AlgorithmImpl_Distributed
    __del__ = lambda self: None

    def computeNoThrow(self):
        return _algorithms_.AlgorithmImpl_Distributed_computeNoThrow(self)

    def compute(self):
        return _algorithms_.AlgorithmImpl_Distributed_compute(self)

    def finalizeComputeNoThrow(self):
        return _algorithms_.AlgorithmImpl_Distributed_finalizeComputeNoThrow(self)

    def finalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Distributed_finalizeCompute(self)

    def checkComputeParams(self):
        return _algorithms_.AlgorithmImpl_Distributed_checkComputeParams(self)

    def checkResult(self):
        return _algorithms_.AlgorithmImpl_Distributed_checkResult(self)

    def checkPartialResult(self):
        return _algorithms_.AlgorithmImpl_Distributed_checkPartialResult(self)

    def checkFinalizeComputeParams(self):
        return _algorithms_.AlgorithmImpl_Distributed_checkFinalizeComputeParams(self)

    def setupCompute(self):
        return _algorithms_.AlgorithmImpl_Distributed_setupCompute(self)

    def resetCompute(self):
        return _algorithms_.AlgorithmImpl_Distributed_resetCompute(self)

    def enableResetOnCompute(self, flag):
        return _algorithms_.AlgorithmImpl_Distributed_enableResetOnCompute(self, flag)

    def setupFinalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Distributed_setupFinalizeCompute(self)

    def resetFinalizeCompute(self):
        return _algorithms_.AlgorithmImpl_Distributed_resetFinalizeCompute(self)

    def enableResetOnFinalizeCompute(self, flag):
        return _algorithms_.AlgorithmImpl_Distributed_enableResetOnFinalizeCompute(self, flag)

    def hostApp(self):
        return _algorithms_.AlgorithmImpl_Distributed_hostApp(self)

    def setHostApp(self, pHost):
        return _algorithms_.AlgorithmImpl_Distributed_setHostApp(self, pHost)
AlgorithmImpl_Distributed_swigregister = _algorithms_.AlgorithmImpl_Distributed_swigregister
AlgorithmImpl_Distributed_swigregister(AlgorithmImpl_Distributed)

class ValidationMetricIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ValidationMetricIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ValidationMetricIface, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _algorithms_.new_ValidationMetricIface()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_ValidationMetricIface
    __del__ = lambda self: None
ValidationMetricIface_swigregister = _algorithms_.ValidationMetricIface_swigregister
ValidationMetricIface_swigregister(ValidationMetricIface)

class Model(daal.data_management.SerializationIface):
    __swig_setmethods__ = {}
    for _s in [daal.data_management.SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Model, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.data_management.SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Model, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _algorithms_.new_Model()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _algorithms_.delete_Model
    __del__ = lambda self: None

    def getSerializationTag(self):
        return _algorithms_.Model_getSerializationTag(self)
Model_swigregister = _algorithms_.Model_swigregister
Model_swigregister(Model)

class Prediction(AlgorithmImpl_Batch):
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Prediction, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Prediction, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Prediction
    __del__ = lambda self: None
Prediction_swigregister = _algorithms_.Prediction_swigregister
Prediction_swigregister(Prediction)

class DistributedPrediction(AlgorithmImpl_Distributed):
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DistributedPrediction, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DistributedPrediction, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_DistributedPrediction
    __del__ = lambda self: None
DistributedPrediction_swigregister = _algorithms_.DistributedPrediction_swigregister
DistributedPrediction_swigregister(DistributedPrediction)

class Analysis_Batch(AlgorithmImpl_Batch):
    r"""
    This class is an alias of Analysis(cmode=daal.batch)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Analysis_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Analysis_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Analysis_Batch
    __del__ = lambda self: None
Analysis_Batch_swigregister = _algorithms_.Analysis_Batch_swigregister
Analysis_Batch_swigregister(Analysis_Batch)

class Analysis_Online(AlgorithmImpl_Online):
    r"""
    This class is an alias of Analysis(cmode=daal.online)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Analysis_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Analysis_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Analysis_Online
    __del__ = lambda self: None
Analysis_Online_swigregister = _algorithms_.Analysis_Online_swigregister
Analysis_Online_swigregister(Analysis_Online)

class Analysis_Distributed(AlgorithmImpl_Distributed):
    r"""
    This class is an alias of Analysis(cmode=daal.distributed)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Analysis_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Analysis_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Analysis_Distributed
    __del__ = lambda self: None
Analysis_Distributed_swigregister = _algorithms_.Analysis_Distributed_swigregister
Analysis_Distributed_swigregister(Analysis_Distributed)

class Training_Batch(AlgorithmImpl_Batch):
    r"""
    This class is an alias of Training(cmode=daal.batch)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Training_Batch, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Batch]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Training_Batch, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Training_Batch
    __del__ = lambda self: None
Training_Batch_swigregister = _algorithms_.Training_Batch_swigregister
Training_Batch_swigregister(Training_Batch)

class Training_Online(AlgorithmImpl_Online):
    r"""
    This class is an alias of Training(cmode=daal.online)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Online]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Training_Online, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Online]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Training_Online, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Training_Online
    __del__ = lambda self: None
Training_Online_swigregister = _algorithms_.Training_Online_swigregister
Training_Online_swigregister(Training_Online)

class Training_Distributed(AlgorithmImpl_Distributed):
    r"""
    This class is an alias of Training(cmode=daal.distributed)
    """
    __swig_setmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Training_Distributed, name, value)
    __swig_getmethods__ = {}
    for _s in [AlgorithmImpl_Distributed]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Training_Distributed, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _algorithms_.delete_Training_Distributed
    __del__ = lambda self: None
Training_Distributed_swigregister = _algorithms_.Training_Distributed_swigregister
Training_Distributed_swigregister(Training_Distributed)

from numpy import float64, float32, intc

class Training(object):
    r"""Factory class for different types of Training."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return Training_Batch(*args)
        if cmode == daal.online:
            return Training_Online(*args)
        if cmode == daal.distributed:
            return Training_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for Training")

class Algorithm(object):
    r"""Factory class for different types of Algorithm."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return Algorithm_Batch(*args)
        if cmode == daal.online:
            return Algorithm_Online(*args)
        if cmode == daal.distributed:
            return Algorithm_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for Algorithm")

class AlgorithmContainerImpl(object):
    r"""Factory class for different types of AlgorithmContainerImpl."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return AlgorithmContainerImpl_Batch(*args)
        if cmode == daal.online:
            return AlgorithmContainerImpl_Online(*args)
        if cmode == daal.distributed:
            return AlgorithmContainerImpl_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for AlgorithmContainerImpl")

class Analysis(object):
    r"""Factory class for different types of Analysis."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return Analysis_Batch(*args)
        if cmode == daal.online:
            return Analysis_Online(*args)
        if cmode == daal.distributed:
            return Analysis_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for Analysis")

class AlgorithmContainer(object):
    r"""Factory class for different types of AlgorithmContainer."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return AlgorithmContainer_Batch(*args)
        if cmode == daal.online:
            return AlgorithmContainer_Online(*args)
        if cmode == daal.distributed:
            return AlgorithmContainer_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for AlgorithmContainer")

class AlgorithmImpl(object):
    r"""Factory class for different types of AlgorithmImpl."""
    def __new__(cls,
                cmode,
                *args, **kwargs):
        if cmode == daal.batch:
            return AlgorithmImpl_Batch(*args)
        if cmode == daal.online:
            return AlgorithmImpl_Online(*args)
        if cmode == daal.distributed:
            return AlgorithmImpl_Distributed(*args)

        raise RuntimeError("No appropriate constructor found for AlgorithmImpl")


# This file is compatible with both classic and new-style classes.


