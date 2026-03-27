#!/bin/bash

auditwheel repair ./dist/*cp38*.whl  &&
auditwheel repair ./dist/*cp39*.whl  &&
auditwheel repair ./dist/*cp310*.whl &&
auditwheel repair ./dist/*cp311*.whl &&
auditwheel repair ./dist/*cp312*.whl &&
auditwheel repair ./dist/*cp313*.whl
# install the manylinux .whl files for testing
${PIP_PATH_38} install  ./wheelhouse/*cp38*.whl      
${PIP_PATH_39} install  ./wheelhouse/*cp39*.whl      
${PIP_PATH_310} install ./wheelhouse/*cp310*.whl       
${PIP_PATH_311} install ./wheelhouse/*cp311*.whl     
${PIP_PATH_312} install ./wheelhouse/*cp312*.whl     
${PIP_PATH_313} install ./wheelhouse/*cp313*.whl     
# copy manylinux .whl files to local directory
cp ./wheelhouse/*cp38*.whl /myvol                        
cp ./wheelhouse/*cp39*.whl /myvol                   
cp ./wheelhouse/*cp310*.whl /myvol                  
cp ./wheelhouse/*cp311*.whl /myvol                  
cp ./wheelhouse/*cp312*.whl /myvol                  
cp ./wheelhouse/*cp313*.whl /myvol        


# loop over
PYTHON_VERSIONS=("${PY_PATH_38}" "${PY_PATH_39}" "${PY_PATH_310}" "${PY_PATH_311}" "${PY_PATH_312}" "${PY_PATH_313}")
for PYTHON in "${PYTHON_VERSIONS[@]}"; do
    echo "Testing: ${PYTHON}" >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    ${PYTHON} -m lingo_tests >> /myvol/test.txt
    cd examples/CHESS
    ${PYTHON} chess.py >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    cd ../..
    cd examples/Cutting
    ${PYTHON} loopCut.py >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    cd ../..
    cd examples/samsizr
    ${PYTHON} samsizr.py >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    cd ../..
    cd examples/Transport
    ${PYTHON} Transport.py >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    cd ../..
    cd examples/ErrorTest
    ${PYTHON} errorTest.py >> /myvol/test.txt
    echo "=========================================================================================" >> /myvol/test.txt
    cd ../..
done