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

import os as _os
import io as _io
import pathlib as _pathlib
from collections import namedtuple as _namedtuple
import warnings as _warnings
import numpy as _np

from . import codec

VERSION_STR = "1.1.0alpha2"

try:
    from os import PathLike as _PathLike
except ImportError:
    _PathLike = str

BzarData     = _namedtuple('BzarData', ('data', 'metadata'))
DEFAULT_KEYS = ('shape', 'arrayorder') + codec.DATA_INFO_KEYS

def _read_exact(fileref, length):
    """returns the exact length of bytes or None"""
    arr = fileref.read(length)
    if len(arr) < length:
        return None
    else:
        return arr

class metadata_dict:
    @staticmethod
    def from_data(data=None, metadata=None, arrayorder='C'):
        """used internally to generate metadata dictionary from the data shape etc.
        and user-supplied metadata dict."""
        if data is None:
            raise ValueError("data cannot be None")
        return metadata_dict.from_dims(dtype=data.dtype, shape=data.shape,
                                        metadata=metadata, arrayorder=arrayorder)

    @staticmethod
    def from_dims(dtype=None, shape=None, metadata=None, arrayorder='C'):
        if (dtype is None) or (shape is None):
            raise ValueError("dtype and shape cannot be None")
        metadict = dict(shape=tuple(shape), arrayorder=arrayorder)
        metadict.update(codec.encode_dtype(dtype))
        if metadata is not None:
            metadict.update(metadata)
        return metadict

def calc_metadata_size(metabin):
    """used internally to calculate the size of the binary metadata dictionary in bytes."""
    if not isinstance(metabin, bytes):
        metabin = codec.encode_metadata_dict(metabin)
    return len(metabin)

def check_suffix(fileref):
    """checks the suffix (extension) of `fileref` and
    add '.bzar' in case of none."""
    if isinstance(fileref, str):
        if len(_os.path.splitext(fileref)[1]) == 0:
            fileref += '.bzar'
    elif isinstance(fileref, bytes):
        if len(_os.path.splitext(fileref)[1]) == 0:
            fileref += b'.bzar'
    elif isinstance(fileref, _PathLike):
        fileref = _pathlib.Path(fileref)
        if len(fileref.suffix) == 0:
            fileref = fileref.with_suffix('.bzar')
    return fileref

def save(fileref, data=None, metadata=None, compression_level=None, order='C'):
    """saves the data/metadata to a file represented by `fileref`."""
    if isinstance(fileref, (str, bytes, _PathLike)):
        fileref = check_suffix(fileref)
        with open(fileref, 'wb') as dest:
            save(dest, data=data, metadata=metadata, order=order)
        return

    # otherwise: assume fileref to be a IOBase
    if not isinstance(data, _np.ndarray):
        data = _np.array(data)
    metadict = metadata_dict.from_data(data=data, metadata=metadata, arrayorder=order)
    metabin  = codec.encode_metadata_dict(metadict)
    metasiz  = calc_metadata_size(metabin)
    databin  = codec.encode_data(data, order, compression_level=compression_level)
    fileref.write(databin)
    fileref.write(metabin)
    fileref.write(codec.encode_metadata_size(metasiz))

def read_data_sizes(fileref):
    """used internally to read the size of the data and the metadata dictionary
    in the file represented by `fileref`. returns a BzarData tuple."""
    if isinstance(fileref, (str, bytes, _PathLike)):
        with open(fileref, 'rb') as src:
            return read_data_sizes(src)

    # otherwise: assume fileref to be a BufferedReader
    if not fileref.seekable():
        raise ValueError(f"the file must be seekable: try reading from a normal file")
    width = codec.METADATA_SIZE_WIDTH
    fileref.seek(-width, _os.SEEK_END)
    metasiz_raw = _read_exact(fileref, width)
    if not metasiz_raw:
        raise codec.BzarDecodeError("failed to read the metadata size")
    metasiz = codec.decode_metadata_size(metasiz_raw)
    endofarray = fileref.seek(-(metasiz + width), _os.SEEK_END)
    datasiz = fileref.tell()
    return BzarData(datasiz, metasiz)

