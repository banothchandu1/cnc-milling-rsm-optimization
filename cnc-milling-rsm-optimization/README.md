# Optimization of Machining Parameters in CNC Milling Using Response Surface Methodology (RSM)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Institution: NIT Hamirpur](https://img.shields.io/badge/NIT%20Hamirpur-Mechanical%20Eng-green.svg)](https://nith.ac.in)

**Author:** Banoth Chandu Nayak  
**Department:** Mechanical Engineering, National Institute of Technology Hamirpur  
**Domain:** Manufacturing Engineering, CNC Machining Optimization, Design of Experiments (DOE)  
**Academic Period:** January 2026 – May 2026  

---

## 📌 Project Overview
This repository provides an autonomous, computationally reproducible Response Surface Methodology (RSM) and Central Composite Design (CCD) framework for dry end-milling of structural alloy steel (AISI 4340 annealed, 32 HRC) using TiAlN-coated solid carbide end-mills.

The primary objective is the multi-factor optimization of machining parameters:
* **Spindle Speed ($N$):** 2000 – 3000 RPM
* **Feed Rate ($f$):** 200 – 500 mm/min
* **Axial Depth of Cut ($a_p$):** 0.75 – 1.75 mm

The model targets arithmetic mean surface roughness ($R_a$), while monitoring tool flank wear ($V_b$), material removal rate (MRR), cycle time ($t_c$), and spindle cutting power ($P_c$).

---

## 🎯 Key Results & 14% Surface Roughness Improvement

| Performance Indicator | Baseline (Center Point) | Optimized Condition | Delta ($\Delta$) | Physical Consequence |
| :--- | :---: | :---: | :---: | :--- |
| **Spindle Speed ($N$)** | $2500	ext{ RPM}$ | **$2800	ext{ RPM}$** | $+12.0\%$ | Elevated cutting temperature, suppresses BUE |
| **Feed Rate ($f$)** | $350	ext{ mm/min}$ | **$250	ext{ mm/min}$** | $-28.6\%$ | Steep drop in kinematic peak-to-valley cusp height |
| **Depth of Cut ($a_p$)** | $1.25	ext{ mm}$ | **$1.05	ext{ mm}$** | $-16.0\%$ | Lower tool deflection force |
| **Surface Roughness ($R_a$)** | **$1.428	ext{ }\mu	ext{m}$** | **$1.228	ext{ }\mu	ext{m}$** | **$-14.01\%$** | **Target Achieved: $14.01\%$ Roughness Reduction** |
| **Tool Flank Wear ($V_b$)** | $0.152	ext{ mm}$ | **$0.161	ext{ mm}$** | $+5.9\%$ | Marginal thermal wear increase |
| **Material Removal Rate (MRR)** | $2.19	ext{ cm}^3/	ext{min}$ | **$1.31	ext{ cm}^3/	ext{min}$** | $-40.2\%$ | Surface quality prioritized over volume rate |
| **Cycle Time ($t_c$)** | $17.14	ext{ s}$ | **$24.00	ext{ s}$** | $+40.0\%$ | Cycle duration for 100 mm pass |
| **Spindle Cutting Power ($P_c$)** | $1.148	ext{ kW}$ | **$0.724	ext{ kW}$** | $-36.9\%$ | Lower energy footprint & spindle thermal stress |

$$	ext{Percentage Reduction} = rac{R_{a,	ext{baseline}} - R_{a,	ext{opt}}}{R_{a,	ext{baseline}}} 	imes 100\% = rac{1.428 - 1.228}{1.428} 	imes 100\% = \mathbf{14.01\%}$$

---

## 📐 Quadratic Response Surface Model

The fitted second-order regression model for surface roughness ($R_a$) in coded variables ($-1.682 \le X_i \le +1.682$):

$$R_a = 1.428 - 0.183 X_1 + 0.248 X_2 + 0.098 X_3 + 0.076 X_1^2 + 0.054 X_2^2 + 0.038 X_3^2 - 0.065 X_1 X_2 - 0.028 X_1 X_3 + 0.042 X_2 X_3$$

* **Model $F$-Statistic:** $98.54$ ($p < 0.0001$, highly significant)
* **$R^2$:** $0.9888$ | **Adjusted $R^2$:** $0.9788$

---

## 📊 Graphical Results

All plots are automatically generated in high resolution (`figures/`):
* `actual_vs_predicted_ra.png`: 1:1 parity scatter plot confirming adequacy.
* `residual_diagnostics.png`: Scatter plot confirming homoscedasticity and normality.
* `main_effects.png`: Individual parameter sensitivity slopes.
* `interaction_effects.png`: Feed rate $	imes$ Spindle speed interaction.
* `ra_3d_surface.png`: 3D response surface of roughness over the parameter domain.
* `ra_contour_plot.png`: Iso-roughness contour map showing baseline vs. optimum.
* `flank_wear_surface.png`: 3D response surface of progressive tool wear.

---

## 💻 Installation & Quickstart

```bash
# Clone your repository
git clone https://github.com/<YOUR-USERNAME>/cnc-milling-rsm-optimization.git
cd cnc-milling-rsm-optimization

# Install dependencies
pip install -r requirements.txt

# Run complete analysis pipeline
python main.py
```

---

## 🔬 Authenticity & Simulation Disclosure
All observations in `data/simulated_machining_data.csv` are generated using a physics-grounded synthetic cutting model calibrated to empirical literature for AISI 4340 dry end-milling. This project is a computational investigation.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
