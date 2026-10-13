"""明确标记的2026-10-12真实候选回放，不是本次生成。"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def historical_material() -> str:
    return (ROOT / "project_steps/01_01_first_sdk_call/material.txt").read_text(
        encoding="utf-8-sig",
    ).strip()


def historical_result() -> dict:
    return {
        "card": {
            "summary": "省人事考试中心统一命制的《综合基础知识》笔试范围包括政治和经济基本理论、公共管理、法律基础、职业能力、职业道德、科技和人文常识、福建省情等，题型全部为客观题。",
            "keywords": ["综合基础知识", "省人事考试中心", "笔试范围", "客观题", "福建省情"],
            "evidence_quote": "省人事考试中心统一命制的《综合基础知识》笔试范围：政治和经济基本理论、公共管理、法律基础、职业能力、职业道德、科技和人文常识、福建省情等。",
            "information_gap": "原文未说明考试时间、报名条件、分值分布、各科目具体占比或未来考试规则。",
        },
        "source_mode": "historical_replay", "prompt_version": "card_json_v1",
        "usage": None, "attempts": 0,
        "provenance": "2026-10-12助手真实候选；见project_steps/02_02_structured_card/RUN_RESULTS.md",
    }
