import os
import subprocess
from pathlib import Path

def should_include(file_path, include_exts, exclude_keywords):
    if any(kw in file_path for kw in exclude_keywords):
        return False
    if include_exts:
        return any(file_path.endswith(ext) for ext in include_exts)
    return True

def generate_tree_header(source_dir, exclude_keywords):
    result = []
    source_path = Path(source_dir).resolve()

    for path in sorted(source_path.rglob("*")):
        rel_path = path.relative_to(source_path.parent)
        if any(kw in str(rel_path) for kw in exclude_keywords):
            continue
        prefix = "├── " if path.is_file() else "└── "
        result.append(f"{prefix}{rel_path}")

    return f"{source_path.parent.name}/\n" + "\n".join(result)

def compile_project(config):
    source_dir = config["source_dir"]
    output_file = config["output_file"]
    include_exts = config["include_extensions"]
    exclude_keywords = config["exclude_keywords"]

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as out_f:
        tree = generate_tree_header(source_dir, exclude_keywords)
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

    print(f"[✓] Compilación completa: {output_file}")
