import pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk, os

nltk.download("vader_lexicon", quiet=True)
sns.set()

# Load comments
if not os.path.exists("youtube_comments.csv"):
    raise SystemExit("youtube_comments.csv not found. Run fetch_comments.py first.")

df = pd.read_csv("youtube_comments.csv")
if df.empty:
    raise SystemExit("youtube_comments.csv is empty.")

# Clean text
df["text"] = df["text"].fillna("").astype(str)

# Run VADER
sia = SentimentIntensityAnalyzer()
df["vader"] = df["text"].apply(lambda t: sia.polarity_scores(t)["compound"])
df["label"] = pd.cut(
    df["vader"],
    bins=[-1, -0.05, 0.05, 1],
    labels=["negative","neutral","positive"]
)

# Run TextBlob
df["tb_polarity"] = df["text"].apply(lambda t: TextBlob(t).sentiment.polarity)

# Save results
df.to_csv("youtube_comments_with_sentiment.csv", index=False)

# Plot bar distribution
plt.figure()
df["label"].value_counts().reindex(["positive","neutral","negative"]).plot(kind="bar", color=["green","gray","red"])
plt.title("YouTube Sentiment Distribution")
plt.xlabel("Sentiment"); plt.ylabel("Count")
plt.tight_layout(); plt.savefig("yt_sentiment_bar.png", dpi=160)

# Plot daily trend (if dates exist)
if "published_at" in df.columns:
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    daily = df.dropna(subset=["published_at"]).groupby(df["published_at"].dt.date)["vader"].mean()
    if not daily.empty:
        plt.figure()
        daily.plot(marker="o")
        plt.axhline(0, linestyle="--", color="black")
        plt.title("YouTube Sentiment Trend (VADER)")
        plt.xlabel("Date"); plt.ylabel("Mean Sentiment")
        plt.tight_layout(); plt.savefig("yt_sentiment_trend.png", dpi=160)

print("Analysis complete. Files saved:")
print("- youtube_comments_with_sentiment.csv")
print("- yt_sentiment_bar.png")
print("- yt_sentiment_trend.png (if dates available)")
