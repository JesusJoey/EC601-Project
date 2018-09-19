#!/bin/bash
#Copyright:Yang Qiao
#Step1:donwload images from a twitter acount to your directory, you can choose the user as well as the number of pictures
python tweepy_hw1.py --username kobebryant --num 100 --folder images

#Step2:convert images into video; setup some parameters
ffmpeg -f image2 -r 1/5 -i /Users/joe/Desktop/BU_2018_fall/EC601/images/%02d.jpg -vcodec libx264 -pix_fmt yuv420p out.mp4

#Step3:get credentials for Google API
export GOOGLE_APPLICATION_CREDENTIALS="My_First_Project-8e0370d1243f.json"

#Step3:using Google_Vision API to describe the content to the images
python google_vision.py
