import os
import subprocess
import sys
import shutil


def build():
    print("[*] Starting Retro Injector build...")
    print("[!] NOTE: this produces an UNSEALED debug build. For a shippable")
    print("[!]       release, use `..\\release.ps1` from the project root")
    print("[!]       instead. That path seals the tree before PyInstaller.")

    # 1. Clean previous build output
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            print(f"[*] Removing old {folder} folder...")
            shutil.rmtree(folder, ignore_errors=True)

    # 2. Ensure PyInstaller is installed for THIS interpreter
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[!] PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 3. Define paths
    script_path = "main.pyw"
    icon_file = "retro_logo.ico"

    # 4. Build command. Invoke via `<python> -m PyInstaller` so we don't
    # depend on the pyinstaller.exe shim being on PATH (it often isn't on
    # a fresh Windows Python install). Uses the same interpreter running
    # this script, so PyInstaller finds the packages we installed above.
    # On Windows, --add-data uses ';' between source and dest.
    separator = ";"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onedir",
        f"--icon={icon_file}",
        f"--add-data=retro/interface/assets{separator}retro/interface/assets",
        f"--add-data=version.json{separator}.",
        f"--add-data=retro/data{separator}retro/data",
        f"--add-data=main.pyw{separator}.",
        "--name=RetroInjector",
        "--noconfirm",
        "--clean",
        script_path,
    ]

    print(f"[*] Executing: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\n[+] Build Complete!")
    print(f"[+] Application folder: {os.path.abspath('dist/RetroInjector')}")
    print("[+] EXE path: dist/RetroInjector/RetroInjector.exe")

if __name__ == "__main__":
    build()
