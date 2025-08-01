from compilator_config import CONFIG
from compiler.project_compiler import compile_project

def run():
    compile_project(CONFIG)

if __name__ == "__main__":
    run()
