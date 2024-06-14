from flask import Flask, jsonify, render_template
import tweepy
import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)

# 環境変数を読み込む
load_dotenv()

consumer_key = os.getenv('SOR5bJJqFOfiP9F9EZa5iQf7X')
consumer_secret = os.getenv('9sEVArXGpssZiz7y31ICTRJDhAeBEujz54emhCbBGGu2OMttqx')
access_token = os.getenv('1801256952384917504-tABureLlYhbDTfnaarso12GZcirbuY')
access_token_secret = os.getenv('qBoKTaj5wx0RIH0lnc9Z7mtY2Irx6P0LLFw5tEUzs7JSi')

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
