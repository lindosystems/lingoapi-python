#include "Python.h"
#include "arrayobject.h"
#include "stdlib.h"
#include "stdio.h"
#include "lingd19.h"
#include "string.h"

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject * error_out(PyObject *m) 
{
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

PyObject *pyLScreateEnvLng(PyObject *self, PyObject *args);
PyObject *pyLScreateEnvLicenseLng(PyObject *self, PyObject *args);
PyObject *pyLSclearPointersLng(PyObject *self, PyObject *args);
PyObject *pyLScloseLogFileLng(PyObject *self, PyObject *args);
PyObject *pyLSdeleteEnvLng(PyObject *self, PyObject *args);
PyObject *pyLSexecuteScriptLng(PyObject *self, PyObject *args);
PyObject *pyLSopenLogFileLng(PyObject *self, PyObject *args);
PyObject *pyLSsetIntPointerLng(PyObject *self, PyObject *args);
PyObject *pyLSsetDouPointerLng(PyObject *self, PyObject *args);
PyObject *pyLSsetCharPointerLng(PyObject *self, PyObject *args);

static PyMethodDef lingo_methods[] = 
{
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {"pyLScreateEnvLng", pyLScreateEnvLng, METH_VARARGS},
    {"pyLScreateEnvLicenseLng", pyLScreateEnvLicenseLng, METH_VARARGS},
    {"pyLSclearPointersLng", pyLSclearPointersLng, METH_VARARGS},
    {"pyLScloseLogFileLng", pyLScloseLogFileLng, METH_VARARGS},
    {"pyLSdeleteEnvLng", pyLSdeleteEnvLng, METH_VARARGS},
    {"pyLSexecuteScriptLng", pyLSexecuteScriptLng, METH_VARARGS},
    {"pyLSopenLogFileLng", pyLSopenLogFileLng, METH_VARARGS},
    {"pyLSsetIntPointerLng", pyLSsetIntPointerLng, METH_VARARGS},
    {"pyLSsetDouPointerLng", pyLSsetDouPointerLng, METH_VARARGS},
    {"pyLSsetCharPointerLng", pyLSsetCharPointerLng, METH_VARARGS},

    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int lingo_traverse(PyObject *m, visitproc visit, void *arg) 
{
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int lingo_clear(PyObject *m) 
{
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}

static struct PyModuleDef moduledef = 
{
        PyModuleDef_HEAD_INIT,
        "lingo",
        NULL,
        sizeof(struct module_state),
        lingo_methods,
        NULL,
        lingo_traverse,
        lingo_clear,
        NULL
};

#define INITERROR return NULL

PyObject *PyInit_lingo(void)

#else
#define INITERROR return

void
initlingo(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("lingo", lingo_methods);
#endif

    import_array();  // to initialize NumPy

    if (module == NULL)
    {
        INITERROR;
    }

    {
        struct module_state *st = GETSTATE(module);

        st->error = PyErr_NewException("lingo.Error", NULL, NULL);
        if (st->error == NULL) 
        {
            Py_DECREF(module);
            INITERROR;
        }
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}

#define PyCreatObj(dim,type,pyobj,array) \
dimension[0] = dim;\
pyobj = (PyArrayObject *)PyArray_SimpleNewFromData(1,dimension,type,(void *)(array));\
pyobj->flags |= NPY_OWNDATA;\

#if PY_MAJOR_VERSION < 3
    #define PyNewObjPtr(pointer_to_value)\
    PyCObject_FromVoidPtr ((void *)pointer_to_value, NULL)
#else
    #define PyNewObjPtr(pointer_to_value)\
    PyCapsule_New((void *)pointer_to_value, NULL, NULL)
#endif

#if PY_MAJOR_VERSION < 3
    #define PyGetObjPtr(pointer_to_value)\
    PyCObject_AsVoidPtr(pointer_to_value)
#else
    #define PyGetObjPtr(pointer_to_value)\
    PyCapsule_GetPointer(pointer_to_value, NULL)
#endif

#define CHECK_ENV\
    pEnv = PyGetObjPtr(pyEnv);\
    if(pEnv == NULL)\
    {\
        nErrLng = LSERR_INVALID_NULL_POINTER_LNG;\
        printf("Illegal NULL pointer (error %d)\n",nErrLng);\
        return Py_BuildValue("i",nErrLng);\
    }\

PyObject *pyLScreateEnvLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;

    pEnv = LScreateEnvLng();

    if(!pEnv)
    {
        printf("\nUnable to create LINGO environment object\n");
        return NULL;
    }

    return PyNewObjPtr(pEnv);
}

PyObject *pyLScreateEnvLicenseLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    char           *pachLicenseKey = NULL;
    int            *pnErrorCode = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    npy_intp       index[1] = {0};

    PyArrayObject  *pyErrorCode = NULL, *pyLicenseKey = NULL;

    if (!PyArg_ParseTuple(args, "O!O!", 
                                 &PyArray_Type,&pyLicenseKey,
                                 &PyArray_Type,&pyErrorCode))
    {
        return NULL;
    }

    if(pyErrorCode && pyErrorCode->dimensions > 0)
        pnErrorCode = (int *)PyArray_GetPtr(pyErrorCode,index);

    if(pyLicenseKey)
        pachLicenseKey = (char *)pyLicenseKey->data;

    pEnv = LScreateEnvLicenseLng(pachLicenseKey, &nErrLng);

    *pnErrorCode = nErrLng;

    if(!pEnv)
    {
        printf("\nUnable to create LINGO environment object\n");
        return NULL;
    }

    return PyNewObjPtr(pEnv);
}

PyObject *pyLSclearPointersLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;

    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "O", 
                                 &pyEnv))
    {
        return NULL;
    }

    CHECK_ENV;

    nErrLng = LSclearPointersLng(pEnv);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLScloseLogFileLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;

    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "O", 
                                 &pyEnv))
    {
        return NULL;
    }

    CHECK_ENV;

    nErrLng = LScloseLogFileLng(pEnv);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSdeleteEnvLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;

    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "O", 
                                 &pyEnv))
    {
        return NULL;
    }

    CHECK_ENV;

    nErrLng = LSdeleteEnvLng(pEnv);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSexecuteScriptLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    char           *paScript;

    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "Os", 
                                 &pyEnv,
                                 &paScript))
    {
        return NULL;
    }

    CHECK_ENV;

    nErrLng = LSexecuteScriptLng(pEnv, paScript);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSopenLogFileLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    char           *paLogFile;

    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "Os", 
                                 &pyEnv,
                                 &paLogFile))
    {
        return NULL;
    }

    CHECK_ENV;

    nErrLng = LSopenLogFileLng(pEnv, paLogFile);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSsetIntPointerLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    int            *pnPointer = NULL;
    int            *pnPointersNow = NULL;
    npy_intp       index[1] = {0};

    PyArrayObject  *pyPointer = NULL, *pyPointersNow = NULL;
    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "OO!O!", 
                                 &pyEnv,
                                 &PyArray_Type,&pyPointer,
                                 &PyArray_Type,&pyPointersNow))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyPointer && pyPointer->dimensions > 0)
        pnPointer = (int *)PyArray_GetPtr(pyPointer,index);

    if(pyPointersNow && pyPointersNow->dimensions > 0)
        pnPointersNow = (int *)PyArray_GetPtr(pyPointersNow,index);

    nErrLng = LSsetPointerLng(pEnv, pnPointer, pnPointersNow);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSsetDouPointerLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    double         *pdPointer = NULL;
    int            *pnPointersNow = NULL;
    npy_intp       index[1] = {0};

    PyArrayObject  *pyPointer = NULL, *pyPointersNow = NULL;
    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "OO!O!", 
                                 &pyEnv,
                                 &PyArray_Type,&pyPointer,
                                 &PyArray_Type,&pyPointersNow))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyPointer && pyPointer->dimensions > 0)
        pdPointer = (double *)PyArray_GetPtr(pyPointer,index);

    if(pyPointersNow && pyPointersNow->dimensions > 0)
        pnPointersNow = (int *)PyArray_GetPtr(pyPointersNow,index);

    nErrLng = LSsetPointerLng(pEnv, pdPointer, pnPointersNow);

    return Py_BuildValue("i",nErrLng); 
}

PyObject *pyLSsetCharPointerLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO    pEnv = NULL;
    LSlngErrorCode nErrLng = LSERR_NO_ERROR_LNG;
    char           *paPointer = NULL;
    int            *pnPointersNow = NULL;
    npy_intp       index[1] = {0};

    PyArrayObject  *pyPointer = NULL, *pyPointersNow = NULL;
    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "OO!O!", 
                                 &pyEnv,
                                 &PyArray_Type,&pyPointer,
                                 &PyArray_Type,&pyPointersNow))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyPointer && pyPointer->dimensions > 0)
        paPointer = (char *)PyArray_GetPtr(pyPointer,index);

    if(pyPointersNow && pyPointersNow->dimensions > 0)
        pnPointersNow = (int *)PyArray_GetPtr(pyPointersNow,index);

    nErrLng = LSsetPointerLng(pEnv, paPointer, pnPointersNow);

    return Py_BuildValue("i",nErrLng); 
}