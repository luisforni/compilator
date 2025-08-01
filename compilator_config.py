from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

dir_name = os.getenv("DIR", "default")

CONFIG = {
    "source_dir": str(Path("..") / dir_name),
    "output_file": str(Path("compiled") / f"{dir_name}.txt"),
    "include_extensions": [".py", ".ts", ".tsx", ".js"],
    "exclude_keywords": [
        "__pycache__", ".git", ".cache", "venv", "env",
        "node_modules", "dist", ".next", "out", "build",
        ".vscode", ".idea", "compiled"
    ],
    "entrypoint": "main:run"
}
