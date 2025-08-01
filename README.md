# 🛠️ Compilator

`compilator` es una herramienta sencilla que permite escanear otro proyecto (por ejemplo, un repositorio Git) y compilar el contenido de sus archivos en un único fichero `.txt` con su árbol de directorios, con opciones para incluir o excluir ciertos tipos de archivos o carpetas.

Ideal para consolidar código fuente, generar documentación o enviar un resumen compacto de un proyecto.

```bash
.
├── /tus_proyectos
|   ├── compilator
|   |   ├── outputs               # directorio con las carpetas compiladas en un fichero .txt
|   |   |   ├── proyecto_1.txt
|   |   |   └── proyecto_2.txt
|   |   └── ...
|   ├── proyecto_1
|   |   └── ...
|   └── proyecto_2            
|       └── ...
```

---

## 📁 Estructura del proyecto

```bash
compilator/
├── main.py           # Script principal que hace la compilación
├── .env              # Configuración de entrada
├── run.sh            # Script ejecutable
├── requirements.txt  # Dependencias (por si se necesitan)
└── outputs/          # Carpeta de salida para los .txt
```

---

## ⚙️ Configuración (`.env`)

Editá el archivo `.env` con las siguientes variables:

```bash
SRC=../otro_proyecto                                                                # Ruta del proyecto a escanear
OUT=outputs/output.txt                                                              # Ruta del archivo de salida
INCLUDE=.py,.txt                                                                    # Extensiones a incluir (separadas por coma)
EXCLUDE=.env,__pycache__,.git,.cache,venv,node_modules,dist,.next,out,build         # Palabras clave o carpetas a excluir
```
---

## 🚀 Cómo usar
Instalá las dependencias:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Ejecutá el script:

```bash
source venv/bin/activate
./run.sh
```

```bash
./run.sh
```

El contenido del proyecto definido en SRC será escaneado, y todos los archivos que cumplan los criterios de inclusión/exclusión serán combinados en un único fichero ubicado en `/outputs/`.

---

## 🧪 Ejemplo

Si tenés este contenido en `.env`:

```bash
SRC=../my_repository
OUT=outputs/{SRC}.txt
EXCLUDE=venv,.git,__pycache__,.env
INCLUDE=.py # se puede dejar vacío o no declarar, y copia el resto de los ficheros
```

Y ejecutás:

```bash
./run.sh
```

Se creará `outputs/my_repository.txt` con todos los `.py` del proyecto, excluyendo carpetas como `.git`, `__pycache__`, etc.

---

## 📦 Dependencias

- python-dotenv: Para cargar automáticamente los parámetros desde `.env`.

Instalación rápida:

```bash
pip install python-dotenv
```

---

## 📜 Ejemplo de salida

Fichero `.env`:

```bash
SRC=../compilator
OUT=outputs/{SRC}.txt
EXCLUDE=.env,.md,__pycache__,.git,.cache,venv,node_modules,dist,.next,out,build,.github,.gitlab,.bitbucket,.azure-pipelines,.circleci,.husky
INCLUDE=
```

El fichero de salida no incluye especificamente una extension determinada (en `INCLUDE`) pero si define que ficheros ignorar en `EXCLUDE`. El fichero `compilator.txt` generado es el siguiente:

```bash
##################### Árbol de directorios #####################


../compilator
├── .env
├── .gitignore
├── main.py
├── outputs
│   ├── compilator.txt
│   ├── proyecto_1.txt
│   └── proyecto_2.txt
├── REAME.md
├── requirements.txt
└── run.sh

1 directory, 9 files



##################### Archivos incluidos #####################


==============================================================
              ../compilator/requirements.txt
==============================================================
python-dotenv



==============================================================
              ../compilator/main.py
==============================================================
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



==============================================================
              ../compilator/run.sh
==============================================================
#!/bin/bash
source .env
python3 main.py
```

✅ Licencia
MIT © 2025 – Luis Forni
