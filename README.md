# Userese Writer · Qwen3.8-Flash

这是 Userese 的可选 Writer：宿主负责确认受众、事实、策略和文案范围，本技能通过阿里云百炼调用 `qwen3.8-flash`，只返回待核实的文案提案。

## 安装

```bash
git clone git@github.com:AsherLay/userese-writer-qwen3-8-flash.git ~/.agents/skills/userese-writer-qwen3-8-flash
```

设置 `QWEN_API_KEY` 或 `DASHSCOPE_API_KEY`。本技能不会把密钥写入项目或报告。

## 使用

在 Agent 中明确点名：

```text
使用 $userese-writer-qwen3-8-flash 处理这个已经确认的 Userese brief，只生成提案。
```

本技能兼容 `userese-brief/v1`，不会被 Userese 自动发现或自动选中。源文件修改与生产发布始终需要后续独立批准。完整约束见 [SKILL.md](SKILL.md)。

另一个兼容实现：[userese-writer-gemini3-7-flash](https://github.com/AsherLay/userese-writer-gemini3-7-flash)。
