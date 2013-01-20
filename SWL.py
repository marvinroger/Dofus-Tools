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
        self._Stream = None
        self._Version = None
        self._FrameRate = None

        self._Classes = None

        self._SWF = None

        self._Template = None

    def Populate(self, stream):
        """
        Populate the class with the SWL stream given
        """
        self._Stream = stream

        SWLFileBinary = BinaryStream(self._Stream, True)

        ByteHeader = SWLFileBinary.readChar()
        if ByteHeader == b"":
            raise SWLInvalidFile("First byte not found.")

        if ByteHeader != 76:
            raise SWLInvalidFile("The first byte doesn't match the SWL pattern.")

        self._Version = SWLFileBinary.readChar()
        self._FrameRate = SWLFileBinary.readUInt32()
        ClassesCount = SWLFileBinary.readInt32()
        if self._Version == b"" or self._FrameRate == b"" or ClassesCount == b"":
            raise SWLInvalidFile("The file doesn't match the SWL pattern.")

        self._Classes = []

        i = 0
        while i < ClassesCount:
            Class = (SWLFileBinary.readString()).decode()
            if Class == b"":
                raise SWLInvalidFile("The file seems corrupted.")
            self._Classes.append(Class)

            i += 1

        self._SWF = SWLFileBinary.readBytes()

    def Build(self, stream):
        """
        Create the SWL represented by the class in the given stream.
        """
        if self._Template is None:
            raise RuntimeError("Template must be defined to build a SWL file")

        SWLFileBuildBinary = BinaryStream(stream, True)

        SWLFileBuildBinary.writeChar(76)

        SWLFileBuildBinary.writeChar(self._Template.Version)
        SWLFileBuildBinary.writeUInt32(self._Template.FrameRate)
        SWLFileBuildBinary.writeInt32(len(self._Template.Classes))

        for Class in self._Template.Classes:
            SWLFileBuildBinary.writeString((Class).encode())

        SWLFileBuildBinary.writeBytes(self._SWF)

    #Accessors

    def _Get_Stream(self):
        return self._Stream

    def _Get_Version(self):
        return self._Version

    def _Get_FrameRate(self):
        return self._FrameRate

    def _Get_Classes(self):
        return self._Classes

    def _Get_SWF(self):
        return self._SWF

    def _Get_Template(self):
        return self._Template

    #Mutators

    def _Set_SWF(self, swf):
        if isinstance(swf, bytes):
            self._SWF = swf
        else:
            raise TypeError("SWF must be a byte object.")

    def _Set_Template(self, template):
        if isinstance(template, SWLFile):
            self._Template = template
        else:
            raise TypeError("Template must be an instance of the SWLFile class.")

    #Properties

    Stream = property(_Get_Stream)
    Version = property(_Get_Version)
    FrameRate = property(_Get_FrameRate)
    Classes = property(_Get_Classes)
    SWF = property(_Get_SWF, _Set_SWF)
    Template = property(_Get_Template, _Set_Template)

if __name__ == "__main__":
    input()