def read_metadata(fileref, complete=False, metadata_size=None):
    """reads and returns the metadta.
    if `complete` is set to True, it returns the non user-supplied metadata (e.g. data shape), too."""
    if isinstance(fileref, (str, bytes, _PathLike)):
        with open(fileref, 'rb') as src:
            return read_metadata(src, complete=complete, metadata_size=metadata_size)

    # otherwise: assume fileref to be a BufferedReader
    if not fileref.seekable():
        raise ValueError(f"the file must be seekable: try writing to a normal file")
    if metadata_size is None:
        _, metadata_size = read_data_sizes(fileref)
    fileref.seek(-(metadata_size + codec.METADATA_SIZE_WIDTH), _os.SEEK_END)
    metadict_raw = _read_exact(fileref, metadata_size)
    if not metadict_raw:
        raise codec.BzarDecodeError("failed to read the metadata dictionary")
    metadict = codec.decode_metadata_dict(metadict_raw)
    if complete == True:
        return metadict
    else:
        return get_user_supplied_metadata(metadict, copy=False)

def get_user_supplied_metadata(metadict, copy=True):
    """retrieves and returns the user-supplied metadata."""
    if copy == True:
        metadict = metadict.copy()
    for key in DEFAULT_KEYS:
        metadict.pop(key)
    return metadict

def load(fileref, with_metadata=False, complete_metadata=False, metadata_dict=None):
    """loads array data from the file represented by `fileref`, and returns it.
    if `with_metadata` is set to True, it returns the metadata, too,
    as a BzarData (data, metadata) tuple."""
    if isinstance(fileref, (str, bytes, _PathLike)):
        with open(fileref, 'rb') as src:
            return load(src, with_metadata=with_metadata,
                            complete_metadata=complete_metadata,
                            metadata_dict=metadata_dict)

    # otherwise: assume fileref to be a BufferedReader
    if not fileref.seekable():
        raise ValueError(f"the file must be seekable: try reading from a normal file")
    datasize, metasize = read_data_sizes(fileref)
    if metadata_dict is None:
        metadata_dict = read_metadata(fileref, complete=True, metadata_size=metasize)
    reshape = False
    if 'shape' not in metadata_dict.keys():
        _warnings.warn("the 'shape' key not found in metadata: a 1-D array is assumed.")
    else:
        reshape = True
    dtype    = codec.decode_data_info(metadata_dict)
    fileref.seek(0)
    data_raw = _read_exact(fileref, datasize)
    if data_raw is None:
        raise codec.BzarDecodeError("failed to read the binary data")
    data = _np.frombuffer(codec.decode_data(data_raw), dtype=dtype)
    if reshape == True:
        data = data.reshape(metadata_dict['shape'])

    if with_metadata == True:
        if complete_metadata == False:
            metadata_dict = get_user_supplied_metadata(metadata_dict)
        return BzarData(data, metadata_dict)
    else:
        return data

