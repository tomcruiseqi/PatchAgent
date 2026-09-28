FROM gcr.io/oss-fuzz-base/base-builder
RUN apt-get update && apt-get install -y --no-install-recommends cmake && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/yasm/yasm.git /src/yasm
COPY build.sh yasm_fuzzer.cc /src/
WORKDIR /src/yasm
