#!/bin/bash
set -euo pipefail

cmake -S /src/yasm -B /work/yasm-build \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_C_COMPILER="$CC" \
  -DCMAKE_C_FLAGS="$CFLAGS -D_GNU_SOURCE" \
  -DCMAKE_EXE_LINKER_FLAGS="$CFLAGS"
# genperf runs during compilation and has unrelated startup leaks.
ASAN_OPTIONS=detect_leaks=0 cmake --build /work/yasm-build -j "$(nproc)"
cp /work/yasm-build/yasm "$OUT/yasm-bin"
"$CXX" $CXXFLAGS /src/yasm_fuzzer.cc "$LIB_FUZZING_ENGINE" -o "$OUT/yasm_fuzzer"
