# This Dockerfile is auto-generated, don't edit manually!
FROM python:3.8-alpine3.10
ENV PYTHON_VERSION 3.8
ENV JAVA_HOME /usr/lib/jvm/default-jvm
COPY --from=getcrosstown/builder:bazel0.26.1-alpine-3.10 /usr/bin/bazel /usr/bin/bazel-real /usr/bin/
COPY --from=getcrosstown/builder:bazel0.26.1-alpine-3.10 /etc/bazel.bazelrc /etc/
RUN apk update && \
    apk add --no-cache gcc g++ musl-dev python3-dev make cmake git
