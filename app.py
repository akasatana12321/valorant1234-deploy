from flask import Flask, jsonify, render_template
import tweepy
import datetime
from dotenv import load_dotenv
import os
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# 環境変数を読み込む
load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# ログに環境変数を出力
logging.info(f"CONSUMER_KEY: {consumer_key}")
logging.info(f"CONSUMER_SECRET: {consumer_secret}")
logging.info(f"ACCESS_TOKEN: {access_token}")
logging.info(f"ACCESS_TOKEN_SECRET: {access_token_secret}")
logging.info(f"BEARER_TOKEN: {bearer_token}")

client = tweepy.Client(bearer_token=bearer_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    try:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        date_since = yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')

        query = '#VALORANT lang:ja -is:retweet'
        response = client.search_recent_tweets(query=query, start_time=date_since, max_results=100, tweet_fields=['created_at', 'public_metrics'])

        sorted_tweets = sorted(response.data, key=lambda tweet: tweet.public_metrics['like_count'], reverse=True)

        tweet_data = [{
            'user': tweet.author_id,
            'text': tweet.text,
            'likes': tweet.public_metrics['like_count'],
            'id': tweet.id
        } for tweet in sorted_tweets]

        return jsonify(tweet_data)
    except tweepy.TweepyException as e:
        logging.error(f"Error fetching tweets: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
