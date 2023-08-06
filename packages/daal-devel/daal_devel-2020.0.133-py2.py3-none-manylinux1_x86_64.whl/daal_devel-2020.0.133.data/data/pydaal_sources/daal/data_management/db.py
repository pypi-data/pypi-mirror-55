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
            fp, pathname, description = imp.find_module('_db_', [dirname(__file__)])
        except ImportError:
            import _db_
            return _db_
        if fp is not None:
            try:
                _mod = imp.load_module('_db_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _db_ = swig_import_helper()
    del swig_import_helper
else:
    import _db_
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
class SQLFeatureManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SQLFeatureManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SQLFeatureManager, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _db_.new_SQLFeatureManager()
        try:
            self.this.append(this)
        except:
            self.this = this

    def addModifier(self, featureIds, modifier, status=None):
        return _db_.SQLFeatureManager_addModifier(self, featureIds, modifier, status)

    def statementResultsNumericTable(self, hdlStmt, nt, maxRows):
        return _db_.SQLFeatureManager_statementResultsNumericTable(self, hdlStmt, nt, maxRows)

    def createDictionary(self, hdlStmt, dictionary):
        return _db_.SQLFeatureManager_createDictionary(self, hdlStmt, dictionary)

    def setLimitQuery(self, query, idx_last_read, maxRows):
        return _db_.SQLFeatureManager_setLimitQuery(self, query, idx_last_read, maxRows)
    __swig_destroy__ = _db_.delete_SQLFeatureManager
    __del__ = lambda self: None
SQLFeatureManager_swigregister = _db_.SQLFeatureManager_swigregister
SQLFeatureManager_swigregister(SQLFeatureManager)

class ODBCDataSourceOptions(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ODBCDataSourceOptions, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ODBCDataSourceOptions, name)
    __repr__ = _swig_repr
    byDefault = _db_.ODBCDataSourceOptions_byDefault
    allocateNumericTable = _db_.ODBCDataSourceOptions_allocateNumericTable
    createDictionaryFromContext = _db_.ODBCDataSourceOptions_createDictionaryFromContext
    __swig_getmethods__["unite"] = lambda x: _db_.ODBCDataSourceOptions_unite
    if _newclass:
        unite = staticmethod(_db_.ODBCDataSourceOptions_unite)

    def __init__(self, *args):
        this = _db_.new_ODBCDataSourceOptions(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getNumericTableAllocationFlag(self):
        return _db_.ODBCDataSourceOptions_getNumericTableAllocationFlag(self)

    def getDictionaryCreationFlag(self):
        return _db_.ODBCDataSourceOptions_getDictionaryCreationFlag(self)
    __swig_destroy__ = _db_.delete_ODBCDataSourceOptions
    __del__ = lambda self: None
ODBCDataSourceOptions_swigregister = _db_.ODBCDataSourceOptions_swigregister
ODBCDataSourceOptions_swigregister(ODBCDataSourceOptions)

def ODBCDataSourceOptions_unite(lhs, rhs):
    return _db_.ODBCDataSourceOptions_unite(lhs, rhs)
ODBCDataSourceOptions_unite = _db_.ODBCDataSourceOptions_unite


def __or__(*args):
    return _db_.__or__(*args)
__or__ = _db_.__or__
class ODBCDataSource_MySQLFeatureManagerFloat64(daal.data_management.DataSourceTemplate_HomogenNumericTable_Float64Float64):
    r"""
    This class is an alias of ODBCDataSource()
    """
    __swig_setmethods__ = {}
    for _s in [daal.data_management.DataSourceTemplate_HomogenNumericTable_Float64Float64]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ODBCDataSource_MySQLFeatureManagerFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.data_management.DataSourceTemplate_HomogenNumericTable_Float64Float64]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ODBCDataSource_MySQLFeatureManagerFloat64, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _db_.new_ODBCDataSource_MySQLFeatureManagerFloat64(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _db_.delete_ODBCDataSource_MySQLFeatureManagerFloat64
    __del__ = lambda self: None

    def executeQuery(self, query):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_executeQuery(self, query)

    def freeHandles(self):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_freeHandles(self)

    def loadDataBlock(self, *args):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_loadDataBlock(self, *args)

    def createDictionaryFromContext(self):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_createDictionaryFromContext(self)

    def getStatus(self):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_getStatus(self)

    def getNumberOfAvailableRows(self):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_getNumberOfAvailableRows(self)

    def getFeatureManager(self):
        return _db_.ODBCDataSource_MySQLFeatureManagerFloat64_getFeatureManager(self)
ODBCDataSource_MySQLFeatureManagerFloat64_swigregister = _db_.ODBCDataSource_MySQLFeatureManagerFloat64_swigregister
ODBCDataSource_MySQLFeatureManagerFloat64_swigregister(ODBCDataSource_MySQLFeatureManagerFloat64)

from numpy import float64, float32, intc

class ODBCDataSource(object):
    r"""Factory class for different types of ODBCDataSource."""
    def __new__(cls,
                *args, **kwargs):
        if 'FeatureManager' not in kwargs or kwargs['FeatureManager'] == daal.data_management.MySQLFeatureManager:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return ODBCDataSource_MySQLFeatureManagerFloat64(*args)

        raise RuntimeError("No appropriate constructor found for ODBCDataSource")


# This file is compatible with both classic and new-style classes.


