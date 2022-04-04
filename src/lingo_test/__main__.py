"""
Purpose: Test whether the lingo library 
loads and functions. This is a very simple test that
creates then deletes a Lingo environment.
"""
import lingo_api as lingo

pEnv = lingo.pyLScreateEnvLng()
if pEnv is None:
    e("cannot create LINGO environment!")
    exit(1)

errorcode = lingo.pyLSdeleteEnvLng(pEnv)
if errorcode != lingo.LSERR_NO_ERROR_LNG:
    exit(1)

print("Lingo API is Working.")