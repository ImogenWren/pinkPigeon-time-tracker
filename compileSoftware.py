import subprocess
import os


def compile_to_exe(script_path):
    # Check if the script exists
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        return

    # Run the PyInstaller command to compile the script
    try:
        subprocess.run(["pyinstaller", "--onefile", "--console", script_path, "--icon=icon/pinkPigeon-logo.ico"], check=True)
        print(f"Compilation completed! Check the 'dist' folder for the .exe file.")
    except subprocess.CalledProcessError:
        print("Compilation failed. Please check the script for errors.")


# Example usage: replace 'your_script.py' with the path to your Python script
compile_to_exe("main.py")
