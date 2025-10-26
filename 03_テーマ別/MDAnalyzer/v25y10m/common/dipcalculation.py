#==========================================================================
# MDAnalyzer/v25y10m/common/dipcalculation.py  
# 電気双極子モーメント計算モジュール
#==========================================================================
#==========================================================================
# 更新履歴=================================================================
# 2025/10/01 - 初版作成
#==========================================================================

#モジュールインポート
import os
import math
import numpy as np
import MDAnalysis as md
from tqdm import tqdm
from time import sleep

# 物理定数の定義（SI単位系）
PHYSICAL_CONSTANTS = {
    'ANGSTROM': 1e-10,  # m
    'DEBYE': 3.33564e-30,  # C·m
    'ELEMENTARY_CHARGE': 1.602176634e-19,  # C
    'PICOSECOND': 1e-12,  # s
}

class DipoleCalculator:
    #水分子の双極子モーメントを計算
    @classmethod
    def water(cls, universe: md.Universe) -> list:
    
        # 分子種ごとの電荷をクラス変数として定義
        WATER_CHARGES = {
         'H': 0.4174 * PHYSICAL_CONSTANTS['ELEMENTARY_CHARGE'],
         'O': -0.8340 * PHYSICAL_CONSTANTS['ELEMENTARY_CHARGE']
        }
    
    
        
        