\"\"\"python-dotenv使用示例\"\"\"

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env
env_path = Path(__file__).parent.parent / \".env\"
load_dotenv(env_path)

# 基本读取
debug = os.getenv(\"DEBUG\", \"false\").lower() == \"true\"
db_url = os.getenv(\"DATABASE_URL\", \"sqlite:///default.db\")
secret_key = os.getenv(\"SECRET_KEY\", \"change-me\")
port = int(os.getenv(\"PORT\", \"8000\"))

# 带默认值和类型转换
redis_url = os.getenv(\"REDIS_URL\", \"redis://localhost:6379\")
api_keys = os.getenv(\"API_KEYS\", \"\").split(\",\") if os.getenv(\"API_KEYS\") else []

print(f\"Debug: {debug}\")
print(f\"DB URL: {db_url}\")
print(f\"Port: {port}\")
print(f\"Redis: {redis_url}\")
print(f\"API Keys: {api_keys}\")
