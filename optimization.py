"""
Numerical Optimization Module
Author: Banoth Chandu Nayak (NIT Hamirpur)
"""

from scipy.optimize import minimize
from src.response_surface_models import predict_response

def single_objective_optimization(model_ra):
    def objective(x):
        return predict_response(model_ra, x[0], x[1], x[2])
    
    x0 = [0.0, 0.0, 0.0]
    bounds = [(-1.0, 1.0), (-1.0, 1.0), (-1.0, 1.0)]
    res = minimize(objective, x0, method='SLSQP', bounds=bounds)
    
    x1_opt, x2_opt, x3_opt = res.x
    n_opt = 2500 + x1_opt * 500
    f_opt = 350 + x2_opt * 150
    ap_opt = 1.25 + x3_opt * 0.50
    ra_opt = res.fun
    
    return {
        'x1_coded': x1_opt, 'x2_coded': x2_opt, 'x3_coded': x3_opt,
        'N_opt': n_opt, 'f_opt': f_opt, 'ap_opt': ap_opt,
        'Ra_opt': ra_opt
    }

def calculate_improvement(baseline_ra, optimized_ra):
    return ((baseline_ra - optimized_ra) / baseline_ra) * 100.0
