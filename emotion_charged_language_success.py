from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import json

# Load the pre-trained emotion analysis pipeline
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

with open("final_campaign_data.txt", "r") as file:
    data = json.load(file)

# Convert the JSON data to a Pandas DataFrame
campaigns = pd.DataFrame(data)

# Function to analyze emotions for a given description
def analyze_emotions(description):
    try:
        result = emotion_pipeline(description)
        # Return the emotion with the highest probability
        dominant_emotion = max(result, key=lambda x: x['score'])
        return dominant_emotion['label']
    except Exception as e:
        return "Error"

# Perform emotion analysis on all campaign descriptions
campaigns["DominantEmotion"] = campaigns["Description"].apply(analyze_emotions)

# Categorize campaigns as emotionally charged or neutral
emotionally_charged_threshold = 0.3
campaigns["EmotionCategory"] = campaigns["DominantEmotion"].apply(
    lambda x: "Neutral" if x == "neutral" else "Emotionally Charged"
)

# Calculate success rates for each emotion
emotion_success = campaigns.groupby("DominantEmotion").agg(
    TotalCampaigns=("Success", "count"),
    SuccessfulCampaigns=("Success", "sum")
)
emotion_success["SuccessRate"] = (emotion_success["SuccessfulCampaigns"] / emotion_success["TotalCampaigns"]) * 100

# Visualize success rates by emotion
plt.figure(figsize=(10, 6))
emotion_success["SuccessRate"].sort_values(ascending=False).plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Success Rates by Dominant Emotion in Campaign Descriptions", fontsize=14)
plt.xlabel("Dominant Emotion", fontsize=12)
plt.ylabel("Success Rate (%)", fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
plt.show()

# Compare success rates between emotionally charged and neutral campaigns
category_success = campaigns.groupby("EmotionCategory").agg(
    TotalCampaigns=("Success", "count"),
    SuccessfulCampaigns=("Success", "sum")
)
category_success["SuccessRate"] = (category_success["SuccessfulCampaigns"] / category_success["TotalCampaigns"]) * 100

# Perform chi-square test to assess statistical significance
contingency_table = pd.crosstab(campaigns["EmotionCategory"], campaigns["Success"])
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Print results
print("Success Rates by Emotion Category:")
print(category_success)
print("\nChi-Square Test Results:")
print(f"Chi2 Statistic: {chi2:.3f}, p-value: {p:.3f}")
