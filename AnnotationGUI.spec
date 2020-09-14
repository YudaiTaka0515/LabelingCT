# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PIL import ImageTk, Image

himimports = [
    "PIL"
]

def get_ImageTk_path():
    from PIL import ImageTk
    ImageTk_path = ImageTk.__path__[0]
    return ImageTk_path

def get_Image_path():
    from PIL import Image
    Image_path = Image.__path__[0]
    return Image_path

a = Analysis(['AnnotationGUI.py'],
             pathex=['P:\\LabelingCT'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
"""
dict_tree = Tree(get_ImageTk_path(), prefix='PIL.ImageTk', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'PIL.ImageTk' not in x[0], a.binaries)

dict_tree = Tree(get_Image_path(), prefix='PIL.Image', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'PIL.Image' not in x[0], a.binaries)
"""

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AnnotationGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
