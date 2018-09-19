# EC601-miniProject
## How to run this mini project
### Using tweepyAPI to download images
* In the tweepy python script, you need to input your consumer_key, consumer_secret, access_key, access_secret of your Twitter Development Account to get credentials.
* When you run tweepy_hw1.py, input *python tweepy_hw1.py --username kobebryant --num 100 --folder images* ,then you can download 100 pictures from KobeBryant's twitter into the folder named images.

### Using FFMPEG to convert images into a video
* In the command line,input: *ffmpeg -f image2 -r 1/5 -i /Users/joe/Desktop/BU_2018_fall/EC601/images/%02d.jpg -vcodec libx264 -pix_fmt yuv420p out.mp4*
* You need to include the directory of your images and I set some parameters of the video.

### Using Google Vision API to describe the contents
* To get credentials for Google Vision API, please input the following in the command line:  
*export GOOGLE_APPLICATION_CREDENTIALS="My_First_Project-8e0370d1243f.json"*  
* Using the API to describe the contents: in the command line,input:  
*python google_vision.py*

## Statements
* To make sure the project run succeffully, you need to pay attention to the directory beacause the images are downloaded to your present directory.
* All the command line statement can be found in bash.sh.
* Because the project has seperate tasks, I did not merge the python scripts to run them at one time, hopefully you will understand that. Thank you for code review!