class Reader:
    """an object for streaming from a bzar archive.
    it implements the context manager.
    """

    def __init__(self, fileref):

        ## open in case not yet
        opened = False # whether it is internally opened
        if isinstance(fileref, (str, bytes, _PathLike)):
            fileref = open(fileref, 'rb')
            opened  = True

        ## check that it is seekable
        if not fileref.seekable():
            if opened == True:
                fileref.close()
            raise ValueError(f"the file must be seekable: try reading from a normal file")

        ## load metadata
        try:
            self.__datasize, self.__metasize = read_data_sizes(fileref)
            self.__metadata = read_metadata(fileref,
                                            complete=True,
                                            metadata_size=self.__metasize)
            self.__dtype = codec.decode_data_info(self.__metadata)
            self.__order = self.__metadata['arrayorder'].upper()
            self.__shape = tuple(self.__metadata['shape'])
            if len(self.__shape) > 1:
                if self.__order == 'C':
                    self.__length, self.__frame = self.__shape[0], self.__shape[1:]
                else:
                    self.__length, self.__frame = self.__shape[-1], self.__shape[:-1]
                self.__elemsize = _np.prod(self.__frame)
            else:
                self.__elemsize = 1
                self.__length   = self.__shape[0]
            self.__position = 0
            empty = _np.array([], dtype=self.__dtype)
            self.__binsize  = self.__elemsize * empty.itemsize

            fileref.seek(0)
            self.__decoder = codec.Decoder(fileref)
        except:
            if opened == True:
                fileref.close()
            raise

    def close(self):
        if self.__decoder is not None:
            self.__decoder.close()
            self.__decoder = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        return self

    def __next__(self):
        return self.read_frame()

    def __getattr__(self, name):
        if name == 'metadata':
            return self.__metadata.copy()
        elif name == 'dtype':
            return self.__dtype
        elif name == 'shape':
            return self.__shape
        elif name == 'frame':
            return self.__frame

    def read_frame(self, size=1):
        """reads a number of frames from the current position.
        returns a number of `dtype` elements, in case the array is of 1D."""
        if self.__decoder is None:
            raise OSError("file is already closed")
        if (self.__position + size) > self.__length:
            raise StopIteration
        binsize = size * self.__binsize
        arr     = _np.frombuffer(self.__decoder.decode(binsize), dtype=self.__dtype)
        if self.__elemsize > 1:
            if size > 1:
                if self.__order == 'C':
                    arr = arr.reshape((-1,)+self.__frame, order='C')
                else:
                    arr = arr.reshape(self.__frame + (-1,), order='F')
            else:
                arr = arr.reshape(self.__frame, order=self.__order)
        else:
            pass
        self.__position += size
        return arr

class Writer:
    """an object for streaming output into a bzar archive.
    it supports the context manager."""

    def __init__(self, fileref, frame=None, dtype=None, metadata=None, compression_level=None, order='C'):
        ## open in case not yet
        opened = False # whether it is internally opened
        if isinstance(fileref, (str, bytes, _PathLike)):
            fileref = open(fileref, 'wb')
            opened  = True
        ## check that it is seekable
        if not fileref.seekable():
            if opened == True:
                fileref.close()
            raise ValueError(f"the file must be seekable: try writing to a normal file")

        self.__frame    = tuple(frame) if frame is not None else None
        self.__dtype    = dtype
        self.__meta     = metadata
        self.__order    = order

        self.__encoder  = None
        try:
            if order.upper() not in ('F', 'C'):
                raise ValueError(f"unknown array order: {order}")
            self.__order   = order.upper()
            self.__encoder = codec.Encoder(fileref, compression_level=compression_level)
            self.__fileref = fileref
        except:
            if opened == True:
                fileref.close()
            raise
        self.__nwritten = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        if self.__fileref is not None:
            metadict = self._get_metadata_dict()
            metabin  = codec.encode_metadata_dict(metadict)
            metasiz  = calc_metadata_size(metadict)
            self.__fileref.write(metabin)
            self.__fileref.write(codec.encode_metadata_size(metasiz))
            self.__fileref.close()
            self.__fileref = None
            self.__encoder = None

    def _get_metadata_dict(self):
        if self.__nwritten == 0:
            raise RuntimeError("nothing to write")
        self.__encoder.flush()
        shape    = (self.__nwritten,)
        if self.__frame is None:
            pass
        else:
            if self.__order == 'C':
                shape = shape + self.__frame
            else:
                shape = self.__frame + shape
        return metadata_dict.from_dims(dtype=self.__dtype, shape=shape,
                                    metadata=self.__meta, arrayorder=self.__order)

    def write(self, array):
        if self.__encoder is None:
            raise ValueError("encoder is not open")

        if self.__dtype is None:
            self.__dtype = array.dtype
        elif array.dtype != self.__dtype:
            raise ValueError("dtype mismatch")

        size = 1
        if self.__frame is None:
            if array.ndim > 1:
                self.__frame = array.shape
                size = 1
            else:
                array = array.reshape((-1,), order=self.__order)
                size  = array.size
        elif array.ndim > len(self.__frame):
            if self.__order == 'C':
                if array.shape[-len(self.__frame):] != self.__frame:
                    raise ValueError("shape mismatch")
                size = array.shape[0]
            else:
                if array.shape[:len(self.__frame)] != self.__frame:
                    raise ValueError("shape mismatch")
                size = array.shape[-1]

        self.__encoder.encode(array.tobytes(order=self.__order))
        self.__nwritten += size
