#!/usr/bin/env python
# encoding: utf-8

# ffmpeg -f image2 -r 2  -i /home/ece-student/Desktop/601hwk/img/image%04d.jpg -vcodec libx264  -t 40 test.mp4
# using the command above to generate the video

# export GOOGLE_APPLICATION_CREDENTIALS="/home/ece-student/Desktop/601hwk/googlekey.json"
# using the googlekey to access cloud vision service

import tweepy 
import json
import urllib.request
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

#Twitter API credentials
consumer_key = "#################"
consumer_secret = "#################"
access_key = "##################"
access_secret = "###################"

#use following command to chang the size of text displayed in the images
font = ImageFont.truetype('LiberationSans-Regular.ttf', 20)

def get_all_tweets(screen_name):

    #Twitter only allows access to a users most recent 3240 tweets with this method
    # Imports the Google Cloud client library
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

    #save most recent 200 tweets
    alltweets.extend(new_tweets)

 
    #write tweet objects to JSON
    file = open('tweet.json', 'w')
    print ("Writing tweet objects to JSON please wait...")
    count=1
    #change the path as your own directory
    path='/home/ece-student/Desktop/601hwk/img/'
    #extracting images in 200 tweets
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
        if 'media'in status._json['entities']:
            urllib.request.urlretrieve(status._json['entities']['media'][0]["media_url_https"], path + 'image'+str('%04d'%count)+'.jpg')
            
            # The name of the image file to annotate
            file_name = os.path.join(os.path.dirname(__file__),  path + 'image'+str('%04d'%count)+'.jpg')
            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            imageFile = path + 'image'+str('%04d'%count)+'.jpg'
            im1=Image.open(imageFile)
            draw = ImageDraw.Draw(im1)
            
            description=[]
            for label in labels:
                description.append(label.description)
            print (description)
            string=','.join(description)  
            
            draw.text((0, 0),string,(0,0,255),font=font)
            draw = ImageDraw.Draw(im1)
            im1.save(path + 'image'+str('%04d'%count)+'.jpg')

            
            count= count+1
        else:
            pass
            
    #close the file
    print ("Done")
    print ('There are'+str(count-1)+'images in 200 tweets')

   
    file.close()

if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@celtics")




