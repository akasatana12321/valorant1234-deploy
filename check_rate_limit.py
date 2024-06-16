from dotenv import load_dotenv
import os
import tweepy
import logging

# .envファイルを読み込む
load_dotenv()

# 環境変数からAPIキーとトークンを取得
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# ログ設定
logging.basicConfig(level=logging.INFO)
logging.info(f"CONSUMER_KEY: {consumer_key}")
logging.info(f"CONSUMER_SECRET: {consumer_secret}")
logging.info(f"ACCESS_TOKEN: {access_token}")
logging.info(f"ACCESS_TOKEN_SECRET: {access_token_secret}")
logging.info(f"BEARER_TOKEN: {bearer_token}")

# クライアントを初期化
client = tweepy.Client(bearer_token=bearer_token)

# レートリミットの状況を確認
try:
    response = client.get_user(username='TwitterDev')
    rate_limit_status = response.headers['x-rate-limit-remaining']
    print(f"Rate limit remaining: {rate_limit_status}")
except tweepy.errors.Forbidden as e:
    logging.error(f"Error fetching tweets: {e}")

