# Challenge 04: 项目重构检查清单
# TODO: 逐项检查你的项目是否满足要求

CHECKLIST = {
    "src_layout": False,       # 使用了 src layout
    "pyproject_toml": False,   # 有 pyproject.toml
    "gitignore": False,        # 有 .gitignore
    "installable": False,      # pip install -e . 可安装
    "conventional_commits": False,  # 使用了 Conventional Commits
    "venv_isolated": False,    # 虚拟环境隔离
}

def check_item(item: str):
    """标记一个检查项"""
    if item in CHECKLIST:
        CHECKLIST[item] = True
        print(f"[OK] {item}")

def show_status():
    """显示检查状态"""
    for item, done in CHECKLIST.items():
        status = "✅" if done else "❌"
        print(f"{status} {item}")
    passed = sum(CHECKLIST.values())
    print(f"\n进度: {passed}/{len(CHECKLIST)}")

if __name__ == "__main__":
    show_status()

