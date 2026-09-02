# Userese Writer batch contract

`brief.json` or `batch.json` is UTF-8 JSON implementing `userese-brief/v1`. It contains one shared writing profile and a list of independently traceable copy items. The input and model result are proposal artifacts only: neither records approval or authorizes source changes.

```json
{
  "protocol": "userese-brief/v1",
  "run": {
    "project": "Example product",
    "goal": "让关键流程文案更直接、更面向首次使用者",
    "target_language": "zh-CN",
    "profile_source": "inferred from README and product UI",
    "audience": "第一次配置自动化流程的个人开发者",
    "situations": ["桌面端首次设置", "任务运行失败后恢复"],
    "brand_voice": ["清楚", "克制", "有帮助"],
    "avoid": ["居高临下", "无依据的承诺"],
    "terms": [
      {"concept": "workflow", "preferred": "流程", "avoid": ["工作流"]}
    ],
    "global_constraints": ["不新增产品能力或事实"]
  },
  "items": [
    {
      "id": "copy-001",
      "location": {
        "path": "src/pages/setup.tsx",
        "line": 42,
        "symbol": "SetupEmptyState"
      },
      "purpose": "空状态标题，引导首次创建流程",
      "original": "No workflows yet",
      "context": "标题下方有一个“创建流程”按钮",
      "constraints": ["标题不超过 14 个汉字", "不重复按钮文字"]
    }
  ],
  "excluded": [
    {
      "location": "src/server/errors.ts",
      "reason": "仅写入开发日志，不向用户展示"
    }
  ]
}
```

## Required fields

- `protocol`: `userese-brief/v1` for new batches. Older compatible batches without this marker remain readable.

- `run`: `project`, `goal`, `target_language`, `audience`, `brand_voice`, `terms`, `global_constraints`.
- `items[]`: unique `id`, `location.path`, `purpose`, `original`, `context`, `constraints`.
- `excluded[]` is recommended for global scans because it makes coverage auditable.

Keep `original` byte-for-byte identical to the source. Use `context` for adjacent labels or behavioral facts, not whole components. Record variables such as `{count}`, `{{name}}`, `${value}`, `%s`, markup, Markdown URLs, keyboard shortcuts and hard character limits in `constraints` even though the validation script also checks common forms.

## Optional standalone project profile

`.userese-writer-qwen3-8-flash.json` may contain the same profile fields as `run` when this Writer is used outside Userese:

```json
{
  "audience": "主要受众",
  "situations": ["典型使用场景"],
  "communication_goal": "希望用户理解或完成什么",
  "brand_voice": ["三个左右可执行的特征"],
  "avoid": ["品牌禁忌"],
  "terms": [
    {"concept": "internal concept", "preferred": "用户看到的词", "avoid": []}
  ],
  "global_constraints": []
}
```

Keep long-lived brand facts here. Put one-off campaign or screen requirements in the run manifest.
