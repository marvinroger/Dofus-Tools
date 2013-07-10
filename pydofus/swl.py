#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ._binarystream import _BinaryStream

# Exceptions


class InvalidSWLFile(Exception):
    def __init__(self, message):
        super(InvalidSWLFile, self).__init__(message)
        self.message = message

# Classes


class SWLReader:
    """Read SWL files"""
    def __init__(self, stream):
        """Load the class with the SWL stream given"""
        # Attributes
        self._stream = stream
        self._version = None
        self._frame_rate = None

        self._classes = None

        self._SWF = None

        # Load the SWL
        SWL_file_binary = _BinaryStream(self._stream, True)

        byte_header = SWL_file_binary.read_char()
        if byte_header == b"":
            raise InvalidSWLFile("First byte not found.")

        if byte_header != 76:
            raise InvalidSWLFile("The first byte doesn't match"
                                 " the SWL pattern.")

        self._version = SWL_file_binary.read_char()
        self._frame_rate = SWL_file_binary.read_uint32()
        classes_count = SWL_file_binary.read_int32()
        if ((self._version == b"" or self._frame_rate == b"" or
             classes_count == b"")):
            raise InvalidSWLFile("The file doesn't match the SWL pattern.")

        self._classes = []

        i = 0
        while i < classes_count:
            class_ = (SWL_file_binary.read_string()).decode()
            if class_ == b"":
                raise InvalidSWLFile("The file appears to be corrupt.")
            self._classes.append(class_)

            i += 1

        self._SWF = SWL_file_binary.read_bytes()

    # Accessors

    def _get_stream(self):
        return self._stream

    def _get_version(self):
        return self._version

    def _get_frame_rate(self):
        return self._frame_rate

    def _get_classes(self):
        return self._classes

    def _get_SWF(self):
        return self._SWF

    # Properties

    stream = property(_get_stream)
    version = property(_get_version)
    frame_rate = property(_get_frame_rate)
    classes = property(_get_classes)
    SWF = property(_get_SWF)


class SWLBuilder:
    """Build SWL files"""
    def __init__(self, template, target):
        self._template = template
        self._target = target
        self._SWF = self._template.SWF

    def build(self):
        """Create the SWL represented by the class in the given stream."""
        SWL_file_build_binary = _BinaryStream(self._target, True)

        SWL_file_build_binary.write_char(76)

        SWL_file_build_binary.write_char(self._template.version)
        SWL_file_build_binary.write_uint32(self._template.frame_rate)
        SWL_file_build_binary.write_int32(len(self._template.classes))

        for class_ in self._template.classes:
            SWL_file_build_binary.write_string((class_).encode())

        SWL_file_build_binary.write_bytes(self._SWF)

    # Mutators

    def _set_SWF(self, swf):
        self._SWF = swf

    # Properties

    SWF = property(None, _set_SWF)
