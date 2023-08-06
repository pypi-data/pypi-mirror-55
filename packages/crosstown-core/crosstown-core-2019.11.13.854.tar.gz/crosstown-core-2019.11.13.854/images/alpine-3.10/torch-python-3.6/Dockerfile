# This Dockerfile is auto-generated, don't edit manually!
FROM getcrosstown/builder:python-3.6-alpine-3.10
RUN apk add --no-cache openblas-dev libexecinfo-dev linux-headers && \
    python -m pip install --no-cache-dir pyyaml && \
    python -m pip install --no-cache-dir --index-url=https://pkgs.crosstown.dev numpy && \
    git clone https://github.com/pytorch/pytorch /pytorch && \
    cd /pytorch && \
    git submodule update --init --recursive
WORKDIR /pytorch
COPY build-wheel.sh /pytorch
