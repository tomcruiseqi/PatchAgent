import json
import os
import urllib.request
from pathlib import Path

for line in (Path.home() / 'secrets.env').read_text().splitlines():
    line = line.removeprefix('export ').strip()
    if '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        os.environ[key.strip()] = value.strip().strip('"\'')

for model, base, env in [
    ('deepseek-flash-cyber', 'https://api.deepseek.com/v1', 'DEEPSEEK_API_KEY'),
    ('deepseek-flash', 'https://api.deepseek.com/v1', 'DEEPSEEK_API_KEY'),
    ('glm-5.3', 'https://api.icompify.com/v1', 'GLM_API_KEY'),
]:
    request = urllib.request.Request(base + '/chat/completions', data=json.dumps({
        'model': model, 'messages': [{'role': 'user', 'content': 'Reply OK'}],
        'max_tokens': 32, 'reasoning_effort': 'low',
    }).encode(), headers={'Authorization': 'Bearer ' + os.environ[env], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = json.load(response)
        print(model, 'ok', body.get('model'), body.get('choices', [{}])[0].get('finish_reason'), flush=True)
    except Exception as error:
        print(model, type(error).__name__, getattr(error, 'code', ''), flush=True)
