import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from patchagent.builder import OSSFuzzBuilder, OSSFuzzPoC
from patchagent.builder.ossfuzz import OSSFUZZ_DEFAULT_ASAN_OPTIONS
from patchagent.parser.sanitizer import Sanitizer


class TestOSSFuzzBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        (self.root / "source").mkdir()
        (self.root / "source" / "main.c").write_text("int main() { return 0; }\n")
        (self.root / "oss-fuzz").mkdir()
        self.builder = OSSFuzzBuilder(
            "demo",
            self.root / "source",
            self.root / "oss-fuzz",
            [Sanitizer.AddressSanitizer],
            workspace=self.root / "workspace",
        )
        self.poc = OSSFuzzPoC(self.root / "poc", "fuzzer")

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def test_address_replay_disables_leaks_and_keeps_ossfuzz_defaults(self) -> None:
        command = self.builder.reproduce_command(self.poc, Sanitizer.AddressSanitizer)

        env = command[command.index("-e") + 1]
        assert env == f"ASAN_OPTIONS={OSSFUZZ_DEFAULT_ASAN_OPTIONS}:detect_leaks=0"
        for option in ["detect_odr_violation=0", "allocator_may_return_null=1", "alloc_dealloc_mismatch=0", "handle_abort=1"]:
            assert option in env, f"Missing OSS-Fuzz default: {option}"
        assert env.rsplit(":", 1)[-1] == "detect_leaks=0", "detect_leaks=0 must override the default"
        assert command[-2:] == ["--", "-detect_leaks=0"]
        assert command[command.index("demo") : command.index("demo") + 3] == ["demo", "fuzzer", self.poc.path]

    def test_leak_replay_keeps_leak_detection(self) -> None:
        command = self.builder.reproduce_command(self.poc, Sanitizer.LeakAddressSanitizer)

        assert command == ["infra/helper.py", "reproduce", "demo", "fuzzer", self.poc.path]

    def test_unremovable_workspace_is_moved_aside(self) -> None:
        patch = "--- a/main.c\n+++ b/main.c\n"
        workspace = self.builder.workspace / self.builder.hash_patch(Sanitizer.AddressSanitizer, patch)
        (workspace / "oss-fuzz" / "build").mkdir(parents=True)

        with (
            mock.patch("patchagent.builder.ossfuzz.shutil.rmtree", side_effect=PermissionError),
            mock.patch("patchagent.builder.ossfuzz.safe_subprocess_run"),
            mock.patch.object(self.builder, "_build_image"),
        ):
            self.builder._build(Sanitizer.AddressSanitizer, patch)

        assert (workspace / ".prepared").read_text() == patch
        assert (workspace / "source" / "main.c").is_file()
        assert not (workspace / "oss-fuzz" / "build").exists()
        assert len(list(self.builder.workspace.glob(f"{workspace.name}.stale-*"))) == 1


if __name__ == "__main__":
    unittest.main()

# python -m patchagent.tests.test_ossfuzz_builder
