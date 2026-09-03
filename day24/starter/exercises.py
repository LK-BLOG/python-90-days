"""
Day 24 练习：工程化基础

请完成以下练习：
1. 创建一个虚拟环境
2. 编写 requirements.txt
3. 配置 pyproject.toml
4. 编写 Makefile
"""

# 练习 1：虚拟环境管理
def create_venv(path=".venv"):
    """创建虚拟环境
    
    TODO: 使用 venv 模块创建虚拟环境
    提示: python -m venv <path>
    """
    pass

def activate_venv_info(path=".venv"):
    """返回虚拟环境激活命令
    
    TODO: 根据操作系统返回正确的激活命令
    Windows: <path>\\Scripts\\activate
    Linux/Mac: source <path>/bin/activate
    """
    pass

# 练习 2：依赖管理
def create_requirements(packages, output_file="requirements.txt"):
    """生成 requirements.txt
    
    TODO: 将包列表写入 requirements.txt，格式为：
    package==version
    """
    pass

def parse_requirements(filepath="requirements.txt"):
    """解析 requirements.txt
    
    TODO: 读取并返回依赖列表
    返回格式: [{"name": "requests", "version": "2.28.1"}, ...]
    """
    pass

def check_missing_packages(requirements_file="requirements.txt"):
    """检查缺失的包
    
    TODO: 对比 requirements.txt 和已安装的包
    返回缺失的包列表
    """
    pass

# 练习 3：项目结构生成
def create_project_structure(project_name, layout="src"):
    """创建标准项目结构
    
    TODO: 根据 layout 类型创建目录结构
    支持 "src" 和 "flat" 两种布局
    
    src layout:
    project_name/
    ├── src/project_name/__init__.py
    ├── tests/__init__.py
    ├── pyproject.toml
    └── README.md
    
    flat layout:
    project_name/
    ├── project_name/__init__.py
    ├── tests/__init__.py
    ├── pyproject.toml
    └── README.md
    """
    pass

# 练习 4：Makefile 生成
def generate_makefile(project_name, targets=None):
    """生成 Makefile
    
    TODO: 生成包含指定 targets 的 Makefile
    默认 targets: install, dev, test, lint, format, clean
    """
    pass

# 练习 5：配置管理
class ConfigManager:
    """配置管理器
    
    TODO: 实现以下功能
    - 从 pyproject.toml 读取配置
    - 支持环境变量覆盖
    - 配置优先级：环境变量 > 文件 > 默认值
    """
    
    def __init__(self, config_file="pyproject.toml", prefix="MYAPP_"):
        self.config_file = config_file
        self.prefix = prefix
        self.defaults = {}
        self.config = {}
    
    def load_defaults(self, defaults):
        """设置默认配置"""
        pass
    
    def load_from_file(self):
        """从 pyproject.toml 加载配置"""
        pass
    
    def load_from_env(self):
        """从环境变量加载配置"""
        pass
    
    def get(self, key, default=None):
        """获取配置值
        
        优先级：环境变量 > 文件 > 默认值
        """
        pass
    
    def set(self, key, value):
        """设置配置值"""
        pass
    
    def all(self):
        """返回所有配置"""
        pass


if __name__ == "__main__":
    # 测试你的代码
    print("Day 24 练习 - Python 工程化")
    
    # 练习 1
    print("\n=== 练习 1：虚拟环境 ===")
    # 测试 create_venv 和 activate_venv_info
    
    # 练习 2
    print("\n=== 练习 2：依赖管理 ===")
    # 测试 create_requirements 和 parse_requirements
    
    # 练习 3
    print("\n=== 练习 3：项目结构 ===")
    # 测试 create_project_structure
    
    # 练习 4
    print("\n=== 练习 4：Makefile ===")
    # 测试 generate_makefile
    
    # 练习 5
    print("\n=== 练习 5：配置管理 ===")
    # 测试 ConfigManager
