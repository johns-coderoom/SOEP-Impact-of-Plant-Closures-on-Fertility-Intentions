# SOEP-Impact-of-Plant-Closures-on-Fertility-Intentions
# Impact of Plant Closures on Fertility Intentions

## 📋 Project Description
This repository contains the analysis for my Summer 2026 internship project investigating the relationship between economic shocks and reproductive behavior. 

Using panel data, this study estimates the impact of **plant closures** (a proxy for exogenous economic displacement) on individual **fertility intentions**. The goal is to determine if job insecurity creates a "wait-and-see" effect on family planning.


<img width="800" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/41cc78ce-ab03-409f-ab2c-a13a366f1415" />

## 🔬 Econometric Model
The analysis employs a **Twoway Fixed Effects (TWFE)** model to control for time-invariant individual characteristics and common macro-economic shocks.



**Model Equation:**
- **Dependent Variable:** Fertility Intentions (Ordinal/Scale)
- **Main Predictor:** `plant_closure_lag` (1-year lag of closure event)
- **Interaction:** `closure_female` (Gender-specific impact)
- **Controls:** Age, Number of Kids, Partner Status, and Household Income.

## 🛠️ Installation & Setup
To reproduce this analysis, you will need Python 3.x and the following libraries:

```bash
pip install pandas linearmodels matplotlib
