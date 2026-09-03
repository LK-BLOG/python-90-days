"""Git 工作流模拟演示"""

import subprocess
import os
import tempfile
import shutil


def run_git(cmd: str, cwd: str) -> str:
    """执行 git 命令并返回输出"""
    result = subprocess.run(
        f"git {cmd}",
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def demo_git_workflow():
    """演示完整的 Git 工作流"""
    # 创建临时目录作为演示仓库
    tmpdir = tempfile.mkdtemp(prefix="git_demo_")
    print(f"[演示] 创建临时仓库: {tmpdir}")

    try:
        # 初始化
        run_git("init", tmpdir)
        run_git("config user.email demo@example.com", tmpdir)
        run_git("config user.name Demo", tmpdir)

        # 创建文件并首次提交
        readme = os.path.join(tmpdir, "README.md")
        with open(readme, "w") as f:
            f.write("# Demo Project\n")
        run_git("add .", tmpdir)
        run_git('commit -m "feat: 初始化项目"', tmpdir)
        print("[1] 首次提交完成")

        # 创建 feature 分支
        run_git("checkout -b feature/utils", tmpdir)
        utils_file = os.path.join(tmpdir, "utils.py")
        with open(utils_file, "w") as f:
            f.write('def greet(name: str) -> str:\n    return f"Hello, {name}!"\n')
        run_git("add .", tmpdir)
        run_git('commit -m "feat(utils): 添加 greet 函数"', tmpdir)
        print("[2] Feature 分支提交完成")

        # 回到 main，合并
        run_git("checkout main", tmpdir)
        run_git("merge feature/utils --no-ff -m 'Merge feature/utils'", tmpdir)
        print("[3] 合并完成")

        # 查看日志
        log = run_git("log --oneline --graph", tmpdir)
        print(f"\n[Git Log]\n{log}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    demo_git_workflow()
