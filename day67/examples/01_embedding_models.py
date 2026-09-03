# -*- coding: utf-8 -*-
MODELS = {
    "text-embedding-3-small": {"dim": 1536, "cost": "$0.02/1M"},
    "text-embedding-3-large": {"dim": 3072, "cost": "$0.13/1M"},
    "all-MiniLM-L6-v2": {"dim": 384, "cost": "免费"},
}
if __name__ == "__main__":
    for n, info in MODELS.items():
        print(f"{n}: {info['dim']}维, {info['cost']}")
