
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stddef.h>

// Only need stdio.h for the demo code that prints the arguments.
#include <stdio.h>

static PyObject *
process(PyObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *x = NULL;
    PyObject *y = NULL;
    PyObject *z = NULL;
    PyObject *alpha = Py_None;
    PyObject *beta = Py_None;
    static char *kwlist[] = {"", "y", "z", "alpha", "beta", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|$OO:process", kwlist,
                                     &x, &y, &z, &alpha, &beta)) {
        return NULL;
    }

    // This demo code just prints the arguments to stdout.
    printf("x:\n");
    PyObject_Print(x, stdout, 0);
    printf("\n");
    printf("y:\n");
    PyObject_Print(y, stdout, 0);
    printf("\n");
    printf("z:\n");
    PyObject_Print(z, stdout, 0);
    printf("\n");
    printf("alpha:\n");
    PyObject_Print(alpha, stdout, 0);
    printf("\n");
    printf("beta:\n");
    PyObject_Print(beta, stdout, 0);
    printf("\n");

    // The demo code returns None; modify as needed.
    Py_RETURN_NONE;
}

static PyObject *
tabulate(PyObject *self, PyObject *args, PyObject *kwargs)
{
    PyObject *x = NULL;
    static char *kwlist[] = {"x", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O:tabulate", kwlist,
                                     &x)) {
        return NULL;
    }

    // This demo code just prints the arguments to stdout.
    printf("x:\n");
    PyObject_Print(x, stdout, 0);
    printf("\n");

    // The demo code returns None; modify as needed.
    Py_RETURN_NONE;
}

#define PROCESS_DOCSTRING \
"process(x, /, y, *, z, alpha, beta)\n"\
"\n"\
"This is the docstring for process().\n"\
""

static PyMethodDef example_methods[] = {
    {"process", (PyCFunction)(void(*)(void)) process, METH_VARARGS | METH_KEYWORDS,
     PROCESS_DOCSTRING},
    {"tabulate", (PyCFunction)(void(*)(void)) tabulate, METH_VARARGS | METH_KEYWORDS,
     "Docstring for tabulate."},
    {NULL, NULL, 0, NULL}
};

#define EXAMPLE_MODULE_DOCSTRING \
"Docstring for the example module.\n"\
"\n"\
"The module defines the functions process() and tabulate().\n"\
""

static struct PyModuleDef examplemodule = {
    PyModuleDef_HEAD_INIT,
    "example",
    EXAMPLE_MODULE_DOCSTRING,
    -1,
    example_methods
};

PyMODINIT_FUNC
PyInit_example(void)
{
    PyObject *module;

    module = PyModule_Create(&examplemodule);
    if (module == NULL) {
        return NULL;
    }

    return module;
}
