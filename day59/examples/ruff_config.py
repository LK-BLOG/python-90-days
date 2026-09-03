\"\"\"ruff配置示例\"\"\"
\"\"\"
# pyproject.toml中的ruff配置

[tool.ruff]
line-length = 88
target-version = \"py310\"

[tool.ruff.lint]
select = [
    \"E\",    # pycodestyle errors
    \"W\",    # pycodestyle warnings
    \"F\",    # pyflakes
    \"I\",    # isort
    \"N\",    # pep8-naming
    \"UP\",   # pyupgrade
    \"B\",    # flake8-bugbear
    \"SIM\",  # flake8-simplify
    \"C4\",   # flake8-comprehensions
    \"DTZ\",  # flake8-datetimez
    \"T20\",  # flake8-print
    \"RET\",  # flake8-return
    \"PT\",   # flake8-pytest-style
    \"RUF\",  # ruff-specific
]
ignore = [\"E501\"]  # 行长度由format处理

[tool.ruff.lint.per-file-ignores]
\"tests/**\" = [\"T20\", \"S101\"]  # 允许print和assert
\"__init__.py\" = [\"F401\"]  # 允许未使用的导入

[tool.ruff.lint.isort]
known-first-party = [\"my_package\"]

[tool.ruff.format]
quote-style = \"double\"
indent-style = \"space\"
skip-magic-trailing-comma = false
line-ending = \"auto\"
\"\"\"
print(\"ruff config documented\")
