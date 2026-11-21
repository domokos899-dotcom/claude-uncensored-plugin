# PyInstaller spec for Claude.ai Uncensored Plugin (Windows desktop)
block_cipher = None

a = Analysis(
    ["claude_uncensored_plugin/__main__.py"],
    pathex=[],
    binaries=[],
    datas=[("config/profiles.json", "config")],
    hiddenimports=["win32file", "win32api", "winreg"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, name="claude-uncensored-plugin", console=False)