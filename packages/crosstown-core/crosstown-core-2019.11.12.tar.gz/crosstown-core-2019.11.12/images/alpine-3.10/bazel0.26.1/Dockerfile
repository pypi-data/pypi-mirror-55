# This Dockerfile is auto-generated, don't edit manually!
FROM alpine:3.10
ENV BAZEL_VERSION 0.26.1
ENV JAVA_HOME /usr/lib/jvm/default-jvm
RUN mkdir /tmp/bazel && \
    cd /tmp/bazel && \
    apk update && \
    apk add --no-cache bash openjdk8 libarchive wget zip git \unzip coreutils git linux-headers protobuf python3 gcc g++ && \
    ln /usr/bin/python3 /usr/bin/python && \
    wget -q https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-dist.zip && \
    unzip bazel-$BAZEL_VERSION-dist.zip && \
    rm bazel-$BAZEL_VERSION-dist.zip && \
    EXTRA_BAZEL_ARGS=--host_javabase=@local_jdk//:jdk ./compile.sh && \
    output/bazel shutdown && \
    echo startup --server_javabase=$JAVA_HOME >> scripts/packages/bazel.bazelrc && \
    install -Dm755 scripts/packages/bazel.sh /usr/bin/bazel && \
    install -Dm755 scripts/packages/bazel.bazelrc /etc/bazel.bazelrc && \
    install -Dm755 output/bazel /usr/bin/bazel-real && \
    cd / && \
    rm -rf /tmp/bazel
