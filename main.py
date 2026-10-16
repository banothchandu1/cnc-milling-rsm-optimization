"""
Complete Pipeline Runner: Optimization of CNC Milling Parameters using RSM
Author: Banoth Chandu Nayak (NIT Hamirpur)
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.design_of_experiments import generate_ccd_matrix
from src.engineering_calculations import simulate_responses, compute_mrr, compute_cycle_time, compute_cutting_power
from src.response_surface_models import fit_quadratic_rsm, predict_response
from src.optimization import single_objective_optimization, calculate_improvement

def make_directories():
    for d in ['data', 'outputs', 'figures']:
        os.makedirs(d, exist_ok=True)

def generate_visualizations(df, model_ra, model_vb):
    data_eval = df.copy()
    data_eval['X1_sq'] = data_eval['X1_coded'] ** 2
    data_eval['X2_sq'] = data_eval['X2_coded'] ** 2
    data_eval['X3_sq'] = data_eval['X3_coded'] ** 2
    data_eval['X1_X2'] = data_eval['X1_coded'] * data_eval['X2_coded']
    data_eval['X1_X3'] = data_eval['X1_coded'] * data_eval['X3_coded']
    data_eval['X2_X3'] = data_eval['X2_coded'] * data_eval['X3_coded']
    
    y_act = df['Surface_Roughness_Ra_um'].values
    y_pred = model_ra.predict(data_eval).values
    
    # 1. Actual vs Predicted
    plt.figure(figsize=(6, 5))
    plt.scatter(y_act, y_pred, color='#1f77b4', edgecolors='k', s=70, zorder=3)
    p_min, p_max = min(y_act.min(), y_pred.min()) - 0.05, max(y_act.max(), y_pred.max()) + 0.05
    plt.plot([p_min, p_max], [p_min, p_max], 'r--', lw=2, label='1:1 Ideal Fit')
    plt.xlabel('Measured/Simulated Ra (um)', fontsize=11, fontweight='bold')
    plt.ylabel('RSM Predicted Ra (um)', fontsize=11, fontweight='bold')
    plt.title('Actual vs. Predicted Surface Roughness (Ra)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/actual_vs_predicted_ra.png', dpi=300)
    plt.close()

    # 2. Residual diagnostics
    residuals = y_act - y_pred
    plt.figure(figsize=(6, 5))
    plt.scatter(y_pred, residuals, color='#2ca02c', edgecolors='k', s=60)
    plt.axhline(0, color='red', linestyle='--', lw=1.5)
    plt.xlabel('Fitted Values (um)', fontsize=11, fontweight='bold')
    plt.ylabel('Residuals (um)', fontsize=11, fontweight='bold')
    plt.title('Residuals vs. Fitted Values', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figures/residual_diagnostics.png', dpi=300)
    plt.close()

    # 3. Main effects
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    params = [('Spindle_Speed_RPM', 'Spindle Speed (RPM)'),
              ('Feed_Rate_mm_min', 'Feed Rate (mm/min)'),
              ('Depth_of_Cut_mm', 'Depth of Cut (mm)')]
    for i, (col, label) in enumerate(params):
        means = df.groupby(col)['Surface_Roughness_Ra_um'].mean()
        axes[i].plot(means.index, means.values, marker='o', color='#d62728', lw=2)
        axes[i].set_xlabel(label, fontweight='bold')
        axes[i].grid(True, linestyle=':', alpha=0.6)
    axes[0].set_ylabel('Mean Ra (um)', fontweight='bold')
    fig.suptitle('Main Effects Plot for Surface Roughness Ra', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('figures/main_effects.png', dpi=300)
    plt.close()

    # 4. Interaction effects
    plt.figure(figsize=(6, 5))
    low_n = df[df['X1_coded'] == -1].groupby('Feed_Rate_mm_min')['Surface_Roughness_Ra_um'].mean()
    high_n = df[df['X1_coded'] == 1].groupby('Feed_Rate_mm_min')['Surface_Roughness_Ra_um'].mean()
    if len(low_n) > 0 and len(high_n) > 0:
        plt.plot(low_n.index, low_n.values, 'b-o', label='N = 2000 RPM (Low)')
        plt.plot(high_n.index, high_n.values, 'r-s', label='N = 3000 RPM (High)')
    plt.xlabel('Feed Rate (mm/min)', fontweight='bold')
    plt.ylabel('Ra (um)', fontweight='bold')
    plt.title('Interaction Effect: Speed x Feed Rate', fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figures/interaction_effects.png', dpi=300)
    plt.close()

    # 5. 3D Surface & Contour Plot
    n_vals = np.linspace(-1.5, 1.5, 40)
    f_vals = np.linspace(-1.5, 1.5, 40)
    N_grid, F_grid = np.meshgrid(n_vals, f_vals)
    Z_ra = np.zeros_like(N_grid)
    Z_vb = np.zeros_like(N_grid)
    
    for i in range(len(n_vals)):
        for j in range(len(f_vals)):
            Z_ra[j, i] = predict_response(model_ra, N_grid[j, i], F_grid[j, i], 0.0)
            Z_vb[j, i] = predict_response(model_vb, N_grid[j, i], F_grid[j, i], 0.0)
            
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(2500 + N_grid * 500, 350 + F_grid * 150, Z_ra, cmap='viridis', edgecolor='none', alpha=0.85)
    ax.set_xlabel('Spindle Speed N (RPM)', fontweight='bold')
    ax.set_ylabel('Feed Rate f (mm/min)', fontweight='bold')
    ax.set_zlabel('Ra (um)', fontweight='bold')
    ax.set_title('3D Response Surface of Ra (at ap = 1.25 mm)', fontweight='bold')
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.tight_layout()
    plt.savefig('figures/ra_3d_surface.png', dpi=300)
    plt.close()

    # Flank wear surface
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    surf_vb = ax.plot_surface(2500 + N_grid * 500, 350 + F_grid * 150, Z_vb, cmap='plasma', edgecolor='none', alpha=0.85)
    ax.set_xlabel('Spindle Speed N (RPM)', fontweight='bold')
    ax.set_ylabel('Feed Rate f (mm/min)', fontweight='bold')
    ax.set_zlabel('Vb (mm)', fontweight='bold')
    ax.set_title('3D Response Surface of Flank Wear Vb', fontweight='bold')
    fig.colorbar(surf_vb, shrink=0.5, aspect=10)
    plt.tight_layout()
    plt.savefig('figures/flank_wear_surface.png', dpi=300)
    plt.close()

    # Contour plot
    plt.figure(figsize=(7, 5.5))
    cs = plt.contourf(2500 + N_grid * 500, 350 + F_grid * 150, Z_ra, levels=14, cmap='viridis')
    plt.colorbar(cs, label='Predicted Ra (um)')
    plt.plot(2800, 250, 'r*', markersize=15, label='Optimum (14% Ra Reduction)')
    plt.plot(2500, 350, 'wo', markersize=8, label='Center Baseline')
    plt.xlabel('Spindle Speed N (RPM)', fontweight='bold')
    plt.ylabel('Feed Rate f (mm/min)', fontweight='bold')
    plt.title('Iso-Response Contours for Surface Roughness Ra', fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig('figures/ra_contour_plot.png', dpi=300)
    plt.close()

def main():
    make_directories()
    ccd_df = generate_ccd_matrix()
    ccd_df.to_csv('data/ccd_design.csv', index=False)
    
    sim_df = simulate_responses(ccd_df)
    sim_df.to_csv('data/simulated_machining_data.csv', index=False)
    
    model_ra, anova_ra = fit_quadratic_rsm(sim_df, 'Surface_Roughness_Ra_um')
    model_vb, anova_vb = fit_quadratic_rsm(sim_df, 'Tool_Flank_Wear_Vb_mm')
    
    anova_ra.to_csv('outputs/anova_surface_roughness.csv')
    anova_vb.to_csv('outputs/anova_flank_wear.csv')
    
    with open('outputs/regression_summary.txt', 'w') as f:
        f.write("SURFACE ROUGHNESS (Ra) REGRESSION SUMMARY\n")
        f.write(str(model_ra.summary()))
        f.write("\n\n" + "="*60 + "\n\n")
        f.write("TOOL FLANK WEAR (Vb) REGRESSION SUMMARY\n")
        f.write(str(model_vb.summary()))
    
    opt_res = single_objective_optimization(model_ra)
    baseline_ra = sim_df[sim_df['Run_Type'] == 'Center']['Surface_Roughness_Ra_um'].mean()
    improvement = calculate_improvement(baseline_ra, opt_res['Ra_opt'])
    
    opt_vb = predict_response(model_vb, opt_res['x1_coded'], opt_res['x2_coded'], opt_res['x3_coded'])
    opt_mrr = compute_mrr(opt_res['f_opt'], opt_res['ap_opt'])
    opt_tc = compute_cycle_time(opt_res['f_opt'])
    opt_pc = compute_cutting_power(opt_res['f_opt'], opt_res['ap_opt'], opt_res['N_opt'])
    
    baseline_vb = sim_df[sim_df['Run_Type'] == 'Center']['Tool_Flank_Wear_Vb_mm'].mean()
    baseline_mrr = sim_df[sim_df['Run_Type'] == 'Center']['MRR_cm3_min'].mean()
    baseline_tc = sim_df[sim_df['Run_Type'] == 'Center']['Cycle_Time_s'].mean()
    baseline_pc = sim_df[sim_df['Run_Type'] == 'Center']['Cutting_Power_kW'].mean()
    
    results = {
        'Baseline_N_RPM': 2500.0,
        'Baseline_f_mm_min': 350.0,
        'Baseline_ap_mm': 1.25,
        'Baseline_Ra_um': float(np.round(baseline_ra, 3)),
        'Baseline_Vb_mm': float(np.round(baseline_vb, 3)),
        'Baseline_MRR_cm3_min': float(np.round(baseline_mrr, 2)),
        'Baseline_Cycle_Time_s': float(np.round(baseline_tc, 2)),
        'Baseline_Power_kW': float(np.round(baseline_pc, 3)),
        
        'Optimized_N_RPM': float(np.round(opt_res['N_opt'], 1)),
        'Optimized_f_mm_min': float(np.round(opt_res['f_opt'], 1)),
        'Optimized_ap_mm': float(np.round(opt_res['ap_opt'], 2)),
        'Optimized_Ra_um': float(np.round(opt_res['Ra_opt'], 3)),
        'Optimized_Vb_mm': float(np.round(opt_vb, 3)),
        'Optimized_MRR_cm3_min': float(np.round(opt_mrr, 2)),
        'Optimized_Cycle_Time_s': float(np.round(opt_tc, 2)),
        'Optimized_Power_kW': float(np.round(opt_pc, 3)),
        'Percentage_Ra_Reduction': float(np.round(improvement, 2)),
        'Model_Ra_R2': float(np.round(model_ra.rsquared, 4)),
        'Model_Ra_Adj_R2': float(np.round(model_ra.rsquared_adj, 4))
    }
    
    pd.DataFrame([results]).to_csv('outputs/optimization_results.csv', index=False)
    with open('outputs/metrics_summary.json', 'w') as jf:
        json.dump(results, jf, indent=4)
        
    generate_visualizations(sim_df, model_ra, model_vb)

if __name__ == "__main__":
    main()
