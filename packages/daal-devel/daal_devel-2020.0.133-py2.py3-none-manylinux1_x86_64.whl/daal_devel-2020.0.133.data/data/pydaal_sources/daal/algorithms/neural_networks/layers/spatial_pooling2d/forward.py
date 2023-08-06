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
            fp, pathname, description = imp.find_module('_forward32_', [dirname(__file__)])
        except ImportError:
            import _forward32_
            return _forward32_
        if fp is not None:
            try:
                _mod = imp.load_module('_forward32_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _forward32_ = swig_import_helper()
    del swig_import_helper
else:
    import _forward32_
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
import daal.algorithms.neural_networks.layers.spatial_pooling2d
class Input(daal.algorithms.neural_networks.layers.forward.Input):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.forward.Input]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Input, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.forward.Input]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _forward32_.new_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _forward32_.delete_Input
    __del__ = lambda self: None

    def getWeightsSizes(self, parameter):
        return _forward32_.Input_getWeightsSizes(self, parameter)

    def getBiasesSizes(self, parameter):
        return _forward32_.Input_getBiasesSizes(self, parameter)

    def check(self, parameter, method):
        return _forward32_.Input_check(self, parameter, method)
Input_swigregister = _forward32_.Input_swigregister
Input_swigregister(Input)

class Result(daal.algorithms.neural_networks.layers.forward.Result):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.forward.Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.neural_networks.layers.forward.Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _forward32_.new_Result()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _forward32_.delete_Result
    __del__ = lambda self: None

    def getValueSize(self, inputSize, par, method):
        return _forward32_.Result_getValueSize(self, inputSize, par, method)

    def check(self, input, parameter, method):
        return _forward32_.Result_check(self, input, parameter, method)
    __swig_getmethods__["computeValueDimensions"] = lambda x: _forward32_.Result_computeValueDimensions
    if _newclass:
        computeValueDimensions = staticmethod(_forward32_.Result_computeValueDimensions)

    def createAuxInputDimensions(self, dataDims):
        return _forward32_.Result_createAuxInputDimensions(self, dataDims)

    def allocate_Float64(self, input, parameter, method):
        r"""
    This function is specialized for float64"""
        return _forward32_.Result_allocate_Float64(self, input, parameter, method)


    def allocate_Float32(self, input, parameter, method):
        r"""
    This function is specialized for float32"""
        return _forward32_.Result_allocate_Float32(self, input, parameter, method)

Result_swigregister = _forward32_.Result_swigregister
Result_swigregister(Result)

def Result_computeValueDimensions(inputDims, param):
    return _forward32_.Result_computeValueDimensions(inputDims, param)
Result_computeValueDimensions = _forward32_.Result_computeValueDimensions

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


