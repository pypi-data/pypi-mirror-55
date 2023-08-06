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
            fp, pathname, description = imp.find_module('_pooling3d_', [dirname(__file__)])
        except ImportError:
            import _pooling3d_
            return _pooling3d_
        if fp is not None:
            try:
                _mod = imp.load_module('_pooling3d_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pooling3d_ = swig_import_helper()
    del swig_import_helper
else:
    import _pooling3d_
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


import daal.algorithms.neural_networks.initializers
import daal.algorithms.neural_networks
import daal.algorithms
import daal.data_management
import daal
import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.layers.forward
import daal.algorithms.engines.mt19937
import daal.algorithms.engines
class KernelSizes(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KernelSizes, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KernelSizes, name)
    __repr__ = _swig_repr

    def __init__(self, first=2, second=2, third=2):
        this = _pooling3d_.new_KernelSizes(first, second, third)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling3d_.KernelSizes_size_set
    __swig_getmethods__["size"] = _pooling3d_.KernelSizes_size_get
    if _newclass:
        size = _swig_property(_pooling3d_.KernelSizes_size_get, _pooling3d_.KernelSizes_size_set)
    __swig_destroy__ = _pooling3d_.delete_KernelSizes
    __del__ = lambda self: None
KernelSizes_swigregister = _pooling3d_.KernelSizes_swigregister
KernelSizes_swigregister(KernelSizes)

class Strides(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Strides, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Strides, name)
    __repr__ = _swig_repr

    def __init__(self, first=2, second=2, third=2):
        this = _pooling3d_.new_Strides(first, second, third)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling3d_.Strides_size_set
    __swig_getmethods__["size"] = _pooling3d_.Strides_size_get
    if _newclass:
        size = _swig_property(_pooling3d_.Strides_size_get, _pooling3d_.Strides_size_set)
    __swig_destroy__ = _pooling3d_.delete_Strides
    __del__ = lambda self: None
Strides_swigregister = _pooling3d_.Strides_swigregister
Strides_swigregister(Strides)

class Paddings(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Paddings, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Paddings, name)
    __repr__ = _swig_repr

    def __init__(self, first=2, second=2, third=2):
        this = _pooling3d_.new_Paddings(first, second, third)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling3d_.Paddings_size_set
    __swig_getmethods__["size"] = _pooling3d_.Paddings_size_get
    if _newclass:
        size = _swig_property(_pooling3d_.Paddings_size_get, _pooling3d_.Paddings_size_set)
    __swig_destroy__ = _pooling3d_.delete_Paddings
    __del__ = lambda self: None
Paddings_swigregister = _pooling3d_.Paddings_swigregister
Paddings_swigregister(Paddings)

class Indices(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Indices, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Indices, name)
    __repr__ = _swig_repr

    def __init__(self, first=0, second=1, third=2):
        this = _pooling3d_.new_Indices(first, second, third)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling3d_.Indices_size_set
    __swig_getmethods__["size"] = _pooling3d_.Indices_size_get
    if _newclass:
        size = _swig_property(_pooling3d_.Indices_size_get, _pooling3d_.Indices_size_set)
    __swig_destroy__ = _pooling3d_.delete_Indices
    __del__ = lambda self: None
Indices_swigregister = _pooling3d_.Indices_swigregister
Indices_swigregister(Indices)

class Parameter(daal.algorithms.neural_networks.layers.Parameter):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.Parameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Parameter, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.Parameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Parameter, name)
    __repr__ = _swig_repr

    def __init__(self, firstIndex, secondIndex, thirdIndex, firstKernelSize=2, secondKernelSize=2, thirdKernelSize=2, firstStride=2, secondStride=2, thirdStride=2, firstPadding=0, secondPadding=0, thirdPadding=0):
        this = _pooling3d_.new_Parameter(firstIndex, secondIndex, thirdIndex, firstKernelSize, secondKernelSize, thirdKernelSize, firstStride, secondStride, thirdStride, firstPadding, secondPadding, thirdPadding)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["strides"] = _pooling3d_.Parameter_strides_set
    __swig_getmethods__["strides"] = _pooling3d_.Parameter_strides_get
    if _newclass:
        strides = _swig_property(_pooling3d_.Parameter_strides_get, _pooling3d_.Parameter_strides_set)
    __swig_setmethods__["paddings"] = _pooling3d_.Parameter_paddings_set
    __swig_getmethods__["paddings"] = _pooling3d_.Parameter_paddings_get
    if _newclass:
        paddings = _swig_property(_pooling3d_.Parameter_paddings_get, _pooling3d_.Parameter_paddings_set)
    __swig_setmethods__["kernelSizes"] = _pooling3d_.Parameter_kernelSizes_set
    __swig_getmethods__["kernelSizes"] = _pooling3d_.Parameter_kernelSizes_get
    if _newclass:
        kernelSizes = _swig_property(_pooling3d_.Parameter_kernelSizes_get, _pooling3d_.Parameter_kernelSizes_set)
    __swig_setmethods__["indices"] = _pooling3d_.Parameter_indices_set
    __swig_getmethods__["indices"] = _pooling3d_.Parameter_indices_get
    if _newclass:
        indices = _swig_property(_pooling3d_.Parameter_indices_get, _pooling3d_.Parameter_indices_set)
    __swig_destroy__ = _pooling3d_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _pooling3d_.Parameter_swigregister
Parameter_swigregister(Parameter)

from numpy import float64, float32, intc


from . import backward
from . import forward

# This file is compatible with both classic and new-style classes.


