#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from BinaryStream import *
else:
    from .BinaryStream import *

#Exceptions

class SWLInvalidFile(Exception):
    def __init__(self, message):
        super(SWLInvalidFile, self).__init__(message)
        self.message = message

#Class itself

class SWLFile:

    def __init__(self):
        self._stream = None
        self._version = None
        self._frame_rate = None

        self._classes = None

        self._SWF = None

        self._template = None

    def populate(self, stream):
        """
        Populate the class with the SWL stream given
        """
        self._stream = stream

        SWL_file_binary = BinaryStream(self._stream, True)

        byte_header = SWL_file_binary.read_char()
        if byte_header == b"":
            raise SWLInvalidFile("First byte not found.")

        if byte_header != 76:
            raise SWLInvalidFile("The first byte don't match the SWL pattern.")

        self._version = SWL_file_binary.read_char()
        self._frame_rate = SWL_file_binary.read_uint32()
        classes_count = SWL_file_binary.read_int32()
        if self._version == b"" or self._frame_rate == b"" or classes_count == b"":
            raise SWLInvalidFile("The file don't match the SWL pattern.")

        self._classes = []

        i = 0
        while i < classes_count:
            class_ = (SWL_file_binary.read_string()).decode()
            if class_ == b"":
                raise SWLInvalidFile("The file appears to be corrupt.")
            self._classes.append(class_)

            i += 1

        self._SWF = SWL_file_binary.read_bytes()

    def build(self, stream):
        """
        Create the SWL represented by the class in the given stream.
        """
        if self._template is None:
            raise RuntimeError("Template must be defined to build a SWL file")

        SWL_file_build_binary = BinaryStream(stream, True)

        SWL_file_build_binary.write_char(76)

        SWL_file_build_binary.write_char(self._template.version)
        SWL_file_build_binary.write_uint32(self._template.frame_rate)
        SWL_file_build_binary.write_int32(len(self._template.classes))

        for class_ in self._template.classes:
            SWL_file_build_binary.write_string((class_).encode())

        SWL_file_build_binary.write_bytes(self._SWF)

    #Accessors

    def _get_stream(self):
        return self._stream

    def _get_version(self):
        return self._version

    def _get_frameRate(self):
        return self._frame_rate

    def _get_classes(self):
        return self._classes

    def _get_SWF(self):
        return self._SWF

    def _get_template(self):
        return self._template

    #Mutators

    def _set_SWF(self, swf):
        if isinstance(swf, bytes):
            self._SWF = swf
        else:
            raise TypeError("SWF must be a byte object.")

    def _set_template(self, template):
        if isinstance(template, SWLFile):
            self._template = template
        else:
            raise TypeError("Template must be an instance of the SWLFile class.")

    #Properties

    stream = property(_get_stream)
    version = property(_het_version)
    frame_rate = property(_get_frame_rate)
    classes = property(_get_classes)
    SWF = property(_get_SWF, _set_SWF)
    template = property(_get_template, _set_template)

if __name__ == "__main__":
    input()