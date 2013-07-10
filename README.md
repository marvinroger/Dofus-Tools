Dofus-Tools [![Build Status](https://travis-ci.org/marvinroger/Dofus-Tools.png)](https://travis-ci.org/marvinroger/Dofus-Tools)
===========

Python 3.x modules to interact with Dofus 2.x special files, like .SWL or .D2P.

Usage
-----

###D2P files

A D2P file contains the resources of the game, like audio, sprites or SWL files.

#####Decompilation

```python
from pydofus.d2p import D2PReader, InvalidD2PFile

stream = open("./samples/sample.d2p", "rb")  # Open the D2P file in binary mode
try:
    D2P = D2PFile(D2P_stream, False)  # Init the D2P object with a D2P file. Must be a stream (Init = get D2P informations, if second parameter is True, load() is called auto)
    D2P.load()  # Populate the D2P object with the actual files in the above given D2P stream. (Load = load files in the D2P in RAM)
    for name, specs in D2P.files.items():
		pass  # Do whatever you want with name the name of the file and specs, which is {position: {offset: <int>, length: <int>}, (if loaded)binary: ByteArray}
except D2PInvalidFile:  # Raised when the D2P file is incorrect
    pass
```

#####Compilation

To build a D2P file, you have to know that D2P files contain some properties that link it to another D2P files. For example, file.d2p contains properties that link it to file_1.d2p. This way, the Dofus parser know that it will need to parse file_1.d2p if it parses file.d2p.
So, in order to build a D2P file, you have to specify the template D2P object that contains the properties.

```python
from pydofus.d2p import D2PReader, D2PBuilder, InvalidD2PFile

template_stream = open("./samples/sample.d2p", "rb")
template = D2PReader(template_stream)  # Second parameter is optional, by default it loads too

builded_stream = open("./sample_compiled.d2p", "wb")
builder = D2PBuilder(template, builded_stream)
#builder.files =  #Specify the files that will be build {Filename => ByteArray of your file, etc}
#Here, we don't do anything so it loads the template files by default
D2P.build()
template_stream.close()
builded_stream.close()
```

The above exemple build the same file as the template as it build the same files. D2P builded file will be exactly the same as the original file. (Checksums are same)

###SWL files

A SWL file contains one and only one SWF file. This is a packaged filetype that we can encounter when extracting D2P file.

#####Decompilation

```python
from pydofus.swl import SWLReader, InvalidSWLFile

stream = open("./samples/sample.swl", "rb") #Open the SWL file in binary mode
SWL = SWLReader()
try:
    SWL = SWLReader(stream) #Populate the SWL object with a SWL file. Must be a stream
    SWF = SWL.SWF #SWF is a ByteArray containing the SWF file
except SWLInvalidFile: #Raised when the SWL file is incorrect
    pass
```

#####Compilation

To build a SWL file, you have to know that SWL files contain some properties (Version, FrameRate, Classes). The Dofus parser uses these properties to use the SWF file.
So, in order to build a SWL file, you have to specify the template SWL object that contains the properties.

```python
from pydofus.swl import SWLReader, SWLBuilder, InvalidSWLFile

template_stream = open("./samples/sample.swl", "rb")
template = SWLReader(template_stream)

builded_stream = open("./sample_compiled.swl", "wb")
builder = SWLBuilder(template, builded_stream)
#builder.SWF =  #Specify the SWF that will be build (<ByteArray>)
#Here, we don't do anything so it loads the template SWF by default
builder.build()
template_stream.close()
builded_stream.close()
```

The above exemple build the same file as the template as it build the same SWF file. SWL builded file will be exactly the same as the original file. (Checksums are same)
