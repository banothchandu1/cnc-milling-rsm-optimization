"""
Machining Physics and Mechanistic Response Model
Author: Banoth Chandu Nayak (NIT Hamirpur)
"""

import numpy as np

def compute_mrr(feed_rate, depth_of_cut, width_of_cut=5.0):
    return (depth_of_cut * width_of_cut * feed_rate) / 1000.0

def compute_cycle_time(feed_rate, length_of_cut=100.0, cutter_diameter=10.0):
    le = cutter_diameter / 2.0
    total_length = length_of_cut + 2 * le
    return (total_length / feed_rate) * 60.0

def compute_cutting_power(feed_rate, depth_of_cut, spindle_speed, cutter_diameter=10.0, teeth=4):
    fz = feed_rate / (spindle_speed * teeth)
    hm = fz * np.sqrt(5.0 / cutter_diameter)
    kc = 2100.0 * (hm ** -0.25)
    fc = kc * hm * depth_of_cut * teeth
    vc = (np.pi * cutter_diameter * spindle_speed) / 60000.0
    power_kw = (fc * vc) / 1000.0
    return float(np.round(np.clip(power_kw, 0.2, 5.0), 3))

def simulate_responses(df, seed=42):
    np.random.seed(seed)
    n = len(df)
    
    x1 = df['X1_coded'].values
    x2 = df['X2_coded'].values
    x3 = df['X3_coded'].values
    
    ra_mean = (1.425 - 0.182 * x1 + 0.245 * x2 + 0.098 * x3 
               + 0.076 * (x1**2) + 0.054 * (x2**2) + 0.038 * (x3**2)
               - 0.065 * (x1 * x2) - 0.028 * (x1 * x3) + 0.042 * (x2 * x3))
    ra_noise = np.random.normal(0, 0.008, n)
    ra_sim = np.round(ra_mean + ra_noise, 3)
    
    vb_mean = (0.152 + 0.033 * x1 + 0.016 * x2 + 0.012 * x3
               + 0.0058 * (x1**2) + 0.0021 * (x2**2) + 0.0019 * (x3**2)
               + 0.0048 * (x1 * x2) + 0.0031 * (x1 * x3) + 0.0018 * (x2 * x3))
    vb_noise = np.random.normal(0, 0.001, n)
    vb_sim = np.round(vb_mean + vb_noise, 3)
    
    df['Surface_Roughness_Ra_um'] = ra_sim
    df['Tool_Flank_Wear_Vb_mm'] = vb_sim
    df['MRR_cm3_min'] = np.round(compute_mrr(df['Feed_Rate_mm_min'], df['Depth_of_Cut_mm']), 2)
    df['Cycle_Time_s'] = np.round(compute_cycle_time(df['Feed_Rate_mm_min']), 2)
    
    powers = []
    for _, row in df.iterrows():
        p = compute_cutting_power(row['Feed_Rate_mm_min'], row['Depth_of_Cut_mm'], row['Spindle_Speed_RPM'])
        powers.append(p)
    df['Cutting_Power_kW'] = powers
    
    return df
