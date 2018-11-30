#!/usr/bin/env python
# encoding: utf-8
#Author - Yang Qiao


import tweepy #https://github.com/tweepy/tweepy
from tweepy import OAuthHandler
import json
import argparse
import sys
import os
import io
import wget
from PIL import Image, ImageDraw, ImageFont

import pymysql
import pymongo
from datetime import datetime
password="qiaoyang"

from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

#Twitter API credentials
consumer_key = "YaHG1WVffVICbhT0Zyi65VKsE"
consumer_secret = "256c1pO658imTmcHzbKFlOe1ZT7r1pfvuaFLWiBwaqMeNqKUv5"
access_key = "1039159247630753792-Yr53oPgqfOpZyfXL4aeqZqANZm25Nb"
access_secret = "ve4FG58q1n7plXNFg6fQCDgN3Zz67l7Ug09N1Cnf5ZwR1"

#connect to mysql
try:
    db = pymysql.connect("localhost","root", password,"miniproj_database");
except Exception as e:
    print("Connection failed!")
    raise e

       
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


#define the contents you need to download
def parse_arguments():
    parser = argparse.ArgumentParser(description='Download images from Twitter')
    parser.add_argument('--username',type=str , help='the twitter name ')
    parser.add_argument('--num', type=int, default=10, help='number of tweets to get')
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
        for media_url in tweet_media_urls(tweet_status):
            file_name = str(count) + ".jpg"
            wget.download(media_url, out=folder+'/'+file_name)
            count+= 1
    imgLog="{0} imgs have been download!".format(count)

    #mysql user information
    cursor=db.cursor()
    sql = """INSERT INTO user(twt_id,log) VALUES (%s, %s)"""
    try:
        cursor.execute(sql,(username,imgLog))
        db.commit()
    except:
        db.rollback()


# python input
arguments = parse_arguments()
username = arguments.username
number = arguments.num
folder= arguments.folder
download_images(api, username, number, folder)

def labelPics(path):
    pathName = path
    paths = "images/"+path
    # The name of the image file to annotate
    file_name = os.path.join(
    os.path.dirname(__file__),paths)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
   
    try:
        db=pymysql.connect("localhost","root",password,"miniproj_database")
    except Exception as e:
        print("Connection failed!")
        raise e
    cursor=db.cursor()
    sql="INSERT INTO label(username,labels) VALUES(%s,%s)"
    for label in labels:
        try:
            cursor.execute(sql,(username,label.description))
            db.commit()
        except:
            db.rollback()

    print("Data stored sucessfully!")

    #draw labels
    font=ImageFont.truetype("FreeMono.ttf", 30)

    imageFile=paths
    im1=Image.open(imageFile)

    draw=ImageDraw.Draw(im1)
    i=0
    for label in labels:
        draw.text((0,i),label.description,(255,255,0),font=font)
        i+=30
    draw=ImageDraw.Draw(im1)
    im1.save("./labeledImgs/"+pathName)

dirs=os.listdir("./images/")
dirs.sort()

for filesDir in dirs:
    labelPics(filesDir)
