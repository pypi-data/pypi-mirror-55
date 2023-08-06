#!/bin/sh

set -exo

git fetch origin
git checkout v${CROSSTOWN_PACKAGE_VERSION}

# Add -l option for libexecinfo (backtrace)
sed -ri 's/(Caffe2_DEPENDENCY_LIBS dl)/\1 execinfo/' CMakeLists.txt
sed -ri 's/CMAKE_SHARED_LINKER_FLAGS "-Wl,--no-as-needed"/CMAKE_SHARED_LINKER_FLAGS "-Wl,--no-as-needed,-lexecinfo"/' CMakeLists.txt

# Build the wheel
export PYTORCH_BUILD_VERSION=${CROSSTOWN_PACKAGE_VERSION}
export PYTORCH_BUILD_NUMBER=0
USE_NUMPY=1 BLAS=OpenBLAS EXTRA_CAFFE2_CMAKE_FLAGS="-DBLAS=OpenBLAS" python setup.py bdist_wheel
mkdir -p ${CROSSTOWN_WHEEL_DIR}/torch
cp dist/*.whl ${CROSSTOWN_WHEEL_DIR}/torch/
