Dofus-Tools
=========

Python 3.x modules to interact with Dofus 2.x special files, like SWL/D2P.

Usage
-----

###D2P files

A D2P file contains the resources of the game, like audio, sprites or SWL files.

#####Decompilation

```python
from D2P import *

D2PStream = open("./MyD2PFile.d2p", "rb") #Open the D2P file in binary mode
D2P = D2PFile()
try:
    D2P.Populate(D2PStream) #Populate the D2P object with a D2P file. Must be a stream
    for Name, File in D2P.Files.item():
	pass #Do whatever you want with Name the name of the file and File a ByteArray containing the file
except D2PInvalidFile: #Raised when the D2P file is incorrect
    pass
```

#####Compilation

To build a D2P file, you have to know that D2P files contain some properties that link it to another D2P files. For example, file.d2p contains properties that link it to file_1.d2p. This way, the Dofus parser know that it will need to parse file_1.d2p if it parses file.d2p.
So, in order to build a D2P file, you have to specify the template D2P object that contains the properties.

```python
from D2P import *

D2PTemplateStream = open("./MyD2PFile.d2p", "rb")
D2PTemplate = D2PFile()
D2P.Populate(D2PTemplateStream)

D2PStream = open("./MyCustomD2PFile.d2p", "wb")
D2P = D2PFile()
D2P.Template = D2PTemplate #Specify the template D2P file
D2P.Files = D2PTemplate.Files #Specify the files that will be builded {Filename => ByteArray of your file}
D2P.Build(D2PStream)
```

The above exemple build the same file as the template as it build the same files. D2P builded file will be exactly the same as the original file. (Checksums are same)

###SWL files

A SWL file contains one and only one SWF file. This is a packaged filetype that we can encounter when extracting D2P file.

#####Decompilation

```python
from SWL import *

SWLStream = open("./MySWLFile.swl", "rb") #Open the SWL file in binary mode
SWL = SWLFile()
try:
    SWL.Populate(SWLStream) #Populate the SWL object with a SWL file. Must be a stream
    SWF = SWL.SWF #SWF is a ByteArray containing the SWF file
except SWLInvalidFile: #Raised when the SWL file is incorrect
    pass
```

#####Compilation

To build a SWL file, you have to know that SWL files contain some properties (Version, FrameRate, Classes). The Dofus parser uses these properties to use the SWF file.
So, in order to build a SWL file, you have to specify the template SWL object that contains the properties.

```python
from SWM import *

SWLTemplateStream = open("./MySWLFile.swl", "rb")
SWLTemplate = SWLFile()
SWL.Populate(SWLTemplateStream)

SWLStream = open("./MyCustomSWLFile.swl", "wb")
SWL = SWLFile()
SWL.Template = SWLTemplate #Specify the template SWL file
SWL.SWF = SWLTemplate.SWF #Specify the SWF file that will be builded (ByteArray)
SWL.Build(SWLStream)
```

The above exemple build the same file as the template as it build the same SWF file. SWL builded file will be exactly the same as the original file. (Checksums are same)