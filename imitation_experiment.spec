# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['imitation_experiment.py'],
    pathex=[],
    binaries=[],
    datas=[('stimuli/', 'stimuli/'), ('pics/', 'pics/'), ('C:\\Users\\NOLA\\.conda\\envs\\exp_imitation\\Lib\\site-packages\\psychopy\\alerts', 'psychopy/alerts/alertsCatalogue')],
    hiddenimports=['psychopy.visual.backends.pygletbackend', 'psychopy.visual.line'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='imitation_experiment',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['vcruntime140.dll'],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Users\\NOLA\\OneDrive\\PhD\\events_conferences_presentations\\icons\\mime.ico',
)
