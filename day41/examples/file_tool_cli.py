import typer
from typing import Optional

app = typer.Typer(help='文件管理工具')

@app.command()
def info(path: str):
    '''显示文件信息'''
    import os
    if not os.path.exists(path):
        typer.echo(f'File not found: {path}', err=True)
        raise typer.Exit(1)
    size = os.path.getsize(path)
    typer.echo(f'Path: {path}')
    typer.echo(f'Size: {size} bytes')

@app.command()
def search(directory: str, pattern: str, extension: Optional[str] = None):
    '''搜索文件'''
    import glob
    pattern_path = f'{directory}/**/*{pattern}*{extension or ""}'
    files = glob.glob(pattern_path, recursive=True)
    for f in files:
        typer.echo(f)
    typer.echo(f'Found {len(files)} files')

@app.command()
def stats(directory: str):
    '''目录统计'''
    import os
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            total_files += 1
            total_size += os.path.getsize(os.path.join(root, f))
    typer.echo(f'Files: {total_files}')
    typer.echo(f'Total size: {total_size / 1024:.1f} KB')

if __name__ == '__main__':
    app()
