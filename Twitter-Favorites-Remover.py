# coding: utf-8

import tweepy
import webbrowser
import sys
import time
import os
from tqdm import tqdm

consumer_key = ''
consumer_secret = ''
callback_url = 'oob'

favorites_count_tmp = 0
pages = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

auth_url = auth.get_authorization_url()
webbrowser.open(auth_url)

verifier = input('\nPlease authenticate your account and get a PIN\nアカウントを認証してPINを取得してください\nPIN: ').strip()
auth.get_access_token(verifier)

auth.set_access_token(auth.access_token, auth.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=10800)
screen_name = api.me().screen_name
print('\nThe following users have been authenticated\n以下のユーザーが認証されました\n@' + screen_name + '\n')

user　=　api.get_user(screen_name = screen_name)
print('Number of favorite\nいいね数\n' + str(user.favourites_count))
favorites_count_tmp = user.favourites_count

print('\n*!W A R N I N G!*\nAre you sure you want to remove all your favorites?\nいいねをすべて削除しますがよろしいですか？')
yorn = input('y/n\n').strip()

if yorn == 'n':
    print('\nExit the tool\nツールを終了します')
    time.sleep(2)
    sys.exit()

progress_bar = tqdm(total = favorites_count_tmp)
progress_bar.set_description('Removing... ')

while favorites_count_tmp > 0:

    for page in pages:
        tweets=api.favorites(screen_name=screen_name, count=200, page=page)

        for tweet in tweets:
            
            while True:
                try:
                    api.destroy_favorite(tweet.id)
                    break
                except TimeoutError:
                    pass

            progress_bar.update(1)
            time.sleep(0.05)

    user = api.get_user(screen_name = screen_name)
    favorites_count_tmp = user.favourites_count

print('\nComplete\n削除が完了しました')

os.system('PAUSE')

print('\nExit the tool\nツールを終了します')
time.sleep(3)
