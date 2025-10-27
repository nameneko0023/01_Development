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
import common.open_file_dialog as filedialog
import common.dipole_moment as dipole

# メイン処理
if __name__ == "__main__":
    #解析ファイルの読み込み
    if filedialog.Set_pdb() and filedialog.Set_dcd():
        print("---ファイルが正常に選択されました。---")
        pdb = filedialog.Get_pdb()
        dcd = print(filedialog.Get_dcd())

        #双極子モーメント情報の取得
        print("---双極子モーメント情報取得中---")
        u = md.Universe(pdb, dcd)
        resnames = set(res.resname for res in u.residues)
        print(f"検出された分子種: {', '.join(resnames)}")


        #双極子モーメント計算の実行
        WAT = None
        SOLUTE = None
        for resname in resnames:
            resname = resname.strip()
            #水分子と溶質分子の双極子モーメント計算の振り分け
            if resname.startswith("HOH"): #水分子
                WAT = dipole.WATER.Get_dipole_water(u)
                break
            elif  resname.startswith("WAT"): #水分子
                WAT = dipole.WATER.Get_dipole_water(u)
        
        ope = input(f"検出された溶質分子: {', '.join(resnames - {'HOH', 'WAT'})}")
        print(ope)
        
        for resname in resnames:
            resname = resname.strip()
        #溶質分子の双極子モーメント計算
        if resname.startswith("MET"): #メタノール
             SOLUTE = dipole.SOLUTE.Get_dipole_methanol(u)
        elif resname.startswith("ETH"): #エタノール
             SOLUTE = dipole.SOLUTE.Get_dipole_ethanol(u)
        else:
            pass
                
        
        


        #解析処理の実行
        print("---誘電緩和曲線の解析処理を実行します。---")
        if SOLUTE:
            #混合物系解析（水溶液）
            dipole.analyze_dielectric_relaxation(WAT, SOLUTE)
        else:
            #純物系解析（水）
            dipole.analyze_dielectric_relaxation(WAT)

        #終了処理
        print("---処理が完了しました。---")
    else:
        print("---ファイルの選択がキャンセルされました。---")
        pass


    



        
