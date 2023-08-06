#!/bin/sh

set -exo

if [ -z ${CROSSTOWN_PACKAGE_VERSION} ]; then
  export PIP_TARGET="${CROSSTOWN_PACKAGE_NAME}"
else
  export PIP_TARGET="${CROSSTOWN_PACKAGE_NAME}==${CROSSTOWN_PACKAGE_VERSION}"
fi

# Build the wheel
mkdir -p ${CROSSTOWN_WHEEL_DIR}/${CROSSTOWN_PACKAGE_NAME}
python -m pip wheel \
  --no-deps \
  --no-binary=${CROSSTOWN_PACKAGE_NAME} \
  --disable-pip-version-check \
  --wheel-dir=${CROSSTOWN_WHEEL_DIR}/${CROSSTOWN_PACKAGE_NAME}/ \
  ${PIP_TARGET}
