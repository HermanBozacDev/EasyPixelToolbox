# easy_pixel.spec
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
import sys

block_cipher = None

a = Analysis(
    ['main.py'],                     # Script principal
    pathex=[str(Path('.').resolve())],
    binaries=[],
    datas=[
        ('assets/*', 'assets'),      # Carpeta de assets
        # ('models/**/*', 'models'), # Descomentá si usás modelos
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='easy_pixel',
    debug=False,
    strip=False,
    upx=True,
    console=True,   # True = ver consola para debug; False = sin ventana negra
    disable_windowed_traceback=False,
    target_arch=None,
)

