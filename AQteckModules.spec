# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['.', 'AQ_lib/AQ_main_window/',
                'AQ_lib/AQ_main_window/AQ_main_field_frame',
                'AQ_lib/AQ_main_window/AQ_main_window_frame',
                'AQ_lib/AQ_device_info_window',
                'AQ_lib/AQ_other',
                'AQ_lib/AQ_param_list_window',
                'AQ_lib/AQ_session',
                'AQ_lib/AQ_watch_list_window',
                'AQ_lib/AQ_window_add_devices',
                'AQ_lib/AQ_window_templates'],
    binaries=[],
    datas=[('Icons', 'Icons'), ('110_device_conf', '110_device_conf')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='AQteckModules',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AQteckModules',
)