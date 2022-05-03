LSERR_NO_ERROR_LNG                  = 0
LSERR_OUT_OF_MEMORY_LNG             = 1
LSERR_UNABLE_TO_OPEN_LOG_FILE_LNG   = 2
LSERR_INVALID_NULL_POINTER_LNG      = 3
LSERR_INVALID_INPUT_LNG             = 4
LSERR_INFO_NOT_AVAILABLE_LNG        = 5
LSERR_UNABLE_TO_COMPLETE_TASK_LNG   = 6
LSERR_INVALID_LICENSE_KEY_LNG       = 7
LSERR_INVALID_VARIABLE_NAME_LNG     = 8
LSERR_USER_INTERRUPT_LNG            = 73
LSERR_CALLBACK_ERROR_SET            = 1001
LSERR_JNI_CALLBACK_NOT_FOUND        = 1000

ErrorDict = {
    LSERR_OUT_OF_MEMORY_LNG             :"Out of dynamic system memory.",
    LSERR_UNABLE_TO_OPEN_LOG_FILE_LNG   :"Unable to open the log file",
    LSERR_INVALID_NULL_POINTER_LNG      :"A NULL pointer was passed to a routine that was expecting a non-NULL pointer.",
    LSERR_INVALID_INPUT_LNG             :"An input argument contained invalid input.",
    LSERR_INFO_NOT_AVAILABLE_LNG        :"A request was made for information that is not currently available.",
    LSERR_UNABLE_TO_COMPLETE_TASK_LNG   :"Unable to successfully complete the specified task.",
    LSERR_INVALID_LICENSE_KEY_LNG       :"The license key passed to LScreateEnvLicenceLng() was invalid.",
    LSERR_INVALID_VARIABLE_NAME_LNG     :"A variable name passed to LSgetCallbackVarPrimal() was invalid.",
    LSERR_USER_INTERRUPT_LNG            :"A user interrupt occurred.",
    LSERR_CALLBACK_ERROR_SET            :"The error callback function raised an exception.",
    LSERR_JNI_CALLBACK_NOT_FOUND        :"A valid callback function was not found",

}

LS_IINFO_VARIABLES_LNG              = 0
LS_IINFO_VARIABLES_INTEGER_LNG      = 1
LS_IINFO_VARIABLES_NONLINEAR_LNG    = 2
LS_IINFO_CONSTRAINTS_LNG            = 3
LS_IINFO_CONSTRAINTS_NONLINEAR_LNG  = 4
LS_IINFO_NONZEROS_LNG               = 5
LS_IINFO_NONZEROS_NONLINEAR_LNG     = 6
LS_IINFO_ITERATIONS_LNG             = 7
LS_IINFO_BRANCHES_LNG               = 8
LS_DINFO_SUMINF_LNG                 = 9
LS_DINFO_OBJECTIVE_LNG              = 10
LS_DINFO_MIP_BOUND_LNG              = 11
LS_DINFO_MIP_BEST_OBJECTIVE_LNG     = 12

LS_STATUS_GLOBAL_LNG                = 0
LS_STATUS_INFEASIBLE_LNG            = 1
LS_STATUS_UNBOUNDED_LNG             = 2
LS_STATUS_UNDETERMINED_LNG          = 3
LS_STATUS_FEASIBLE_LNG              = 4
LS_STATUS_INFORUNB_LNG              = 5
LS_STATUS_LOCAL_LNG                 = 6
LS_STATUS_LOCAL_INFEASIBLE_LNG      = 7
LS_STATUS_CUTOFF_LNG                = 8
LS_STATUS_NUMERIC_ERROR_LNG         = 9


SET      = 0
PARAM    = 1
VAR      = 2
PtrTypeDict = {0: "SET", 1: "PARAM", 2: "VAR"}