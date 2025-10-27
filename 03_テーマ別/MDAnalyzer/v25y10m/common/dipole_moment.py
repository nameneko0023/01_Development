#==========================================================================
# MDAnalyzer/v25y10m/common/dipcalculation.py  
# 電気双極子モーメント計算モジュール
#==========================================================================
#==========================================================================
# 更新履歴=================================================================
# 2025/10/01 - 初版作成
#==========================================================================

#モジュールインポート
import numpy as np
import math
import MDAnalysis as md
from tqdm import tqdm
from time import sleep

# 物理定数の定義（SI単位系）
from config.constants import PHYSICAL_CONSTANTS

class WATER:
    #水分子の双極子モーメントを計算
    @classmethod
    def Get_dipole_water(cls, universe: md.Universe) -> list:
       #水分子の原子電荷（単位：e）}
        WATER_CHARGES = {
            'O': -0.834,    # 酸素
            'H': 0.417,     # 水素
        }

        dipole_moments = []
        for ts in tqdm(universe.trajectory, desc="Calculating water dipole moments"):
            total_dipole = np.zeros(3)
            for water in universe.select_atoms('resname HOH*').residues:
                dipole = np.zeros(3)
                for atom in water.atoms:
                    charge = WATER_CHARGES.get(atom.element, 0)
                    position = atom.position * PHYSICAL_CONSTANTS['ANGSTROM']
                    dipole += charge * position
                total_dipole += dipole
            dipole_moments.append(np.linalg.norm(total_dipole) / PHYSICAL_CONSTANTS['DEBYE'])
            sleep(0.01)  # プログレスバーの更新を見やすくするための遅延
        return dipole_moments

class   SOLUTE:
    def Get_dipole_methanol(cls, universe: md.Universe) -> list:
        #メタノール分子の双極子モーメントを計算
        #原子電荷（単位：e）
        METHANOL_CHARGES = {
            'C': 0.265,     # 炭素
            'O': -0.683,    # 酸素
            'H': 0.098,     # 水素
        }

        dipole_moments = []
        for ts in tqdm(universe.trajectory, desc="Calculating methanol dipole moments"):
            total_dipole = np.zeros(3)
            for methanol in universe.select_atoms('resname MET*').residues:
                dipole = np.zeros(3)
                for atom in methanol.atoms:
                    charge = METHANOL_CHARGES.get(atom.element, 0)
                    position = atom.position * PHYSICAL_CONSTANTS['ANGSTROM']
                    dipole += charge * position
                total_dipole += dipole
            dipole_moments.append(np.linalg.norm(total_dipole) / PHYSICAL_CONSTANTS['DEBYE'])
            sleep(0.01)  # プログレスバーの更新を見やすくするための遅延
        return dipole_moments
    
    def Get_dipole_ethanol(cls, universe: md.Universe) -> list:
        #エタノール分子の双極子モーメントを計算
        #原子電荷（単位：e）
        ETHANOL_CHARGES = {
            'C': 0.265,     # 炭素
            'O': -0.683,    # 酸素
            'H': 0.098,     # 水素
        }

        dipole_moments = []
        for ts in tqdm(universe.trajectory, desc="Calculating ethanol dipole moments"):
            total_dipole = np.zeros(3)
            for ethanol in universe.select_atoms('resname ETH*').residues:
                dipole = np.zeros(3)
                for atom in ethanol.atoms:
                    charge = ETHANOL_CHARGES.get(atom.element, 0)
                    position = atom.position * PHYSICAL_CONSTANTS['ANGSTROM']
                    dipole += charge * position
                total_dipole += dipole
            dipole_moments.append(np.linalg.norm(total_dipole) / PHYSICAL_CONSTANTS['DEBYE'])
            sleep(0.01)  # プログレスバーの更新を見やすくするための遅延
        return dipole_moments
    
    
        
        