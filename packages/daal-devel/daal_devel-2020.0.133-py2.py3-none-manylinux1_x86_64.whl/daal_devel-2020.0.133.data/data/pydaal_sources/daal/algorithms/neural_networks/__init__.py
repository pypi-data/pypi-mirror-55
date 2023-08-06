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
            fp, pathname, description = imp.find_module('_neural_networks_', [dirname(__file__)])
        except ImportError:
            import _neural_networks_
            return _neural_networks_
        if fp is not None:
            try:
                _mod = imp.load_module('_neural_networks_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _neural_networks_ = swig_import_helper()
    del swig_import_helper
else:
    import _neural_networks_
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
import daal.algorithms.neural_networks.layers.backward
import daal.algorithms.neural_networks.layers
import daal.algorithms.neural_networks.initializers
import daal.algorithms.engines.mt19937
import daal.algorithms.engines
import daal.algorithms.neural_networks.layers.forward
class LearnableParametersIface(daal.data_management.SerializationIface):
    __swig_setmethods__ = {}
    for _s in [daal.data_management.SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LearnableParametersIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.data_management.SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LearnableParametersIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _neural_networks_.delete_LearnableParametersIface
    __del__ = lambda self: None

    def copyToTable(self, *args):
        return _neural_networks_.LearnableParametersIface_copyToTable(self, *args)

    def copyFromTable(self, *args):
        return _neural_networks_.LearnableParametersIface_copyFromTable(self, *args)
LearnableParametersIface_swigregister = _neural_networks_.LearnableParametersIface_swigregister
LearnableParametersIface_swigregister(LearnableParametersIface)

class ModelImpl(daal.algorithms.Model):
    __swig_setmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModelImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.algorithms.Model]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ModelImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_destroy__ = _neural_networks_.delete_ModelImpl
    __del__ = lambda self: None

    def getNextLayers(self):
        return _neural_networks_.ModelImpl_getNextLayers(self)

    def setWeightsAndBiases(self, weightsAndBiases):
        return _neural_networks_.ModelImpl_setWeightsAndBiases(self, weightsAndBiases)

    def getWeightsAndBiases(self):
        return _neural_networks_.ModelImpl_getWeightsAndBiases(self)
ModelImpl_swigregister = _neural_networks_.ModelImpl_swigregister
ModelImpl_swigregister(ModelImpl)

class ForwardLayers(_object):
    r"""
 <a name='DAAL-CLASS-ALGORITHMS__NEURAL_NETWORKS__FORWARDLAYERS'></a>
 \brief Represents a collection of forward stages of neural network layers"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ForwardLayers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ForwardLayers, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _neural_networks_.new_ForwardLayers(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _neural_networks_.delete_ForwardLayers
    __del__ = lambda self: None

    def size(self):
        return _neural_networks_.ForwardLayers_size(self)

    def capacity(self):
        return _neural_networks_.ForwardLayers_capacity(self)

    def get(self, *args):
        return _neural_networks_.ForwardLayers_get(self, *args)

    def data(self, *args):
        return _neural_networks_.ForwardLayers_data(self, *args)

    def push_back(self, x):
        return _neural_networks_.ForwardLayers_push_back(self, x)

    def safe_push_back(self, x):
        return _neural_networks_.ForwardLayers_safe_push_back(self, x)

    def __lshift__(self, x):
        return _neural_networks_.ForwardLayers___lshift__(self, x)

    def resize(self, newCapacity):
        return _neural_networks_.ForwardLayers_resize(self, newCapacity)

    def clear(self):
        return _neural_networks_.ForwardLayers_clear(self)

    def insert(self, *args):
        return _neural_networks_.ForwardLayers_insert(self, *args)

    def erase(self, pos):
        return _neural_networks_.ForwardLayers_erase(self, pos)

    def __getitem__(self, i):
        return _neural_networks_.ForwardLayers___getitem__(self, i)

    def __setitem__(self, i, v):
        return _neural_networks_.ForwardLayers___setitem__(self, i, v)
ForwardLayers_swigregister = _neural_networks_.ForwardLayers_swigregister
ForwardLayers_swigregister(ForwardLayers)

class BackwardLayers(_object):
    r"""
 <a name='DAAL-CLASS-ALGORITHMS__NEURAL_NETWORKS__BACKWARDLAYERS'></a>
 \brief Represents a collection of backward stages of neural network layers"""
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BackwardLayers, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BackwardLayers, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _neural_networks_.new_BackwardLayers(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _neural_networks_.delete_BackwardLayers
    __del__ = lambda self: None

    def size(self):
        return _neural_networks_.BackwardLayers_size(self)

    def capacity(self):
        return _neural_networks_.BackwardLayers_capacity(self)

    def get(self, *args):
        return _neural_networks_.BackwardLayers_get(self, *args)

    def data(self, *args):
        return _neural_networks_.BackwardLayers_data(self, *args)

    def push_back(self, x):
        return _neural_networks_.BackwardLayers_push_back(self, x)

    def safe_push_back(self, x):
        return _neural_networks_.BackwardLayers_safe_push_back(self, x)

    def __lshift__(self, x):
        return _neural_networks_.BackwardLayers___lshift__(self, x)

    def resize(self, newCapacity):
        return _neural_networks_.BackwardLayers_resize(self, newCapacity)

    def clear(self):
        return _neural_networks_.BackwardLayers_clear(self)

    def insert(self, *args):
        return _neural_networks_.BackwardLayers_insert(self, *args)

    def erase(self, pos):
        return _neural_networks_.BackwardLayers_erase(self, pos)

    def __getitem__(self, i):
        return _neural_networks_.BackwardLayers___getitem__(self, i)

    def __setitem__(self, i, v):
        return _neural_networks_.BackwardLayers___setitem__(self, i, v)
BackwardLayers_swigregister = _neural_networks_.BackwardLayers_swigregister
BackwardLayers_swigregister(BackwardLayers)

from numpy import float64, float32, intc


# This file is compatible with both classic and new-style classes.


