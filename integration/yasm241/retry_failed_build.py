"""Verify that retrying a failed OSS-Fuzz build returns a build error twice."""

import os
from pathlib import Path

from patchagent.builder import OSSFuzzBuilder, OSSFuzzPoC
from patchagent.parser.sanitizer import Sanitizer
from patchagent.task import PatchTask, ValidationResult


case = Path(os.environ.get("YASM_CASE_DIR", Path(__file__).resolve().parent))
bad_patch = (case / "invalid-build.patch").read_text()
builder = OSSFuzzBuilder(
    "yasm241",
    case / "yasm",
    Path(os.environ.get("OSS_FUZZ_PATH", case / "oss-fuzz")),
    [Sanitizer.AddressSanitizer],
    workspace=case / "retry-workspace",
    clean_up=False,
)
if os.environ.get("PATCHAGENT_IMAGE_READY") == "1":
    builder._image_built = True
task = PatchTask([OSSFuzzPoC(case / "poc.asm", "yasm_fuzzer")], builder)
for attempt in range(2):
    status, _ = task.validate(bad_patch)
    print(f"attempt {attempt + 1}: {status.value}", flush=True)
    assert status == ValidationResult.BuildFailed
