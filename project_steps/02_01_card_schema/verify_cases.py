"""核对人工学习卡字段/业务边界；不是模型生成评估或多人权限测试。"""

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from pydantic import ValidationError

import main as lesson


def expect_failure(candidate: dict[str, object], material: str, error_type: type) -> None:
    """指定非法候选必须被拒绝；不回显原始输入。"""
    try:
        lesson.validate_card(candidate, material)
    except error_type:
        return
    raise AssertionError("非法候选未被指定类别拒绝。")


def check_cli(case: str) -> tuple[int, str]:
    """运行实际入口，收集退出码/安全反馈。"""
    output = io.StringIO()
    with redirect_stdout(output), redirect_stderr(output):
        code = lesson.main(["--case", case])
    return code, output.getvalue()


def main() -> int:
    """基础校验通过0；独立字段未实现时--exercise明确返回1。"""
    if sys.argv[1:] not in ([], ["--exercise"]):
        print("仅支持无参数或--exercise。")
        return 2
    with (
        patch("socket.socket.connect", side_effect=AssertionError("离线禁止联网")),
        patch("socket.create_connection", side_effect=AssertionError("离线禁止联网")),
        patch("socket.getaddrinfo", side_effect=AssertionError("离线禁止DNS")),
    ):
        material = lesson.MATERIAL_PATH.read_text(encoding="utf-8-sig").strip()
        normal = lesson.build_candidate("normal")
        card = lesson.validate_card(normal, material)
        assert card.summary == normal["summary"]
        assert card.model_dump()["evidence_quote"] == "题型全部为客观题。"
        count = 1
        missing = normal.copy()
        del missing["summary"]
        expect_failure(missing, material, ValidationError)
        count += 1
        for field, value in (
            ("summary", 123), ("summary", None), ("summary", "   "),
            ("summary", "甲" * 301), ("keywords", "客观题"),
            ("keywords", []), ("keywords", [123]), ("keywords", ["甲"] * 6),
            ("evidence_quote", "   "), ("owner_user_id", "other_user"),
        ):
            candidate = normal.copy()
            candidate[field] = value
            expect_failure(candidate, material, ValidationError)
            count += 1
        for field, value in (("keywords", ["   "]), ("evidence_quote", "不存在的原文。")):
            candidate = normal.copy()
            candidate[field] = value
            expect_failure(candidate, material, ValueError)
            count += 1
        boundary = normal.copy()
        boundary["summary"] = "甲" * 300
        boundary["keywords"] = ["关键词"] * 5
        lesson.validate_card(boundary, material)
        count += 1
        for case, expected in (
            ("normal", 0), ("wrong_type", 2), ("invalid_quote", 2),
            ("unsupported_claim", 0), ("untrusted_text", 0),
        ):
            code, output = check_cli(case)
            assert code == expected and "真实模型请求数：0" in output
            if code == 0:
                assert '"review_status": "pending_manual_review"' in output
                assert f'"owner_user_id": "{lesson.DEMO_OWNER}"' in output
            if case == "unsupported_claim":
                assert "内容不能通过" in output
            if case == "untrusted_text":
                assert "没有执行其命令" in output
            count += 1
        print(f"{count}项基础校验通过；引用存在不等于摘要有据。")
        print("真实模型请求0；人工候选不算AI回答，不验证内容正确或多人隔离。")
        if sys.argv[1:] == ["--exercise"]:
            if "information_gap" not in lesson.LearningCard.model_fields:
                print("独立字段待完成：新增information_gap并补正常人工输入；练习退出1。")
                return 1
            gap = card.model_dump().get("information_gap")
            assert isinstance(gap, str) and gap.strip() and len(gap) <= 200
            invalid = normal.copy()
            del invalid["information_gap"]
            expect_failure(invalid, material, ValidationError)
            for value in ("   ", "甲" * 201, 123):
                invalid = normal.copy()
                invalid["information_gap"] = value
                expect_failure(invalid, material, ValidationError)
            print("5项独立字段练习通过：正常、必填、非空、长度和类型。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
