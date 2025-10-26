# ==========================================================================
# MDAnalyzer/v25y10m/common/dipole_calculator.py
# 電気双極子モーメント計算モジュール（最適化版）
# ==========================================================================
# ==========================================================================
# 更新履歴
# 2025/10/24 - 初版作成: dipcalculation.py の最適化版
# ==========================================================================

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
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

# 分子種ごとの部分電荷定義
@dataclass
class MolecularCharges:
子種ごとの部分電荷を管理するクラス"""
    charges: Dict[str, float]
    
    @property
    def e_charges(self) -> Dict[str, float]:
        """電気素量単位での電荷を返す"""
        e = PHYSICAL_CONSTANTS['ELEMENTARY_CHARGE']
        return {k: v * e for k, v in self.charges.items()}

# 各分子種の電荷定義
WATER_CHARGES = MolecularCharges({
    'H': 0.4174,
    'O': -0.8340
})

METHANOL_CHARGES = MolecularCharges({
    'H1': 0.4000,
    'O': -0.6500,
    'H46': 0.0500,
    'C': 0.1000
})

ETHANOL_CHARGES = MolecularCharges({
    'C1': -0.1500,
    'C2': 0.1500,
    'O3': -0.6500,
    'H15': 0.0500,
    'H6': 0.4000
})

def calculate_vector_magnitude(vector: np.ndarray) -> float:
    """3次元ベクトルの大きさを計算"""
    return np.sqrt(np.sum(vector ** 2))

def calculate_dipole_component(pos1: np.ndarray, pos2: np.ndarray, charge: float) -> np.ndarray:
    """双極子モーメントの成分を計算
    
    Args:
        pos1: 原子1の位置ベクトル
        pos2: 原子2の位置ベクトル
        charge: 電荷（素電荷単位）
    
    Returns:
        双極子モーメント成分（デバイ単位）
    """
    return charge * (pos1 - pos2) * (PHYSICAL_CONSTANTS['ANGSTROM'] / PHYSICAL_CONSTANTS['DEBYE'])

class DipoleCalculator:
    """双極子モーメント計算クラス"""
    
    @staticmethod
    def calculate_water_dipole(universe: md.Universe, selection: str = "resname HOH*") -> List[np.ndarray]:
        """水分子の双極子モーメントを計算
        
        Args:
            universe: MDAnalysis Universe オブジェクト
            selection: 水分子を選択するための MDAnalysis 選択文字列
        
        Returns:
            各時刻での双極子モーメント（デバイ単位）
        """
        dipoles = []
        charges = WATER_CHARGES.e_charges
        
        for ts in tqdm(universe.trajectory, desc="water_trajectory"):
            water = universe.select_atoms(selection)
            O = water.select_atoms("name OH2").positions
            H1 = water.select_atoms("name H1").positions
            H2 = water.select_atoms("name H2").positions
            
            OH1 = calculate_dipole_component(O, H1, charges['H'])
            OH2 = calculate_dipole_component(O, H2, charges['H'])
            
            total_dipole = OH1 + OH2
            dipoles.append(total_dipole)
            
        sleep(0.05)  # プログレスバー表示用
        
        # 最初のフレームの結果を表示
        print("\n===== 水分子の双極子モーメント =====")
        print("※ 値はデバイ単位")
        print(f"O-H1: {calculate_vector_magnitude(OH1[0]):.4f}")
        print(f"O-H2: {calculate_vector_magnitude(OH2[0]):.4f}")
        print(f"Total: {calculate_vector_magnitude(dipoles[0][0]):.4f}")
        print("=" * 40)
        
        return dipoles

    @staticmethod
    def calculate_methanol_dipole(universe: md.Universe, selection: str = "resname UNK*") -> List[np.ndarray]:
        """メタノールの双極子モーメントを計算"""
        dipoles = []
        charges = METHANOL_CHARGES.e_charges
        
        for ts in tqdm(universe.trajectory, desc="methanol_trajectory"):
            mol = universe.select_atoms(selection)
            
            # 原子位置の取得
            C = mol.select_atoms("name C3").positions
            O = mol.select_atoms("name O2").positions
            H1 = mol.select_atoms("name H1").positions
            H_methyl = [
                mol.select_atoms("name H4").positions,
                mol.select_atoms("name H5").positions,
                mol.select_atoms("name H6").positions
            ]
            
            # C-H（メチル基）とC-O成分の計算
            ch_co = sum(calculate_dipole_component(C, h, charges['H46']) for h in H_methyl)
            ch_co += calculate_dipole_component(O, C, charges['C'])
            
            # O-H成分の計算
            oh = calculate_dipole_component(O, H1, charges['H1'])
            
            total_dipole = ch_co + oh
            dipoles.append(total_dipole)
        
        sleep(0.05)
        
        # 最初のフレームの結果を表示
        print("\n===== メタノールの双極子モーメント =====")
        print("※ 値はデバイ単位")
        print(f"CH-CO: {calculate_vector_magnitude(ch_co[0]):.4f}")
        print(f"OH: {calculate_vector_magnitude(oh[0]):.4f}")
        print(f"Total: {calculate_vector_magnitude(dipoles[0][0]):.4f}")
        print("=" * 40)
        
        return dipoles

def analyze_trajectory(universe: md.Universe, molecule_type: str = "Water") -> Tuple[str, List[np.ndarray]]:
    """トラジェクトリ解析のメインインターフェース
    
    Args:
        universe: MDAnalysis Universe オブジェクト
        molecule_type: 分子種（"Water", "Methanol", "Ethanol" のいずれか）
    
    Returns:
        (分子種, 双極子モーメントのリスト)
    """
    calc = DipoleCalculator()
    
    if molecule_type.lower() == "water":
        dipoles = calc.calculate_water_dipole(universe)
    elif molecule_type.lower() == "methanol":
        dipoles = calc.calculate_methanol_dipole(universe)
    else:
        raise ValueError(f"未対応の分子種: {molecule_type}")
    
    return molecule_type, dipoles

# 使用例
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("使用法: python dipole_calculator.py [pdb_file] [dcd_file]")
        sys.exit(1)
        
    # トラジェクトリの読み込み
    universe = md.Universe(sys.argv[1], sys.argv[2])
    
    # 解析実行
    molecule_type = input("分子種を選択（Water/Methanol）: ").strip()
    mol_type, dipoles = analyze_trajectory(universe, molecule_type)
    
    print(f"\n{mol_type}の解析が完了しました。")
    print(f"トラジェクトリ長: {len(dipoles)} フレーム")