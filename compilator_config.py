dir = "compilator"

CONFIG = {
    "source_dir": f'../{dir}',
    "output_file": f"compiled/{dir}.txt",
    "include_extensions": [".py", ".ts", ".tsx", ".js"],
    "exclude_keywords": [
        "__pycache__", ".git", ".cache", "venv", "env",
        "node_modules", "dist", ".next", "out", "build",
        ".vscode", ".idea", "compiled"
    ],
    "entrypoint": "main:run"
}
