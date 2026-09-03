\"\"\"构建和发布演示\"\"\"

import subprocess
import sys
from pathlib import Path


def build_package():
    print(\"=== Building package ===\")
    for d in [\"dist\", \"build\"]:
        subprocess.run([sys.executable, \"-c\", f\"import shutil; shutil.rmtree('{d}', ignore_errors=True)\"], check=False)

    result = subprocess.run(
        [sys.executable, \"-m\", \"build\"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f\"Build failed: {result.stderr}\")
        return False
    print(\"Build successful!\")
    return True


def check_package():
    print(\"\\n=== Checking package ===\")
    result = subprocess.run(
        [sys.executable, \"-m\", \"twine\", \"check\", \"dist/*\"],
        capture_output=True, text=True
    )
    print(result.stdout)
    return result.returncode == 0


def list_dist():
    print(\"\\n=== Distribution files ===\")
    for f in Path(\"dist\").glob(\"*\"):
        print(f\"  {f.name} ({f.stat().st_size / 1024:.1f} KB)\")


if __name__ == \"__main__\":
    if build_package():
        check_package()
        list_dist()
