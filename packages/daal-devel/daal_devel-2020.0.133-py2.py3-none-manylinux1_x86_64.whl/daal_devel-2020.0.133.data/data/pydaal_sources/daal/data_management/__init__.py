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
            fp, pathname, description = imp.find_module('_data_management_', [dirname(__file__)])
        except ImportError:
            import _data_management_
            return _data_management_
        if fp is not None:
            try:
                _mod = imp.load_module('_data_management_', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _data_management_ = swig_import_helper()
    del swig_import_helper
else:
    import _data_management_
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


import numpy

import daal
class SerializationIface(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, SerializationIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, SerializationIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_SerializationIface
    __del__ = lambda self: None

    def serialize(self, archive):
        return _data_management_.SerializationIface_serialize(self, archive)

    def deserialize(self, archive):
        return _data_management_.SerializationIface_deserialize(self, archive)

    def getSerializationTag(self):
        return _data_management_.SerializationIface_getSerializationTag(self)
SerializationIface_swigregister = _data_management_.SerializationIface_swigregister
SerializationIface_swigregister(SerializationIface)

class SerializationDesc(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SerializationDesc, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SerializationDesc, name)
    __repr__ = _swig_repr

    def __init__(self, func, tag):
        this = _data_management_.new_SerializationDesc(func, tag)
        try:
            self.this.append(this)
        except:
            self.this = this

    def tag(self):
        return _data_management_.SerializationDesc_tag(self)

    def creator(self):
        return _data_management_.SerializationDesc_creator(self)

    def next(self):
        return _data_management_.SerializationDesc_next(self)
    __swig_getmethods__["first"] = lambda x: _data_management_.SerializationDesc_first
    if _newclass:
        first = staticmethod(_data_management_.SerializationDesc_first)
    __swig_destroy__ = _data_management_.delete_SerializationDesc
    __del__ = lambda self: None
SerializationDesc_swigregister = _data_management_.SerializationDesc_swigregister
SerializationDesc_swigregister(SerializationDesc)

def SerializationDesc_first():
    return _data_management_.SerializationDesc_first()
SerializationDesc_first = _data_management_.SerializationDesc_first

class DataBlock(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataBlock, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DataBlock, name)
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataBlock
    __del__ = lambda self: None

    def getSize(self):
        return _data_management_.DataBlock_getSize(self)

    def __init__(self, *args):
        this = _data_management_.new_DataBlock(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getArray(self):
        return _data_management_.DataBlock_getArray(self)

    def setArray(self, outBlock):
        return _data_management_.DataBlock_setArray(self, outBlock)
DataBlock_swigregister = _data_management_.DataBlock_swigregister
DataBlock_swigregister(DataBlock)

import daal.services
import daal.data_management.features
import daal.data_management.modifiers.csv
import daal.data_management.modifiers

_data_management_.defaultLevel_swigconstant(_data_management_)
defaultLevel = _data_management_.defaultLevel

_data_management_.level0_swigconstant(_data_management_)
level0 = _data_management_.level0

_data_management_.level1_swigconstant(_data_management_)
level1 = _data_management_.level1

_data_management_.level2_swigconstant(_data_management_)
level2 = _data_management_.level2

_data_management_.level3_swigconstant(_data_management_)
level3 = _data_management_.level3

_data_management_.level4_swigconstant(_data_management_)
level4 = _data_management_.level4

_data_management_.level5_swigconstant(_data_management_)
level5 = _data_management_.level5

_data_management_.level6_swigconstant(_data_management_)
level6 = _data_management_.level6

_data_management_.level7_swigconstant(_data_management_)
level7 = _data_management_.level7

_data_management_.level8_swigconstant(_data_management_)
level8 = _data_management_.level8

_data_management_.level9_swigconstant(_data_management_)
level9 = _data_management_.level9

_data_management_.lastCompressionLevel_swigconstant(_data_management_)
lastCompressionLevel = _data_management_.lastCompressionLevel

_data_management_.zlib_swigconstant(_data_management_)
zlib = _data_management_.zlib

_data_management_.lzo_swigconstant(_data_management_)
lzo = _data_management_.lzo

_data_management_.rle_swigconstant(_data_management_)
rle = _data_management_.rle

_data_management_.bzip2_swigconstant(_data_management_)
bzip2 = _data_management_.bzip2
class CompressionParameter(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressionParameter, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CompressionParameter, name)
    __repr__ = _swig_repr
    __swig_setmethods__["level"] = _data_management_.CompressionParameter_level_set
    __swig_getmethods__["level"] = _data_management_.CompressionParameter_level_get
    if _newclass:
        level = _swig_property(_data_management_.CompressionParameter_level_get, _data_management_.CompressionParameter_level_set)

    def __init__(self, *args):
        this = _data_management_.new_CompressionParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CompressionParameter
    __del__ = lambda self: None
CompressionParameter_swigregister = _data_management_.CompressionParameter_swigregister
CompressionParameter_swigregister(CompressionParameter)

class CompressionIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressionIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CompressionIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.CompressionIface_setInputDataBlock(self, inBlock, offset)

    def isOutputDataBlockFull(self):
        return _data_management_.CompressionIface_isOutputDataBlockFull(self)

    def getUsedOutputDataBlockSize(self):
        return _data_management_.CompressionIface_getUsedOutputDataBlockSize(self)

    def run(self, outBlock, offset):
        return _data_management_.CompressionIface_run(self, outBlock, offset)
    __swig_destroy__ = _data_management_.delete_CompressionIface
    __del__ = lambda self: None
CompressionIface_swigregister = _data_management_.CompressionIface_swigregister
CompressionIface_swigregister(CompressionIface)

class Compression(CompressionIface):
    __swig_setmethods__ = {}
    for _s in [CompressionIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Compression, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressionIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Compression, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Compression_setInputDataBlock(self, inBlock, offset)

    def isOutputDataBlockFull(self):
        return _data_management_.Compression_isOutputDataBlockFull(self)

    def getUsedOutputDataBlockSize(self):
        return _data_management_.Compression_getUsedOutputDataBlockSize(self)

    def run(self, outBlock, offset):
        return _data_management_.Compression_run(self, outBlock, offset)
    __swig_destroy__ = _data_management_.delete_Compression
    __del__ = lambda self: None

    def checkInputParams(self, inBlock):
        return _data_management_.Compression_checkInputParams(self, inBlock)

    def checkOutputParams(self, outBlock):
        return _data_management_.Compression_checkOutputParams(self, outBlock)
Compression_swigregister = _data_management_.Compression_swigregister
Compression_swigregister(Compression)

class CompressorImpl(Compression):
    __swig_setmethods__ = {}
    for _s in [Compression]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressorImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [Compression]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CompressorImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_CompressorImpl
    __del__ = lambda self: None
CompressorImpl_swigregister = _data_management_.CompressorImpl_swigregister
CompressorImpl_swigregister(CompressorImpl)

class DecompressorImpl(Compression):
    __swig_setmethods__ = {}
    for _s in [Compression]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DecompressorImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [Compression]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DecompressorImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DecompressorImpl
    __del__ = lambda self: None
DecompressorImpl_swigregister = _data_management_.DecompressorImpl_swigregister
DecompressorImpl_swigregister(DecompressorImpl)

class CompressionStream(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressionStream, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CompressionStream, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_CompressionStream(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CompressionStream
    __del__ = lambda self: None

    def __lshift__(self, inBlock):
        return _data_management_.CompressionStream___lshift__(self, inBlock)

    def getCompressedBlocksCollection(self):
        return _data_management_.CompressionStream_getCompressedBlocksCollection(self)

    def getCompressedDataSize(self):
        return _data_management_.CompressionStream_getCompressedDataSize(self)

    def copyCompressedArray(self, *args):
        return _data_management_.CompressionStream_copyCompressedArray(self, *args)

    def push_back(self, inBlock):
        return _data_management_.CompressionStream_push_back(self, inBlock)
CompressionStream_swigregister = _data_management_.CompressionStream_swigregister
CompressionStream_swigregister(CompressionStream)

class DecompressionStream(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DecompressionStream, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DecompressionStream, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_DecompressionStream(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DecompressionStream
    __del__ = lambda self: None

    def __lshift__(self, inBlock):
        return _data_management_.DecompressionStream___lshift__(self, inBlock)

    def getDecompressedBlocksCollection(self):
        return _data_management_.DecompressionStream_getDecompressedBlocksCollection(self)

    def getDecompressedDataSize(self):
        return _data_management_.DecompressionStream_getDecompressedDataSize(self)

    def copyDecompressedArray(self, *args):
        return _data_management_.DecompressionStream_copyDecompressedArray(self, *args)

    def push_back(self, inBlock):
        return _data_management_.DecompressionStream_push_back(self, inBlock)
DecompressionStream_swigregister = _data_management_.DecompressionStream_swigregister
DecompressionStream_swigregister(DecompressionStream)

class Bzip2CompressionParameter(CompressionParameter):
    __swig_setmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Bzip2CompressionParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Bzip2CompressionParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_Bzip2CompressionParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Bzip2CompressionParameter
    __del__ = lambda self: None
Bzip2CompressionParameter_swigregister = _data_management_.Bzip2CompressionParameter_swigregister
Bzip2CompressionParameter_swigregister(Bzip2CompressionParameter)

class LzoCompressionParameter(CompressionParameter):
    __swig_setmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, LzoCompressionParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, LzoCompressionParameter, name)
    __repr__ = _swig_repr

    def __init__(self, _preHeadBytes=0, _postHeadBytes=0):
        this = _data_management_.new_LzoCompressionParameter(_preHeadBytes, _postHeadBytes)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_LzoCompressionParameter
    __del__ = lambda self: None
    __swig_setmethods__["preHeadBytes"] = _data_management_.LzoCompressionParameter_preHeadBytes_set
    __swig_getmethods__["preHeadBytes"] = _data_management_.LzoCompressionParameter_preHeadBytes_get
    if _newclass:
        preHeadBytes = _swig_property(_data_management_.LzoCompressionParameter_preHeadBytes_get, _data_management_.LzoCompressionParameter_preHeadBytes_set)
    __swig_setmethods__["postHeadBytes"] = _data_management_.LzoCompressionParameter_postHeadBytes_set
    __swig_getmethods__["postHeadBytes"] = _data_management_.LzoCompressionParameter_postHeadBytes_get
    if _newclass:
        postHeadBytes = _swig_property(_data_management_.LzoCompressionParameter_postHeadBytes_get, _data_management_.LzoCompressionParameter_postHeadBytes_set)
LzoCompressionParameter_swigregister = _data_management_.LzoCompressionParameter_swigregister
LzoCompressionParameter_swigregister(LzoCompressionParameter)

class RleCompressionParameter(CompressionParameter):
    __swig_setmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, RleCompressionParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, RleCompressionParameter, name)
    __repr__ = _swig_repr

    def __init__(self, _isBlockHeader=1):
        this = _data_management_.new_RleCompressionParameter(_isBlockHeader)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_RleCompressionParameter
    __del__ = lambda self: None
    __swig_setmethods__["isBlockHeader"] = _data_management_.RleCompressionParameter_isBlockHeader_set
    __swig_getmethods__["isBlockHeader"] = _data_management_.RleCompressionParameter_isBlockHeader_get
    if _newclass:
        isBlockHeader = _swig_property(_data_management_.RleCompressionParameter_isBlockHeader_get, _data_management_.RleCompressionParameter_isBlockHeader_set)
RleCompressionParameter_swigregister = _data_management_.RleCompressionParameter_swigregister
RleCompressionParameter_swigregister(RleCompressionParameter)

class ZlibCompressionParameter(CompressionParameter):
    __swig_setmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ZlibCompressionParameter, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressionParameter]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ZlibCompressionParameter, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_ZlibCompressionParameter(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_ZlibCompressionParameter
    __del__ = lambda self: None
    __swig_setmethods__["gzHeader"] = _data_management_.ZlibCompressionParameter_gzHeader_set
    __swig_getmethods__["gzHeader"] = _data_management_.ZlibCompressionParameter_gzHeader_get
    if _newclass:
        gzHeader = _swig_property(_data_management_.ZlibCompressionParameter_gzHeader_get, _data_management_.ZlibCompressionParameter_gzHeader_set)
ZlibCompressionParameter_swigregister = _data_management_.ZlibCompressionParameter_swigregister
ZlibCompressionParameter_swigregister(ZlibCompressionParameter)


_data_management_.readOnly_swigconstant(_data_management_)
readOnly = _data_management_.readOnly

_data_management_.writeOnly_swigconstant(_data_management_)
writeOnly = _data_management_.writeOnly

_data_management_.readWrite_swigconstant(_data_management_)
readWrite = _data_management_.readWrite
class DataArchiveIface(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataArchiveIface, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataArchiveIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataArchiveIface
    __del__ = lambda self: None

    def write(self, ptr):
        return _data_management_.DataArchiveIface_write(self, ptr)

    def read(self, ptr):
        return _data_management_.DataArchiveIface_read(self, ptr)

    def getSizeOfArchive(self):
        return _data_management_.DataArchiveIface_getSizeOfArchive(self)

    def getArchiveAsString(self):
        return _data_management_.DataArchiveIface_getArchiveAsString(self)

    def copyArchiveToArray(self, ptr):
        return _data_management_.DataArchiveIface_copyArchiveToArray(self, ptr)

    def setMajorVersion(self, majorVersion):
        return _data_management_.DataArchiveIface_setMajorVersion(self, majorVersion)

    def setMinorVersion(self, minorVersion):
        return _data_management_.DataArchiveIface_setMinorVersion(self, minorVersion)

    def setUpdateVersion(self, updateVersion):
        return _data_management_.DataArchiveIface_setUpdateVersion(self, updateVersion)

    def getMajorVersion(self):
        return _data_management_.DataArchiveIface_getMajorVersion(self)

    def getMinorVersion(self):
        return _data_management_.DataArchiveIface_getMinorVersion(self)

    def getUpdateVersion(self):
        return _data_management_.DataArchiveIface_getUpdateVersion(self)
DataArchiveIface_swigregister = _data_management_.DataArchiveIface_swigregister
DataArchiveIface_swigregister(DataArchiveIface)

class DataArchiveImpl(DataArchiveIface):
    __swig_setmethods__ = {}
    for _s in [DataArchiveIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataArchiveImpl, name, value)
    __swig_getmethods__ = {}
    for _s in [DataArchiveIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataArchiveImpl, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataArchiveImpl
    __del__ = lambda self: None

    def setMajorVersion(self, majorVersion):
        return _data_management_.DataArchiveImpl_setMajorVersion(self, majorVersion)

    def setMinorVersion(self, minorVersion):
        return _data_management_.DataArchiveImpl_setMinorVersion(self, minorVersion)

    def setUpdateVersion(self, updateVersion):
        return _data_management_.DataArchiveImpl_setUpdateVersion(self, updateVersion)

    def getMajorVersion(self):
        return _data_management_.DataArchiveImpl_getMajorVersion(self)

    def getMinorVersion(self):
        return _data_management_.DataArchiveImpl_getMinorVersion(self)

    def getUpdateVersion(self):
        return _data_management_.DataArchiveImpl_getUpdateVersion(self)
DataArchiveImpl_swigregister = _data_management_.DataArchiveImpl_swigregister
DataArchiveImpl_swigregister(DataArchiveImpl)

class DataArchive(DataArchiveImpl):
    __swig_setmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataArchive, name, value)
    __swig_getmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataArchive, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_DataArchive(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DataArchive
    __del__ = lambda self: None

    def write(self, ptr):
        return _data_management_.DataArchive_write(self, ptr)

    def read(self, ptr):
        return _data_management_.DataArchive_read(self, ptr)

    def getSizeOfArchive(self):
        return _data_management_.DataArchive_getSizeOfArchive(self)

    def getArchiveAsString(self):
        return _data_management_.DataArchive_getArchiveAsString(self)

    def copyArchiveToArray(self, ptr):
        return _data_management_.DataArchive_copyArchiveToArray(self, ptr)

    def getArchiveAsArray(self):
        return _data_management_.DataArchive_getArchiveAsArray(self)
DataArchive_swigregister = _data_management_.DataArchive_swigregister
DataArchive_swigregister(DataArchive)

class CompressedDataArchive(DataArchiveImpl):
    __swig_setmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressedDataArchive, name, value)
    __swig_getmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CompressedDataArchive, name)
    __repr__ = _swig_repr

    def __init__(self, compressor):
        this = _data_management_.new_CompressedDataArchive(compressor)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CompressedDataArchive
    __del__ = lambda self: None

    def write(self, ptr):
        return _data_management_.CompressedDataArchive_write(self, ptr)

    def read(self, ptr):
        return _data_management_.CompressedDataArchive_read(self, ptr)

    def getSizeOfArchive(self):
        return _data_management_.CompressedDataArchive_getSizeOfArchive(self)

    def getArchiveAsString(self):
        return _data_management_.CompressedDataArchive_getArchiveAsString(self)

    def copyArchiveToArray(self, ptr):
        return _data_management_.CompressedDataArchive_copyArchiveToArray(self, ptr)
CompressedDataArchive_swigregister = _data_management_.CompressedDataArchive_swigregister
CompressedDataArchive_swigregister(CompressedDataArchive)

class DecompressedDataArchive(DataArchiveImpl):
    __swig_setmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DecompressedDataArchive, name, value)
    __swig_getmethods__ = {}
    for _s in [DataArchiveImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DecompressedDataArchive, name)
    __repr__ = _swig_repr

    def __init__(self, decompressor):
        this = _data_management_.new_DecompressedDataArchive(decompressor)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DecompressedDataArchive
    __del__ = lambda self: None

    def write(self, ptr):
        return _data_management_.DecompressedDataArchive_write(self, ptr)

    def read(self, ptr):
        return _data_management_.DecompressedDataArchive_read(self, ptr)

    def getSizeOfArchive(self):
        return _data_management_.DecompressedDataArchive_getSizeOfArchive(self)

    def getArchiveAsString(self):
        return _data_management_.DecompressedDataArchive_getArchiveAsString(self)

    def copyArchiveToArray(self, ptr):
        return _data_management_.DecompressedDataArchive_copyArchiveToArray(self, ptr)
DecompressedDataArchive_swigregister = _data_management_.DecompressedDataArchive_swigregister
DecompressedDataArchive_swigregister(DecompressedDataArchive)

class InputDataArchive(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputDataArchive, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, InputDataArchive, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_InputDataArchive(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_InputDataArchive
    __del__ = lambda self: None

    def archiveHeader(self):
        return _data_management_.InputDataArchive_archiveHeader(self)

    def archiveFooter(self):
        return _data_management_.InputDataArchive_archiveFooter(self)

    def segmentHeader(self, tag=0):
        return _data_management_.InputDataArchive_segmentHeader(self, tag)

    def segmentFooter(self):
        return _data_management_.InputDataArchive_segmentFooter(self)

    def setSingleObj(self, ptr):
        return _data_management_.InputDataArchive_setSingleObj(self, ptr)

    def getSizeOfArchive(self):
        return _data_management_.InputDataArchive_getSizeOfArchive(self)

    def getArchiveAsString(self):
        return _data_management_.InputDataArchive_getArchiveAsString(self)

    def copyArchiveToArray(self, ptr):
        return _data_management_.InputDataArchive_copyArchiveToArray(self, ptr)

    def getDataArchive(self):
        return _data_management_.InputDataArchive_getDataArchive(self)

    def getArchiveAsArray(self):
        return _data_management_.InputDataArchive_getArchiveAsArray(self)
InputDataArchive_swigregister = _data_management_.InputDataArchive_swigregister
InputDataArchive_swigregister(InputDataArchive)

class OutputDataArchive(daal.Base):
    __swig_setmethods__ = {}
    for _s in [daal.Base]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OutputDataArchive, name, value)
    __swig_getmethods__ = {}
    for _s in [daal.Base]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OutputDataArchive, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_OutputDataArchive(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_OutputDataArchive
    __del__ = lambda self: None

    def archiveHeader(self):
        return _data_management_.OutputDataArchive_archiveHeader(self)

    def archiveFooter(self):
        return _data_management_.OutputDataArchive_archiveFooter(self)

    def segmentHeader(self):
        return _data_management_.OutputDataArchive_segmentHeader(self)

    def segmentFooter(self):
        return _data_management_.OutputDataArchive_segmentFooter(self)

    def setSingleObj(self, ptr):
        return _data_management_.OutputDataArchive_setSingleObj(self, ptr)

    def get(self):
        return _data_management_.OutputDataArchive_get(self)

    def getMajorVersion(self):
        return _data_management_.OutputDataArchive_getMajorVersion(self)

    def getMinorVersion(self):
        return _data_management_.OutputDataArchive_getMinorVersion(self)

    def getUpdateVersion(self):
        return _data_management_.OutputDataArchive_getUpdateVersion(self)
OutputDataArchive_swigregister = _data_management_.OutputDataArchive_swigregister
OutputDataArchive_swigregister(OutputDataArchive)

class DataCollection(SerializationIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataCollection, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataCollection, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.DataCollection_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.DataCollection_serializationTag)

    def getSerializationTag(self):
        return _data_management_.DataCollection_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_DataCollection(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DataCollection
    __del__ = lambda self: None

    def get(self, *args):
        return _data_management_.DataCollection_get(self, *args)

    def push_back(self, x):
        return _data_management_.DataCollection_push_back(self, x)

    def __lshift__(self, x):
        return _data_management_.DataCollection___lshift__(self, x)

    def size(self):
        return _data_management_.DataCollection_size(self)

    def clear(self):
        return _data_management_.DataCollection_clear(self)

    def erase(self, pos):
        return _data_management_.DataCollection_erase(self, pos)

    def resize(self, newCapacity):
        return _data_management_.DataCollection_resize(self, newCapacity)

    def __getitem__(self, i):
        return _data_management_.DataCollection___getitem__(self, i)

    def __setitem__(self, i, v):
        return _data_management_.DataCollection___setitem__(self, i, v)
DataCollection_swigregister = _data_management_.DataCollection_swigregister
DataCollection_swigregister(DataCollection)

def DataCollection_serializationTag():
    return _data_management_.DataCollection_serializationTag()
DataCollection_serializationTag = _data_management_.DataCollection_serializationTag

class NumericTableFeature(SerializationIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, NumericTableFeature, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, NumericTableFeature, name)
    __repr__ = _swig_repr
    __swig_setmethods__["indexType"] = _data_management_.NumericTableFeature_indexType_set
    __swig_getmethods__["indexType"] = _data_management_.NumericTableFeature_indexType_get
    if _newclass:
        indexType = _swig_property(_data_management_.NumericTableFeature_indexType_get, _data_management_.NumericTableFeature_indexType_set)
    __swig_setmethods__["pmmlType"] = _data_management_.NumericTableFeature_pmmlType_set
    __swig_getmethods__["pmmlType"] = _data_management_.NumericTableFeature_pmmlType_get
    if _newclass:
        pmmlType = _swig_property(_data_management_.NumericTableFeature_pmmlType_get, _data_management_.NumericTableFeature_pmmlType_set)
    __swig_setmethods__["featureType"] = _data_management_.NumericTableFeature_featureType_set
    __swig_getmethods__["featureType"] = _data_management_.NumericTableFeature_featureType_get
    if _newclass:
        featureType = _swig_property(_data_management_.NumericTableFeature_featureType_get, _data_management_.NumericTableFeature_featureType_set)
    __swig_setmethods__["typeSize"] = _data_management_.NumericTableFeature_typeSize_set
    __swig_getmethods__["typeSize"] = _data_management_.NumericTableFeature_typeSize_get
    if _newclass:
        typeSize = _swig_property(_data_management_.NumericTableFeature_typeSize_get, _data_management_.NumericTableFeature_typeSize_set)
    __swig_setmethods__["categoryNumber"] = _data_management_.NumericTableFeature_categoryNumber_set
    __swig_getmethods__["categoryNumber"] = _data_management_.NumericTableFeature_categoryNumber_get
    if _newclass:
        categoryNumber = _swig_property(_data_management_.NumericTableFeature_categoryNumber_get, _data_management_.NumericTableFeature_categoryNumber_set)

    def __init__(self):
        this = _data_management_.new_NumericTableFeature()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_NumericTableFeature
    __del__ = lambda self: None

    def getSerializationTag(self):
        return _data_management_.NumericTableFeature_getSerializationTag(self)

    def getIndexType(self):
        return _data_management_.NumericTableFeature_getIndexType(self)

    def setType_Float64(self):
        r"""
    This function is specialized for float64"""
        return _data_management_.NumericTableFeature_setType_Float64(self)


    def setType_Float32(self):
        r"""
    This function is specialized for float32"""
        return _data_management_.NumericTableFeature_setType_Float32(self)


    def setType_Intc(self):
        r"""
    This function is specialized for intc"""
        return _data_management_.NumericTableFeature_setType_Intc(self)

NumericTableFeature_swigregister = _data_management_.NumericTableFeature_swigregister
NumericTableFeature_swigregister(NumericTableFeature)

class DictionaryIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DictionaryIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DictionaryIface, name)
    __repr__ = _swig_repr
    notEqual = _data_management_.DictionaryIface_notEqual
    equal = _data_management_.DictionaryIface_equal

    def __init__(self):
        this = _data_management_.new_DictionaryIface()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DictionaryIface
    __del__ = lambda self: None
DictionaryIface_swigregister = _data_management_.DictionaryIface_swigregister
DictionaryIface_swigregister(DictionaryIface)

class CategoricalFeatureDictionary(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CategoricalFeatureDictionary, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CategoricalFeatureDictionary, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_CategoricalFeatureDictionary()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CategoricalFeatureDictionary
    __del__ = lambda self: None
CategoricalFeatureDictionary_swigregister = _data_management_.CategoricalFeatureDictionary_swigregister
CategoricalFeatureDictionary_swigregister(CategoricalFeatureDictionary)

class DataSourceFeature(SerializationIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceFeature, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceFeature, name)
    __repr__ = _swig_repr
    __swig_setmethods__["ntFeature"] = _data_management_.DataSourceFeature_ntFeature_set
    __swig_getmethods__["ntFeature"] = _data_management_.DataSourceFeature_ntFeature_get
    if _newclass:
        ntFeature = _swig_property(_data_management_.DataSourceFeature_ntFeature_get, _data_management_.DataSourceFeature_ntFeature_set)
    __swig_setmethods__["name_length"] = _data_management_.DataSourceFeature_name_length_set
    __swig_getmethods__["name_length"] = _data_management_.DataSourceFeature_name_length_get
    if _newclass:
        name_length = _swig_property(_data_management_.DataSourceFeature_name_length_get, _data_management_.DataSourceFeature_name_length_set)
    __swig_setmethods__["name"] = _data_management_.DataSourceFeature_name_set
    __swig_getmethods__["name"] = _data_management_.DataSourceFeature_name_get
    if _newclass:
        name = _swig_property(_data_management_.DataSourceFeature_name_get, _data_management_.DataSourceFeature_name_set)
    __swig_setmethods__["cat_dict"] = _data_management_.DataSourceFeature_cat_dict_set
    __swig_getmethods__["cat_dict"] = _data_management_.DataSourceFeature_cat_dict_get
    if _newclass:
        cat_dict = _swig_property(_data_management_.DataSourceFeature_cat_dict_get, _data_management_.DataSourceFeature_cat_dict_set)

    def __init__(self, *args):
        this = _data_management_.new_DataSourceFeature(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_DataSourceFeature
    __del__ = lambda self: None

    def getFeatureName(self):
        return _data_management_.DataSourceFeature_getFeatureName(self)

    def getCategoricalDictionary(self):
        return _data_management_.DataSourceFeature_getCategoricalDictionary(self)

    def setCategoricalDictionary(self, dictionary):
        return _data_management_.DataSourceFeature_setCategoricalDictionary(self, dictionary)

    def setFeatureName(self, featureName):
        return _data_management_.DataSourceFeature_setFeatureName(self, featureName)

    def getSerializationTag(self):
        return _data_management_.DataSourceFeature_getSerializationTag(self)

    def getIndexType(self):
        return _data_management_.DataSourceFeature_getIndexType(self)

    def setType_Float64(self):
        r"""
    This function is specialized for float64"""
        return _data_management_.DataSourceFeature_setType_Float64(self)


    def setType_Float32(self):
        r"""
    This function is specialized for float32"""
        return _data_management_.DataSourceFeature_setType_Float32(self)


    def setType_Intc(self):
        r"""
    This function is specialized for intc"""
        return _data_management_.DataSourceFeature_setType_Intc(self)

DataSourceFeature_swigregister = _data_management_.DataSourceFeature_swigregister
DataSourceFeature_swigregister(DataSourceFeature)

class NumericTableIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, NumericTableIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, NumericTableIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_NumericTableIface
    __del__ = lambda self: None
    notAllocated = _data_management_.NumericTableIface_notAllocated
    userAllocated = _data_management_.NumericTableIface_userAllocated
    internallyAllocated = _data_management_.NumericTableIface_internallyAllocated
    doNotAllocate = _data_management_.NumericTableIface_doNotAllocate
    notAllocate = _data_management_.NumericTableIface_notAllocate
    doAllocate = _data_management_.NumericTableIface_doAllocate
    minimum = _data_management_.NumericTableIface_minimum
    maximum = _data_management_.NumericTableIface_maximum
    sum = _data_management_.NumericTableIface_sum
    sumSquares = _data_management_.NumericTableIface_sumSquares
    counters = _data_management_.NumericTableIface_counters
    nonNormalized = _data_management_.NumericTableIface_nonNormalized
    standardScoreNormalized = _data_management_.NumericTableIface_standardScoreNormalized
    minMaxNormalized = _data_management_.NumericTableIface_minMaxNormalized
    soa = _data_management_.NumericTableIface_soa
    aos = _data_management_.NumericTableIface_aos
    csrArray = _data_management_.NumericTableIface_csrArray
    upperPackedSymmetricMatrix = _data_management_.NumericTableIface_upperPackedSymmetricMatrix
    lowerPackedSymmetricMatrix = _data_management_.NumericTableIface_lowerPackedSymmetricMatrix
    upperPackedTriangularMatrix = _data_management_.NumericTableIface_upperPackedTriangularMatrix
    lowerPackedTriangularMatrix = _data_management_.NumericTableIface_lowerPackedTriangularMatrix
    arrow = _data_management_.NumericTableIface_arrow
    layout_unknown = _data_management_.NumericTableIface_layout_unknown

    def setDictionary(self, ddict):
        return _data_management_.NumericTableIface_setDictionary(self, ddict)

    def getDictionary(self):
        return _data_management_.NumericTableIface_getDictionary(self)

    def resetDictionary(self):
        return _data_management_.NumericTableIface_resetDictionary(self)

    def getFeatureType(self, feature_idx):
        return _data_management_.NumericTableIface_getFeatureType(self, feature_idx)

    def getNumberOfCategories(self, feature_idx):
        return _data_management_.NumericTableIface_getNumberOfCategories(self, feature_idx)

    def getDataLayout(self):
        return _data_management_.NumericTableIface_getDataLayout(self)

    def resize(self, nrows):
        return _data_management_.NumericTableIface_resize(self, nrows)

    def setNumberOfColumns(self, ncol):
        return _data_management_.NumericTableIface_setNumberOfColumns(self, ncol)

    def setNumberOfRows(self, nrow):
        return _data_management_.NumericTableIface_setNumberOfRows(self, nrow)

    def allocateDataMemory(self, *args):
        return _data_management_.NumericTableIface_allocateDataMemory(self, *args)

    def freeDataMemory(self):
        return _data_management_.NumericTableIface_freeDataMemory(self)

    def allocateBasicStatistics(self):
        return _data_management_.NumericTableIface_allocateBasicStatistics(self)

    def check(self, description, checkDataAllocation=True):
        return _data_management_.NumericTableIface_check(self, description, checkDataAllocation)
NumericTableIface_swigregister = _data_management_.NumericTableIface_swigregister
NumericTableIface_swigregister(NumericTableIface)

class DenseNumericTableIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DenseNumericTableIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DenseNumericTableIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DenseNumericTableIface
    __del__ = lambda self: None

    def getBlockOfRows(self, *args):
        return _data_management_.DenseNumericTableIface_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.DenseNumericTableIface_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.DenseNumericTableIface_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.DenseNumericTableIface_releaseBlockOfColumnValues(self, *args)

    def getBlockOfRowsAsDouble(self, vector_idx, vector_num):
        return _data_management_.DenseNumericTableIface_getBlockOfRowsAsDouble(self, vector_idx, vector_num)

    def getBlockOfColumnValuesAsDouble(self, feature_idx, vector_idx, value_num):
        return _data_management_.DenseNumericTableIface_getBlockOfColumnValuesAsDouble(self, feature_idx, vector_idx, value_num)

    def getBlockOfRowsAsFloat(self, vector_idx, vector_num):
        return _data_management_.DenseNumericTableIface_getBlockOfRowsAsFloat(self, vector_idx, vector_num)

    def getBlockOfColumnValuesAsFloat(self, feature_idx, vector_idx, value_num):
        return _data_management_.DenseNumericTableIface_getBlockOfColumnValuesAsFloat(self, feature_idx, vector_idx, value_num)

    def getBlockOfRowsAsInt(self, vector_idx, vector_num):
        return _data_management_.DenseNumericTableIface_getBlockOfRowsAsInt(self, vector_idx, vector_num)

    def getBlockOfColumnValuesAsInt(self, feature_idx, vector_idx, value_num):
        return _data_management_.DenseNumericTableIface_getBlockOfColumnValuesAsInt(self, feature_idx, vector_idx, value_num)
DenseNumericTableIface_swigregister = _data_management_.DenseNumericTableIface_swigregister
DenseNumericTableIface_swigregister(DenseNumericTableIface)
cvar = _data_management_.cvar
packed_mask = cvar.packed_mask

class NumericTable(SerializationIface, NumericTableIface, DenseNumericTableIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface, NumericTableIface, DenseNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, NumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, NumericTableIface, DenseNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, NumericTable, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_NumericTable
    __del__ = lambda self: None

    def setDictionary(self, ddict):
        return _data_management_.NumericTable_setDictionary(self, ddict)

    def getDictionary(self):
        return _data_management_.NumericTable_getDictionary(self)

    def resetDictionary(self):
        return _data_management_.NumericTable_resetDictionary(self)

    def resize(self, nrows):
        return _data_management_.NumericTable_resize(self, nrows)

    def getNumberOfColumns(self):
        return _data_management_.NumericTable_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.NumericTable_getNumberOfRows(self)

    def setNumberOfColumns(self, ncol):
        return _data_management_.NumericTable_setNumberOfColumns(self, ncol)

    def setNumberOfRows(self, nrow):
        return _data_management_.NumericTable_setNumberOfRows(self, nrow)

    def allocateDataMemory(self, *args):
        return _data_management_.NumericTable_allocateDataMemory(self, *args)

    def freeDataMemory(self):
        return _data_management_.NumericTable_freeDataMemory(self)

    def getDataLayout(self):
        return _data_management_.NumericTable_getDataLayout(self)

    def getFeatureType(self, feature_idx):
        return _data_management_.NumericTable_getFeatureType(self, feature_idx)

    def getNumberOfCategories(self, feature_idx):
        return _data_management_.NumericTable_getNumberOfCategories(self, feature_idx)

    def getDataMemoryStatus(self):
        return _data_management_.NumericTable_getDataMemoryStatus(self)

    def isNormalized(self, flag):
        return _data_management_.NumericTable_isNormalized(self, flag)

    def setNormalizationFlag(self, flag):
        return _data_management_.NumericTable_setNormalizationFlag(self, flag)

    def allocateBasicStatistics(self):
        return _data_management_.NumericTable_allocateBasicStatistics(self)

    def check(self, description, checkDataAllocation=True):
        return _data_management_.NumericTable_check(self, description, checkDataAllocation)

    def assign(self, *args):
        return _data_management_.NumericTable_assign(self, *args)
    __swig_setmethods__["basicStatistics"] = _data_management_.NumericTable_basicStatistics_set
    __swig_getmethods__["basicStatistics"] = _data_management_.NumericTable_basicStatistics_get
    if _newclass:
        basicStatistics = _swig_property(_data_management_.NumericTable_basicStatistics_get, _data_management_.NumericTable_basicStatistics_set)

    def getValue_Float64(self, *args):
        r"""
    This function is specialized for float64"""
        return _data_management_.NumericTable_getValue_Float64(self, *args)


    def getValue_Float32(self, *args):
        r"""
    This function is specialized for float32"""
        return _data_management_.NumericTable_getValue_Float32(self, *args)


    def getValue_Intc(self, *args):
        r"""
    This function is specialized for intc"""
        return _data_management_.NumericTable_getValue_Intc(self, *args)

NumericTable_swigregister = _data_management_.NumericTable_swigregister
NumericTable_swigregister(NumericTable)

class BasicStatisticsDataCollection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BasicStatisticsDataCollection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BasicStatisticsDataCollection, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_BasicStatisticsDataCollection()
        try:
            self.this.append(this)
        except:
            self.this = this

    def get(self, id):
        return _data_management_.BasicStatisticsDataCollection_get(self, id)

    def set(self, id, value):
        return _data_management_.BasicStatisticsDataCollection_set(self, id, value)
    __swig_destroy__ = _data_management_.delete_BasicStatisticsDataCollection
    __del__ = lambda self: None
BasicStatisticsDataCollection_swigregister = _data_management_.BasicStatisticsDataCollection_swigregister
BasicStatisticsDataCollection_swigregister(BasicStatisticsDataCollection)


def checkNumericTable(nt, description, unexpectedLayouts=0, expectedLayouts=0, nColumns=0, nRows=0, checkDataAllocation=True):
    return _data_management_.checkNumericTable(nt, description, unexpectedLayouts, expectedLayouts, nColumns, nRows, checkDataAllocation)
checkNumericTable = _data_management_.checkNumericTable
class TensorIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, TensorIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, TensorIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    notAllocated = _data_management_.TensorIface_notAllocated
    userAllocated = _data_management_.TensorIface_userAllocated
    internallyAllocated = _data_management_.TensorIface_internallyAllocated
    doNotAllocate = _data_management_.TensorIface_doNotAllocate
    notAllocate = _data_management_.TensorIface_notAllocate
    doAllocate = _data_management_.TensorIface_doAllocate
    __swig_destroy__ = _data_management_.delete_TensorIface
    __del__ = lambda self: None

    def setDimensions(self, *args):
        return _data_management_.TensorIface_setDimensions(self, *args)

    def allocateDataMemory(self, *args):
        return _data_management_.TensorIface_allocateDataMemory(self, *args)

    def freeDataMemory(self):
        return _data_management_.TensorIface_freeDataMemory(self)

    def resize(self, dimensions):
        return _data_management_.TensorIface_resize(self, dimensions)

    def check(self, description):
        return _data_management_.TensorIface_check(self, description)

    def getSampleTensor(self, firstDimIndex):
        return _data_management_.TensorIface_getSampleTensor(self, firstDimIndex)
TensorIface_swigregister = _data_management_.TensorIface_swigregister
TensorIface_swigregister(TensorIface)

class TensorLayoutIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, TensorLayoutIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, TensorLayoutIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_TensorLayoutIface
    __del__ = lambda self: None

    def shuffleDimensions(self, dimsOrder):
        return _data_management_.TensorLayoutIface_shuffleDimensions(self, dimsOrder)
TensorLayoutIface_swigregister = _data_management_.TensorLayoutIface_swigregister
TensorLayoutIface_swigregister(TensorLayoutIface)

class TensorLayout(SerializationIface, TensorLayoutIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface, TensorLayoutIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, TensorLayout, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, TensorLayoutIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, TensorLayout, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_TensorLayout
    __del__ = lambda self: None

    def getDimensions(self):
        return _data_management_.TensorLayout_getDimensions(self)
TensorLayout_swigregister = _data_management_.TensorLayout_swigregister
TensorLayout_swigregister(TensorLayout)

class TensorOffsetLayout(TensorLayout):
    __swig_setmethods__ = {}
    for _s in [TensorLayout]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, TensorOffsetLayout, name, value)
    __swig_getmethods__ = {}
    for _s in [TensorLayout]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, TensorOffsetLayout, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_TensorOffsetLayout(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_TensorOffsetLayout
    __del__ = lambda self: None

    def getOffsets(self):
        return _data_management_.TensorOffsetLayout_getOffsets(self)

    def getIndices(self):
        return _data_management_.TensorOffsetLayout_getIndices(self)

    def isLayout(self, layout):
        return _data_management_.TensorOffsetLayout_isLayout(self, layout)

    def isDefaultLayout(self):
        return _data_management_.TensorOffsetLayout_isDefaultLayout(self)

    def isRawLayout(self):
        return _data_management_.TensorOffsetLayout_isRawLayout(self)

    def shuffleDimensions(self, dimsOrder):
        return _data_management_.TensorOffsetLayout_shuffleDimensions(self, dimsOrder)

    def sortOffsets(self):
        return _data_management_.TensorOffsetLayout_sortOffsets(self)

    def getSerializationTag(self):
        return _data_management_.TensorOffsetLayout_getSerializationTag(self)
TensorOffsetLayout_swigregister = _data_management_.TensorOffsetLayout_swigregister
TensorOffsetLayout_swigregister(TensorOffsetLayout)

class DenseTensorIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DenseTensorIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DenseTensorIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DenseTensorIface
    __del__ = lambda self: None

    def getSubtensorEx(self, *args):
        return _data_management_.DenseTensorIface_getSubtensorEx(self, *args)

    def releaseSubtensor(self, *args):
        return _data_management_.DenseTensorIface_releaseSubtensor(self, *args)

    def getSubtensor(self, *args):
        return _data_management_.DenseTensorIface_getSubtensor(self, *args)

    def createDefaultSubtensorLayout(self):
        return _data_management_.DenseTensorIface_createDefaultSubtensorLayout(self)

    def createRawSubtensorLayout(self):
        return _data_management_.DenseTensorIface_createRawSubtensorLayout(self)
DenseTensorIface_swigregister = _data_management_.DenseTensorIface_swigregister
DenseTensorIface_swigregister(DenseTensorIface)

class Tensor(SerializationIface, TensorIface, DenseTensorIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface, TensorIface, DenseTensorIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Tensor, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, TensorIface, DenseTensorIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Tensor, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_Tensor
    __del__ = lambda self: None

    def getDataMemoryStatus(self):
        return _data_management_.Tensor_getDataMemoryStatus(self)

    def getNumberOfDimensions(self):
        return _data_management_.Tensor_getNumberOfDimensions(self)

    def getDimensionSize(self, dimIdx):
        return _data_management_.Tensor_getDimensionSize(self, dimIdx)

    def getDimensions(self):
        return _data_management_.Tensor_getDimensions(self)

    def getSize(self, *args):
        return _data_management_.Tensor_getSize(self, *args)

    def check(self, description):
        return _data_management_.Tensor_check(self, description)

    def getLayoutPtr(self):
        return _data_management_.Tensor_getLayoutPtr(self)

    def allocateDataMemory(self, *args):
        return _data_management_.Tensor_allocateDataMemory(self, *args)

    def freeDataMemory(self):
        return _data_management_.Tensor_freeDataMemory(self)

    def resize(self, dimensions):
        return _data_management_.Tensor_resize(self, dimensions)
Tensor_swigregister = _data_management_.Tensor_swigregister
Tensor_swigregister(Tensor)


def checkTensor(tensor, description, dims=None):
    return _data_management_.checkTensor(tensor, description, dims)
checkTensor = _data_management_.checkTensor
class AOSNumericTable(NumericTable):
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, AOSNumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, AOSNumericTable, name)
    __repr__ = _swig_repr

    def __init__(self, ary):
        this = _data_management_.new_AOSNumericTable(ary)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_AOSNumericTable
    __del__ = lambda self: None

    def getSerializationTag(self):
        return _data_management_.AOSNumericTable_getSerializationTag(self)

    def getBlockOfRows(self, *args):
        return _data_management_.AOSNumericTable_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.AOSNumericTable_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.AOSNumericTable_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.AOSNumericTable_releaseBlockOfColumnValues(self, *args)

    def allocateDataMemory(self, *args):
        return _data_management_.AOSNumericTable_allocateDataMemory(self, *args)

    def freeDataMemory(self):
        return _data_management_.AOSNumericTable_freeDataMemory(self)
AOSNumericTable_swigregister = _data_management_.AOSNumericTable_swigregister
AOSNumericTable_swigregister(AOSNumericTable)

class SOANumericTable(NumericTable):
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, SOANumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, SOANumericTable, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.SOANumericTable_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.SOANumericTable_serializationTag)

    def getSerializationTag(self):
        return _data_management_.SOANumericTable_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_SOANumericTable(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_SOANumericTable
    __del__ = lambda self: None

    def getBlockOfRows(self, *args):
        return _data_management_.SOANumericTable_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.SOANumericTable_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.SOANumericTable_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.SOANumericTable_releaseBlockOfColumnValues(self, *args)

    def setDictionary(self, ddict):
        return _data_management_.SOANumericTable_setDictionary(self, ddict)

    def setArray(self, ary, idx):
        return _data_management_.SOANumericTable_setArray(self, ary, idx)

    def getArray(self, index):
        return _data_management_.SOANumericTable_getArray(self, index)
SOANumericTable_swigregister = _data_management_.SOANumericTable_swigregister
SOANumericTable_swigregister(SOANumericTable)

def SOANumericTable_serializationTag():
    return _data_management_.SOANumericTable_serializationTag()
SOANumericTable_serializationTag = _data_management_.SOANumericTable_serializationTag

class CSRNumericTableIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSRNumericTableIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSRNumericTableIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    zeroBased = _data_management_.CSRNumericTableIface_zeroBased
    oneBased = _data_management_.CSRNumericTableIface_oneBased
    __swig_destroy__ = _data_management_.delete_CSRNumericTableIface
    __del__ = lambda self: None

    def getDataSize(self):
        return _data_management_.CSRNumericTableIface_getDataSize(self)

    def getSparseBlock(self, *args):
        return _data_management_.CSRNumericTableIface_getSparseBlock(self, *args)

    def releaseSparseBlock(self, *args):
        return _data_management_.CSRNumericTableIface_releaseSparseBlock(self, *args)
CSRNumericTableIface_swigregister = _data_management_.CSRNumericTableIface_swigregister
CSRNumericTableIface_swigregister(CSRNumericTableIface)

class CSRNumericTable(NumericTable, CSRNumericTableIface):
    __swig_setmethods__ = {}
    for _s in [NumericTable, CSRNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSRNumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, CSRNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CSRNumericTable, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.CSRNumericTable_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.CSRNumericTable_serializationTag)

    def getSerializationTag(self):
        return _data_management_.CSRNumericTable_getSerializationTag(self)
    __swig_destroy__ = _data_management_.delete_CSRNumericTable
    __del__ = lambda self: None

    def resize(self, nrows):
        return _data_management_.CSRNumericTable_resize(self, nrows)

    def getBlockOfRows(self, *args):
        return _data_management_.CSRNumericTable_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.CSRNumericTable_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.CSRNumericTable_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.CSRNumericTable_releaseBlockOfColumnValues(self, *args)

    def getSparseBlock(self, *args):
        return _data_management_.CSRNumericTable_getSparseBlock(self, *args)

    def releaseSparseBlock(self, *args):
        return _data_management_.CSRNumericTable_releaseSparseBlock(self, *args)

    def allocateDataMemory(self, *args):
        return _data_management_.CSRNumericTable_allocateDataMemory(self, *args)

    def getCSRIndexing(self):
        return _data_management_.CSRNumericTable_getCSRIndexing(self)

    def check(self, description, checkDataAllocation=True):
        return _data_management_.CSRNumericTable_check(self, description, checkDataAllocation)

    def getDataSize(self):
        return _data_management_.CSRNumericTable_getDataSize(self)

    def __init__(self, *args):
        this = _data_management_.new_CSRNumericTable(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def setArrays(self, *args):
        return _data_management_.CSRNumericTable_setArrays(self, *args)

    def getArrays(self):
        return _data_management_.CSRNumericTable_getArrays(self)
CSRNumericTable_swigregister = _data_management_.CSRNumericTable_swigregister
CSRNumericTable_swigregister(CSRNumericTable)

def CSRNumericTable_serializationTag():
    return _data_management_.CSRNumericTable_serializationTag()
CSRNumericTable_serializationTag = _data_management_.CSRNumericTable_serializationTag

class MergedNumericTable(NumericTable):
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, MergedNumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, MergedNumericTable, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.MergedNumericTable_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.MergedNumericTable_serializationTag)

    def getSerializationTag(self):
        return _data_management_.MergedNumericTable_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_MergedNumericTable(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def addNumericTable(self, table):
        return _data_management_.MergedNumericTable_addNumericTable(self, table)

    def resize(self, nrow):
        return _data_management_.MergedNumericTable_resize(self, nrow)

    def getDataMemoryStatus(self):
        return _data_management_.MergedNumericTable_getDataMemoryStatus(self)

    def getBlockOfRows(self, *args):
        return _data_management_.MergedNumericTable_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.MergedNumericTable_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.MergedNumericTable_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.MergedNumericTable_releaseBlockOfColumnValues(self, *args)

    def allocateBasicStatistics(self):
        return _data_management_.MergedNumericTable_allocateBasicStatistics(self)
    __swig_destroy__ = _data_management_.delete_MergedNumericTable
    __del__ = lambda self: None
MergedNumericTable_swigregister = _data_management_.MergedNumericTable_swigregister
MergedNumericTable_swigregister(MergedNumericTable)

def MergedNumericTable_serializationTag():
    return _data_management_.MergedNumericTable_serializationTag()
MergedNumericTable_serializationTag = _data_management_.MergedNumericTable_serializationTag

class RowMergedNumericTable(NumericTable):
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, RowMergedNumericTable, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, RowMergedNumericTable, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.RowMergedNumericTable_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.RowMergedNumericTable_serializationTag)

    def getSerializationTag(self):
        return _data_management_.RowMergedNumericTable_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_RowMergedNumericTable(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def addNumericTable(self, table):
        return _data_management_.RowMergedNumericTable_addNumericTable(self, table)

    def resize(self, nrows):
        return _data_management_.RowMergedNumericTable_resize(self, nrows)

    def getDataMemoryStatus(self):
        return _data_management_.RowMergedNumericTable_getDataMemoryStatus(self)

    def getBlockOfRows(self, *args):
        return _data_management_.RowMergedNumericTable_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.RowMergedNumericTable_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.RowMergedNumericTable_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.RowMergedNumericTable_releaseBlockOfColumnValues(self, *args)
    __swig_destroy__ = _data_management_.delete_RowMergedNumericTable
    __del__ = lambda self: None
RowMergedNumericTable_swigregister = _data_management_.RowMergedNumericTable_swigregister
RowMergedNumericTable_swigregister(RowMergedNumericTable)

def RowMergedNumericTable_serializationTag():
    return _data_management_.RowMergedNumericTable_serializationTag()
RowMergedNumericTable_serializationTag = _data_management_.RowMergedNumericTable_serializationTag

class PackedArrayNumericTableIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedArrayNumericTableIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PackedArrayNumericTableIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_PackedArrayNumericTableIface
    __del__ = lambda self: None

    def getPackedArray(self, *args):
        return _data_management_.PackedArrayNumericTableIface_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedArrayNumericTableIface_releasePackedArray(self, *args)
PackedArrayNumericTableIface_swigregister = _data_management_.PackedArrayNumericTableIface_swigregister
PackedArrayNumericTableIface_swigregister(PackedArrayNumericTableIface)

class DataSourceIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    readyForLoad = _data_management_.DataSourceIface_readyForLoad
    waitingForRows = _data_management_.DataSourceIface_waitingForRows
    endOfData = _data_management_.DataSourceIface_endOfData
    notReady = _data_management_.DataSourceIface_notReady
    notDictionaryFromContext = _data_management_.DataSourceIface_notDictionaryFromContext
    doDictionaryFromContext = _data_management_.DataSourceIface_doDictionaryFromContext
    notAllocateNumericTable = _data_management_.DataSourceIface_notAllocateNumericTable
    doAllocateNumericTable = _data_management_.DataSourceIface_doAllocateNumericTable

    def getDictionary(self):
        return _data_management_.DataSourceIface_getDictionary(self)

    def setDictionary(self, dict):
        return _data_management_.DataSourceIface_setDictionary(self, dict)

    def createDictionaryFromContext(self):
        return _data_management_.DataSourceIface_createDictionaryFromContext(self)

    def getStatus(self):
        return _data_management_.DataSourceIface_getStatus(self)

    def getNumberOfColumns(self):
        return _data_management_.DataSourceIface_getNumberOfColumns(self)

    def getNumericTableNumberOfColumns(self):
        return _data_management_.DataSourceIface_getNumericTableNumberOfColumns(self)

    def getNumberOfAvailableRows(self):
        return _data_management_.DataSourceIface_getNumberOfAvailableRows(self)

    def allocateNumericTable(self):
        return _data_management_.DataSourceIface_allocateNumericTable(self)

    def getNumericTable(self):
        return _data_management_.DataSourceIface_getNumericTable(self)

    def freeNumericTable(self):
        return _data_management_.DataSourceIface_freeNumericTable(self)

    def loadDataBlock(self, *args):
        return _data_management_.DataSourceIface_loadDataBlock(self, *args)
    __swig_destroy__ = _data_management_.delete_DataSourceIface
    __del__ = lambda self: None
DataSourceIface_swigregister = _data_management_.DataSourceIface_swigregister
DataSourceIface_swigregister(DataSourceIface)

class DataSource(DataSourceIface):
    __swig_setmethods__ = {}
    for _s in [DataSourceIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSource, name, value)
    __swig_getmethods__ = {}
    for _s in [DataSourceIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSource, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataSource
    __del__ = lambda self: None

    def getDictionary(self):
        return _data_management_.DataSource_getDictionary(self)

    def setDictionary(self, dict):
        return _data_management_.DataSource_setDictionary(self, dict)

    def createDictionaryFromContext(self):
        return _data_management_.DataSource_createDictionaryFromContext(self)

    def loadDataBlock(self, *args):
        return _data_management_.DataSource_loadDataBlock(self, *args)

    def getNumericTable(self):
        return _data_management_.DataSource_getNumericTable(self)

    def getNumberOfColumns(self):
        return _data_management_.DataSource_getNumberOfColumns(self)

    def status(self):
        return _data_management_.DataSource_status(self)

    def getNumericTableNumberOfColumns(self):
        return _data_management_.DataSource_getNumericTableNumberOfColumns(self)
DataSource_swigregister = _data_management_.DataSource_swigregister
DataSource_swigregister(DataSource)

class CsvDataSourceOptions(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsvDataSourceOptions, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CsvDataSourceOptions, name)
    __repr__ = _swig_repr
    byDefault = _data_management_.CsvDataSourceOptions_byDefault
    allocateNumericTable = _data_management_.CsvDataSourceOptions_allocateNumericTable
    createDictionaryFromContext = _data_management_.CsvDataSourceOptions_createDictionaryFromContext
    parseHeader = _data_management_.CsvDataSourceOptions_parseHeader
    __swig_getmethods__["unite"] = lambda x: _data_management_.CsvDataSourceOptions_unite
    if _newclass:
        unite = staticmethod(_data_management_.CsvDataSourceOptions_unite)

    def __init__(self, *args):
        this = _data_management_.new_CsvDataSourceOptions(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def getNumericTableAllocationFlag(self):
        return _data_management_.CsvDataSourceOptions_getNumericTableAllocationFlag(self)

    def getDictionaryCreationFlag(self):
        return _data_management_.CsvDataSourceOptions_getDictionaryCreationFlag(self)

    def getParseHeaderFlag(self):
        return _data_management_.CsvDataSourceOptions_getParseHeaderFlag(self)
    __swig_destroy__ = _data_management_.delete_CsvDataSourceOptions
    __del__ = lambda self: None
CsvDataSourceOptions_swigregister = _data_management_.CsvDataSourceOptions_swigregister
CsvDataSourceOptions_swigregister(CsvDataSourceOptions)

def CsvDataSourceOptions_unite(lhs, rhs):
    return _data_management_.CsvDataSourceOptions_unite(lhs, rhs)
CsvDataSourceOptions_unite = _data_management_.CsvDataSourceOptions_unite


def __or__(lhs, rhs):
    return _data_management_.__or__(lhs, rhs)
__or__ = _data_management_.__or__
class FeatureAuxData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, FeatureAuxData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, FeatureAuxData, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_FeatureAuxData(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_setmethods__["idx"] = _data_management_.FeatureAuxData_idx_set
    __swig_getmethods__["idx"] = _data_management_.FeatureAuxData_idx_get
    if _newclass:
        idx = _swig_property(_data_management_.FeatureAuxData_idx_get, _data_management_.FeatureAuxData_idx_set)
    __swig_setmethods__["wide"] = _data_management_.FeatureAuxData_wide_set
    __swig_getmethods__["wide"] = _data_management_.FeatureAuxData_wide_get
    if _newclass:
        wide = _swig_property(_data_management_.FeatureAuxData_wide_get, _data_management_.FeatureAuxData_wide_set)
    __swig_setmethods__["nCats"] = _data_management_.FeatureAuxData_nCats_set
    __swig_getmethods__["nCats"] = _data_management_.FeatureAuxData_nCats_get
    if _newclass:
        nCats = _swig_property(_data_management_.FeatureAuxData_nCats_get, _data_management_.FeatureAuxData_nCats_set)
    __swig_setmethods__["dsFeat"] = _data_management_.FeatureAuxData_dsFeat_set
    __swig_getmethods__["dsFeat"] = _data_management_.FeatureAuxData_dsFeat_get
    if _newclass:
        dsFeat = _swig_property(_data_management_.FeatureAuxData_dsFeat_get, _data_management_.FeatureAuxData_dsFeat_set)
    __swig_setmethods__["ntFeat"] = _data_management_.FeatureAuxData_ntFeat_set
    __swig_getmethods__["ntFeat"] = _data_management_.FeatureAuxData_ntFeat_get
    if _newclass:
        ntFeat = _swig_property(_data_management_.FeatureAuxData_ntFeat_get, _data_management_.FeatureAuxData_ntFeat_set)
    __swig_setmethods__["buffer"] = _data_management_.FeatureAuxData_buffer_set
    __swig_getmethods__["buffer"] = _data_management_.FeatureAuxData_buffer_get
    if _newclass:
        buffer = _swig_property(_data_management_.FeatureAuxData_buffer_get, _data_management_.FeatureAuxData_buffer_set)
    __swig_destroy__ = _data_management_.delete_FeatureAuxData
    __del__ = lambda self: None
FeatureAuxData_swigregister = _data_management_.FeatureAuxData_swigregister
FeatureAuxData_swigregister(FeatureAuxData)

class ModifierIface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ModifierIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ModifierIface, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def apply(self, funcList, auxVect):
        return _data_management_.ModifierIface_apply(self, funcList, auxVect)
    __swig_destroy__ = _data_management_.delete_ModifierIface
    __del__ = lambda self: None
    __swig_getmethods__["contFunc"] = lambda x: _data_management_.ModifierIface_contFunc
    if _newclass:
        contFunc = staticmethod(_data_management_.ModifierIface_contFunc)
    __swig_getmethods__["catFunc"] = lambda x: _data_management_.ModifierIface_catFunc
    if _newclass:
        catFunc = staticmethod(_data_management_.ModifierIface_catFunc)
    __swig_getmethods__["nullFunc"] = lambda x: _data_management_.ModifierIface_nullFunc
    if _newclass:
        nullFunc = staticmethod(_data_management_.ModifierIface_nullFunc)
ModifierIface_swigregister = _data_management_.ModifierIface_swigregister
ModifierIface_swigregister(ModifierIface)

def ModifierIface_contFunc(word, aux, arr):
    return _data_management_.ModifierIface_contFunc(word, aux, arr)
ModifierIface_contFunc = _data_management_.ModifierIface_contFunc

def ModifierIface_catFunc(word, aux, arr):
    return _data_management_.ModifierIface_catFunc(word, aux, arr)
ModifierIface_catFunc = _data_management_.ModifierIface_catFunc

def ModifierIface_nullFunc(word, aux, arr):
    return _data_management_.ModifierIface_nullFunc(word, aux, arr)
ModifierIface_nullFunc = _data_management_.ModifierIface_nullFunc

class MakeCategorical(ModifierIface):
    __swig_setmethods__ = {}
    for _s in [ModifierIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, MakeCategorical, name, value)
    __swig_getmethods__ = {}
    for _s in [ModifierIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, MakeCategorical, name)
    __repr__ = _swig_repr

    def __init__(self, idx):
        this = _data_management_.new_MakeCategorical(idx)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_MakeCategorical
    __del__ = lambda self: None

    def apply(self, funcList, auxVect):
        return _data_management_.MakeCategorical_apply(self, funcList, auxVect)
MakeCategorical_swigregister = _data_management_.MakeCategorical_swigregister
MakeCategorical_swigregister(MakeCategorical)

class OneHotEncoder(ModifierIface):
    __swig_setmethods__ = {}
    for _s in [ModifierIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, OneHotEncoder, name, value)
    __swig_getmethods__ = {}
    for _s in [ModifierIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, OneHotEncoder, name)
    __repr__ = _swig_repr

    def __init__(self, idx, nCats):
        this = _data_management_.new_OneHotEncoder(idx, nCats)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_OneHotEncoder
    __del__ = lambda self: None

    def apply(self, funcList, auxVect):
        return _data_management_.OneHotEncoder_apply(self, funcList, auxVect)
OneHotEncoder_swigregister = _data_management_.OneHotEncoder_swigregister
OneHotEncoder_swigregister(OneHotEncoder)

class ColumnFilter(ModifierIface):
    __swig_setmethods__ = {}
    for _s in [ModifierIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, ColumnFilter, name, value)
    __swig_getmethods__ = {}
    for _s in [ModifierIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, ColumnFilter, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_ColumnFilter()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_ColumnFilter
    __del__ = lambda self: None

    def odd(self):
        return _data_management_.ColumnFilter_odd(self)

    def even(self):
        return _data_management_.ColumnFilter_even(self)

    def none(self):
        return _data_management_.ColumnFilter_none(self)

    def list(self, valid):
        return _data_management_.ColumnFilter_list(self, valid)

    def apply(self, funcList, auxVect):
        return _data_management_.ColumnFilter_apply(self, funcList, auxVect)
ColumnFilter_swigregister = _data_management_.ColumnFilter_swigregister
ColumnFilter_swigregister(ColumnFilter)

class CSVFeatureManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSVFeatureManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSVFeatureManager, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_CSVFeatureManager()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CSVFeatureManager
    __del__ = lambda self: None

    def setDelimiter(self, delimiter):
        return _data_management_.CSVFeatureManager_setDelimiter(self, delimiter)

    def getNumericTableNumberOfColumns(self):
        return _data_management_.CSVFeatureManager_getNumericTableNumberOfColumns(self)

    def setFeatureDetailsFromDictionary(self, dictionary):
        return _data_management_.CSVFeatureManager_setFeatureDetailsFromDictionary(self, dictionary)

    def addModifier(self, *args):
        return _data_management_.CSVFeatureManager_addModifier(self, *args)

    def parseRowAsHeader(self, rawRowData):
        return _data_management_.CSVFeatureManager_parseRowAsHeader(self, rawRowData)

    def parseRowAsDictionary(self, rawRowData, dictionary):
        return _data_management_.CSVFeatureManager_parseRowAsDictionary(self, rawRowData, dictionary)

    def parseRowIn(self, rawRowData, dictionary, nt, ntRowIndex):
        return _data_management_.CSVFeatureManager_parseRowIn(self, rawRowData, dictionary, nt, ntRowIndex)

    def finalize(self, dictionary):
        return _data_management_.CSVFeatureManager_finalize(self, dictionary)
CSVFeatureManager_swigregister = _data_management_.CSVFeatureManager_swigregister
CSVFeatureManager_swigregister(CSVFeatureManager)


def convertToHomogen_Float64(*args):
    return _data_management_.convertToHomogen_Float64(*args)
convertToHomogen_Float64 = _data_management_.convertToHomogen_Float64

def convertToHomogen_Float32(*args):
    return _data_management_.convertToHomogen_Float32(*args)
convertToHomogen_Float32 = _data_management_.convertToHomogen_Float32

def convertToHomogen_Intc(*args):
    return _data_management_.convertToHomogen_Intc(*args)
convertToHomogen_Intc = _data_management_.convertToHomogen_Intc
class NumericTableDictionary(SerializationIface, DictionaryIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface, DictionaryIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, NumericTableDictionary, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, DictionaryIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, NumericTableDictionary, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.NumericTableDictionary_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.NumericTableDictionary_serializationTag)

    def getSerializationTag(self):
        return _data_management_.NumericTableDictionary_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_NumericTableDictionary(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_getmethods__["create"] = lambda x: _data_management_.NumericTableDictionary_create
    if _newclass:
        create = staticmethod(_data_management_.NumericTableDictionary_create)
    __swig_destroy__ = _data_management_.delete_NumericTableDictionary
    __del__ = lambda self: None

    def resetDictionary(self):
        return _data_management_.NumericTableDictionary_resetDictionary(self)

    def setAllFeatures(self, defaultFeature):
        return _data_management_.NumericTableDictionary_setAllFeatures(self, defaultFeature)

    def setNumberOfFeatures(self, numberOfFeatures):
        return _data_management_.NumericTableDictionary_setNumberOfFeatures(self, numberOfFeatures)

    def getNumberOfFeatures(self):
        return _data_management_.NumericTableDictionary_getNumberOfFeatures(self)

    def getFeaturesEqual(self):
        return _data_management_.NumericTableDictionary_getFeaturesEqual(self)

    def setFeature(self, feature, idx):
        return _data_management_.NumericTableDictionary_setFeature(self, feature, idx)

    def checkDictionary(self):
        return _data_management_.NumericTableDictionary_checkDictionary(self)

    def __getitem__(self, i):
        return _data_management_.NumericTableDictionary___getitem__(self, i)

    def __setitem__(self, i, v):
        return _data_management_.NumericTableDictionary___setitem__(self, i, v)
NumericTableDictionary_swigregister = _data_management_.NumericTableDictionary_swigregister
NumericTableDictionary_swigregister(NumericTableDictionary)

def NumericTableDictionary_serializationTag():
    return _data_management_.NumericTableDictionary_serializationTag()
NumericTableDictionary_serializationTag = _data_management_.NumericTableDictionary_serializationTag

def NumericTableDictionary_create(*args):
    return _data_management_.NumericTableDictionary_create(*args)
NumericTableDictionary_create = _data_management_.NumericTableDictionary_create

class DataSourceDictionary(SerializationIface, DictionaryIface):
    __swig_setmethods__ = {}
    for _s in [SerializationIface, DictionaryIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceDictionary, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, DictionaryIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceDictionary, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.DataSourceDictionary_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.DataSourceDictionary_serializationTag)

    def getSerializationTag(self):
        return _data_management_.DataSourceDictionary_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_DataSourceDictionary(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_getmethods__["create"] = lambda x: _data_management_.DataSourceDictionary_create
    if _newclass:
        create = staticmethod(_data_management_.DataSourceDictionary_create)
    __swig_destroy__ = _data_management_.delete_DataSourceDictionary
    __del__ = lambda self: None

    def resetDictionary(self):
        return _data_management_.DataSourceDictionary_resetDictionary(self)

    def setAllFeatures(self, defaultFeature):
        return _data_management_.DataSourceDictionary_setAllFeatures(self, defaultFeature)

    def setNumberOfFeatures(self, numberOfFeatures):
        return _data_management_.DataSourceDictionary_setNumberOfFeatures(self, numberOfFeatures)

    def getNumberOfFeatures(self):
        return _data_management_.DataSourceDictionary_getNumberOfFeatures(self)

    def getFeaturesEqual(self):
        return _data_management_.DataSourceDictionary_getFeaturesEqual(self)

    def setFeature(self, feature, idx):
        return _data_management_.DataSourceDictionary_setFeature(self, feature, idx)

    def checkDictionary(self):
        return _data_management_.DataSourceDictionary_checkDictionary(self)

    def __getitem__(self, i):
        return _data_management_.DataSourceDictionary___getitem__(self, i)

    def __setitem__(self, i, v):
        return _data_management_.DataSourceDictionary___setitem__(self, i, v)
DataSourceDictionary_swigregister = _data_management_.DataSourceDictionary_swigregister
DataSourceDictionary_swigregister(DataSourceDictionary)

def DataSourceDictionary_serializationTag():
    return _data_management_.DataSourceDictionary_serializationTag()
DataSourceDictionary_serializationTag = _data_management_.DataSourceDictionary_serializationTag

def DataSourceDictionary_create(*args):
    return _data_management_.DataSourceDictionary_create(*args)
DataSourceDictionary_create = _data_management_.DataSourceDictionary_create

class BlockDescriptor_Float64(_object):
    r"""
    This class is an alias of BlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BlockDescriptor_Float64, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BlockDescriptor_Float64, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_BlockDescriptor_Float64()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_BlockDescriptor_Float64
    __del__ = lambda self: None

    def getBlockSharedPtr(self):
        return _data_management_.BlockDescriptor_Float64_getBlockSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.BlockDescriptor_Float64_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.BlockDescriptor_Float64_getNumberOfRows(self)

    def reset(self):
        return _data_management_.BlockDescriptor_Float64_reset(self)

    def resizeBuffer(self, nColumns, nRows, auxMemorySize=0):
        return _data_management_.BlockDescriptor_Float64_resizeBuffer(self, nColumns, nRows, auxMemorySize)

    def setDetails(self, columnIdx, rowIdx, rwFlag):
        return _data_management_.BlockDescriptor_Float64_setDetails(self, columnIdx, rowIdx, rwFlag)

    def getColumnsOffset(self):
        return _data_management_.BlockDescriptor_Float64_getColumnsOffset(self)

    def getRowsOffset(self):
        return _data_management_.BlockDescriptor_Float64_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.BlockDescriptor_Float64_getRWFlag(self)

    def getAdditionalBufferPtr(self):
        return _data_management_.BlockDescriptor_Float64_getAdditionalBufferPtr(self)

    def getAdditionalBufferSharedPtr(self):
        return _data_management_.BlockDescriptor_Float64_getAdditionalBufferSharedPtr(self)

    def getArray(self):
        return _data_management_.BlockDescriptor_Float64_getArray(self)
BlockDescriptor_Float64_swigregister = _data_management_.BlockDescriptor_Float64_swigregister
BlockDescriptor_Float64_swigregister(BlockDescriptor_Float64)

class BlockDescriptor_Float32(_object):
    r"""
    This class is an alias of BlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BlockDescriptor_Float32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BlockDescriptor_Float32, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_BlockDescriptor_Float32()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_BlockDescriptor_Float32
    __del__ = lambda self: None

    def getBlockSharedPtr(self):
        return _data_management_.BlockDescriptor_Float32_getBlockSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.BlockDescriptor_Float32_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.BlockDescriptor_Float32_getNumberOfRows(self)

    def reset(self):
        return _data_management_.BlockDescriptor_Float32_reset(self)

    def resizeBuffer(self, nColumns, nRows, auxMemorySize=0):
        return _data_management_.BlockDescriptor_Float32_resizeBuffer(self, nColumns, nRows, auxMemorySize)

    def setDetails(self, columnIdx, rowIdx, rwFlag):
        return _data_management_.BlockDescriptor_Float32_setDetails(self, columnIdx, rowIdx, rwFlag)

    def getColumnsOffset(self):
        return _data_management_.BlockDescriptor_Float32_getColumnsOffset(self)

    def getRowsOffset(self):
        return _data_management_.BlockDescriptor_Float32_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.BlockDescriptor_Float32_getRWFlag(self)

    def getAdditionalBufferPtr(self):
        return _data_management_.BlockDescriptor_Float32_getAdditionalBufferPtr(self)

    def getAdditionalBufferSharedPtr(self):
        return _data_management_.BlockDescriptor_Float32_getAdditionalBufferSharedPtr(self)

    def getArray(self):
        return _data_management_.BlockDescriptor_Float32_getArray(self)
BlockDescriptor_Float32_swigregister = _data_management_.BlockDescriptor_Float32_swigregister
BlockDescriptor_Float32_swigregister(BlockDescriptor_Float32)

class BlockDescriptor_Intc(_object):
    r"""
    This class is an alias of BlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BlockDescriptor_Intc, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BlockDescriptor_Intc, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_BlockDescriptor_Intc()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_BlockDescriptor_Intc
    __del__ = lambda self: None

    def getBlockSharedPtr(self):
        return _data_management_.BlockDescriptor_Intc_getBlockSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.BlockDescriptor_Intc_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.BlockDescriptor_Intc_getNumberOfRows(self)

    def reset(self):
        return _data_management_.BlockDescriptor_Intc_reset(self)

    def resizeBuffer(self, nColumns, nRows, auxMemorySize=0):
        return _data_management_.BlockDescriptor_Intc_resizeBuffer(self, nColumns, nRows, auxMemorySize)

    def setDetails(self, columnIdx, rowIdx, rwFlag):
        return _data_management_.BlockDescriptor_Intc_setDetails(self, columnIdx, rowIdx, rwFlag)

    def getColumnsOffset(self):
        return _data_management_.BlockDescriptor_Intc_getColumnsOffset(self)

    def getRowsOffset(self):
        return _data_management_.BlockDescriptor_Intc_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.BlockDescriptor_Intc_getRWFlag(self)

    def getAdditionalBufferPtr(self):
        return _data_management_.BlockDescriptor_Intc_getAdditionalBufferPtr(self)

    def getAdditionalBufferSharedPtr(self):
        return _data_management_.BlockDescriptor_Intc_getAdditionalBufferSharedPtr(self)

    def getArray(self):
        return _data_management_.BlockDescriptor_Intc_getArray(self)
BlockDescriptor_Intc_swigregister = _data_management_.BlockDescriptor_Intc_swigregister
BlockDescriptor_Intc_swigregister(BlockDescriptor_Intc)

class CSRBlockDescriptor_Float64(_object):
    r"""
    This class is an alias of CSRBlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSRBlockDescriptor_Float64, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSRBlockDescriptor_Float64, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_CSRBlockDescriptor_Float64()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CSRBlockDescriptor_Float64
    __del__ = lambda self: None

    def getBlockValuesPtr(self):
        return _data_management_.CSRBlockDescriptor_Float64_getBlockValuesPtr(self)

    def getBlockValuesSharedPtr(self):
        return _data_management_.CSRBlockDescriptor_Float64_getBlockValuesSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.CSRBlockDescriptor_Float64_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.CSRBlockDescriptor_Float64_getNumberOfRows(self)

    def getDataSize(self):
        return _data_management_.CSRBlockDescriptor_Float64_getDataSize(self)

    def reset(self):
        return _data_management_.CSRBlockDescriptor_Float64_reset(self)

    def resizeValuesBuffer(self, nValues):
        return _data_management_.CSRBlockDescriptor_Float64_resizeValuesBuffer(self, nValues)

    def resizeRowsBuffer(self, nRows):
        return _data_management_.CSRBlockDescriptor_Float64_resizeRowsBuffer(self, nRows)

    def setDetails(self, nColumns, rowIdx, rwFlag):
        return _data_management_.CSRBlockDescriptor_Float64_setDetails(self, nColumns, rowIdx, rwFlag)

    def getRowsOffset(self):
        return _data_management_.CSRBlockDescriptor_Float64_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.CSRBlockDescriptor_Float64_getRWFlag(self)

    def getBlockColumnIndices(self):
        return _data_management_.CSRBlockDescriptor_Float64_getBlockColumnIndices(self)

    def getBlockRowIndices(self):
        return _data_management_.CSRBlockDescriptor_Float64_getBlockRowIndices(self)

    def getBlockValues(self):
        return _data_management_.CSRBlockDescriptor_Float64_getBlockValues(self)
CSRBlockDescriptor_Float64_swigregister = _data_management_.CSRBlockDescriptor_Float64_swigregister
CSRBlockDescriptor_Float64_swigregister(CSRBlockDescriptor_Float64)

class CSRBlockDescriptor_Float32(_object):
    r"""
    This class is an alias of CSRBlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSRBlockDescriptor_Float32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSRBlockDescriptor_Float32, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_CSRBlockDescriptor_Float32()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CSRBlockDescriptor_Float32
    __del__ = lambda self: None

    def getBlockValuesPtr(self):
        return _data_management_.CSRBlockDescriptor_Float32_getBlockValuesPtr(self)

    def getBlockValuesSharedPtr(self):
        return _data_management_.CSRBlockDescriptor_Float32_getBlockValuesSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.CSRBlockDescriptor_Float32_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.CSRBlockDescriptor_Float32_getNumberOfRows(self)

    def getDataSize(self):
        return _data_management_.CSRBlockDescriptor_Float32_getDataSize(self)

    def reset(self):
        return _data_management_.CSRBlockDescriptor_Float32_reset(self)

    def resizeValuesBuffer(self, nValues):
        return _data_management_.CSRBlockDescriptor_Float32_resizeValuesBuffer(self, nValues)

    def resizeRowsBuffer(self, nRows):
        return _data_management_.CSRBlockDescriptor_Float32_resizeRowsBuffer(self, nRows)

    def setDetails(self, nColumns, rowIdx, rwFlag):
        return _data_management_.CSRBlockDescriptor_Float32_setDetails(self, nColumns, rowIdx, rwFlag)

    def getRowsOffset(self):
        return _data_management_.CSRBlockDescriptor_Float32_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.CSRBlockDescriptor_Float32_getRWFlag(self)

    def getBlockColumnIndices(self):
        return _data_management_.CSRBlockDescriptor_Float32_getBlockColumnIndices(self)

    def getBlockRowIndices(self):
        return _data_management_.CSRBlockDescriptor_Float32_getBlockRowIndices(self)

    def getBlockValues(self):
        return _data_management_.CSRBlockDescriptor_Float32_getBlockValues(self)
CSRBlockDescriptor_Float32_swigregister = _data_management_.CSRBlockDescriptor_Float32_swigregister
CSRBlockDescriptor_Float32_swigregister(CSRBlockDescriptor_Float32)

class CSRBlockDescriptor_Intc(_object):
    r"""
    This class is an alias of CSRBlockDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CSRBlockDescriptor_Intc, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CSRBlockDescriptor_Intc, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_CSRBlockDescriptor_Intc()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_CSRBlockDescriptor_Intc
    __del__ = lambda self: None

    def getBlockValuesPtr(self):
        return _data_management_.CSRBlockDescriptor_Intc_getBlockValuesPtr(self)

    def getBlockValuesSharedPtr(self):
        return _data_management_.CSRBlockDescriptor_Intc_getBlockValuesSharedPtr(self)

    def getNumberOfColumns(self):
        return _data_management_.CSRBlockDescriptor_Intc_getNumberOfColumns(self)

    def getNumberOfRows(self):
        return _data_management_.CSRBlockDescriptor_Intc_getNumberOfRows(self)

    def getDataSize(self):
        return _data_management_.CSRBlockDescriptor_Intc_getDataSize(self)

    def reset(self):
        return _data_management_.CSRBlockDescriptor_Intc_reset(self)

    def resizeValuesBuffer(self, nValues):
        return _data_management_.CSRBlockDescriptor_Intc_resizeValuesBuffer(self, nValues)

    def resizeRowsBuffer(self, nRows):
        return _data_management_.CSRBlockDescriptor_Intc_resizeRowsBuffer(self, nRows)

    def setDetails(self, nColumns, rowIdx, rwFlag):
        return _data_management_.CSRBlockDescriptor_Intc_setDetails(self, nColumns, rowIdx, rwFlag)

    def getRowsOffset(self):
        return _data_management_.CSRBlockDescriptor_Intc_getRowsOffset(self)

    def getRWFlag(self):
        return _data_management_.CSRBlockDescriptor_Intc_getRWFlag(self)

    def getBlockColumnIndices(self):
        return _data_management_.CSRBlockDescriptor_Intc_getBlockColumnIndices(self)

    def getBlockRowIndices(self):
        return _data_management_.CSRBlockDescriptor_Intc_getBlockRowIndices(self)

    def getBlockValues(self):
        return _data_management_.CSRBlockDescriptor_Intc_getBlockValues(self)
CSRBlockDescriptor_Intc_swigregister = _data_management_.CSRBlockDescriptor_Intc_swigregister
CSRBlockDescriptor_Intc_swigregister(CSRBlockDescriptor_Intc)

class Compressor_Bzip2(CompressorImpl):
    r"""
    This class is an alias of Compressor()
    """
    __swig_setmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Compressor_Bzip2, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Compressor_Bzip2, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Compressor_Bzip2()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Compressor_Bzip2
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Compressor_Bzip2_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Compressor_Bzip2_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Compressor_Bzip2_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Compressor_Bzip2_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Compressor_Bzip2_parameter_get, _data_management_.Compressor_Bzip2_parameter_set)
Compressor_Bzip2_swigregister = _data_management_.Compressor_Bzip2_swigregister
Compressor_Bzip2_swigregister(Compressor_Bzip2)

class Compressor_Lzo(CompressorImpl):
    r"""
    This class is an alias of Compressor()
    """
    __swig_setmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Compressor_Lzo, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Compressor_Lzo, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Compressor_Lzo()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Compressor_Lzo
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Compressor_Lzo_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Compressor_Lzo_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Compressor_Lzo_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Compressor_Lzo_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Compressor_Lzo_parameter_get, _data_management_.Compressor_Lzo_parameter_set)
Compressor_Lzo_swigregister = _data_management_.Compressor_Lzo_swigregister
Compressor_Lzo_swigregister(Compressor_Lzo)

class Compressor_Rle(CompressorImpl):
    r"""
    This class is an alias of Compressor()
    """
    __swig_setmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Compressor_Rle, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Compressor_Rle, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Compressor_Rle()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Compressor_Rle
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Compressor_Rle_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Compressor_Rle_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Compressor_Rle_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Compressor_Rle_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Compressor_Rle_parameter_get, _data_management_.Compressor_Rle_parameter_set)
Compressor_Rle_swigregister = _data_management_.Compressor_Rle_swigregister
Compressor_Rle_swigregister(Compressor_Rle)

class Compressor_Zlib(CompressorImpl):
    r"""
    This class is an alias of Compressor()
    """
    __swig_setmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Compressor_Zlib, name, value)
    __swig_getmethods__ = {}
    for _s in [CompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Compressor_Zlib, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Compressor_Zlib()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Compressor_Zlib
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Compressor_Zlib_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Compressor_Zlib_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Compressor_Zlib_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Compressor_Zlib_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Compressor_Zlib_parameter_get, _data_management_.Compressor_Zlib_parameter_set)
Compressor_Zlib_swigregister = _data_management_.Compressor_Zlib_swigregister
Compressor_Zlib_swigregister(Compressor_Zlib)

class Decompressor_Bzip2(DecompressorImpl):
    r"""
    This class is an alias of Decompressor()
    """
    __swig_setmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Decompressor_Bzip2, name, value)
    __swig_getmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Decompressor_Bzip2, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Decompressor_Bzip2()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Decompressor_Bzip2
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Decompressor_Bzip2_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Decompressor_Bzip2_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Decompressor_Bzip2_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Decompressor_Bzip2_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Decompressor_Bzip2_parameter_get, _data_management_.Decompressor_Bzip2_parameter_set)
Decompressor_Bzip2_swigregister = _data_management_.Decompressor_Bzip2_swigregister
Decompressor_Bzip2_swigregister(Decompressor_Bzip2)

class Decompressor_Lzo(DecompressorImpl):
    r"""
    This class is an alias of Decompressor()
    """
    __swig_setmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Decompressor_Lzo, name, value)
    __swig_getmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Decompressor_Lzo, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Decompressor_Lzo()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Decompressor_Lzo
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Decompressor_Lzo_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Decompressor_Lzo_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Decompressor_Lzo_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Decompressor_Lzo_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Decompressor_Lzo_parameter_get, _data_management_.Decompressor_Lzo_parameter_set)
Decompressor_Lzo_swigregister = _data_management_.Decompressor_Lzo_swigregister
Decompressor_Lzo_swigregister(Decompressor_Lzo)

class Decompressor_Rle(DecompressorImpl):
    r"""
    This class is an alias of Decompressor()
    """
    __swig_setmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Decompressor_Rle, name, value)
    __swig_getmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Decompressor_Rle, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Decompressor_Rle()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Decompressor_Rle
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Decompressor_Rle_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Decompressor_Rle_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Decompressor_Rle_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Decompressor_Rle_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Decompressor_Rle_parameter_get, _data_management_.Decompressor_Rle_parameter_set)
Decompressor_Rle_swigregister = _data_management_.Decompressor_Rle_swigregister
Decompressor_Rle_swigregister(Decompressor_Rle)

class Decompressor_Zlib(DecompressorImpl):
    r"""
    This class is an alias of Decompressor()
    """
    __swig_setmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Decompressor_Zlib, name, value)
    __swig_getmethods__ = {}
    for _s in [DecompressorImpl]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Decompressor_Zlib, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_Decompressor_Zlib()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_Decompressor_Zlib
    __del__ = lambda self: None

    def setInputDataBlock(self, inBlock, offset):
        return _data_management_.Decompressor_Zlib_setInputDataBlock(self, inBlock, offset)

    def run(self, outBlock, offset):
        return _data_management_.Decompressor_Zlib_run(self, outBlock, offset)
    __swig_setmethods__["parameter"] = _data_management_.Decompressor_Zlib_parameter_set
    __swig_getmethods__["parameter"] = _data_management_.Decompressor_Zlib_parameter_get
    if _newclass:
        parameter = _swig_property(_data_management_.Decompressor_Zlib_parameter_get, _data_management_.Decompressor_Zlib_parameter_set)
Decompressor_Zlib_swigregister = _data_management_.Decompressor_Zlib_swigregister
Decompressor_Zlib_swigregister(Decompressor_Zlib)

class HomogenNumericTable_Float64(NumericTable):
    r"""
    This class is an alias of HomogenNumericTable()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenNumericTable_Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenNumericTable_Float64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenNumericTable_Float64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenNumericTable_Float64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenNumericTable_Float64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenNumericTable_Float64_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenNumericTable_Float64_create)
    __swig_destroy__ = _data_management_.delete_HomogenNumericTable_Float64
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.HomogenNumericTable_Float64_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Float64_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Float64_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Float64_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Float64_releaseBlockOfColumnValues(self, *args)

    def __getitem__(self, i):
        return _data_management_.HomogenNumericTable_Float64___getitem__(self, i)

    def getArray(self):
        return _data_management_.HomogenNumericTable_Float64_getArray(self)
HomogenNumericTable_Float64_swigregister = _data_management_.HomogenNumericTable_Float64_swigregister
HomogenNumericTable_Float64_swigregister(HomogenNumericTable_Float64)

def HomogenNumericTable_Float64_serializationTag():
    return _data_management_.HomogenNumericTable_Float64_serializationTag()
HomogenNumericTable_Float64_serializationTag = _data_management_.HomogenNumericTable_Float64_serializationTag

def HomogenNumericTable_Float64_create(*args):
    return _data_management_.HomogenNumericTable_Float64_create(*args)
HomogenNumericTable_Float64_create = _data_management_.HomogenNumericTable_Float64_create

class HomogenNumericTable_Float32(NumericTable):
    r"""
    This class is an alias of HomogenNumericTable()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenNumericTable_Float32, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenNumericTable_Float32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenNumericTable_Float32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenNumericTable_Float32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenNumericTable_Float32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenNumericTable_Float32_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenNumericTable_Float32_create)
    __swig_destroy__ = _data_management_.delete_HomogenNumericTable_Float32
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.HomogenNumericTable_Float32_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Float32_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Float32_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Float32_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Float32_releaseBlockOfColumnValues(self, *args)

    def __getitem__(self, i):
        return _data_management_.HomogenNumericTable_Float32___getitem__(self, i)

    def getArray(self):
        return _data_management_.HomogenNumericTable_Float32_getArray(self)
HomogenNumericTable_Float32_swigregister = _data_management_.HomogenNumericTable_Float32_swigregister
HomogenNumericTable_Float32_swigregister(HomogenNumericTable_Float32)

def HomogenNumericTable_Float32_serializationTag():
    return _data_management_.HomogenNumericTable_Float32_serializationTag()
HomogenNumericTable_Float32_serializationTag = _data_management_.HomogenNumericTable_Float32_serializationTag

def HomogenNumericTable_Float32_create(*args):
    return _data_management_.HomogenNumericTable_Float32_create(*args)
HomogenNumericTable_Float32_create = _data_management_.HomogenNumericTable_Float32_create

class HomogenNumericTable_Intc(NumericTable):
    r"""
    This class is an alias of HomogenNumericTable()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenNumericTable_Intc, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenNumericTable_Intc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenNumericTable_Intc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenNumericTable_Intc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenNumericTable_Intc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenNumericTable_Intc_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenNumericTable_Intc_create)
    __swig_destroy__ = _data_management_.delete_HomogenNumericTable_Intc
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.HomogenNumericTable_Intc_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Intc_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.HomogenNumericTable_Intc_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Intc_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.HomogenNumericTable_Intc_releaseBlockOfColumnValues(self, *args)

    def __getitem__(self, i):
        return _data_management_.HomogenNumericTable_Intc___getitem__(self, i)

    def getArray(self):
        return _data_management_.HomogenNumericTable_Intc_getArray(self)
HomogenNumericTable_Intc_swigregister = _data_management_.HomogenNumericTable_Intc_swigregister
HomogenNumericTable_Intc_swigregister(HomogenNumericTable_Intc)

def HomogenNumericTable_Intc_serializationTag():
    return _data_management_.HomogenNumericTable_Intc_serializationTag()
HomogenNumericTable_Intc_serializationTag = _data_management_.HomogenNumericTable_Intc_serializationTag

def HomogenNumericTable_Intc_create(*args):
    return _data_management_.HomogenNumericTable_Intc_create(*args)
HomogenNumericTable_Intc_create = _data_management_.HomogenNumericTable_Intc_create

class HomogenTensor_Float64(Tensor):
    r"""
    This class is an alias of HomogenTensor()
    """
    __swig_setmethods__ = {}
    for _s in [Tensor]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenTensor_Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [Tensor]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenTensor_Float64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenTensor_Float64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenTensor_Float64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenTensor_Float64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenTensor_Float64_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenTensor_Float64_create)
    __swig_destroy__ = _data_management_.delete_HomogenTensor_Float64
    __del__ = lambda self: None

    def getTensorLayout(self):
        return _data_management_.HomogenTensor_Float64_getTensorLayout(self)

    def createDefaultSubtensorLayout(self):
        return _data_management_.HomogenTensor_Float64_createDefaultSubtensorLayout(self)

    def createRawSubtensorLayout(self):
        return _data_management_.HomogenTensor_Float64_createRawSubtensorLayout(self)

    def setDimensions(self, *args):
        return _data_management_.HomogenTensor_Float64_setDimensions(self, *args)

    def assign(self, initValue):
        return _data_management_.HomogenTensor_Float64_assign(self, initValue)

    def getSubtensorEx(self, *args):
        return _data_management_.HomogenTensor_Float64_getSubtensorEx(self, *args)

    def getSubtensor(self, *args):
        return _data_management_.HomogenTensor_Float64_getSubtensor(self, *args)

    def releaseSubtensor(self, *args):
        return _data_management_.HomogenTensor_Float64_releaseSubtensor(self, *args)

    def getSampleTensor(self, firstDimIndex):
        return _data_management_.HomogenTensor_Float64_getSampleTensor(self, firstDimIndex)

    def getArray(self):
        return _data_management_.HomogenTensor_Float64_getArray(self)
HomogenTensor_Float64_swigregister = _data_management_.HomogenTensor_Float64_swigregister
HomogenTensor_Float64_swigregister(HomogenTensor_Float64)

def HomogenTensor_Float64_serializationTag():
    return _data_management_.HomogenTensor_Float64_serializationTag()
HomogenTensor_Float64_serializationTag = _data_management_.HomogenTensor_Float64_serializationTag

def HomogenTensor_Float64_create(*args):
    return _data_management_.HomogenTensor_Float64_create(*args)
HomogenTensor_Float64_create = _data_management_.HomogenTensor_Float64_create

class HomogenTensor_Float32(Tensor):
    r"""
    This class is an alias of HomogenTensor()
    """
    __swig_setmethods__ = {}
    for _s in [Tensor]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenTensor_Float32, name, value)
    __swig_getmethods__ = {}
    for _s in [Tensor]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenTensor_Float32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenTensor_Float32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenTensor_Float32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenTensor_Float32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenTensor_Float32_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenTensor_Float32_create)
    __swig_destroy__ = _data_management_.delete_HomogenTensor_Float32
    __del__ = lambda self: None

    def getTensorLayout(self):
        return _data_management_.HomogenTensor_Float32_getTensorLayout(self)

    def createDefaultSubtensorLayout(self):
        return _data_management_.HomogenTensor_Float32_createDefaultSubtensorLayout(self)

    def createRawSubtensorLayout(self):
        return _data_management_.HomogenTensor_Float32_createRawSubtensorLayout(self)

    def setDimensions(self, *args):
        return _data_management_.HomogenTensor_Float32_setDimensions(self, *args)

    def assign(self, initValue):
        return _data_management_.HomogenTensor_Float32_assign(self, initValue)

    def getSubtensorEx(self, *args):
        return _data_management_.HomogenTensor_Float32_getSubtensorEx(self, *args)

    def getSubtensor(self, *args):
        return _data_management_.HomogenTensor_Float32_getSubtensor(self, *args)

    def releaseSubtensor(self, *args):
        return _data_management_.HomogenTensor_Float32_releaseSubtensor(self, *args)

    def getSampleTensor(self, firstDimIndex):
        return _data_management_.HomogenTensor_Float32_getSampleTensor(self, firstDimIndex)

    def getArray(self):
        return _data_management_.HomogenTensor_Float32_getArray(self)
HomogenTensor_Float32_swigregister = _data_management_.HomogenTensor_Float32_swigregister
HomogenTensor_Float32_swigregister(HomogenTensor_Float32)

def HomogenTensor_Float32_serializationTag():
    return _data_management_.HomogenTensor_Float32_serializationTag()
HomogenTensor_Float32_serializationTag = _data_management_.HomogenTensor_Float32_serializationTag

def HomogenTensor_Float32_create(*args):
    return _data_management_.HomogenTensor_Float32_create(*args)
HomogenTensor_Float32_create = _data_management_.HomogenTensor_Float32_create

class HomogenTensor_Intc(Tensor):
    r"""
    This class is an alias of HomogenTensor()
    """
    __swig_setmethods__ = {}
    for _s in [Tensor]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, HomogenTensor_Intc, name, value)
    __swig_getmethods__ = {}
    for _s in [Tensor]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, HomogenTensor_Intc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.HomogenTensor_Intc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.HomogenTensor_Intc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.HomogenTensor_Intc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.HomogenTensor_Intc_create
    if _newclass:
        create = staticmethod(_data_management_.HomogenTensor_Intc_create)
    __swig_destroy__ = _data_management_.delete_HomogenTensor_Intc
    __del__ = lambda self: None

    def getTensorLayout(self):
        return _data_management_.HomogenTensor_Intc_getTensorLayout(self)

    def createDefaultSubtensorLayout(self):
        return _data_management_.HomogenTensor_Intc_createDefaultSubtensorLayout(self)

    def createRawSubtensorLayout(self):
        return _data_management_.HomogenTensor_Intc_createRawSubtensorLayout(self)

    def setDimensions(self, *args):
        return _data_management_.HomogenTensor_Intc_setDimensions(self, *args)

    def assign(self, initValue):
        return _data_management_.HomogenTensor_Intc_assign(self, initValue)

    def getSubtensorEx(self, *args):
        return _data_management_.HomogenTensor_Intc_getSubtensorEx(self, *args)

    def getSubtensor(self, *args):
        return _data_management_.HomogenTensor_Intc_getSubtensor(self, *args)

    def releaseSubtensor(self, *args):
        return _data_management_.HomogenTensor_Intc_releaseSubtensor(self, *args)

    def getSampleTensor(self, firstDimIndex):
        return _data_management_.HomogenTensor_Intc_getSampleTensor(self, firstDimIndex)

    def getArray(self):
        return _data_management_.HomogenTensor_Intc_getArray(self)
HomogenTensor_Intc_swigregister = _data_management_.HomogenTensor_Intc_swigregister
HomogenTensor_Intc_swigregister(HomogenTensor_Intc)

def HomogenTensor_Intc_serializationTag():
    return _data_management_.HomogenTensor_Intc_serializationTag()
HomogenTensor_Intc_serializationTag = _data_management_.HomogenTensor_Intc_serializationTag

def HomogenTensor_Intc_create(*args):
    return _data_management_.HomogenTensor_Intc_create(*args)
HomogenTensor_Intc_create = _data_management_.HomogenTensor_Intc_create

class KeyValueCollection_SerializationIface(_object):
    r"""
    This class is an alias of KeyValueCollection()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KeyValueCollection_SerializationIface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KeyValueCollection_SerializationIface, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_KeyValueCollection_SerializationIface(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_KeyValueCollection_SerializationIface
    __del__ = lambda self: None

    def getKeyByIndex(self, idx):
        return _data_management_.KeyValueCollection_SerializationIface_getKeyByIndex(self, idx)

    def getValueByIndex(self, idx):
        return _data_management_.KeyValueCollection_SerializationIface_getValueByIndex(self, idx)

    def getValueByIndexConst(self, idx):
        return _data_management_.KeyValueCollection_SerializationIface_getValueByIndexConst(self, idx)

    def size(self):
        return _data_management_.KeyValueCollection_SerializationIface_size(self)

    def clear(self):
        return _data_management_.KeyValueCollection_SerializationIface_clear(self)

    def __getitem__(self, i):
        return _data_management_.KeyValueCollection_SerializationIface___getitem__(self, i)

    def __setitem__(self, i, v):
        return _data_management_.KeyValueCollection_SerializationIface___setitem__(self, i, v)
KeyValueCollection_SerializationIface_swigregister = _data_management_.KeyValueCollection_SerializationIface_swigregister
KeyValueCollection_SerializationIface_swigregister(KeyValueCollection_SerializationIface)

class KeyValueCollection_Input(_object):
    r"""
    This class is an alias of KeyValueCollection()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KeyValueCollection_Input, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KeyValueCollection_Input, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_KeyValueCollection_Input(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_KeyValueCollection_Input
    __del__ = lambda self: None

    def getKeyByIndex(self, idx):
        return _data_management_.KeyValueCollection_Input_getKeyByIndex(self, idx)

    def getValueByIndex(self, idx):
        return _data_management_.KeyValueCollection_Input_getValueByIndex(self, idx)

    def getValueByIndexConst(self, idx):
        return _data_management_.KeyValueCollection_Input_getValueByIndexConst(self, idx)

    def size(self):
        return _data_management_.KeyValueCollection_Input_size(self)

    def clear(self):
        return _data_management_.KeyValueCollection_Input_clear(self)

    def __getitem__(self, i):
        return _data_management_.KeyValueCollection_Input___getitem__(self, i)

    def __setitem__(self, i, v):
        return _data_management_.KeyValueCollection_Input___setitem__(self, i, v)
KeyValueCollection_Input_swigregister = _data_management_.KeyValueCollection_Input_swigregister
KeyValueCollection_Input_swigregister(KeyValueCollection_Input)

class Matrix_Float64(HomogenNumericTable_Float64):
    r"""
    This class is an alias of Matrix()
    """
    __swig_setmethods__ = {}
    for _s in [HomogenNumericTable_Float64]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Matrix_Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [HomogenNumericTable_Float64]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Matrix_Float64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.Matrix_Float64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.Matrix_Float64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.Matrix_Float64_getSerializationTag(self)
    __swig_destroy__ = _data_management_.delete_Matrix_Float64
    __del__ = lambda self: None
    __swig_getmethods__["create"] = lambda x: _data_management_.Matrix_Float64_create
    if _newclass:
        create = staticmethod(_data_management_.Matrix_Float64_create)
Matrix_Float64_swigregister = _data_management_.Matrix_Float64_swigregister
Matrix_Float64_swigregister(Matrix_Float64)

def Matrix_Float64_serializationTag():
    return _data_management_.Matrix_Float64_serializationTag()
Matrix_Float64_serializationTag = _data_management_.Matrix_Float64_serializationTag

def Matrix_Float64_create(*args):
    return _data_management_.Matrix_Float64_create(*args)
Matrix_Float64_create = _data_management_.Matrix_Float64_create

class Matrix_Float32(HomogenNumericTable_Float32):
    r"""
    This class is an alias of Matrix()
    """
    __swig_setmethods__ = {}
    for _s in [HomogenNumericTable_Float32]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Matrix_Float32, name, value)
    __swig_getmethods__ = {}
    for _s in [HomogenNumericTable_Float32]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Matrix_Float32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.Matrix_Float32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.Matrix_Float32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.Matrix_Float32_getSerializationTag(self)
    __swig_destroy__ = _data_management_.delete_Matrix_Float32
    __del__ = lambda self: None
    __swig_getmethods__["create"] = lambda x: _data_management_.Matrix_Float32_create
    if _newclass:
        create = staticmethod(_data_management_.Matrix_Float32_create)
Matrix_Float32_swigregister = _data_management_.Matrix_Float32_swigregister
Matrix_Float32_swigregister(Matrix_Float32)

def Matrix_Float32_serializationTag():
    return _data_management_.Matrix_Float32_serializationTag()
Matrix_Float32_serializationTag = _data_management_.Matrix_Float32_serializationTag

def Matrix_Float32_create(*args):
    return _data_management_.Matrix_Float32_create(*args)
Matrix_Float32_create = _data_management_.Matrix_Float32_create

class Matrix_Intc(HomogenNumericTable_Intc):
    r"""
    This class is an alias of Matrix()
    """
    __swig_setmethods__ = {}
    for _s in [HomogenNumericTable_Intc]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, Matrix_Intc, name, value)
    __swig_getmethods__ = {}
    for _s in [HomogenNumericTable_Intc]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, Matrix_Intc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.Matrix_Intc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.Matrix_Intc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.Matrix_Intc_getSerializationTag(self)
    __swig_destroy__ = _data_management_.delete_Matrix_Intc
    __del__ = lambda self: None
    __swig_getmethods__["create"] = lambda x: _data_management_.Matrix_Intc_create
    if _newclass:
        create = staticmethod(_data_management_.Matrix_Intc_create)
Matrix_Intc_swigregister = _data_management_.Matrix_Intc_swigregister
Matrix_Intc_swigregister(Matrix_Intc)

def Matrix_Intc_serializationTag():
    return _data_management_.Matrix_Intc_serializationTag()
Matrix_Intc_serializationTag = _data_management_.Matrix_Intc_serializationTag

def Matrix_Intc_create(*args):
    return _data_management_.Matrix_Intc_create(*args)
Matrix_Intc_create = _data_management_.Matrix_Intc_create

class SerializableKeyValueCollection_SerializationIface(SerializationIface, KeyValueCollection_SerializationIface):
    r"""
    This class is an alias of SerializableKeyValueCollection()
    """
    __swig_setmethods__ = {}
    for _s in [SerializationIface, KeyValueCollection_SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, SerializableKeyValueCollection_SerializationIface, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, KeyValueCollection_SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, SerializableKeyValueCollection_SerializationIface, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.SerializableKeyValueCollection_SerializationIface_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.SerializableKeyValueCollection_SerializationIface_serializationTag)

    def getSerializationTag(self):
        return _data_management_.SerializableKeyValueCollection_SerializationIface_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_SerializableKeyValueCollection_SerializationIface(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_SerializableKeyValueCollection_SerializationIface
    __del__ = lambda self: None
SerializableKeyValueCollection_SerializationIface_swigregister = _data_management_.SerializableKeyValueCollection_SerializationIface_swigregister
SerializableKeyValueCollection_SerializationIface_swigregister(SerializableKeyValueCollection_SerializationIface)

def SerializableKeyValueCollection_SerializationIface_serializationTag():
    return _data_management_.SerializableKeyValueCollection_SerializationIface_serializationTag()
SerializableKeyValueCollection_SerializationIface_serializationTag = _data_management_.SerializableKeyValueCollection_SerializationIface_serializationTag

class SubtensorDescriptor_Float64(_object):
    r"""
    This class is an alias of SubtensorDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SubtensorDescriptor_Float64, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SubtensorDescriptor_Float64, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_SubtensorDescriptor_Float64()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_SubtensorDescriptor_Float64
    __del__ = lambda self: None

    def getNumberOfDims(self):
        return _data_management_.SubtensorDescriptor_Float64_getNumberOfDims(self)

    def getLayout(self):
        return _data_management_.SubtensorDescriptor_Float64_getLayout(self)

    def getInplaceFlag(self):
        return _data_management_.SubtensorDescriptor_Float64_getInplaceFlag(self)

    def reset(self):
        return _data_management_.SubtensorDescriptor_Float64_reset(self)

    def resizeBuffer(self):
        return _data_management_.SubtensorDescriptor_Float64_resizeBuffer(self)

    def setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag):
        return _data_management_.SubtensorDescriptor_Float64_setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag)

    def saveOffsetLayout(self, layout):
        return _data_management_.SubtensorDescriptor_Float64_saveOffsetLayout(self, layout)

    def saveOffsetLayoutCopy(self, layout):
        return _data_management_.SubtensorDescriptor_Float64_saveOffsetLayoutCopy(self, layout)

    def getSize(self):
        return _data_management_.SubtensorDescriptor_Float64_getSize(self)

    def getFixedDims(self):
        return _data_management_.SubtensorDescriptor_Float64_getFixedDims(self)

    def getRangeDimIdx(self):
        return _data_management_.SubtensorDescriptor_Float64_getRangeDimIdx(self)

    def getRangeDimNum(self):
        return _data_management_.SubtensorDescriptor_Float64_getRangeDimNum(self)

    def getRWFlag(self):
        return _data_management_.SubtensorDescriptor_Float64_getRWFlag(self)

    def getArray(self):
        return _data_management_.SubtensorDescriptor_Float64_getArray(self)

    def getSubtensorDimSizes(self):
        return _data_management_.SubtensorDescriptor_Float64_getSubtensorDimSizes(self)

    def getFixedDimNums(self):
        return _data_management_.SubtensorDescriptor_Float64_getFixedDimNums(self)
SubtensorDescriptor_Float64_swigregister = _data_management_.SubtensorDescriptor_Float64_swigregister
SubtensorDescriptor_Float64_swigregister(SubtensorDescriptor_Float64)

class SubtensorDescriptor_Float32(_object):
    r"""
    This class is an alias of SubtensorDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SubtensorDescriptor_Float32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SubtensorDescriptor_Float32, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_SubtensorDescriptor_Float32()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_SubtensorDescriptor_Float32
    __del__ = lambda self: None

    def getNumberOfDims(self):
        return _data_management_.SubtensorDescriptor_Float32_getNumberOfDims(self)

    def getLayout(self):
        return _data_management_.SubtensorDescriptor_Float32_getLayout(self)

    def getInplaceFlag(self):
        return _data_management_.SubtensorDescriptor_Float32_getInplaceFlag(self)

    def reset(self):
        return _data_management_.SubtensorDescriptor_Float32_reset(self)

    def resizeBuffer(self):
        return _data_management_.SubtensorDescriptor_Float32_resizeBuffer(self)

    def setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag):
        return _data_management_.SubtensorDescriptor_Float32_setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag)

    def saveOffsetLayout(self, layout):
        return _data_management_.SubtensorDescriptor_Float32_saveOffsetLayout(self, layout)

    def saveOffsetLayoutCopy(self, layout):
        return _data_management_.SubtensorDescriptor_Float32_saveOffsetLayoutCopy(self, layout)

    def getSize(self):
        return _data_management_.SubtensorDescriptor_Float32_getSize(self)

    def getFixedDims(self):
        return _data_management_.SubtensorDescriptor_Float32_getFixedDims(self)

    def getRangeDimIdx(self):
        return _data_management_.SubtensorDescriptor_Float32_getRangeDimIdx(self)

    def getRangeDimNum(self):
        return _data_management_.SubtensorDescriptor_Float32_getRangeDimNum(self)

    def getRWFlag(self):
        return _data_management_.SubtensorDescriptor_Float32_getRWFlag(self)

    def getArray(self):
        return _data_management_.SubtensorDescriptor_Float32_getArray(self)

    def getSubtensorDimSizes(self):
        return _data_management_.SubtensorDescriptor_Float32_getSubtensorDimSizes(self)

    def getFixedDimNums(self):
        return _data_management_.SubtensorDescriptor_Float32_getFixedDimNums(self)
SubtensorDescriptor_Float32_swigregister = _data_management_.SubtensorDescriptor_Float32_swigregister
SubtensorDescriptor_Float32_swigregister(SubtensorDescriptor_Float32)

class SubtensorDescriptor_Intc(_object):
    r"""
    This class is an alias of SubtensorDescriptor()
    """
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SubtensorDescriptor_Intc, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SubtensorDescriptor_Intc, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _data_management_.new_SubtensorDescriptor_Intc()
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_SubtensorDescriptor_Intc
    __del__ = lambda self: None

    def getNumberOfDims(self):
        return _data_management_.SubtensorDescriptor_Intc_getNumberOfDims(self)

    def getLayout(self):
        return _data_management_.SubtensorDescriptor_Intc_getLayout(self)

    def getInplaceFlag(self):
        return _data_management_.SubtensorDescriptor_Intc_getInplaceFlag(self)

    def reset(self):
        return _data_management_.SubtensorDescriptor_Intc_reset(self)

    def resizeBuffer(self):
        return _data_management_.SubtensorDescriptor_Intc_resizeBuffer(self)

    def setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag):
        return _data_management_.SubtensorDescriptor_Intc_setDetails(self, tensorNDims, tensorDimNums, nFixedDims, fixedDimNums, rangeDimIdx, rangeDimNum, rwFlag)

    def saveOffsetLayout(self, layout):
        return _data_management_.SubtensorDescriptor_Intc_saveOffsetLayout(self, layout)

    def saveOffsetLayoutCopy(self, layout):
        return _data_management_.SubtensorDescriptor_Intc_saveOffsetLayoutCopy(self, layout)

    def getSize(self):
        return _data_management_.SubtensorDescriptor_Intc_getSize(self)

    def getFixedDims(self):
        return _data_management_.SubtensorDescriptor_Intc_getFixedDims(self)

    def getRangeDimIdx(self):
        return _data_management_.SubtensorDescriptor_Intc_getRangeDimIdx(self)

    def getRangeDimNum(self):
        return _data_management_.SubtensorDescriptor_Intc_getRangeDimNum(self)

    def getRWFlag(self):
        return _data_management_.SubtensorDescriptor_Intc_getRWFlag(self)

    def getArray(self):
        return _data_management_.SubtensorDescriptor_Intc_getArray(self)

    def getSubtensorDimSizes(self):
        return _data_management_.SubtensorDescriptor_Intc_getSubtensorDimSizes(self)

    def getFixedDimNums(self):
        return _data_management_.SubtensorDescriptor_Intc_getFixedDimNums(self)
SubtensorDescriptor_Intc_swigregister = _data_management_.SubtensorDescriptor_Intc_swigregister
SubtensorDescriptor_Intc_swigregister(SubtensorDescriptor_Intc)

class DataSourceTemplate_HomogenNumericTable_Float64Float64(DataSource):
    r"""
    This class is an alias of DataSourceTemplate()
    """
    __swig_setmethods__ = {}
    for _s in [DataSource]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceTemplate_HomogenNumericTable_Float64Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [DataSource]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceTemplate_HomogenNumericTable_Float64Float64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataSourceTemplate_HomogenNumericTable_Float64Float64
    __del__ = lambda self: None

    def freeNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_Float64Float64_freeNumericTable(self)

    def allocateNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_Float64Float64_allocateNumericTable(self)
DataSourceTemplate_HomogenNumericTable_Float64Float64_swigregister = _data_management_.DataSourceTemplate_HomogenNumericTable_Float64Float64_swigregister
DataSourceTemplate_HomogenNumericTable_Float64Float64_swigregister(DataSourceTemplate_HomogenNumericTable_Float64Float64)

class DataSourceTemplate_HomogenNumericTable_Float32Float64(DataSource):
    r"""
    This class is an alias of DataSourceTemplate()
    """
    __swig_setmethods__ = {}
    for _s in [DataSource]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceTemplate_HomogenNumericTable_Float32Float64, name, value)
    __swig_getmethods__ = {}
    for _s in [DataSource]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceTemplate_HomogenNumericTable_Float32Float64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataSourceTemplate_HomogenNumericTable_Float32Float64
    __del__ = lambda self: None

    def freeNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_Float32Float64_freeNumericTable(self)

    def allocateNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_Float32Float64_allocateNumericTable(self)
DataSourceTemplate_HomogenNumericTable_Float32Float64_swigregister = _data_management_.DataSourceTemplate_HomogenNumericTable_Float32Float64_swigregister
DataSourceTemplate_HomogenNumericTable_Float32Float64_swigregister(DataSourceTemplate_HomogenNumericTable_Float32Float64)

class DataSourceTemplate_HomogenNumericTable_IntcFloat64(DataSource):
    r"""
    This class is an alias of DataSourceTemplate()
    """
    __swig_setmethods__ = {}
    for _s in [DataSource]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, DataSourceTemplate_HomogenNumericTable_IntcFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [DataSource]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, DataSourceTemplate_HomogenNumericTable_IntcFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_DataSourceTemplate_HomogenNumericTable_IntcFloat64
    __del__ = lambda self: None

    def freeNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_IntcFloat64_freeNumericTable(self)

    def allocateNumericTable(self):
        return _data_management_.DataSourceTemplate_HomogenNumericTable_IntcFloat64_allocateNumericTable(self)
DataSourceTemplate_HomogenNumericTable_IntcFloat64_swigregister = _data_management_.DataSourceTemplate_HomogenNumericTable_IntcFloat64_swigregister
DataSourceTemplate_HomogenNumericTable_IntcFloat64_swigregister(DataSourceTemplate_HomogenNumericTable_IntcFloat64)

class CsvDataSource_CSVFeatureManagerFloat64(DataSourceTemplate_HomogenNumericTable_Float64Float64):
    r"""
    This class is an alias of CsvDataSource()
    """
    __swig_setmethods__ = {}
    for _s in [DataSourceTemplate_HomogenNumericTable_Float64Float64]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, CsvDataSource_CSVFeatureManagerFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [DataSourceTemplate_HomogenNumericTable_Float64Float64]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, CsvDataSource_CSVFeatureManagerFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _data_management_.delete_CsvDataSource_CSVFeatureManagerFloat64
    __del__ = lambda self: None

    def getFeatureManager(self):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_getFeatureManager(self)

    def getNumericTableNumberOfColumns(self):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_getNumericTableNumberOfColumns(self)

    def setDictionary(self, dict):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_setDictionary(self, dict)

    def loadDataBlock(self, *args):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_loadDataBlock(self, *args)

    def createDictionaryFromContext(self):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_createDictionaryFromContext(self)

    def getNumberOfAvailableRows(self):
        return _data_management_.CsvDataSource_CSVFeatureManagerFloat64_getNumberOfAvailableRows(self)
CsvDataSource_CSVFeatureManagerFloat64_swigregister = _data_management_.CsvDataSource_CSVFeatureManagerFloat64_swigregister
CsvDataSource_CSVFeatureManagerFloat64_swigregister(CsvDataSource_CSVFeatureManagerFloat64)

class FileDataSource_CSVFeatureManagerFloat64(CsvDataSource_CSVFeatureManagerFloat64):
    r"""
    This class is an alias of FileDataSource()
    """
    __swig_setmethods__ = {}
    for _s in [CsvDataSource_CSVFeatureManagerFloat64]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, FileDataSource_CSVFeatureManagerFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [CsvDataSource_CSVFeatureManagerFloat64]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, FileDataSource_CSVFeatureManagerFloat64, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_FileDataSource_CSVFeatureManagerFloat64(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_FileDataSource_CSVFeatureManagerFloat64
    __del__ = lambda self: None

    def createDictionaryFromContext(self):
        return _data_management_.FileDataSource_CSVFeatureManagerFloat64_createDictionaryFromContext(self)

    def getStatus(self):
        return _data_management_.FileDataSource_CSVFeatureManagerFloat64_getStatus(self)
FileDataSource_CSVFeatureManagerFloat64_swigregister = _data_management_.FileDataSource_CSVFeatureManagerFloat64_swigregister
FileDataSource_CSVFeatureManagerFloat64_swigregister(FileDataSource_CSVFeatureManagerFloat64)

class PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_releasePackedArray(self, *args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_swigregister = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_swigregister
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_swigregister(PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64)

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag():
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag()
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_serializationTag

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create(*args):
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create(*args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create

class PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_releasePackedArray(self, *args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_swigregister = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_swigregister
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_swigregister(PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32)

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag():
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag()
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_serializationTag

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create(*args):
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create(*args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create

class PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_releasePackedArray(self, *args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_swigregister = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_swigregister
PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_swigregister(PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc)

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag():
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag()
PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_serializationTag

def PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create(*args):
    return _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create(*args)
PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create = _data_management_.PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create

class PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_releasePackedArray(self, *args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_swigregister = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_swigregister
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_swigregister(PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64)

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag():
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag()
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_serializationTag

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create(*args):
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create(*args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create

class PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_releasePackedArray(self, *args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_swigregister = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_swigregister
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_swigregister(PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32)

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag():
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag()
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_serializationTag

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create(*args):
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create(*args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create

class PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedSymmetricMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create
    if _newclass:
        create = staticmethod(_data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create)
    __swig_destroy__ = _data_management_.delete_PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc
    __del__ = lambda self: None

    def assign(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_releasePackedArray(self, *args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_swigregister = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_swigregister
PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_swigregister(PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc)

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag():
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag()
PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_serializationTag

def PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create(*args):
    return _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create(*args)
PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create = _data_management_.PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create

class PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_releasePackedArray(self, *args)
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_swigregister = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_swigregister
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_swigregister(PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64)

def PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag():
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag()
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_serializationTag

def PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create(*args):
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create(*args)
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create

class PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_releasePackedArray(self, *args)
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_swigregister = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_swigregister
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_swigregister(PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32)

def PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag():
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag()
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_serializationTag

def PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create(*args):
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create(*args)
PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create

class PackedTriangularMatrix_UpperPackedTriangularMatrixIntc(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixIntc, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_UpperPackedTriangularMatrixIntc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_UpperPackedTriangularMatrixIntc
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_releasePackedArray(self, *args)
PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_swigregister = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_swigregister
PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_swigregister(PackedTriangularMatrix_UpperPackedTriangularMatrixIntc)

def PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag():
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag()
PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_serializationTag

def PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create(*args):
    return _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create(*args)
PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create = _data_management_.PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create

class PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_releasePackedArray(self, *args)
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_swigregister = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_swigregister
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_swigregister(PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64)

def PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag():
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag()
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_serializationTag

def PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create(*args):
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create(*args)
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create

class PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_releasePackedArray(self, *args)
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_swigregister = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_swigregister
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_swigregister(PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32)

def PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag():
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag()
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_serializationTag

def PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create(*args):
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create(*args)
PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create

class PackedTriangularMatrix_LowerPackedTriangularMatrixIntc(NumericTable, PackedArrayNumericTableIface):
    r"""
    This class is an alias of PackedTriangularMatrix()
    """
    __swig_setmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixIntc, name, value)
    __swig_getmethods__ = {}
    for _s in [NumericTable, PackedArrayNumericTableIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, PackedTriangularMatrix_LowerPackedTriangularMatrixIntc, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag)

    def getSerializationTag(self):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_getSerializationTag(self)
    __swig_getmethods__["create"] = lambda x: _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create
    if _newclass:
        create = staticmethod(_data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create)
    __swig_destroy__ = _data_management_.delete_PackedTriangularMatrix_LowerPackedTriangularMatrixIntc
    __del__ = lambda self: None

    def setNumberOfColumns(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_setNumberOfColumns(self, nDim)

    def setNumberOfRows(self, nDim):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_setNumberOfRows(self, nDim)

    def assign(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_assign(self, *args)

    def getBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_getBlockOfRows(self, *args)

    def releaseBlockOfRows(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_releaseBlockOfRows(self, *args)

    def getBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_getBlockOfColumnValues(self, *args)

    def releaseBlockOfColumnValues(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_releaseBlockOfColumnValues(self, *args)

    def getPackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_getPackedArray(self, *args)

    def releasePackedArray(self, *args):
        return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_releasePackedArray(self, *args)
PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_swigregister = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_swigregister
PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_swigregister(PackedTriangularMatrix_LowerPackedTriangularMatrixIntc)

def PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag():
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag()
PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_serializationTag

def PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create(*args):
    return _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create(*args)
PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create = _data_management_.PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create

class StringDataSource_CSVFeatureManagerFloat64(CsvDataSource_CSVFeatureManagerFloat64):
    r"""
    This class is an alias of StringDataSource()
    """
    __swig_setmethods__ = {}
    for _s in [CsvDataSource_CSVFeatureManagerFloat64]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StringDataSource_CSVFeatureManagerFloat64, name, value)
    __swig_getmethods__ = {}
    for _s in [CsvDataSource_CSVFeatureManagerFloat64]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StringDataSource_CSVFeatureManagerFloat64, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _data_management_.new_StringDataSource_CSVFeatureManagerFloat64(*args)
        try:
            self.this.append(this)
        except:
            self.this = this

    def setData(self, data):
        return _data_management_.StringDataSource_CSVFeatureManagerFloat64_setData(self, data)

    def getData(self):
        return _data_management_.StringDataSource_CSVFeatureManagerFloat64_getData(self)

    def resetData(self):
        return _data_management_.StringDataSource_CSVFeatureManagerFloat64_resetData(self)

    def createDictionaryFromContext(self):
        return _data_management_.StringDataSource_CSVFeatureManagerFloat64_createDictionaryFromContext(self)

    def getStatus(self):
        return _data_management_.StringDataSource_CSVFeatureManagerFloat64_getStatus(self)
    __swig_destroy__ = _data_management_.delete_StringDataSource_CSVFeatureManagerFloat64
    __del__ = lambda self: None
StringDataSource_CSVFeatureManagerFloat64_swigregister = _data_management_.StringDataSource_CSVFeatureManagerFloat64_swigregister
StringDataSource_CSVFeatureManagerFloat64_swigregister(StringDataSource_CSVFeatureManagerFloat64)

class KeyValueDataCollection(SerializationIface, KeyValueCollection_SerializationIface):
    r"""
    This class is an alias of SerializableKeyValueCollection()
    """
    __swig_setmethods__ = {}
    for _s in [SerializationIface, KeyValueCollection_SerializationIface]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, KeyValueDataCollection, name, value)
    __swig_getmethods__ = {}
    for _s in [SerializationIface, KeyValueCollection_SerializationIface]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, KeyValueDataCollection, name)
    __repr__ = _swig_repr
    __swig_getmethods__["serializationTag"] = lambda x: _data_management_.KeyValueDataCollection_serializationTag
    if _newclass:
        serializationTag = staticmethod(_data_management_.KeyValueDataCollection_serializationTag)

    def getSerializationTag(self):
        return _data_management_.KeyValueDataCollection_getSerializationTag(self)

    def __init__(self, *args):
        this = _data_management_.new_KeyValueDataCollection(*args)
        try:
            self.this.append(this)
        except:
            self.this = this
    __swig_destroy__ = _data_management_.delete_KeyValueDataCollection
    __del__ = lambda self: None
KeyValueDataCollection_swigregister = _data_management_.KeyValueDataCollection_swigregister
KeyValueDataCollection_swigregister(KeyValueDataCollection)

def KeyValueDataCollection_serializationTag():
    return _data_management_.KeyValueDataCollection_serializationTag()
KeyValueDataCollection_serializationTag = _data_management_.KeyValueDataCollection_serializationTag

from numpy import float64, float32, intc

class HomogenTensor(object):
    r"""Factory class for different types of HomogenTensor."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return HomogenTensor_Float64_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return HomogenTensor_Float32_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return HomogenTensor_Intc_create(*args)

        raise RuntimeError("No appropriate constructor found for HomogenTensor")

class KeyValueCollection(object):
    r"""Factory class for different types of KeyValueCollection."""
    def __new__(cls,
                T,
                *args, **kwargs):
        if T == daal.data_management.SerializationIface:
            return KeyValueCollection_SerializationIface(*args)
        if T == daal.algorithms.Input:
            return KeyValueCollection_Input(*args)

        raise RuntimeError("No appropriate constructor found for KeyValueCollection")

class HomogenNumericTable(object):
    r"""Factory class for different types of HomogenNumericTable."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return HomogenNumericTable_Float64_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return HomogenNumericTable_Float32_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return HomogenNumericTable_Intc_create(*args)

        raise RuntimeError("No appropriate constructor found for HomogenNumericTable")

class StringDataSource(object):
    r"""Factory class for different types of StringDataSource."""
    def __new__(cls,
                *args, **kwargs):
        if 'FeatureManager' not in kwargs or kwargs['FeatureManager'] == daal.data_management.CSVFeatureManager:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return StringDataSource_CSVFeatureManagerFloat64(*args)

        raise RuntimeError("No appropriate constructor found for StringDataSource")

class PackedTriangularMatrix(object):
    r"""Factory class for different types of PackedTriangularMatrix."""
    def __new__(cls,
                packedLayout,
                *args, **kwargs):
        if packedLayout == daal.data_management.NumericTableIface.upperPackedTriangularMatrix:
            if 'ntype' not in kwargs or kwargs['ntype'] == float64:
                return PackedTriangularMatrix_UpperPackedTriangularMatrixFloat64_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == float32:
                return PackedTriangularMatrix_UpperPackedTriangularMatrixFloat32_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == intc:
                return PackedTriangularMatrix_UpperPackedTriangularMatrixIntc_create(*args)
        if packedLayout == daal.data_management.NumericTableIface.lowerPackedTriangularMatrix:
            if 'ntype' not in kwargs or kwargs['ntype'] == float64:
                return PackedTriangularMatrix_LowerPackedTriangularMatrixFloat64_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == float32:
                return PackedTriangularMatrix_LowerPackedTriangularMatrixFloat32_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == intc:
                return PackedTriangularMatrix_LowerPackedTriangularMatrixIntc_create(*args)

        raise RuntimeError("No appropriate constructor found for PackedTriangularMatrix")

class BlockDescriptor(object):
    r"""Factory class for different types of BlockDescriptor."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return BlockDescriptor_Float64(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return BlockDescriptor_Float32(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return BlockDescriptor_Intc(*args)

        raise RuntimeError("No appropriate constructor found for BlockDescriptor")

class SubtensorDescriptor(object):
    r"""Factory class for different types of SubtensorDescriptor."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return SubtensorDescriptor_Float64(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return SubtensorDescriptor_Float32(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return SubtensorDescriptor_Intc(*args)

        raise RuntimeError("No appropriate constructor found for SubtensorDescriptor")

class Compressor(object):
    r"""Factory class for different types of Compressor."""
    def __new__(cls,
                CompressionMethod,
                *args, **kwargs):
        if CompressionMethod == daal.data_management.bzip2:
            return Compressor_Bzip2(*args)
        if CompressionMethod == daal.data_management.lzo:
            return Compressor_Lzo(*args)
        if CompressionMethod == daal.data_management.rle:
            return Compressor_Rle(*args)
        if CompressionMethod == daal.data_management.zlib:
            return Compressor_Zlib(*args)

        raise RuntimeError("No appropriate constructor found for Compressor")

class CsvDataSource(object):
    r"""Factory class for different types of CsvDataSource."""
    def __new__(cls,
                *args, **kwargs):
        if 'FeatureManager' not in kwargs or kwargs['FeatureManager'] == daal.data_management.CSVFeatureManager:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return CsvDataSource_CSVFeatureManagerFloat64(*args)

        raise RuntimeError("No appropriate constructor found for CsvDataSource")

class DataSourceTemplate(object):
    r"""Factory class for different types of DataSourceTemplate."""
    def __new__(cls,
                TableType,
                *args, **kwargs):
        if TableType == daal.data_management.HomogenNumericTable_float64:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return DataSourceTemplate_HomogenNumericTable_Float64Float64(*args)
        if TableType == daal.data_management.HomogenNumericTable_float32:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return DataSourceTemplate_HomogenNumericTable_Float32Float64(*args)
        if TableType == daal.data_management.HomogenNumericTable_intc:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return DataSourceTemplate_HomogenNumericTable_IntcFloat64(*args)

        raise RuntimeError("No appropriate constructor found for DataSourceTemplate")

class PackedSymmetricMatrix(object):
    r"""Factory class for different types of PackedSymmetricMatrix."""
    def __new__(cls,
                packedLayout,
                *args, **kwargs):
        if packedLayout == daal.data_management.NumericTableIface.upperPackedSymmetricMatrix:
            if 'ntype' not in kwargs or kwargs['ntype'] == float64:
                return PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat64_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == float32:
                return PackedSymmetricMatrix_UpperPackedSymmetricMatrixFloat32_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == intc:
                return PackedSymmetricMatrix_UpperPackedSymmetricMatrixIntc_create(*args)
        if packedLayout == daal.data_management.NumericTableIface.lowerPackedSymmetricMatrix:
            if 'ntype' not in kwargs or kwargs['ntype'] == float64:
                return PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat64_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == float32:
                return PackedSymmetricMatrix_LowerPackedSymmetricMatrixFloat32_create(*args)
            if 'ntype' in kwargs and kwargs['ntype'] == intc:
                return PackedSymmetricMatrix_LowerPackedSymmetricMatrixIntc_create(*args)

        raise RuntimeError("No appropriate constructor found for PackedSymmetricMatrix")

class SerializableKeyValueCollection(object):
    r"""Factory class for different types of SerializableKeyValueCollection."""
    def __new__(cls,
                T,
                *args, **kwargs):
        if T == daal.data_management.SerializationIface:
            return SerializableKeyValueCollection_SerializationIface(*args)

        raise RuntimeError("No appropriate constructor found for SerializableKeyValueCollection")

class FileDataSource(object):
    r"""Factory class for different types of FileDataSource."""
    def __new__(cls,
                *args, **kwargs):
        if 'FeatureManager' not in kwargs or kwargs['FeatureManager'] == daal.data_management.CSVFeatureManager:
            if 'StatsType' not in kwargs or kwargs['StatsType'] == float64:
                return FileDataSource_CSVFeatureManagerFloat64(*args)

        raise RuntimeError("No appropriate constructor found for FileDataSource")

class CSRBlockDescriptor(object):
    r"""Factory class for different types of CSRBlockDescriptor."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return CSRBlockDescriptor_Float64(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return CSRBlockDescriptor_Float32(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return CSRBlockDescriptor_Intc(*args)

        raise RuntimeError("No appropriate constructor found for CSRBlockDescriptor")

class Decompressor(object):
    r"""Factory class for different types of Decompressor."""
    def __new__(cls,
                CompressionMethod,
                *args, **kwargs):
        if CompressionMethod == daal.data_management.bzip2:
            return Decompressor_Bzip2(*args)
        if CompressionMethod == daal.data_management.lzo:
            return Decompressor_Lzo(*args)
        if CompressionMethod == daal.data_management.rle:
            return Decompressor_Rle(*args)
        if CompressionMethod == daal.data_management.zlib:
            return Decompressor_Zlib(*args)

        raise RuntimeError("No appropriate constructor found for Decompressor")

class Matrix(object):
    r"""Factory class for different types of Matrix."""
    def __new__(cls,
                *args, **kwargs):
        if 'ntype' not in kwargs or kwargs['ntype'] == float64:
            return Matrix_Float64_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == float32:
            return Matrix_Float32_create(*args)
        if 'ntype' in kwargs and kwargs['ntype'] == intc:
            return Matrix_Intc_create(*args)

        raise RuntimeError("No appropriate constructor found for Matrix")


def convertToHomogen(ntable, ntype=float64):
    if ntype == float64:
        return convertToHomogen_Float64(ntable)
    elif ntype == float32:
        return convertToHomogen_Float32(ntable)
    elif ntype == intc:
        return convertToHomogen_Intc(ntable)
    else:
        raise TypeError("Cannot convert to HomogenNumericTable with data type {}".format(ntype))

# This file is compatible with both classic and new-style classes.


