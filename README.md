YouTube Sentiment Analyzer

Fetch YouTube comments and run sentiment analysis (VADER + TextBlob), producing CSV outputs and charts.

What it does
- Authenticates with Google OAuth (Testing mode)
- Lists your channel and latest uploads
- Downloads comments for any video(s)
- Analyzes sentiment per comment
- Exports:
  - youtube_comments.csv
  - youtube_comments_with_sentiment.csv
  - yt_sentiment_bar.png (class distribution)
  - yt_sentiment_trend.png (daily sentiment trend)

Tech
- Python, Google API Client, OAuth
- YouTube Data API v3
- NLP: NLTK VADER, TextBlob
- Pandas/Matplotlib/Seaborn for analysis & charts

Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Authenticate
python3 save_token.py

Usage
List latest uploads:
python3 auth_and_list.py

Fetch comments (replace VIDEO_ID):
python3 fetch_comments.py VIDEO_ID 1000

Analyze & generate charts:
python3 analyze_sentiment.py

Repo structure
auth_and_list.py
fetch_comments.py
analyze_sentiment.py
save_token.py
video_stats.py
requirements.txt
.gitignore
README.md
