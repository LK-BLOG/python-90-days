# Challenge 01: Git 仓库初始化
# 这个挑战在命令行中完成，此文件仅作为记录模板
#
# 完成后在此记录你的操作步骤：
# 1. git init
# 2. git add .
# 3. git commit -m "..."
# 4. ...

steps = []

def record_step(step: str):
    """记录你完成的步骤"""
    steps.append(step)
    print(f"[{len(steps)}] {step}")

def show_log():
    """展示操作日志"""
    for i, s in enumerate(steps, 1):
        print(f"{i}. {s}")

if __name__ == "__main__":
    record_step("TODO: 在这里记录你的 git 操作步骤")
    show_log()

