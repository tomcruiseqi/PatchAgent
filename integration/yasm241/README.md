# yasm PR #241 OSS-Fuzz reproduction

This fixture exercises yasm commit `721134a8aee87a94f19b53c6dc43a956427973a0` with the null-dereference PoC from [PR #241](https://github.com/yasm/yasm/pull/241). OSS-Fuzz does not include a yasm project, so this directory supplies a local project definition and a small fuzzer that runs yasm as a subprocess. Ordinary assembly syntax errors are accepted; sanitizer reports are returned to libFuzzer.

Set `PATCHAGENT_ROOT` to this checkout and prepare a case directory with yasm, OSS-Fuzz, and the PoC:

```sh
export PATCHAGENT_ROOT=/path/to/PatchAgent
export YASM_CASE_DIR=/path/to/yasm241-case
export OSS_FUZZ_PATH="$YASM_CASE_DIR/oss-fuzz"

git clone https://github.com/yasm/yasm.git "$YASM_CASE_DIR/yasm"
git -C "$YASM_CASE_DIR/yasm" checkout 721134a8aee87a94f19b53c6dc43a956427973a0
git clone --depth 1 https://github.com/google/oss-fuzz.git "$OSS_FUZZ_PATH"
cp -R "$PATCHAGENT_ROOT/integration/yasm241" "$OSS_FUZZ_PATH/projects/yasm241"
curl -L https://github.com/yasm/yasm/pull/241.patch -o "$YASM_CASE_DIR/pr241.patch"
printf %s ZGIgaO4QAHhdCmwAgAAAXQpsYWJlbDE3ClthYjE6ClthYnNvbHV0ZSdsYWJlbDFdCng6 | base64 -d > "$YASM_CASE_DIR/poc.asm"
```

Build the OSS-Fuzz image and fuzzer, then confirm the original null dereference:

```sh
cd "$OSS_FUZZ_PATH"
python3 infra/helper.py build_image --pull yasm241
python3 infra/helper.py build_fuzzers --sanitizer address --clean yasm241 "$YASM_CASE_DIR/yasm"
python3 infra/helper.py check_build --sanitizer address yasm241
python3 infra/helper.py reproduce yasm241 yasm_fuzzer "$YASM_CASE_DIR/poc.asm"
```

`validate_patch.py` exercises `PatchTask.initialize()` and `PatchTask.validate()` with the PR patch. Set `PATCHAGENT_SANITIZER=LeakAddressSanitizer` to verify that explicit leak-detection tasks still report leaks. `retry_failed_build.py` submits a deliberately uncompilable patch twice and checks that both attempts return `Build failed` without a workspace exception.

To run the model-backed agent, install PatchAgent in the Python environment and set `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `PATCHAGENT_MODEL`. For example:

```sh
export OPENAI_API_KEY='your-token'
export OPENAI_BASE_URL='https://your-openai-compatible-endpoint/v1'
export PATCHAGENT_MODEL=deepseek-v4.1-flash
export YASM_CASE_DIR OSS_FUZZ_PATH
python "$PATCHAGENT_ROOT/integration/yasm241/run_agent.py"
```

`run_agent.py` accepts `PATCHAGENT_SINGLE_MAX_ITERATIONS` for a deterministic, temperature-zero run. A completed patch is written to the case directory using `PATCHAGENT_RUN_NAME` as its filename prefix.

The yasm PR #241 case was tested with `deepseek-v4.1-flash` at 30 iterations and temperature 0. The model independently generated a null guard in `libyasm/expr.c`, called `validate`, and the run ended with `Patch is found`. The 15-iteration fast run returned no patch. `model_hint.txt` and `PATCHAGENT_FORCE_VALIDATE=1` support a separate controlled check of the known PR candidate.
