# idasm
A Python Assembler Script Tool for IDA Pro based on "patching".

# Overview
This lib is based on famous IDA plugin "patching". But "patching" is not exposing api to python script. Some boring patching works should be automatic. So We need a fantastic lib to help us patching in IDA.

"patching" is an eminent plugin. So we can reuse its code to finish this project.


# Why we need this lib?
- IDA assembler interface is hard to use when we want to do some automatic patches in python script.

# version
This project version will sync with "patching" version.
- v0.1.2

(patching link)[https://github.com/gaasedelen/patching/releases]  

# How to use ?
1. download the repository
2. select the plateform code to your ida script working directory.
3. add the idasm_* directory path to your python system path.
4. import it.
5. Do what you want to do.

# Example
```
import sys
sys.path.append("/the/path/to/idasmxxxx")
import idasm
idasm.patch_address_by_assembly(0xBAAAAAAD, "call 0xdeadbeef")
```

# Authors
- Markus Gaasedelen [@gaasedelen](https://twitter.com/gaasedelen)
- lyciumlee [@lyciumlee](https://github.com/lyciumlee)
