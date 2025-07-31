import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

DEFAULT_EXCLUDES = [
    "__pycache__",
    ".git",
    ".cache",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "dist",
    ".next",
    "out",
    "build",
    ".github",
    ".gitlab",
    ".circleci",
    ".bitbucket",
    ".azure",
    ".vscode",
    ".idea",
    ".husky",
    ".config"
]

def should_include(file_path, include_exts, exclude_keywords):
    if any(kw in file_path for kw in exclude_keywords):
        return False
    if include_exts:
        return any(file_path.endswith(ext) for ext in include_exts)
    return True

def generate_tree_header(source_dir):
    exclude_pattern = '|'.join(DEFAULT_EXCLUDES)
    try:
        result = subprocess.run(
            ["tree", "-a", "-I", exclude_pattern, source_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"# Error generando árbol de directorio: {e}"

def compile_project(source_dir, output_file, include_exts, exclude_keywords):
    with open(output_file, 'w', encoding='utf-8') as out_f:
        tree = generate_tree_header(source_dir)
        out_f.write("##################### Árbol de directorios #####################\n\n\n")
        out_f.write(tree)
        out_f.write("\n\n\n##################### Archivos incluidos #####################")
        for root, _, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                if should_include(full_path, include_exts, exclude_keywords):
                    out_f.write(f"\n\n\n==============================================================\n")
                    out_f.write(f"              {full_path}\n")
                    out_f.write(f"==============================================================\n")
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            out_f.write(f.read())
                    except Exception as e:
                        out_f.write(f"# Error leyendo {full_path}: {e}\n")

if __name__ == "__main__":
    load_dotenv()

    src = os.getenv("SRC")
    if not os.path.exists(src):
        print(f"❌ Error: la ruta definida en SRC no existe → {src}")
        exit(1)

    raw_out = os.getenv("OUT")
    include = os.getenv("INCLUDE", "")
    exclude = os.getenv("EXCLUDE", "")

    include_exts = [ext.strip() for ext in include.split(",") if ext.strip()]
    exclude_keywords = list(set(
        [e.strip() for e in exclude.split(",") if e.strip()] + DEFAULT_EXCLUDES
    ))

    if "{SRC}" in raw_out:
        src_name = Path(src).resolve().name or "root"
        out = raw_out.replace("{SRC}", src_name)
    else:
        out = raw_out

    os.makedirs(os.path.dirname(out), exist_ok=True)
    compile_project(src, out, include_exts, exclude_keywords)

    print(f"✅ Compilación completa en: {out}")
