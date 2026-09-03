"""示例3：pyproject.toml 解析"""
import tomllib  # Python 3.11+，低版本用 tomli

def parse_pyproject(path="pyproject.toml"):
    """解析 pyproject.toml 文件"""
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
        
        project = data.get("project", {})
        print(f"项目名: {project.get('name')}")
        print(f"版本: {project.get('version')}")
        print(f"描述: {project.get('description')}")
        print(f"Python 版本: {project.get('requires-python')}")
        
        deps = project.get("dependencies", [])
        print(f"依赖数量: {len(deps)}")
        for dep in deps:
            print(f"  - {dep}")
        
        optional = project.get("optional-dependencies", {})
        for group, deps in optional.items():
            print(f"\n可选依赖组 [{group}]:")
            for dep in deps:
                print(f"  - {dep}")
        
        return data
    except FileNotFoundError:
        print(f"文件不存在: {path}")
        return None
    except Exception as e:
        print(f"解析错误: {e}")
        return None

if __name__ == "__main__":
    parse_pyproject()
