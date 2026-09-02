#!/usr/bin/env python3
"""Render a human-reviewable before/after Markdown report."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def fence(text: str) -> str:
    longest = 0
    current = 0
    for char in text:
        if char == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    marker = "`" * max(3, longest + 1)
    return f"{marker}text\n{text}\n{marker}"


def location_label(location: dict[str, Any]) -> str:
    label = str(location.get("path", "unknown"))
    if location.get("line") is not None:
        label += f":{location['line']}"
    if location.get("symbol"):
        label += f" · {location['symbol']}"
    return label


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("result", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    try:
        manifest = read_object(args.manifest)
        result = read_object(args.result)
        run = manifest["run"]
        source_items = manifest["items"]
        result_items = result.get("items", [])
        result_by_id = {
            item.get("id"): item for item in result_items if isinstance(item, dict) and item.get("id")
        }
        warnings_by_id: dict[str, list[str]] = defaultdict(list)
        validation = result.get("validation", {})
        for warning in validation.get("warnings", []):
            item_id = str(warning).split(":", 1)[0]
            warnings_by_id[item_id].append(str(warning))

        lines = [
            f"# 文案改写提案：{run.get('project', 'Untitled project')}",
            "",
            "> 本文档仅供核实。生成本提案时未修改产品源文件，也未提交或发布。",
            "",
            "## 运行摘要",
            "",
            f"- 目标：{run.get('goal', '')}",
            f"- 目标语言：{run.get('target_language', '')}",
            f"- 受众：{run.get('audience', '')}",
            f"- 调性：{'、'.join(map(str, run.get('brand_voice', []))) or '未配置'}",
            f"- 画像来源：{run.get('profile_source', '未记录')}",
            f"- 模型：{result.get('model', 'unknown')}（thinking: {result.get('thinking', 'unknown')}）",
            f"- 文案项：{len(source_items)}；API 批次：{result.get('batch_count', 'unknown')}",
            f"- 用量：`{json.dumps(result.get('usage', {}), ensure_ascii=False)}`",
            "",
            "## 审批与实施状态",
            "",
            "- 提案：等待用户核实",
            "- 产品源文件：未修改",
            "- 代码提交与推送：未执行",
            "- 生产部署与发布：未执行",
            "",
        ]

        excluded = manifest.get("excluded", [])
        if excluded:
            lines.extend(["## 已检查但排除", ""])
            for entry in excluded:
                lines.append(f"- `{entry.get('location', 'unknown')}`：{entry.get('reason', '')}")
            lines.append("")

        errors = validation.get("errors", [])
        all_warnings = validation.get("warnings", [])
        lines.extend(["## 校验", ""])
        if not errors and not all_warnings:
            lines.append("未发现结构或受保护标记异常。")
        else:
            for error in errors:
                lines.append(f"- 错误：{error}")
            for warning in all_warnings:
                lines.append(f"- 警告：{warning}")
        lines.extend(["", "## Before / After", ""])

        for source in source_items:
            item_id = source["id"]
            rewritten = result_by_id.get(item_id)
            lines.extend(
                [
                    f"### {item_id} · {location_label(source['location'])}",
                    "",
                    f"用途：{source.get('purpose', '')}",
                    "",
                    "Before",
                    "",
                    fence(source.get("original", "")),
                    "",
                    "Proposed After",
                    "",
                ]
            )
            if rewritten:
                lines.extend(
                    [
                        fence(str(rewritten.get("rewrite", ""))),
                        "",
                        f"- 决策：`{rewritten.get('decision', 'unknown')}`",
                        f"- 说明：{rewritten.get('rationale', '')}",
                    ]
                )
            else:
                lines.extend(["_缺少模型结果_", "", "- 决策：`missing`"])
            for warning in warnings_by_id.get(item_id, []):
                lines.append(f"- 校验警告：{warning}")
            lines.append("")

        lines.extend(
            [
                "## 核实后的选择",
                "",
                "请明确回复以下一种决定：批准全部、批准指定 ID、要求修改指定 ID，或放弃本次提案。",
                "批准修改工作区不包含提交、推送、合并、部署或发布；生产动作需要查看实际差异后另行授权。",
                "",
            ]
        )

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"Wrote report -> {args.output}")
        return 0
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
