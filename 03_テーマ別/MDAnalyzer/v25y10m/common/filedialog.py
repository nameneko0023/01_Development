#==========================================================================
# MDAnalyzer/v25y10m/common/filedialog.py
# ファイルダイアログ関連モジュール
#==========================================================================
#==========================================================================
# 更新履歴=================================================================
# 2025/10/01 - 初版作成
#==========================================================================

#モジュールインポート
import tkinter as tk
from tkinter import filedialog as tkfd

#ファイルパス格納用グローバル変数==========================================
pdb_path = ""
dcd_path = ""
#==========================================================================

#解析ファイルを選択（共通）================================================
def Set_file(title:None, initialdir=".", filetypes=None):
    root = tk.Tk()
    root.withdraw()
    try:
        file_path = tkfd.askopenfilename(
            title=title,
            initialdir=initialdir,
            filetypes=filetypes
        )
        return file_path
    except Exception as e:
        print(f"ファイル選択中にエラーが発生しました: {e}")
        return None
    finally:
        try:
            root.destroy()
        except Exception:
            pass
#========================================================================


# 解析対象のPDBファイル取得==============================================
def Set_pdb():
    global pdb_path
    pdb_path = Set_file(
        title="解析対象のトポロジーファイルを選択してください",
        initialdir=".",
        filetypes=[("PDBファイル", "*.pdb")]
    )
    return pdb_path

def Get_pdb():    
    return pdb_path
#=========================================================================


# 解析対象のDCDファイル取得===============================================
def Set_dcd():
    global dcd_path
    dcd_path = Set_file(
        title="解析対象の分子軌道ファイルを選択してください",
        initialdir=".",
        filetypes=[("DCDファイル", "*.dcd")]
    )
    return dcd_path

def Get_dcd():
    return dcd_path
#==========================================================================


