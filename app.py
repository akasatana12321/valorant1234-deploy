import tweepy
import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# 環境変数からAPIキーとトークンを取得
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

logger.info(f"CONSUMER_KEY: {consumer_key}")
logger.info(f"CONSUMER_SECRET: {consumer_secret}")
logger.info(f"ACCESS_TOKEN: {access_token}")
logger.info(f"ACCESS_TOKEN_SECRET: {access_token_secret}")

# Tweepyの認証
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    try:
        # ツイートを取得
        tweets = api.home_timeline(count=10)
        tweets_data = [{'text': tweet.text, 'created_at': tweet.created_at} for tweet in tweets]
        return jsonify(tweets_data)
    except tweepy.TweepError as e:
        logger.error(f"Error fetching tweets: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
