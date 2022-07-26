#include "Python.h"
#include "arrayobject.h"
#include "stdlib.h"
#include "stdbool.h"
#include "stdio.h"
#include "lingd20.h"
#include "string.h"

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

struct module_state {
    PyObject *error;
};

#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))




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
PyObject *pyLSsetCallbackSolverLng(PyObject *self, PyObject *args);
PyObject *pyLSgetDouCallbackInfoLng(PyObject *self, PyObject *args);
PyObject *pyLSgetIntCallbackInfoLng(PyObject *self, PyObject *args);
PyObject *pyLSgetCallbackVarPrimalLng(PyObject *self, PyObject *args);
PyObject *pyLSsetCallbackErrorLng(PyObject *self, PyObject *args);

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
    {"pyLSsetCallbackSolverLng", pyLSsetCallbackSolverLng, METH_VARARGS},
    {"pyLSgetDouCallbackInfoLng", pyLSgetDouCallbackInfoLng, METH_VARARGS},
    {"pyLSgetIntCallbackInfoLng", pyLSgetIntCallbackInfoLng, METH_VARARGS},
    {"pyLSgetCallbackVarPrimalLng", pyLSgetCallbackVarPrimalLng, METH_VARARGS},
    {"pyLSsetCallbackErrorLng", pyLSsetCallbackErrorLng, METH_VARARGS},

    {NULL, NULL}
};

/*New Exceptions*/
static PyObject *InterruptionError;
/* PyObjects for Callbacks*/
static PyObject *cbpyEnv   = NULL;
static PyObject *cbSolver  = NULL;
static PyObject *cbError   = NULL;
static PyObject *cbuData   = NULL;
static bool usr_interrupt = false;
static bool cbError_set   = false;

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





PyMODINIT_FUNC
PyInit_lingo(void){

    PyObject *module = PyModule_Create(&moduledef);


    import_array();  // to initialize NumPy

    if (module == NULL)
    {
         return NULL;
    }

    {
        struct module_state *st = GETSTATE(module);

        st->error = PyErr_NewException("lingo.Error", NULL, NULL);
        if (st->error == NULL) 
        {
            Py_DECREF(module);
             return NULL;
        }

    }

    return module;

}

#define PyCreatObj(dim,type,pyobj,array) \
dimension[0] = dim;\
pyobj = (PyArrayObject *)PyArray_SimpleNewFromData(1,dimension,type,(void *)(array));\
pyobj->flags |= NPY_OWNDATA;\


#define PyNewObjPtr(pointer_to_value)\
PyCapsule_New((void *)pointer_to_value, NULL, NULL)



#define PyGetObjPtr(pointer_to_value)\
PyCapsule_GetPointer(pointer_to_value, NULL)


#define CHECK_ENV\
    pEnv = PyGetObjPtr(pyEnv);\
    if(pEnv == NULL)\
    {\
        nErrLng = LSERR_INVALID_NULL_POINTER_LNG;\
        printf("Illegal NULL pointer (error %d)\n",nErrLng);\
        return Py_BuildValue("i",nErrLng);\
    }\

#define Reset_CB_Flags\
    usr_interrupt = false;\
    cbError_set   = false;\

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

    if(usr_interrupt){
        PyErr_Clear();
        nErrLng = 73;
        Reset_CB_Flags;

    }
    if(cbError_set){
        PyErr_Clear();
        nErrLng = 1001;
        Reset_CB_Flags;
    }

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

    PyArrayObject *pyPointer = NULL, *pyPointersNow = NULL;
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




int CALLTYPE relayCallbackSolver(pLSenvLINGO pL, int nReserved, void *pUserData)
{
    int retvalue = 0;
    PyObject *arglist = NULL;
    PyObject *result = NULL;

    {
        // Build up the argument list...
        arglist = Py_BuildValue("(OiO)", cbpyEnv, nReserved, cbuData);
        // ...for calling the Python cb function
        if (arglist)
            result = PyEval_CallObject(cbSolver, arglist);
    }
    if (result && PyLong_Check(result)) 
    {
        retvalue = PyLong_AsLong(result);
    }
    {
        Py_XDECREF(result);
        Py_DECREF(arglist);
    }
    if (retvalue == -1){
        usr_interrupt = true;
    }
    return retvalue;
}


PyObject *pyLSsetCallbackSolverLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO     pEnv     = NULL;
    LSlngErrorCode  nErrLng  = LSERR_NO_ERROR_LNG;
    PyObject       *newCb    = NULL;
    PyObject       *newUData = NULL;
    PyObject       *pyEnv;


    if (PyArg_ParseTuple(args, "OOO", &pyEnv, &newCb, &newUData))
    {
        if (!PyCallable_Check(newCb)) 
        {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }

            CHECK_ENV;

            Py_XINCREF(newCb);     /* Add a reference to new callback */
            Py_XDECREF(cbSolver);   /* Dispose of previous callback */
            cbSolver = newCb;      /* Remember new callback */

            Py_XINCREF(newUData);  
            Py_XDECREF(cbuData);      
            cbuData = newUData;       

            Py_XINCREF(pyEnv);   
            Py_XDECREF(cbpyEnv);      
            cbpyEnv = pyEnv;      

        nErrLng = LSsetCallbackSolverLng(pEnv, relayCallbackSolver, NULL);
        }

    return Py_BuildValue("i",nErrLng); 
}

