# 辅助脚本

## 模型接口预检

[`campaign_probe.py`](campaign_probe.py) 用于补丁生成对比实验前的模型 API 连通性检查，依次向脚本中配置的三个模型发送 `Reply OK` 请求，并输出响应状态。

在 `~/secrets.env` 中配置 `DEEPSEEK_API_KEY` 和 `GLM_API_KEY` 后，从仓库根目录运行：

```bash
python3 scripts/campaign_probe.py
```

脚本使用 Python 标准库，要求 Python 3.9 或更高版本。密钥文件位置基于用户主目录，不受脚本移动影响。运行会向对应服务发送实际 API 请求。
