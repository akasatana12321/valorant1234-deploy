from flask import Flask, redirect, url_for, request, session, jsonify, render_template
import tweepy
import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 環境変数を読み込む
load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, callback='http://127.0.0.1:5000/callback')
client = tweepy.Client(bearer_token=bearer_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.TweepyException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/callback')
def callback():
    try:
        request_token = session.pop('request_token')
        auth.request_token = request_token
        verifier = request.args.get('oauth_verifier')
        auth.get_access_token(verifier)
        api = tweepy.API(auth)
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        return redirect(url_for('index'))
    except tweepy.TweepyException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tweets', methods=['GET'])
def get_tweets():
    try:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        date_since = yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')

        query = '#VALORANT lang:ja -is:retweet'
        response = client.search_recent_tweets(query=query, start_time=date_since, max_results=100, tweet_fields=['created_at', 'public_metrics'])

        if response.data:
            sorted_tweets = sorted(response.data, key=lambda tweet: tweet.public_metrics['like_count'], reverse=True)
            tweet_data = [{
                'user': tweet.author_id,
                'text': tweet.text,
                'likes': tweet.public_metrics['like_count'],
                'id': tweet.id
            } for tweet in sorted_tweets]

            return jsonify(tweet_data)
        else:
            return jsonify([])
    except tweepy.Forbidden as e:
        return jsonify({"error": "Access forbidden: " + str(e)}), 403
    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
