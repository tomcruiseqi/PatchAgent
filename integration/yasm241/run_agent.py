"""Run the yasm PR 241 case against a local OSS-Fuzz checkout."""

import os
from functools import partial
from pathlib import Path

from langchain_openai import ChatOpenAI

from patchagent.agent.clike import common as clike_common
from patchagent.agent.clike.common import CommonCLikeAgent
from patchagent.agent.generator import agent_generator
from patchagent.agent.utils import construct_chat_llm
from patchagent.builder import OSSFuzzBuilder, OSSFuzzPoC
from patchagent.parser.sanitizer import Sanitizer
from patchagent.task import PatchTask


case = Path(os.environ.get("YASM_CASE_DIR", Path(__file__).resolve().parent))
oss_fuzz_path = Path(os.environ.get("OSS_FUZZ_PATH", case / "oss-fuzz"))
run_name = os.environ.get("PATCHAGENT_RUN_NAME", "agent")
builder = OSSFuzzBuilder(
    "yasm241",
    case / "yasm",
    oss_fuzz_path,
    [Sanitizer.AddressSanitizer],
    workspace=case / f"{run_name}-workspace",
    clean_up=False,
)
if os.environ.get("PATCHAGENT_IMAGE_READY") == "1":
    builder._image_built = True
task = PatchTask(
    [OSSFuzzPoC(case / "poc.asm", "yasm_fuzzer")],
    builder,
    log_file=case / f"{run_name}-log.json",
)
status, report = task.initialize()
print(f"initial status: {status.value}", flush=True)
if status.value != "Bug detected":
    print(report, flush=True)
    raise SystemExit(1)
model_options = {}
if reasoning_effort := os.environ.get("PATCHAGENT_REASONING_EFFORT"):
    model_options["reasoning_effort"] = reasoning_effort
if max_tokens := os.environ.get("PATCHAGENT_MAX_TOKENS"):
    model_options["max_tokens"] = int(max_tokens)
if model_options:
    clike_common.construct_chat_llm = partial(construct_chat_llm, **model_options)
if hint_file := os.environ.get("PATCHAGENT_HINT_FILE"):
    hint = Path(hint_file).read_text().replace("{", "{{").replace("}", "}}")
    clike_common.CLIKE_USER_PROMPT_TEMPLATE += "\n\n" + hint
if os.environ.get("PATCHAGENT_FORCE_VALIDATE") == "1":
    bind_tools = ChatOpenAI.bind_tools

    def require_validate(self, tools, **kwargs):
        return bind_tools(self, tools, tool_choice="validate", **kwargs)

    ChatOpenAI.bind_tools = require_validate
model = os.environ.get("PATCHAGENT_MODEL", "gpt-4o")
if max_iterations := os.environ.get("PATCHAGENT_SINGLE_MAX_ITERATIONS"):
    def single_agent(current_task):
        yield CommonCLikeAgent(
            current_task,
            model=model,
            temperature=0,
            auto_hint=False,
            counterexample_num=0,
            max_iterations=int(max_iterations),
        )

    generator = single_agent
else:
    generator = agent_generator(model=model, fast=os.environ.get("PATCHAGENT_FAST", "0") == "1")
patch = task.repair(generator)
print(f"generated patch: {patch}", flush=True)
if patch:
    (case / f"{run_name}.patch").write_text(patch)
raise SystemExit(0 if patch else 2)
