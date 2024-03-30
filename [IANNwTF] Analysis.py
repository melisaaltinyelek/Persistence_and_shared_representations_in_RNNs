#%%
# import necessary libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scipy.stats as stats
import matplotlib.pyplot as plt

# %%
# read data
df_AB = pd.read_csv("df_AB_all_accuracies_run1.csv")
df_AC = pd.read_csv("df_AC_all_accuracies_run1.csv")
df_loss_accuracies = pd.read_csv("loss_df_run1.csv")


# prepare data for analysis
df_AB.insert(0, "condition", ["A&B"] * len(df_AB))
df_AC.insert(0, "condition", ["A&C"] * len(df_AC))
df_concat = pd.concat([df_AB, df_AC], axis = 0)
df_concat.insert(0, "accuracy", list(df_loss_accuracies["accuracy"]) * 2)

# for analysis filter rows where accuracy is greater or equal than 0.9 = 90%
df_analysis = df_concat.loc[(df_concat["accuracy"]  >=  0.9)]
df_analysis = df_analysis.loc[:, ~df_analysis.columns.str.startswith('Un')]
df_analysis = df_analysis.loc[:, ~df_analysis.columns.str.startswith('in')]
df_analysis = pd.melt(df_analysis, id_vars='condition', value_vars=["val_acc_cuepos0" ,
"val_acc_cuepos1",	"val_acc_cuepos2",	"val_acc_cuepos3",	"val_acc_cuepos4",	"val_acc_cuepos5",	"val_acc_cuepos6",	"val_acc_cuepos7",	"val_acc_cuepos8",	"val_acc_cuepos9"])
df_analysis = df_analysis.rename(columns={"variable" : "cue_position", "value" : "accuracy"})
#%%
# (Two-Way ANOVA (Typ III)) .. levene test ist missing
model = ols('accuracy ~ C(condition) + C(cue_position) + C(condition):C(cue_position)', data=df_analysis).fit()
sm.stats.anova_lm(model, typ=3)
#%%
# Two-sample t-test (Welch)
stats.ttest_ind(a=list(df_analysis.loc[df_analysis["condition"] == "A&B"]["accuracy"]), b=list(df_analysis.loc[df_analysis["condition"] == "A&C"]["accuracy"]), equal_var= False)
# %%
# create boxplot
df_analysis.boxplot(column=['accuracy'], by='condition', grid=False, color='black')
# np.var(df_analysis.loc[df_analysis["condition"] == "A&B"]["accuracy"])
# np.var(df_analysis.loc[df_analysis["condition"] == "A&C"]["accuracy"])
# %%
df_analysis.boxplot(column=['accuracy'], by='cue_position', grid=False, color='black', rot= 90)

# %%
