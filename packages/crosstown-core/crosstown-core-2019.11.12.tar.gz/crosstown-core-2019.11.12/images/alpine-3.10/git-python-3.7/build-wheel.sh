#!/bin/sh

set -exo

# Clone the repository
mkdir /repo
git clone --recurse-submodules -j4 ${CROSSTOWN_GIT_REPO} /repo
cd /repo
git checkout ${CROSSTOWN_GIT_TAG}

# Build the wheel
mkdir -p ${CROSSTOWN_WHEEL_DIR}/${CROSSTOWN_PACKAGE_NAME}
python setup.py bdist_wheel
cp dist/*.whl ${CROSSTOWN_WHEEL_DIR}/${CROSSTOWN_PACKAGE_NAME}/
