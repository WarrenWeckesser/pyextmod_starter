# Copyright © 2021 Warren Weckesser
# Distributed under the MIT license.

"""
This module defines the function

    def generate_extmod(module_name, module_doc, funcs,
                        c_filename=None, setup_filename="setup.py")

It generates C code for a Python extension module, with boilerplate code
for defining functions with in the extension module that have signatures
like those in the list of functions provided by the `funcs` parameter.
Only the function signatures of the functions in `funcs` are used; the
bodies of the functions are ignored.

`generate_extmod` generates the boilerplate code for the extension module,
but the code will not do anything useful.  The intent is for a developer to
run this once, and then edit the C file to implement whatever the extension
module is supposed to do.

"""

import textwrap
import inspect


def quote_wrap(s):
    return '"' + s + '"'


header = """
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stddef.h>

// Only need stdio.h for the demo code that prints the arguments.
#include <stdio.h>
"""

init_start = """
PyMODINIT_FUNC
PyInit_{module_name}(void)
{{
    PyObject *module;

    module = PyModule_Create(&{module_name}module);
    if (module == NULL) {{
        return NULL;
    }}
"""

init_end = """
    return module;
}
"""

func_start = """
static PyObject *
{func_name}(PyObject *self, PyObject *args, PyObject *kwargs)
{{
"""

func_end = """
    // The demo code returns None; modify as needed.
    Py_RETURN_NONE;
}
"""

methods_table_start = """
static PyMethodDef {module_name}_methods[] = {{
"""

methods_table_entry = """\
    {{"{func_name}", (PyCFunction)(void(*)(void)) {func_name}, METH_VARARGS | METH_KEYWORDS,
     {doc}}},
"""

methods_table_end = """\
    {NULL, NULL, 0, NULL}
};
"""

module_definition_struct = """
static struct PyModuleDef {module_name}module = {{
    PyModuleDef_HEAD_INIT,
    "{module_name}",
    {module_doc},
    -1,
    {module_name}_methods
}};
"""


def _generate_function(func, out):
    sig = inspect.signature(func)
    param_names = list(sig.parameters)
    func_name = func.__name__
    out.write(func_start.format(func_name=func_name))
    # fmt is the format string that will be used in PyArg_ParseTupleAndKeywords
    fmt = ''
    kwlist = []
    has_default = False
    for name, param_type in sig.parameters.items():
        if func.__kwdefaults__ and name in func.__kwdefaults__:
            # Ignore the default value, and use Py_None as the default.
            out.write(f'    PyObject *{name} = Py_None;\n')
            if not has_default:
                has_default = True
                fmt += '|$'
        else:
            out.write(f'    PyObject *{name} = NULL;\n')
        if param_type.kind != param_type.POSITIONAL_ONLY:
            kwlist.append(name)
        else:
            kwlist.append('')
        fmt += 'O'

    fmt += f':{func_name}'
    kwlist_str = ", ".join([quote_wrap(kw) for kw in kwlist])
    param_refs = ", ".join(['&' + kw for kw in param_names])
    out.write(f'    static char *kwlist[] = {{{kwlist_str}, NULL}};\n')
    fmt = quote_wrap(fmt)
    out.write(f'    if (!PyArg_ParseTupleAndKeywords(args, kwargs, {fmt}, kwlist,\n')
    out.write(f'                                     {param_refs})) {{\n')
    out.write('        return NULL;\n')
    out.write('    }\n')
    out.write('\n')
    out.write('    // This demo code just prints the arguments to stdout.\n')
    for param_name in param_names:
        out.write(f'    printf("{param_name}:\\n");\n')
        out.write(f'    PyObject_Print({param_name}, stdout, 0);\n')
        out.write('    printf("\\n");\n')

    out.write(func_end)


def _docstring_literal(doc, name, out):
    if doc is None:
        return 'NULL'
    doc = textwrap.dedent(doc).strip()
    lines = doc.splitlines()
    if len(lines) > 1:
        macro_name = f'{name.upper()}_DOCSTRING'
        out.write(f"\n#define {macro_name} \\\n")
        for line in doc.splitlines():
            out.write(f'"{line}\\n"\\\n')
        out.write('""\n')
        return macro_name
    else:
        return quote_wrap(doc)


def _generate_methods_table(module_name, funcs, out):
    docstrings = []
    for func in funcs:
        docstrings.append(_docstring_literal(func.__doc__, func.__name__, out))

    out.write(methods_table_start.format(module_name=module_name))
    for func, doc in zip(funcs, docstrings):
        func_name = func.__name__
        out.write(methods_table_entry.format(func_name=func_name, doc=doc))
    out.write(methods_table_end)


def _generate_module_definition_struct(module_name, module_doc, out):
    doc = _docstring_literal(module_doc, module_name + "_MODULE", out)
    out.write(module_definition_struct.format(module_name=module_name,
                                              module_doc=doc))


def generate_extmod(module_name, module_doc, funcs,
                    c_filename=None, setup_filename="setup.py"):
    """
    Generate the boilerplate code for a Python extenstion module.

    Parameters
    ----------
    module_name : str
        The extension module name.
    module_doc : str or None
        The docstring for the module.
    funcs : list[callable]
        For each function in ``funcs``, a function with the same name is
        created in the extension module.  The function will parse its arguments
        as objects, and print them to stdout.  (This is just so the module can
        be compiled and tested; the intent is for the user to edit the file
        to do something useful.)
    c_filename : str, optional
        The name of the C file for the extension module.  If not given, the
        name will be generated as ``f"{module_name}module.c".
    setup_filename : str
        The name of the setup script.  The default is `"setup.py"`.
    """
    if not module_name.isidentifier():
        raise ValueError(f"invalid name {module_name!r}; name must be a "
                         "valid identifier.")

    if c_filename is None:
        c_filename = f'{module_name}module.c'

    with open(c_filename, 'w') as out:

        out.write(header)

        if callable(funcs):
            funcs = [funcs]

        for func in funcs:
            _generate_function(func, out)

        _generate_methods_table(module_name, funcs, out)

        _generate_module_definition_struct(module_name, module_doc, out)

        out.write(init_start.format(module_name=module_name))

        out.write(init_end)

    with open(setup_filename, 'w') as setup_out:
        setup_out.write('from distutils.core import setup, Extension\n')
        setup_out.write('\n')
        setup_out.write(f"{module_name} = Extension('{module_name}',\n")
        setup_out.write(f"{' '*len(module_name)}             "
                        f"sources=['{c_filename}'])\n")
        setup_out.write("\n")
        setup_out.write(f"setup(name='{module_name}',\n")
        setup_out.write("      version='0.1',\n")
        setup_out.write(f"      ext_modules=[{module_name}])\n")
