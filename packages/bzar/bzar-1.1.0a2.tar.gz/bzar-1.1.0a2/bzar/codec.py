#
# MIT License
#
# Copyright (c) 2019 Keisuke Sehara
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""functions related to encoding/decoding of data and metadata."""

import sys as _sys
import json as _json
import struct as _struct
import warnings as _warnings
import zlib as _zlib

import numpy as _np

SizeEncoder               = _struct.Struct('Q')
METADATA_SIZE_WIDTH       = 8
DATA_INFO_KEYS            = ('datatype', 'byteorder')
DEFAULT_COMPRESSION_LEVEL = 6

DtypeDecoder        = {
    'byte':    (_np.ubyte,   False),
    'bool8':   (_np.bool,    False),
    'int8':    (_np.int8,    False),
    'uint8':   (_np.uint8,   False),
    'int16':   (_np.int16,   True),
    'uint16':  (_np.uint16,  True),
    'int32':   (_np.int32,   True),
    'uint32':  (_np.uint32,  True),
    'int64':   (_np.int64,   True),
    'uint64':  (_np.uint64,  True),
    'float32': (_np.float32, False),
    'float64': (_np.float64, False)
}
ByteOrderDecoder    = {
    'little': '<',
    'big':    '>'
}

class BzarDecodeError(IOError):
    def __init__(self, msg):
        super().__init__(msg)

def encode_byteorder(dtype):
    """used internally to resolve the byte order."""
    order = dtype.byteorder
    if order in ('@', '='):
        return _sys.byteorder # 'little' or 'big'
    elif order == '<':
        return 'little'
    elif order in ('>', '!'):
        return 'big'
    else:
        raise ValueError(f"unknown endian-ness: {order}")

def encode_dtype(dtype):
    """returns information about the data type as a dict."""
    datatype = None

    if dtype.char == 'c':
        datatype  = 'byte'
        order     = 'NA'

    elif dtype.char == 'b':
        datatype  = 'int8'
        order     = 'NA'

    elif dtype.char == 'B':
        datatype  = 'uint8'
        order     = 'NA'

    elif dtype.char == '?':
        datatype  = 'bool8'
        order     = 'NA'

    elif dtype.char == 'h':
        datatype  = 'int16'
        order     = encode_byteorder(dtype)

    elif dtype.char == 'H':
        datatype  = 'uint16'
        order     = encode_byteorder(dtype)

    elif dtype.char in ('i', 'l'):
        datatype  = f'int{dtype.itemsize*8}'
        order     = encode_byteorder(dtype)

    elif dtype.char in ('I', 'L'):
        datatype  = f'uint{dtype.itemsize*8}'
        order     = encode_byteorder(dtype)

    elif dtype.char == 'q':
        datatype  = 'int64'
        order     = encode_byteorder(dtype)

    elif dtype.char == 'Q':
        datatype  = 'uint64'
        order     = encode_byteorder(dtype)

    elif dtype.char == 'f':
        datatype  = 'float32'
        order     = 'NA'

    elif dtype.char == 'd':
        datatype  = 'float64'
        order     = 'NA'

    if datatype is None:
        raise ValueError(f"unsupported data type: {str(dtype)}")
    return dict(datatype=datatype, byteorder=order)

def decode_data_info(metadict):
    """used internally to generate 'dtype' object from the metadata dictionary."""
    if 'datatype' not in metadict.keys():
        raise KeyError(f"'datatype' not found in the metadata dictionary")
    datatype = metadict['datatype']
    if datatype not in DtypeDecoder.keys():
        raise KeyError(f"unknown data type: {datatype}")
    basetype, byteorder_sensitive = DtypeDecoder[datatype]
    if byteorder_sensitive == True:
        baseorder = _sys.byteorder
        if 'byteorder' not in metadict.keys():
            _warnings.warn("'byteorder' not found in the metadata dictionary: the native order is assumed.")
            return basetype
        order = metadict['byteorder']
        if order != baseorder:
            return basetype.newbyteorder(ByteOrderDecoder[order])
        else:
            return basetype
    else:
        return basetype

def encode_metadata_dict(metadict):
    """used internally to encode the metadata dictionary into its binary format."""
    return _json.dumps(metadict, separators=(',', ':')).encode('ascii')

def decode_metadata_dict(rawbytes):
    """used internally to decode the metadata dictionary from its binary format."""
    metadict = _json.loads(rawbytes.decode('ascii'))
    for key, val in metadict.items():
        if isinstance(val, list):
            metadict[key] = tuple(val)
    return metadict

def encode_metadata_size(metasiz):
    """used internally to encode the size of the metadata dictionary."""
    return SizeEncoder.pack(metasiz)

def decode_metadata_size(binarray):
    """used internally to decode the size of the metadata dictionary."""
    return SizeEncoder.unpack(binarray)[0]

def encode_data(data, order='C', compression_level=None):
    """encode a numpy.ndarray object."""
    if compression_level is None:
        compression_level = DEFAULT_COMPRESSION_LEVEL
    return _zlib.compress(data.tobytes(order=order), compression_level)

def decode_data(rawdata):
    return _zlib.decompress(rawdata)

class Encoder:
    """a binary stream encoder into a bzar archive."""

    def __init__(self, fileref, compression_level=None):
        """opens an encoder. it assumes that `fileref` is an opened binary writer,
        at the start of the stream."""
        self.__ref = fileref
        if compression_level is None:
            compression_level = DEFAULT_COMPRESSION_LEVEL
        self.__lib   = _zlib.compressobj(level=compression_level)
        self.__nwritten = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.flush()

    def encode(self, bindata, order='C'):
        self.__nwritten += self.__ref.write(self.__lib.compress(bindata))
        return len(bindata)

    def flush(self):
        if self.__lib is not None:
            self.__nwritten += self.__ref.write(self.__lib.flush())
            self.__lib = None
        return self.__nwritten

    def __getattr__(self, name):
        if name == 'bytes':
            return self.__nwritten

class Decoder:
    """a binary stream decoder from a bzar archive."""

    def __init__(self, fileref):
        """opens an decoder. it assumes that `fileref` is an opened binary reader,
        at the start of the stream."""
        self.__ref = fileref
        self.__lib = _zlib.decompressobj(memLevel=9)
        self.__buf = b''

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def decode(self, size=1):
        """reads some bytes (specified with `size`) from the archive.
        note that, without any necessary cares, it can overrun into the metadata section."""
        while len(self.__buf) < size:
            self.__buf += self.__lib.decompress(self.__ref.read(1))
        buf, self.__buf = self.__buf[:size], self.__buf[size:]
        return buf

    def close(self, close_file=True):
        """closes the internal decompressor AND the internal file reference, in case close_file is True."""
        if self.__ref is not None:
            self.__lib.flush()
            if close_file == True:
                self.__ref.close()
            self.__ref = None
            self.__lib = None
