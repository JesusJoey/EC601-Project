#!/usr/bin/env python
# encoding: utf-8
#Author - Yang Qiao


import tweepy #https://github.com/tweepy/tweepy
from tweepy import OAuthHandler
import json
import argparse
import os
import wget

#Twitter API credentials
consumer_key = "YaHG1WVffVICbhT0Zyi65VKsE"
consumer_secret = "256c1pO658imTmcHzbKFlOe1ZT7r1pfvuaFLWiBwaqMeNqKUv5"
access_key = "1039159247630753792-Yr53oPgqfOpZyfXL4aeqZqANZm25Nb"
access_secret = "ve4FG58q1n7plXNFg6fQCDgN3Zz67l7Ug09N1Cnf5ZwR1"
       
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#define the contents you need to download
def parse_arguments():
    parser = argparse.ArgumentParser(description='Download images from Twitter')
    parser.add_argument('--username',type=str , help='the twitter name ')
    parser.add_argument('--num', type=int, default=100, help='number of tweets to get')
    parser.add_argument('--folder', default='images', type=str, help='folder to store images')
    args = parser.parse_args()
    return args

#aquire the status in json created by the tweepyAPI
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

#get media_url in the json
def tweet_media_urls(tweet_status):
  media = tweet_status._json.get('extended_entities', {}).get('media', [])
  if (len(media) == 0):
    return []
  else:
    return [item['media_url'] for item in media]

#donwload images from twitter acoounts
def download_images(api, username, number, folder):
    status = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items()
    os.makedirs(folder)
    count = 0
    for tweet_status in status:
        if (count >= number):
            break
        i = 0
        for media_url in tweet_media_urls(tweet_status):
            file_name = str(count) + ".jpg"
            wget.download(media_url, out=folder+'/'+file_name)
            count+= 1
# python input
arguments = parse_arguments()
username = arguments.username
number = arguments.num
folder= arguments.folder
download_images(api, username, number, folder)

       
 
