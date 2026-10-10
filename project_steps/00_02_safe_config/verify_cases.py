"""隔离配置验证：不用真实 Key，不请求模型，不改变根目录 .env。

供你运行后观察错误分类；先读 main.py，本文件的 subprocess 细节可暂缓。
测试使用惰性标记检验配置读取和脱敏，不模拟模型回答或 API 成功。
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_case(env_path: Path, process_values: dict[str, str]) -> subprocess.CompletedProcess:
    """每例启动独立子进程，防止上一例加载的环境变量影响下一例。"""
    environment = os.environ.copy()
    # 只调整测试子进程的副本，不修改你的终端或本机真实配置。
    for name in (
        "DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "DEEPSEEK_API_BASE",
        "PYTHON_DOTENV_DISABLED",
    ):
        environment.pop(name, None)
    environment.update(process_values)
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(Path(__file__).with_name("main.py")), str(env_path)],
        env=environment, capture_output=True, text=True, encoding="utf-8", check=False,
    )


def main() -> int:
    marker = "CONFIG_TEST_MARKER_ONLY_NOT_A_PROVIDER_KEY"
    # 临时文件包含惰性测试数据，退出 with 后自动清理，不使用真实 Key。
    with tempfile.TemporaryDirectory(prefix="langchain-config-check-") as temporary:
        folder = Path(temporary)
        normal = folder / "normal.env"
        normal.write_text(
            f"DEEPSEEK_API_KEY={marker}\nDEEPSEEK_MODEL=learning-model\n",
            encoding="utf-8",
        )
        missing = folder / "missing-key.env"
        missing.write_text("DEEPSEEK_MODEL=learning-model\n", encoding="utf-8")
        blank = folder / "blank-key.env"
        blank.write_text('DEEPSEEK_API_KEY="   "\n', encoding="utf-8")
        untrusted = folder / "untrusted.env"
        # 把其他配置写成同一个标记，检验程序也不打印这些原始值。
        untrusted.write_text(
            f"DEEPSEEK_API_KEY={marker}\nDEEPSEEK_MODEL={marker}\n"
            f"DEEPSEEK_API_BASE={marker}\nIGNORED_TEXT=$(do_not_execute)\n",
            encoding="utf-8",
        )
        # 表中第二列是进程注入值，第三列是预期退出码。
        cases = [
            ("文件配置读取", normal, {}, 0),
            ("缺 Key", missing, {}, 2),
            ("空白 Key", blank, {}, 2),
            ("文件不存在且进程无 Key", folder / "absent.env", {}, 2),
            ("进程 Key 优先于空文件值", blank,
             {"DEEPSEEK_API_KEY": marker, "DEEPSEEK_MODEL": "learning-model"}, 0),
            ("进程空 Key 不被文件覆盖", normal, {"DEEPSEEK_API_KEY": ""}, 2),
            ("不可信配置不回显不执行", untrusted, {}, 0),
        ]
        for name, env_path, process_values, expected in cases:
            result = run_case(env_path, process_values)
            output = result.stdout + result.stderr
            passed = (
                result.returncode == expected
                and marker not in output
                and "$(do_not_execute)" not in output
                and "Traceback" not in output
            )
            if expected == 2:
                passed = passed and "DEEPSEEK_API_KEY" in output
            print(f"{name}：{'通过' if passed else '失败'}，退出码 {result.returncode}")
            if not passed:
                # 不打印失败的完整输出，避免脱敏测试失败时泄漏原始值。
                return 1

        # TODO 验收探针：Key 在进程内注入，文件只改变 MODEL，不动真实 .env。
        for name, contents in (
            ("模型名缺失", ""),
            ("模型名空白", 'DEEPSEEK_MODEL="   "\n'),
        ):
            exercise = folder / "exercise.env"
            exercise.write_text(contents, encoding="utf-8")
            result = run_case(exercise, {"DEEPSEEK_API_KEY": marker})
            output = result.stdout + result.stderr
            if marker in output or "Traceback" in output:
                print(f"{name}：出现泄漏或未知异常，失败。")
                return 1
            if result.returncode == 2 and "DEEPSEEK_MODEL" in output:
                print(f"{name}：独立练习规则通过，退出码 2。")
            elif result.returncode == 0:
                print(f"{name}：当前退出 0；TODO 完成后目标为退出 2。")
            else:
                print(f"{name}：退出码或错误字段不符，需要定位。")
                return 1
    print("已实现规则检查完成；独立练习是否通过看上方探针，不以脚本退出 0 代替。")
    print("真实模型请求数：0；未验证 API Key 有效性。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
