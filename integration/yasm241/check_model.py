"""Check candidate OpenAI-compatible model aliases without storing the token."""

import os
import sys

from openai import OpenAI


token = sys.stdin.readline().strip()
if not token:
    raise SystemExit("missing token on stdin")
client = OpenAI(base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1"), api_key=token, timeout=45, max_retries=0)
for model in ("deepseek-v4.1-flash",):
    try:
        reply = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply OK."}],
            max_tokens=64,
        )
        choice = reply.choices[0]
        print(model, "status=ok", "finish=", choice.finish_reason, "content=", choice.message.content)
        break
    except Exception as error:
        print(model, "status=error", type(error).__name__, getattr(error, "status_code", None))
