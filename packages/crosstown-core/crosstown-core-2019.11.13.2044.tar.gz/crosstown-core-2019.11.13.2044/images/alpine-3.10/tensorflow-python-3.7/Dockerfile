# This Dockerfile is auto-generated, don't edit manually!
FROM getcrosstown/builder:python-3.7-alpine-3.10
RUN apk add --no-cache libc6-compat libexecinfo-dev libunwind-dev bash build-base patch perl sed && \
    apk add --no-cache hdf5-dev --repository=http://dl-3.alpinelinux.org/alpine/edge/testing && \
    python -m pip install --no-cache-dir --index-url=https://pkgs.crosstown.dev --extra-index-url=https://pypi.org/simple numpy h5py && \
    git clone https://github.com/tensorflow/tensorflow /tensorflow && \
    cd /tensorflow && \
    git submodule update --init --recursive
WORKDIR /tensorflow
COPY build-wheel.sh *.patch /tensorflow/
