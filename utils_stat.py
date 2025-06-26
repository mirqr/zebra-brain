from matplotlib.pylab import exp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import kruskal, f_oneway
from sklearn import experimental
import statsmodels.stats.multicomp as mc
from statsmodels.stats.multitest import multipletests

def kruskal_wallis_anova(df, experiment_folder=".", kind=None):
    assert kind != None, "kind must be specified"

    # Strip leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # List of brain region columns (excluding 'name' and 'group')
    roi_cols = [col for col in df.columns if col.startswith("Reg")]

    # Run Kruskal-Wallis test for each brain region
    kruskal_results = []
    for col in roi_cols:
        groups = [group[col].dropna().values for name, group in df.groupby("group")] 
        stat, p = kruskal(*groups)
        stat_an, p_an = f_oneway(*groups) # anova 
        kruskal_results.append({"Region": col, "Kruskal_Stat": stat, "p_value": p, "anova_stat": stat_an, "anova_p_value": p_an})
        
        #kruskal_results.append({"Region": col, "Kruskal_Stat": stat, "p_value": p})


    kruskal_df = pd.DataFrame(kruskal_results)

    # Apply Benjamini-Hochberg FDR correction
    kruskal_df["p_adj"] = multipletests(kruskal_df["p_value"], method="fdr_bh")[1]
    kruskal_df["Significant_kruskal"] = kruskal_df["p_adj"] < 0.05
    kruskal_df["Significant_anova"] = kruskal_df["anova_p_value"] < 0.05

    # write 
    num = len(roi_cols)
    #kruskal_df.to_csv(f"{experiment_folder}/kruskal_anova_results_{kind}_{num}.csv", index=False)
    # excel 
    kruskal_df.to_excel(f"{experiment_folder}/kruskal_anova_results_{kind}_{num}.xlsx", index=False)

    return kruskal_df
    # difference between kruskal and anova is 


from scipy.stats import mannwhitneyu
from itertools import combinations
from statsmodels.stats.multitest import fdrcorrection

def pairwise_mannwhitneyu(df, experiment_folder=".", kind=None):
    assert kind != None, "kind must be specified"

    # Prepare long-form DataFrame again
    df_long = df.melt(id_vars=["name", "group"], var_name="Region", value_name="Activity")

    # Get all pairwise genotype combinations
    genotype_pairs = list(combinations(df["group"].unique(), 2))

    # Perform pairwise Mann-Whitney U tests for each brain region
    results = []
    for region in df_long["Region"].unique():
        region_data = df_long[df_long["Region"] == region]
        for g1, g2 in genotype_pairs:
            data1 = region_data[region_data["group"] == g1]["Activity"]
            data2 = region_data[region_data["group"] == g2]["Activity"]
            stat, p = mannwhitneyu(data1, data2, alternative="two-sided")
            results.append({
                "Region": region,
                "Group1": g1,
                "Group2": g2,
                "U_stat": stat,
                "p_value": p
            })

    # Convert to DataFrame and adjust p-values
    # same as fdrcorrection but more options
    pairwise_df = pd.DataFrame(results)
    pairwise_df["p_adj"] = multipletests(pairwise_df["p_value"], method="fdr_bh")[1]
    
    # FDR correction 
    #fdr_results = fdrcorrection(pairwise_df["p_value"], alpha=0.05)
    #pairwise_df["FDR_p"] = fdr_results[1]
    #pairwise_df["Significant_FDR"] = fdr_results[0]

    pairwise_df["Significant"] = pairwise_df["p_adj"] < 0.05

    # sort 
    pairwise_df = pairwise_df.sort_values(by="p_adj")

    # write
    num = len(df_long["Region"].unique())
    #pairwise_df.to_csv(f"{experiment_folder}/pairwise_mannwhitneyu_results_{kind}_{num}.csv", index=False)
    # excel
    pairwise_df.to_excel(f"{experiment_folder}/pairwise_mannwhitneyu_results_{kind}_{num}.xlsx", index=False)

    return pairwise_df


def box_plot(df, experiment_folder='.', kind = None):
    # assert 
    assert kind in ['roi', 'vol'], 'kind must be roi or vol'
    # Calculate summary statistics by group for each brain region
    brain_regions = [col for col in df.columns if col.startswith('Reg')]


    # 1. Box plots for each brain region by group

    #plt.figure(figsize=(18, 12))
    # do 8 by 8
    chunks = [ brain_regions[i:i + 8] for i in range(0, len(brain_regions), 8) ]
    for i, chunk in enumerate(chunks):
        plt.figure(figsize=(18, 12))
        for j, region in enumerate(chunk):
            plt.subplot(2, 4, j+1)
            sns.boxplot(x='group', y=region, data=df, showmeans=True, hue='group')
            plt.title(f"{region}")
        plt.tight_layout()
        if kind == None:
            plt.show()
        else:
            plt.savefig(f'{experiment_folder}/boxplots_{kind}_{len(brain_regions)}_{i}.png')


# non usare per ora
def box_plot_long(df):
    brain_regions = [col for col in df.columns if col.startswith('Reg')]
    num_regions = len(brain_regions)
    chunks = [ brain_regions[i:i + 8] for i in range(0, len(brain_regions), 8) ]
    for i, chunk in enumerate(chunks):
        df_temp = df[['name', 'group'] + chunk]
        df_long = df_temp.melt(id_vars=["name", "group"], 
                  var_name="Region", 
                  value_name="Activity")
        plt.figure(figsize=(14, 8))
        sns.boxplot(data=df_long, x="Region", y="Activity", hue="group")
        plt.xticks(rotation=45)
        # add grid 
        plt.grid(True)
        #plt.title(f"Brain Region Activity by Genotype {i}")
    plt.tight_layout()
    plt.show()
