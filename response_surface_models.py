"""
Response Surface Regression & ANOVA Modeling Module
Author: Banoth Chandu Nayak (NIT Hamirpur)
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

def fit_quadratic_rsm(df, response_col='Surface_Roughness_Ra_um'):
    data = df.copy()
    data['X1_sq'] = data['X1_coded'] ** 2
    data['X2_sq'] = data['X2_coded'] ** 2
    data['X3_sq'] = data['X3_coded'] ** 2
    data['X1_X2'] = data['X1_coded'] * data['X2_coded']
    data['X1_X3'] = data['X1_coded'] * data['X3_coded']
    data['X2_X3'] = data['X2_coded'] * data['X3_coded']
    
    formula = (f"{response_col} ~ X1_coded + X2_coded + X3_coded + "
               f"X1_sq + X2_sq + X3_sq + X1_X2 + X1_X3 + X2_X3")
    
    model = ols(formula, data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return model, anova_table

def predict_response(model, x1, x2, x3):
    df_eval = pd.DataFrame({
        'X1_coded': [x1], 'X2_coded': [x2], 'X3_coded': [x3],
        'X1_sq': [x1**2], 'X2_sq': [x2**2], 'X3_sq': [x3**2],
        'X1_X2': [x1 * x2], 'X1_X3': [x1 * x3], 'X2_X3': [x2 * x3]
    })
    return float(model.predict(df_eval)[0])
