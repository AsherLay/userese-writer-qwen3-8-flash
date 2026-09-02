---
name: userese-writer-qwen3-8-flash
license: MIT
disable-model-invocation: true
description: >-
  Userese 的可选文案 Writer。仅在用户明确点名后，通过阿里云百炼调用 Qwen3.8-Flash，把已确认的 userese-brief/v1 批次写成可核实的 before/after 提案；不重新决定受众、定位或结构，不直接修改产品文件。
  Optional Userese writer. Call Qwen3.8-Flash on a confirmed userese-brief/v1 and return checkable before/after copy. Better for Chinese. Do not run unless the user names this skill.
---

# Userese Writer: Qwen3.8-Flash

本技能只负责“怎么写”。受众、内容方向、事实、范围和结构由宿主或 Userese 在调用前确定。

## 运行边界

- 只有用户明确写出本技能名称时才运行；不要因为检测到它已安装而自动选择。
- 输入必须是用户已确认范围的 `userese-brief/v1` 文件，或符合 [批次协议](references/batch-contract.md) 的 `batch.json`。
- 只生成文案提案。允许写入 `.userese-writer-qwen3-8-flash/runs/<UTC 时间>/`，不得在同一次运行中修改产品源文件。
- 不改变页面结构、信息顺序、产品行为、受众、定位和事实。信息不足时返回 `needs-context`。
- 用户看过具体 before/after 并明确批准后，宿主才能修改指定文案；提交、推送、合并、部署和发布仍需独立授权。

如果没有经过确认的 brief，停止调用并让宿主先使用 Userese 完成知识发现、全量文案清单、范围确认和内容策略。不要让 Qwen 代替这些工作。

## 调用

首次产生费用前，告诉用户模型、文案项数和预计批次数。然后执行：

```bash
python3 <skill-dir>/scripts/invoke.py brief.json result.json --dry-run
python3 <skill-dir>/scripts/invoke.py brief.json result.json
python3 <skill-dir>/scripts/render_report.py brief.json result.json before-after.md
```

脚本调用阿里云百炼的 OpenAI 兼容 `chat/completions` 接口，并使用 `response_format: json_schema`。默认模型为 `qwen3.8-flash`，默认关闭思考以减少额外消耗。用户用英文说话时，按 README 的 English 启动提示回复。

可用配置：

- `--model` 或 `USERESE_WRITER_QWEN_MODEL`
- `--thinking disabled|low|medium|xhigh` 或 `USERESE_WRITER_QWEN_THINKING`
- `--base-url` 或 `USERESE_WRITER_QWEN_BASE_URL`
- `QWEN_API_KEY` 或 `DASHSCOPE_API_KEY`；若当前环境中不存在，再读取 `~/.claude/settings.json` 的 `env`

旧环境变量 `WRITE_QWEN_MODEL`、`WRITE_QWEN_THINKING` 和 `QWEN_BASE_URL` 仍作为兼容回退。任何密钥都不得写进项目、批次、报告或终端输出。

## 核验与交付

宿主逐项检查输出是否保留原意、事实、动作语义、变量、标记、链接、术语和长度约束。缺项、重复 ID、未知 ID 和受保护标记变化都必须处理；无法安全判断时保留原文。

`before-after.md` 必须明确标注：源文件未修改、等待用户核实、未提交、未发布。向用户报告提案数量和警告后停止，等待其批准全部、批准指定 ID、要求调整或放弃。
