"""Простая точка запуска дипломного проекта."""

import subprocess
import sys


if __name__ == "__main__":
    subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
