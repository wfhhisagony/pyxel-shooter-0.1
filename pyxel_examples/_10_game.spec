# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['_10_game.py',
    '_0_global.py',
    '_1_bullet.py',
    '_2_enemy.py',
    '_3_mytimer.py',
    '_4_player.py',
    '_5_powerbar.py',
    '_6_recruit.py',
    '_7_scoreboard.py',
    '_8_skill.py',
    '_9_utils.py'
],
             pathex=['C:\\Users\\86183\\Desktop\\pyxel_examples'],
             binaries=[],
             datas=[('C:\\Users\\86183\\Desktop\\pyxel_examples\\assets','assets')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='_10_game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='_10_game')
