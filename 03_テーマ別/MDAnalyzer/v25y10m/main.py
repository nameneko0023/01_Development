#=============================================================
# MDAnalyzer: A Molecular Dynamics Analysis Tool
# Version: 25y10m
# Main Script
#=============================================================
#=============================================================
# 更新履歴====================================================
# 2025/10/01 - 初版作成
#=============================================================

#標準モジュール
import MDAnalysis as md
# 自作モジュール
import common.filedialog as filedialog
import config.constants as con

# メイン処理
if __name__ == "__main__":
    if filedialog.Set_pdb() and filedialog.Set_dcd():
        print("---ファイルが正常に選択されました。---")
        print(filedialog.Get_pdb())
        print(filedialog.Get_dcd())

        print("---計算中---")
       
        
        
        exit()
    else:
        exit()
    


    



        
