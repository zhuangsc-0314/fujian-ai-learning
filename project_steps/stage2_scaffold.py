"""旧骨架入口兼容层；现在转发到完整参考演示。"""

from project_steps.stage2_reference import run_reference


def preview_lesson(lesson_id: str, title: str, exercise: str) -> int:
    """保留旧签名；参考运行不代替用户独立练习验收。"""
    return run_reference(lesson_id, title)
