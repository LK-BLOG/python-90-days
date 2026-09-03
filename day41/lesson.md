# Day 41 课程：CLI 工具开发

## 第一部分：Typer（推荐）

### 1.1 安装

`ash
pip install typer[all]
`

### 1.2 基础用法

`python
import typer
from typing import Optional

app = typer.Typer(help="我的工具箱")

@app.command()
def hello(name: str, greeting: str = "Hello"):
    typer.echo(f"{greeting}, {name}!")

@app.command()
def add(a: int, b: int):
    typer.echo(f"{a} + {b} = {a + b}")

if __name__ == "__main__":
    app()
# 运行: python cli.py hello World
# 运行: python cli.py add 1 2
`

### 1.3 类型支持

`python
@app.command()
def deploy(
    env: str = typer.Argument(..., help="环境名称"),
    version: str = typer.Option("latest", "--version", "-v"),
    dry_run: bool = typer.Option(False, "--dry-run", "-d"),
    config: Optional[str] = typer.Option(None, "--config", "-c"),
    count: int = typer.Option(1, "--count", "-n", min=1, max=10),
):
    if dry_run:
        typer.echo("Dry run mode")
    typer.echo(f"Deploying {version} to {env}")
`

### 1.4 子命令

`python
app = typer.Typer()
users_app = typer.Typer()
app.add_typer(users_app, name="users")

@app.command()
def init(project_name: str):
    typer.echo(f"Initializing project: {project_name}")

@users_app.command("list")
def list_users():
    typer.echo("Listing users...")

@users_app.command("create")
def create_user(name: str, email: str):
    typer.echo(f"Creating user: {name}")

@users_app.command("delete")
def delete_user(user_id: int):
    typer.echo(f"Deleting user {user_id}")
`

### 1.5 进度条和颜色

`python
import time

@app.command()
def process():
    with typer.progressbar(range(100)) as progress:
        for value in progress:
            time.sleep(0.02)
    typer.secho("Done!", fg=typer.colors.GREEN, bold=True)
`

### 1.6 确认和选择

`python
@app.command()
def delete(user_id: int):
    confirm = typer.confirm(f"Are you sure you want to delete user {user_id}?")
    if not confirm:
        raise typer.Abort()
    typer.echo(f"Deleted user {user_id}")

@app.command()
def select_action():
    action = typer.prompt("Choose action", type=typer.Choice(["create", "update", "delete"]))
    typer.echo(f"You chose: {action}")
`

---

## 第二部分：Click 框架

`python
import click

@click.group()
def cli():
    """My CLI tool"""
    pass

@cli.command()
@click.option("--name", "-n", required=True, help="Your name")
@click.option("--count", default=1, help="Number of greetings")
def hello(name, count):
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@cli.group()
def users():
    """User management"""
    pass

@users.command("list")
def list_users():
    click.echo("Users: Alice, Bob")

@users.command("create")
@click.argument("name")
@click.option("--email", required=True)
def create_user(name, email):
    click.echo(f"Created user: {name} ({email})")

if __name__ == "__main__":
    cli()
`

---

## 第三部分：CLI 测试

`python
from typer.testing import CliRunner
from mycli import app

runner = CliRunner()

def test_hello():
    result = runner.invoke(app, ["hello", "World"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout

def test_add():
    result = runner.invoke(app, ["add", "2", "3"])
    assert "5" in result.stdout
`

---

## 第四部分：打包

`	oml
# pyproject.toml
[project.scripts]
my-tool = "mycli:app"
# 安装后: my-tool hello World
`

## 常见错误
1. 参数类型不对 -> CLI 解析失败
2. 没有 help 信息 -> 用户不知道怎么用
3. 没有错误处理 -> 报错信息不友好

## 动手练习
1. 用 Typer 创建一个文件管理工具
2. 实现子命令系统
3. 添加进度条
4. 编写 CLI 测试
