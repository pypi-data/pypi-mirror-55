#!/bin/sh

set -exo

git fetch origin
git checkout v${CROSSTOWN_PACKAGE_VERSION}

patch -p1 < tensorflow-${CROSSTOWN_PACKAGE_VERSION}.patch

# Install Keras Applications and Keras Preprocessing
python -m pip install keras-applications keras-preprocessing

# Confgure the build
CC_OPT_FLAGS=-march=native \
PYTHON_BIN_PATH=/usr/local/bin/python \
PYTHON_LIB_PATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages \
TF_NEED_JEMALLOC=1 \
TF_ENABLE_XLA=0 \
TF_NEED_GDR=0 \
TF_NEED_VERBS=0 \
TF_NEED_OPENCL=0 \
TF_NEED_CUDA=0 \
TF_NEED_MPI=0 \
TF_NEED_OPENCL_SYCL=0 \
TF_DOWNLOAD_CLANG=0 \
TF_NEED_ROCM=0 \
TF_SET_ANDROID_WORKSPACE=0 \
bash configure

# Build the wheel
bazel build -c opt --verbose_failures \
  //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package ./dist
mkdir -p ${CROSSTOWN_WHEEL_DIR}/tensorflow
cp dist/* ${CROSSTOWN_WHEEL_DIR}/tensorflow/
