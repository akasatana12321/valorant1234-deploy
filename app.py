from flask import Flask, jsonify, render_template
import tweepy
import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)

# 環境変数を読み込む
load_dotenv()

# デバッグ用プリント
print("Checking environment variables...")
print(f"CONSUMER_KEY: {os.getenv('CONSUMER_KEY')}")
print(f"CONSUMER_SECRET: {os.getenv('CONSUMER_SECRET')}")
print(f"ACCESS_TOKEN: {os.getenv('ACCESS_TOKEN')}")
print(f"ACCESS_TOKEN_SECRET: {os.getenv('ACCESS_TOKEN_SECRET')}")

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# 読み込まれた環境変数を確認するためのデバッグプリント
print(f"Consumer Key: {consumer_key}")
print(f"Consumer Secret: {consumer_secret}")
print(f"Access Token: {access_token}")
print(f"Access Token Secret: {access_token_secret}")

# 環境変数が正しく設定されているか確認
if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
    print("One or more environment variables are not set. Check your .env file and ensure it is located in the correct directory.")
    exit(1)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    date_since = yesterday.strftime('%Y-%m-%d')

    tweets = api.search_tweets(q='#VALORANT filter:videos', lang='ja', since=date_since, count=100)
    sorted_tweets = sorted(tweets, key=lambda tweet: tweet.favorite_count, reverse=True)

    tweet_data = [{
        'user': tweet.user.screen_name,
        'text': tweet.text,
        'likes': tweet.favorite_count,
        'id': tweet.id_str
    } for tweet in sorted_tweets]

    return jsonify(tweet_data)

if __name__ == '__main__':
    app.run(debug=True)
