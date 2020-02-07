#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include "sonic.h"

#define ACTIVE_SENSORS 7

static PyObject*
sonar_read(PyObject* self, PyObject* args);

static PyObject*
sonar_read_all(PyObject* self, PyObject* args);

static PyMethodDef
SonarMethods[] = {
    {"read", sonar_read, METH_VARARGS, "Read a sensor"},
    {"read_all", sonar_read_all, METH_VARARGS, "Read all sensors"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef
sonarmodule = {
    PyModuleDef_HEAD_INIT,
    "sonar",
    NULL,
    -1,
    SonarMethods
};

PyMODINIT_FUNC
PyInit_sonar(void)
{
    PyObject* m;

    m = PyModule_Create(&sonarmodule);
    if(NULL == m)
    {
        return NULL;
    }

    PyModule_AddIntConstant(m, "LEFT", 0);
    PyModule_AddIntConstant(m, "LEFT45 ", 1);
    PyModule_AddIntConstant(m, "LEFT_FRONT ", 2);
    PyModule_AddIntConstant(m, "RIGHT_FRONT ", 3);
    PyModule_AddIntConstant(m, "RIGHT45", 4);
    PyModule_AddIntConstant(m, "RIGHT", 5);
    PyModule_AddIntConstant(m, "BACK", 6);

    initialize();

    return m;
}

PyObject*
sonar_read(PyObject* self, PyObject* args)
{
    int port = 0;

    if(!PyArg_ParseTuple(args, "i", &port))
    {
        // TODO: no port given -> exception
        return NULL;
    }

    double result = measure(port);
    if(0.0 == result)
    {
        return Py_None;
    }
    return PyLong_FromDouble(result);
}

PyObject*
sonar_read_all(PyObject* self, PyObject* args)
{
    PyObject* result = PyList_New(ACTIVE_SENSORS);

    for(int i = 0; i < ACTIVE_SENSORS; i++)
    {
        PyObject* subargs = Py_BuildValue("i", i);
        PyList_SetItem(result, i, sonar_read(self, subargs));
    }

    return result;
}
