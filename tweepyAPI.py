#!/usr/bin/env python
# encoding: utf-8
#Author - Yang Qiao


import tweepy #https://github.com/tweepy/tweepy
import json
import os
from skimage import io

#Twitter API credentials
consumer_key = "YaHG1WVffVICbhT0Zyi65VKsE"
consumer_secret = "256c1pO658imTmcHzbKFlOe1ZT7r1pfvuaFLWiBwaqMeNqKUv5"
access_key = "1039159247630753792-Yr53oPgqfOpZyfXL4aeqZqANZm25Nb"
access_secret = "ve4FG58q1n7plXNFg6fQCDgN3Zz67l7Ug09N1Cnf5ZwR1"


def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 15):
            break
        print ("...%s tweets downloaded so far" % (len(alltweets)))
       
    #write tweet objects to JSON
    file = open('tweet.json', 'w') 
    print ("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)

    #close the file
    print ("Done")
    file.close()

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@realDonaldTrump")
    #save the image from the URLs in json
    image1=io.imread('http://pbs.twimg.com/ext_tw_video_thumb/1041792175556763648/pu/img/ULdtURmfcW4UeTeh.jpg')
    io.imsave('/Users/joe/Downloads/img/1.jpg',image1)
    image2=io.imread('http://pbs.twimg.com/media/DnUN4tmX0AESUdj.jpg')
    io.imsave('/Users/joe/Downloads/img/2.jpg',image2)
    image3=io.imread('http://pbs.twimg.com/media/DnLtwQfWsAAlO-7.jpg')
    io.imsave('/Users/joe/Downloads/img/3.jpg',image3)
    image4=io.imread('http://abs.twimg.com/images/themes/theme1/bg.png')
    io.imsave('/Users/joe/Downloads/img/4.jpg',image4)
    image5=io.imread('https://abs.twimg.com/images/themes/theme2/bg.gif')
    io.imsave('/Users/joe/Downloads/img/5.jpg',image5)
    
