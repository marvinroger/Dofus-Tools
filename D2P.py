#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from BinaryStream import *
else:
    from .BinaryStream import *

from collections import OrderedDict

#Exceptions

class D2PInvalidFile(Exception):
    def __init__(self, message):
        super(D2PInvalidFile, self).__init__(message)
        self.message = message

#Class itself

class D2PFile:

    def __init__(self):
        self._Stream = None

        self._BaseOffset = None
        self._BaseLength = None
        self._IndexesOffset = None
        self._NumberIndexes = None
        self._PropertiesOffset = None
        self._NumberProperties = None

        self._Properties = None

        self._FilesPosition = None

        self._Files = None

        self._Template = None

    def Populate(self, stream):
        """
        Populate the class with the D2P stream given
        """
        self._Stream = stream

        D2PFileBinary = BinaryStream(self._Stream, True)

        BytesHeader = D2PFileBinary.readBytes(2)
        if BytesHeader == b"":
            raise D2PInvalidFile("First bytes not found.")

        if BytesHeader != b"\x02\x01":
            raise D2PInvalidFile("The first bytes doesn't match the SWL pattern.")

        self._Stream.seek(-24, 2) #Set position to end - 24 bytes

        self._BaseOffset = D2PFileBinary.readUInt32()
        self._BaseLength = D2PFileBinary.readUInt32()
        self._IndexesOffset = D2PFileBinary.readUInt32()
        self._NumberIndexes = D2PFileBinary.readUInt32()
        self._PropertiesOffset = D2PFileBinary.readUInt32()
        self._NumberProperties = D2PFileBinary.readUInt32()


        if self._BaseOffset == b"" or self._BaseLength == b"" or self._IndexesOffset == b"" or self._NumberIndexes == b"" or self._PropertiesOffset == b"" or self._NumberProperties == b"":
            raise D2PInvalidFile("The file doesn't match the D2P pattern.")


        self._Stream.seek(self._IndexesOffset, 0)

        #Read indexes

        self._FilesPosition = OrderedDict()

        i = 0
        while i < self._NumberIndexes:
            FileName = (D2PFileBinary.readString()).decode()
            Offset = D2PFileBinary.readInt32()
            Length = D2PFileBinary.readInt32()
            if FileName == b"" or Offset == b"" or Length == b"":
                raise D2PInvalidFile("The file seems corrupted.")
            self._FilesPosition[FileName] = {"Offset" : Offset + self._BaseOffset, "Length" : Length}

            i += 1

        self._Stream.seek(self._PropertiesOffset, 0)

        #Read properties

        self._Properties = OrderedDict()

        i = 0
        while i < self._NumberProperties:
            PropertyType = (D2PFileBinary.readString()).decode()
            PropertyValue = (D2PFileBinary.readString()).decode()
            if PropertyType == b"" or PropertyValue == b"":
                raise D2PInvalidFile("The file seems corrupted.")
            self._Properties[PropertyType] = PropertyValue

            i += 1

        #Populate _Files

        self._Files = OrderedDict()

        for FileName, Position in self._FilesPosition.items():
            self._Stream.seek(Position["Offset"], 0)

            self._Files[FileName] = D2PFileBinary.readBytes(Position["Length"])



    def Build(self, stream):
        """
        Create the D2P represented by the class in the given stream.
        """
        if self._Template is None:
            raise RuntimeError("Template must be defined to build a D2P file")

        D2PFileBuildBinary = BinaryStream(stream, True)

        D2PFileBuildBinary.writeBytes(b"\x02\x01")

        self._BaseOffset = stream.tell()

        for FileName, File in self._Files.items():
            D2PFileBuildBinary.writeBytes(File)

        self._BaseLength = stream.tell() - self._BaseOffset

        self._IndexesOffset = stream.tell()
        self._NumberIndexes = 0

        print(self._FilesPosition.items())

        input()

        for FileName, Position in self._FilesPosition.items():
            D2PFileBuildBinary.writeString(FileName.encode())
            D2PFileBuildBinary.writeInt32(Position["Offset"])
            D2PFileBuildBinary.writeInt32(Position["Length"])
            self._NumberIndexes += 1

        self._PropertiesOffset = stream.tell()
        self._NumberProperties = 0

        for PropertyType, PropertyValue in self._Template._Properties.items():
            D2PFileBuildBinary.writeString(PropertyType.encode())
            D2PFileBuildBinary.writeString(PropertyValue.encode())
            self._NumberProperties += 1

        D2PFileBuildBinary.writeUInt32(self._BaseOffset)
        D2PFileBuildBinary.writeUInt32(self._BaseLength)
        D2PFileBuildBinary.writeUInt32(self._IndexesOffset)
        D2PFileBuildBinary.writeUInt32(self._NumberIndexes)
        D2PFileBuildBinary.writeUInt32(self._PropertiesOffset)
        D2PFileBuildBinary.writeUInt32(self._NumberProperties)

    #Accessors

    def _Get_Stream(self):
        return self._Stream

    def _Get_Properties(self):
        return self._Properties

    def _Get_FilesPosition(self):
        return self._FilesPosition

    def _Get_Files(self):
        return self._Files

    def _Get_Template(self):
        return self._Template

    #Mutators

    def _Set_Properties(self, properties):
        if isinstance(properties, OrderedDict):
            self._Properties = properties
        else:
            raise TypeError("Properties must be a dictionnary of byte object. (Property => Value)")

    def _Set_Files(self, files):
        if isinstance(files, OrderedDict):
            self._Files = files
            self._FilesPosition = OrderedDict()

            #Update positions
            ActualOffset = 0

            for FileName, File in self._Files.items():
                self._FilesPosition[FileName] = {"Offset" : ActualOffset, "Length" : len(File)}
                ActualOffset += self._FilesPosition[FileName]["Length"]
        else:
            raise TypeError("Files must be a dictionnary of byte object. (FileName => Bytes)")

    def _Set_Template(self, template):
        if isinstance(template, D2PFile):
            self._Template = template
        else:
            raise TypeError("Template must be an instance of the D2PFile class.")

    #Properties

    Stream = property(_Get_Stream)
    Properties = property(_Get_Properties, _Set_Properties)
    FilesPosition = property(_Get_FilesPosition)
    Files = property(_Get_Files, _Set_Files)
    Template = property(_Get_Template, _Set_Template)

if __name__ == "__main__":
    input()