#!/usr/bin/python3
# -*- coding: utf-8 -*-

from struct import *


class _BinaryStream:
    """Allow some binary operations on a stream opened in binary mode"""
    def __init__(self, base_stream, big_endian=False):
        self._base_stream = base_stream
        self._big_endian = big_endian

    # Write functions

    def write_bytes(self, value):
        self._base_stream.write(value)

    def write_char(self, value):
        self._pack('b', value)

    def write_uchar(self, value):
        self._pack('B', value)

    def write_bool(self, value):
        self._pack('?', value)

    def write_int16(self, value):
        self._pack('h', value)

    def write_uint16(self, value):
        self._pack('H', value)

    def write_int32(self, value):
        self._pack('i', value)

    def write_uint32(self, value):
        self._pack('I', value)

    def write_int64(self, value):
        self._pack('q', value)

    def write_uint64(self, value):
        self._pack('Q', value)

    def write_float(self, value):
        self._pack('f', value)

    def write_double(self, value):
        self._pack('d', value)

    def write_string(self, value):
        length = len(value)
        self.write_uint16(length)
        self._pack(str(length) + 's', value)

    def _pack(self, fmt, data):
        if self._big_endian:
            fmt = ">" + fmt
        else:
            fmt = "<" + fmt
        return self.write_bytes(pack(fmt, data))

    # Read functions

    def read_byte(self):
        return self._base_stream.read(1)

    def read_bytes(self, length=None):
        if length is None:
            bytes = self._base_stream.read()
        else:
            bytes = self._base_stream.read(length)
        return bytes

    def read_char(self):
        return self._unpack('b')

    def read_uchar(self):
        return self._unpack('B')

    def read_bool(self):
        return self._unpack('?')

    def read_int16(self):
        return self._unpack('h', 2)

    def read_uint16(self):
        return self._unpack('H', 2)

    def read_int32(self):
        return self._unpack('i', 4)

    def read_uint32(self):
        return self._unpack('I', 4)

    def read_int64(self):
        return self._unpack('q', 8)

    def read_uint64(self):
        return self._unpack('Q', 8)

    def read_float(self):
        return self._unpack('f', 4)

    def read_double(self):
        return self._unpack('d', 8)

    def read_string(self):
        length = self.read_uint16()
        return self._unpack(str(length) + 's', length)

    def _unpack(self, fmt, length=1):
        bytes = self.read_bytes(length)
        if self._big_endian:
            fmt = ">" + fmt
        else:
            fmt = "<" + fmt
        return unpack(fmt, bytes)[0]
