"""
Chạy toàn bộ demo Chương 8 và xuất hình vào figures/.

Chạy: python run_all.py
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = sorted(HERE.glob("0*.py"))


def main():
    print(f"Tìm thấy {len(SCRIPTS)} demo. Bắt đầu chạy...\n")
    for script in SCRIPTS:
        print("=" * 72)
        print(f"CHẠY: {script.name}")
        print("=" * 72)
        subprocess.run([sys.executable, str(script)], cwd=HERE, check=True)
        print()

    print("=" * 72)
    print(f"Xong. Hình đã lưu trong: {HERE / 'figures'}")
    print("=" * 72)


if __name__ == "__main__":
    main()
