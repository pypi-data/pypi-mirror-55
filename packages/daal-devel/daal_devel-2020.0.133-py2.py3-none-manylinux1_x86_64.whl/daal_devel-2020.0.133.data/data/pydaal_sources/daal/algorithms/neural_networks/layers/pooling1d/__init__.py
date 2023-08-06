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
            fp, pathname, description = imp.find_module('_pooling1d_', [dirname(__file__)])
        except ImportError:
            import _pooling1d_
            return _pooling1d_
        if fp is not None:
            try:
                _mod = imp.load_module('_pooling1d_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _pooling1d_ = swig_import_helper()
    del swig_import_helper
else:
    import _pooling1d_
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
class KernelSize(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KernelSize, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KernelSize, name)
    __repr__ = _swig_repr

    def __init__(self, first=2):
        this = _pooling1d_.new_KernelSize(first)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling1d_.KernelSize_size_set
    __swig_getmethods__["size"] = _pooling1d_.KernelSize_size_get
    if _newclass:
        size = _swig_property(_pooling1d_.KernelSize_size_get, _pooling1d_.KernelSize_size_set)
    __swig_destroy__ = _pooling1d_.delete_KernelSize
    __del__ = lambda self: None
KernelSize_swigregister = _pooling1d_.KernelSize_swigregister
KernelSize_swigregister(KernelSize)

class Stride(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Stride, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Stride, name)
    __repr__ = _swig_repr

    def __init__(self, first=2):
        this = _pooling1d_.new_Stride(first)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling1d_.Stride_size_set
    __swig_getmethods__["size"] = _pooling1d_.Stride_size_get
    if _newclass:
        size = _swig_property(_pooling1d_.Stride_size_get, _pooling1d_.Stride_size_set)
    __swig_destroy__ = _pooling1d_.delete_Stride
    __del__ = lambda self: None
Stride_swigregister = _pooling1d_.Stride_swigregister
Stride_swigregister(Stride)

class Padding(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Padding, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Padding, name)
    __repr__ = _swig_repr

    def __init__(self, first=0):
        this = _pooling1d_.new_Padding(first)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling1d_.Padding_size_set
    __swig_getmethods__["size"] = _pooling1d_.Padding_size_get
    if _newclass:
        size = _swig_property(_pooling1d_.Padding_size_get, _pooling1d_.Padding_size_set)
    __swig_destroy__ = _pooling1d_.delete_Padding
    __del__ = lambda self: None
Padding_swigregister = _pooling1d_.Padding_swigregister
Padding_swigregister(Padding)

class Index(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Index, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Index, name)
    __repr__ = _swig_repr

    def __init__(self, first=2):
        this = _pooling1d_.new_Index(first)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["size"] = _pooling1d_.Index_size_set
    __swig_getmethods__["size"] = _pooling1d_.Index_size_get
    if _newclass:
        size = _swig_property(_pooling1d_.Index_size_get, _pooling1d_.Index_size_set)
    __swig_destroy__ = _pooling1d_.delete_Index
    __del__ = lambda self: None
Index_swigregister = _pooling1d_.Index_swigregister
Index_swigregister(Index)

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

    def __init__(self, index, kernelSize=2, stride=2, padding=0):
        this = _pooling1d_.new_Parameter(index, kernelSize, stride, padding)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["stride"] = _pooling1d_.Parameter_stride_set
    __swig_getmethods__["stride"] = _pooling1d_.Parameter_stride_get
    if _newclass:
        stride = _swig_property(_pooling1d_.Parameter_stride_get, _pooling1d_.Parameter_stride_set)
    __swig_setmethods__["padding"] = _pooling1d_.Parameter_padding_set
    __swig_getmethods__["padding"] = _pooling1d_.Parameter_padding_get
    if _newclass:
        padding = _swig_property(_pooling1d_.Parameter_padding_get, _pooling1d_.Parameter_padding_set)
    __swig_setmethods__["kernelSize"] = _pooling1d_.Parameter_kernelSize_set
    __swig_getmethods__["kernelSize"] = _pooling1d_.Parameter_kernelSize_get
    if _newclass:
        kernelSize = _swig_property(_pooling1d_.Parameter_kernelSize_get, _pooling1d_.Parameter_kernelSize_set)
    __swig_setmethods__["index"] = _pooling1d_.Parameter_index_set
    __swig_getmethods__["index"] = _pooling1d_.Parameter_index_get
    if _newclass:
        index = _swig_property(_pooling1d_.Parameter_index_get, _pooling1d_.Parameter_index_set)
    __swig_destroy__ = _pooling1d_.delete_Parameter
    __del__ = lambda self: None
Parameter_swigregister = _pooling1d_.Parameter_swigregister
Parameter_swigregister(Parameter)

from numpy import float64, float32, intc


from . import backward
from . import forward

# This file is compatible with both classic and new-style classes.


