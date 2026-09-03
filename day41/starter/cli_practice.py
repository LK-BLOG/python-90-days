# Day 41 CLI 骨架 - TODO: 用 Typer 实现
import typer

app = typer.Typer(name='mytool', help='我的工具箱')

@app.command()
def init(name: str):
    '''初始化项目'''
    # TODO: 创建项目目录结构
    pass

@app.command()
def build(config: str = 'config.yaml'):
    '''构建项目'''
    # TODO: 读取配置并构建
    pass

@app.command()
def deploy(env: str = 'dev'):
    '''部署项目'''
    # TODO: 部署到指定环境
    pass

if __name__ == '__main__':
    app()
