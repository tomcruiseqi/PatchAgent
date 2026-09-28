"""Exercise PatchTask.initialize and PatchTask.validate without an LLM."""

import os
from pathlib import Path

from patchagent.builder import OSSFuzzBuilder, OSSFuzzPoC
from patchagent.parser.sanitizer import Sanitizer
from patchagent.task import PatchTask


case = Path(os.environ.get("YASM_CASE_DIR", Path(__file__).resolve().parent))
sanitizer = Sanitizer(os.environ.get("PATCHAGENT_SANITIZER", "AddressSanitizer"))
task = PatchTask(
    [OSSFuzzPoC(case / "poc.asm", "yasm_fuzzer")],
    OSSFuzzBuilder(
        "yasm241",
        case / "yasm",
        Path(os.environ.get("OSS_FUZZ_PATH", case / "oss-fuzz")),
        [sanitizer],
        workspace=case / "validation-workspace",
        clean_up=False,
    ),
)
before, detail = task.initialize()
print(f"before: {before.value}", flush=True)
print(detail[:500], flush=True)
after, detail = task.validate((case / "pr241.patch").read_text())
print(f"after: {after.value}", flush=True)
print(detail[:1000], flush=True)
