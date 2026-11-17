# PatchAgent 三模型补丁生成对比

本结果包位于当前仓库 `results/patchagent-model-comparison-20261117/`，由 192.168.0.230 上的 campaign 结果整理而来，共完成 18 个计分任务：3 个模型分别处理 yasm #241/#242/#243 和 Assimp #5763/#5764/#5765。每个计分任务使用一个 agent、temperature=0、最多 30 次迭代、AddressSanitizer 验证。所有任务的基线初始化状态都是 `Bug detected`。

`SUMMARY.md` 和 `summary.csv` 给出模型汇总及逐案例的补丁结果、交互次数、候选补丁数、工具调用数和 token 数。`interactions` 是 LangChain chat-model callback 计数；SDK/provider 内部重试不会逐次计入。候选补丁尝试数是传给 PatchAgent `validate` 工具的非空补丁数；唯一候选按每次 run 的 SHA-256 去重。工具调用数来自 PatchAgent context 日志。错误的传输尝试保存在 `attempts/`，不计入终局评分；成功重试结果计入最终汇总。

六个原始 PoC 已复制到 `inputs/<case>/`；API 连通性预检日志为 `preflight/model-probe.log`。每个模型/案例的原始 stdout 在 `jobs/<model>/<case>/stdout.log`，完整 PatchAgent 对话和工具结果在 `patchagent.json`，最终补丁在 `final.patch`，每个待验证候选在 `candidate-patches/`。`run.json` 记录状态、输入哈希、模型参数和统计。`models.yaml` 保存安全的模型配置，不含密钥。API 密钥只从 `/home/qzt/secrets.env` 读取，未写入结果。

准备目录没有 yasm #243 的 PoC，因此加入了一个本地最小输入；其 AddressSanitizer 基线复现记录在 `preflight/yasm243-baseline-reproduce.json` 和日志中，输入副本为 `preflight/yasm243-poc.asm`。与 PR #243 描述的 `handle_dot_label` heap out-of-bounds 一致。

为适配远端工具链，运行器加载 bundled libclang 16.0.6，覆盖 PatchAgent `proxy/internal.py` 导入时设置的本机 libclang 路径。Assimp 的 OSS-Fuzz harness 只增加了旧源码构建兼容参数，并跳过当前项目脚本引用、但历史 checkout 中不存在的额外 fuzzer 源文件；Assimp 源码 checkout 本身未修改。具体变更见 `setup-assimp-compat.patch`、修改前后的脚本和 `manifest.json`。

`SHA256SUMS` 列出结果日志、候选、PoC 输入、预检及归档尝试文件的 SHA-256；大型可复用编译工作区未传输。密钥值未包含在结果包中。
