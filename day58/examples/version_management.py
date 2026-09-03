\"\"\"版本管理\"\"\"

import re
from pathlib import Path


def get_version(init_path: str = \"src/awesome_tool/__init__.py\") -> str:
    content = Path(init_path).read_text()
    match = re.search(r'__version__\\s*=\\s*\"([^\"]+)\"', content)
    if not match:
        raise ValueError(f\"Version not found in {init_path}\")
    return match.group(1)


def bump_version(version: str, bump_type: str = \"patch\") -> str:
    parts = version.split(\".\")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == \"major\":
        return f\"{major + 1}.0.0\"
    elif bump_type == \"minor\":
        return f\"{major}.{minor + 1}.0\"
    elif bump_type == \"patch\":
        return f\"{major}.{minor}.{patch + 1}\"
    else:
        raise ValueError(f\"Unknown bump type: {bump_type}\")


def update_version(init_path: str, new_version: str) -> None:
    content = Path(init_path).read_text()
    content = re.sub(
        r'__version__\\s*=\\s*\"[^\"]+\"',
        f'__version__ = \"{new_version}\"',
        content
    )
    Path(init_path).write_text(content)
    print(f\"Version updated to {new_version}\")


if __name__ == \"__main__\":
    current = \"1.2.3\"
    print(f\"Current: {current}\")
    print(f\"Patch:   {bump_version(current, 'patch')}\")
    print(f\"Minor:   {bump_version(current, 'minor')}\")
    print(f\"Major:   {bump_version(current, 'major')}\")