void CALLTYPE relayCallbackError(pLSenvLINGO pL, void *pUserData, int nErrorCode, char *pcErrorText)
{
    PyObject *arglist = NULL;
    PyObject *result = NULL;

    {
        // Build up the argument list...
        arglist = Py_BuildValue("(OOis)", cbpyEnv, cbuData, nErrorCode, pcErrorText);
        // ...for calling the Python cb function
        if (arglist)
            result = PyEval_CallObject(cbError, arglist);
    }
    if(PyErr_Occurred()){
        cbError_set = true;
    }
    {
        Py_XDECREF(result);
        Py_DECREF(arglist);
    }



}

PyObject *pyLSsetCallbackErrorLng(PyObject *self, PyObject *args)
{

    pLSenvLINGO     pEnv     = NULL;
    LSlngErrorCode  nErrLng  = LSERR_NO_ERROR_LNG;
    PyObject       *newCbError    = NULL;
    PyObject       *newUData = NULL;
    PyObject       *pyEnv;


    if (PyArg_ParseTuple(args, "OOO", &pyEnv, &newCbError, &newUData))
    {
        if (!PyCallable_Check(newCbError)) 
        {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
            CHECK_ENV;


            Py_XINCREF(newCbError);     /* Add a reference to new callback */
            Py_XDECREF(cbError);        /* Dispose of previous callback    */
            cbError = newCbError;       /* Remember new callback           */

            Py_XINCREF(newUData);  
            Py_XDECREF(cbuData);      
            cbuData = newUData;       

            Py_XINCREF(pyEnv);   
            Py_XDECREF(cbpyEnv);      
            cbpyEnv = pyEnv;      

        nErrLng = LSsetCallbackErrorLng(pEnv, relayCallbackError, NULL);

        }

    return Py_BuildValue("i",nErrLng); 

}


PyObject *pyLSgetDouCallbackInfoLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO     pEnv     = NULL;
    LSlngErrorCode  nErrLng  = LSERR_NO_ERROR_LNG;
    int             nObject;
    PyArrayObject  *pyResults = NULL;
    void         *pdResults = NULL;
    npy_intp        index[1] = {0};
    PyObject     *pyEnv;


    if (!PyArg_ParseTuple(args, "OiO!", 
                                 &pyEnv,
                                 &nObject,
                                 &PyArray_Type,&pyResults))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyResults && pyResults->dimensions > 0)
        pdResults = (void *)PyArray_GetPtr(pyResults,index);   

     nErrLng = LSgetCallbackInfoLng(pEnv, nObject, pdResults);


    return Py_BuildValue("i",nErrLng);
}


PyObject *pyLSgetIntCallbackInfoLng(PyObject *self, PyObject *args)
{
    pLSenvLINGO     pEnv      = NULL;
    LSlngErrorCode  nErrLng   = LSERR_NO_ERROR_LNG;
    int             nObject;
    PyArrayObject  *pyResults = NULL;
    void            *piResults = NULL;
    npy_intp        index[1]  = {0};
    PyObject       *pyEnv;


    if (!PyArg_ParseTuple(args, "OiO!", 
                                 &pyEnv,
                                 &nObject,
                                 &PyArray_Type,&pyResults))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyResults && pyResults->dimensions > 0)
        piResults = (void *)PyArray_GetPtr(pyResults,index);   

     nErrLng = LSgetCallbackInfoLng(pEnv, nObject, piResults);


    return Py_BuildValue("i",nErrLng);
}


// LSgetCallbackVarPrimalLng( pLSenvLINGO pL, const char* pcVarName, 
//  double* pdPrimal);

 PyObject *pyLSgetCallbackVarPrimalLng(PyObject *self, PyObject *args)
 {
    pLSenvLINGO     pEnv      = NULL;
    LSlngErrorCode  nErrLng   = LSERR_NO_ERROR_LNG;
    char           *paPointer = NULL;
    double         *pdPointer = NULL;
    npy_intp        index[1]  = {0};

    PyArrayObject *pyCharPointer = NULL;
    PyArrayObject *pyDouPointer  = NULL;
    PyObject       *pyEnv;

    if (!PyArg_ParseTuple(args, "OO!O!", 
                                 &pyEnv,
                                 &PyArray_Type,&pyCharPointer,
                                 &PyArray_Type,&pyDouPointer))
    {
        return NULL;
    }

    CHECK_ENV;

    if(pyCharPointer && pyCharPointer->dimensions > 0)
        paPointer = (char *)PyArray_GetPtr(pyCharPointer,index);   

    if(pyDouPointer && pyDouPointer->dimensions > 0)
        pdPointer = (double *)PyArray_GetPtr(pyDouPointer,index);   


     nErrLng = LSgetCallbackVarPrimalLng(pEnv, paPointer, pdPointer);

     return Py_BuildValue("i",nErrLng);
 }



