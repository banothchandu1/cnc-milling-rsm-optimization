"""
Design of Experiments Module: Central Composite Design (CCD) Generator
Author: Banoth Chandu Nayak (NIT Hamirpur)
"""

import numpy as np
import pandas as pd

def generate_ccd_matrix(alpha=1.682):
    """
    Generates a 3-factor Central Composite Design matrix (Rotatable, alpha=1.682).
    Factors:
      X1: Spindle Speed (RPM) [Low: 2000, Center: 2500, High: 3000]
      X2: Feed Rate (mm/min)  [Low: 200,  Center: 350,  High: 500]
      X3: Depth of Cut (mm)   [Low: 0.75, Center: 1.25, High: 1.75]
    """
    factorial_coded = []
    for x1 in [-1, 1]:
        for x2 in [-1, 1]:
            for x3 in [-1, 1]:
                factorial_coded.append([x1, x2, x3, 'Factorial'])
                
    axial_coded = [
        [-alpha, 0, 0, 'Axial'],
        [ alpha, 0, 0, 'Axial'],
        [0, -alpha, 0, 'Axial'],
        [0,  alpha, 0, 'Axial'],
        [0, 0, -alpha, 'Axial'],
        [0, 0,  alpha, 'Axial']
    ]
    
    center_coded = [[0, 0, 0, 'Center'] for _ in range(6)]
    
    all_runs = factorial_coded + axial_coded + center_coded
    df = pd.DataFrame(all_runs, columns=['X1_coded', 'X2_coded', 'X3_coded', 'Run_Type'])
    df['Run_Order'] = np.arange(1, len(df) + 1)
    
    df['Spindle_Speed_RPM'] = np.round(2500 + df['X1_coded'] * 500, 1)
    df['Feed_Rate_mm_min'] = np.round(350 + df['X2_coded'] * 150, 1)
    df['Depth_of_Cut_mm'] = np.round(1.25 + df['X3_coded'] * 0.50, 2)
    
    return df[['Run_Order', 'Run_Type', 'X1_coded', 'X2_coded', 'X3_coded', 
               'Spindle_Speed_RPM', 'Feed_Rate_mm_min', 'Depth_of_Cut_mm']]

if __name__ == "__main__":
    design = generate_ccd_matrix()
    design.to_csv("data/ccd_design.csv", index=False)
    print("CCD Matrix Generated Successfully with 20 runs.")
