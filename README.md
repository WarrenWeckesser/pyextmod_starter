pyextmod_starter
================

This module defines the function

    def generate_extmod(module_name, module_doc, funcs, numpy=False,
                        c_filename=None, setup_filename="setup.py")

It generates C code for a Python extension module, with boilerplate code
for defining functions in the extension module that have signatures like
those in the list of functions provided by the `funcs` parameter.  Only the
function signatures of the functions in `funcs` are used; the bodies of the
functions are ignored.

`generate_extmod` generates the boilerplate code for the extension module,
but the code will not do anything useful.  The intent is for a developer to
run this once, and then edit the C file to implement whatever the extension
module is supposed to do.

There is an example in the Python file

* [make_example_ext_module.py](https://github.com/WarrenWeckesser/pyextmod_starter/blob/main/examples/make_example_ext_module.py)

in the `examples/` directory.  The result of running that file is the creation
of two files:

* [examplemodule.c](https://github.com/WarrenWeckesser/pyextmod_starter/blob/main/examples/examplemodule.c)
* [setup.py](https://github.com/WarrenWeckesser/pyextmod_starter/blob/main/examples/setup.py)
