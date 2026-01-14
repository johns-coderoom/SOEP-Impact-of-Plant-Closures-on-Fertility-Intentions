import pandas as pd
import numpy as np 
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt

df = pd.read_csv("soep_microdata.csv")

df = df.set_index(["pid", "syear"]).sort_index()

# sex: 1 = male, 2 = female
df["female"] = (df["sex"] == 2).astype(int)

df["fertility_intent"] = df["plb0031"].replace({
    1: 1,   # yes
    2: 0,   # no
    3: np.nan
})

df["plant_closure"] = (df["plb0304"] == 5).astype(int)

# Lag exposure so shock precedes intention change
df["plant_closure_lag"] = df.groupby(level=0)["plant_closure"].shift(1)

df["age_sq"] = df["age"] ** 2

# Partner in household (SOEP standard)
df["partner"] = df["partner"].fillna(0)

# Number of children
df["kids"] = df["kids"].fillna(0)

# Log household income
df["ln_hinc"] = np.log(df["hinc"].replace(0, np.nan))

df["closure_female"] = df["plant_closure_lag"] * df["female"]

controls = ["age", "age_sq", "kids", "partner", "ln_hinc"]

import pandas as pd
from linearmodels.panel import PanelOLS

# 1. Create the interaction term
df["closure_female"] = df["plant_closure_lag"] * df["female"]

# 2. Define your variables
# NOTE: 'age' is usually perfectly collinear with Time Effects. 
# If it keeps crashing, remove 'age' and 'age_sq' from this list.
controls = ["age_sq", "kids", "partner", "ln_hinc"] 
exog_vars = ["plant_closure_lag", "closure_female"] + controls

# 3. Drop missing values BEFORE running the model to stop the Warning
# This ensures the model only sees 'clean' data
modeling_df = df[["fertility_intent"] + exog_vars].dropna()

import pandas as pd
from linearmodels.panel import PanelOLS

# 1. Prepare data and drop NaNs to avoid the MissingValueWarning
df["closure_female"] = df["plant_closure_lag"] * df["female"]
controls = ["age", "age_sq", "kids", "partner", "ln_hinc"]
exog_vars = ["plant_closure_lag", "closure_female"] + controls

# Drop NaNs before modeling
modeling_df = df[["fertility_intent"] + exog_vars].dropna()

# 2. Define the model
# PLACE drop_absorbed=True HERE
model = PanelOLS(
    modeling_df["fertility_intent"],
    modeling_df[exog_vars],
    entity_effects=True,
    time_effects=True,
    drop_absorbed=True  # Correct location
)

# 3. Fit the model
# Only clustering arguments go here
results = model.fit(
    cov_type="clustered",
    cluster_entity=True
)

print(results.summary)

df_reset = df.reset_index()

closure_year = (
    df_reset[df_reset["plant_closure"] == 1]
    .groupby("pid")["syear"]
    .min()
)

df["closure_year"] = df.index.get_level_values(0).map(closure_year)

df["event_time"] = df.index.get_level_values(1) - df["closure_year"]

for k in range(-5, 6):
    df[f"event_{k}"] = (df["event_time"] == k).astype(int)

event_terms = [f"event_{k}" for k in range(-5, 6) if k != -1]

event_model = PanelOLS(
    df["fertility_intent"],
    df[event_terms],
    entity_effects=True,
    time_effects=True
)

event_results = event_model.fit(
    cov_type="clustered",
    cluster_entity=True
)

print(event_results.summary)

coefs = event_results.params
ses = event_results.std_errors

event_times = [int(v.split("_")[1]) for v in coefs.index]

plt.figure(figsize=(8,5))
plt.errorbar(
    event_times,
    coefs,
    yerr=1.96 * ses,
    fmt="o"
)
plt.axhline(0, linestyle="--")
plt.axvline(0, linestyle=":")
plt.xlabel("Years Relative to Plant Closure")
plt.ylabel("Effect on Fertility Intentions")
plt.title("SOEP Event Study: Plant Closure")
plt.show()




    
