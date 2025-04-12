import os
import subprocess

def convert_ui_files(ui_root):
    for root, dirs, files in os.walk(ui_root):
        for file in files:
            if file.endswith(".ui"):
                ui_path = os.path.join(root, file)
                py_name = f"ui_{os.path.splitext(file)[0]}.py"
                py_path = os.path.join(root, py_name)

                cmd = ["pyside2-uic", ui_path, "-o", py_path]
                try:
                    print(f"Converting: {ui_path} → {py_path}")
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"[ERROR] Failed to convert {ui_path}: {e}")

if __name__ == "__main__":
    # Укажи путь к корню проекта (где лежат .ui)
    # project_root = os.path.dirname(os.path.abspath(__file__))
    convert_ui_files("UI/forms/")
