import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr


with open("final_campaign_data.txt", "r") as file:
    data = json.load(file)

# Convert the JSON data to a Pandas DataFrame
campaigns = pd.DataFrame(data)

def RQ1():
    # Define goal ranges for grouping
    bins = [0, 1000, 10000, 50000, 100000, 500000, 1000000, float('inf')]
    labels = ["0–1k", "1k–10k", "10k–50k", "50k–100k", "100k–500k", "500k–1M", "1M+"]

    # Add a goal range column
    campaigns["GoalRange"] = pd.cut(campaigns["GoalAmount"], bins=bins, labels=labels, right=False)

    # # Group by goal range and calculate success rates
    grouped = campaigns.groupby("GoalRange").agg(
        TotalCampaigns=("success", "count"),
        SuccessfulCampaigns=("success", "sum")
    )
    grouped["SuccessRate"] = (grouped["SuccessfulCampaigns"] / grouped["TotalCampaigns"]) * 100

    # # Reset index for easier plotting
    grouped = grouped.reset_index()

    # Visualization
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        data=grouped, x="GoalRange", y="SuccessRate", palette="viridis", edgecolor="black"
    )

    # Add labels to the bars
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            p.get_x() + p.get_width() / 2,  # X-coordinate: Center of the bar
            height + 1,  # Y-coordinate: Slightly above the bar
            f'{height:.1f}%',  # Text to display
            ha="center", va="bottom", fontsize=10, color="black"
        )

    # Plot aesthetics
    plt.title("Success Rates by Goal Amount Range", fontsize=16)
    plt.xlabel("Goal Amount Range", fontsize=14)
    plt.ylabel("Success Rate (%)", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# Define the Spearman rank correlation function
def compute_spearman_correlation(x, y):
    """
    Computes the Spearman rank correlation coefficient between two lists.

    Args:
        x (list): List of x-values.
        y (list): List of y-values.

    Returns:
        float: Spearman rank correlation coefficient.
        float: p-value for the test.
    """
    spearman_corr, p_value = spearmanr(x, y)
    return spearman_corr, p_value


# Define the Pearson correlation function
def compute_pearson_correlation(x, y):
    """
    Computes the Pearson correlation coefficient between two lists.

    Args:
        x (list): List of x-values.
        y (list): List of y-values.

    Returns:
        float: Pearson correlation coefficient.
        float: p-value for the test.
    """
    pearson_corr, p_value = pearsonr(x, y)
    return pearson_corr, p_value


# labels = ["0–1k", "1k–10k", "10k–50k", "50k–100k", "100k–500k", "500k–1M", "1M+"]
# Prepare data based on the plot you provided
goal_ranges = [500, 5000, 30000, 75000, 300000, 750000, 1500000]  # Approximate midpoints of goal ranges
success_rates = [41.2, 23.1, 19.2, 9.9, 6.7, 2.3, 0.0]  # Success rates from the plot

# Call the Spearman rank correlation function
spearman_corr, spearman_p = compute_spearman_correlation(goal_ranges, success_rates)
print(f"Spearman Rank Correlation: {spearman_corr:.3f}, p-value: {spearman_p:.3f}")

# Call the Pearson correlation function
pearson_corr, pearson_p = compute_pearson_correlation(goal_ranges, success_rates)
print(f"Pearson Correlation: {pearson_corr:.3f}, p-value: {pearson_p:.3f}")


# RQ1()
    