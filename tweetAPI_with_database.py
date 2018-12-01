#!/usr/bin/env python
# encoding: utf-8

#  ffmpeg -y -r 2 -i /home/ece-student/Desktop/601hwk/img/image%04d.jpg -s 1024*540 test.mp4

# using the command above to generate the video-

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

import pymongo
from collections import Counter

import pymysql


#Twitter API credentials
consumer_key = "frxPsqLOA8itHCihffT5bcezH"
consumer_secret = "wt9cmEoEVlbMnHWCAyPLQmCe8nuzx3fe7AVVDHD8zbqLnp6OWs"
access_key = "1040690616462725121-dHBkVcfHJl3egcoDMFqINj8fvzjSEe"
access_secret = "CnztumLQUezuteatlJL1gVxUposRjFEeX7gd0GxoVd3V3"

font = ImageFont.truetype('LiberationSans-Regular.ttf', 20)



def get_all_tweets(screen_name, num):


    #Twitter only allows access to a users most recent 3240 tweets with this method
    # Imports the Google Cloud client library
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    description_list = []
    
    # Instantiates a client
    client = vision.ImageAnnotatorClient()


    #make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name = screen_name,count = num)
    except:
        print("There is problem to access the tweeter, please check the tweeter id and the internet")
        os._exit(0)

    #save most recent 200 tweets
    alltweets.extend(new_tweets)

 
    #write tweet objects to JSON
    file = open('tweet.json', 'w')
    print ("Writing tweet objects to JSON please wait...")
    count=1
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
            
            #description stores the labels in each img,des_list stores all the labels
            description = []
            
            
            for label in labels:
                description.append(label.description)
            print (description)
            string = ','.join(description)
#            print(string)
            description_list.append(string)
            draw.text((0, 0),string,(0,0,255),font=font)
            draw = ImageDraw.Draw(im1)
            im1.save(path + 'image'+str('%04d'%count)+'.jpg')

            count= count+1
        else:
            pass
            
    #close the file
    print ("Done")
    print ('There are '+str(count-1)+' images in' + " " + str(num) + " " +'tweets')
#    print (description_list)
    all_tag_list = []
    for i in range(0,len(description_list)):
        tag_str = description_list[i].split(',')
        for j in range(0,len(tag_str)):
            all_tag_list.append(tag_str[j])
    word_counts = Counter(all_tag_list)
    common = word_counts.most_common(1)
    word = common[0][0]
    print("##############################")
    print('most popular word is '+ word)
    print("##############################")
    return description_list, word
    file.close()
    
    
    
    
    
    
    
def mongodb_database(tag_list, tweet_id, num, word):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient.tweeterAPI
    mycol = mydb.search_history
    mydic = {"name":tweet_id, 'num':num, 'pic_num':len(tag_list), 'description':[], 'word':word}
    for i in range(0,len(tag_list)):
        tag_str = tag_list[i].split(',')
        for j in range(0,len(tag_str)):
            mydic['description'].append(tag_str[j])
    mycol.insert_one(mydic)
    for i in mycol.find():
        print (i)
        print('***************************************')
        
        
def mongodb_search(keyword):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient.tweeterAPI
    mycol = mydb.search_history
#    mycol.delete_many({})
    for info in mycol.find({"$or":[{"name":keyword},{"description":keyword}]}):
        print(info)
    print("###############################################################")
        
def mongodb_imgperfeed():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient.tweeterAPI
    mycol = mydb.search_history
    avg = mycol.aggregate([{"$group":{"_id":"pic per feed", "average":{"$avg":"$pic_num"}}}])
    print(list(avg))
    print("###############################################################")
    
def mongodb_popular():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient.tweeterAPI
    mycol = mydb.search_history
    pop = mycol.aggregate([{"$group":{"_id": word}}])
    print(list(pop))
    print("###############################################################")
          
          
          
          
          
def mysql_database(tag_list, tweet_id, num, word):
    string_list = []
    for i in range(0,len(tag_list)):
        tag_str = tag_list[i].split(',')
        for j in range(0,len(tag_str)):
            string_list.append(tag_str[j])
    string = ','.join(string_list)
    try:
        db = pymysql.connect("localhost","root","bu","tweetAPI" )
        cursor = db.cursor()
        sql = "INSERT INTO search_history (user_id, img_num, tags, popular_word) VALUES (%s, %s, %s, %s)"
        values = (tweet_id, int(num), string, word)
        cursor.execute(sql,values)
        db.commit()
        db.close()
        print("write complete")
        print("###########################################################")
    except:
        print('cannot write to mysql db')
        
def mysql_search(keyword):
    db = pymysql.connect("localhost","root","bu","tweetAPI" )
    cursor = db.cursor()
    sql = "select * from search_history where LOCATE('"+ keyword+"',tags)>0;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(0,len(result)):
        print(result[i])
        print(' ')
    db.close()
    print("###########################################################")
          
def mysql_picsperfeed():
    db = pymysql.connect("localhost","root","bu","tweetAPI" )
    cursor = db.cursor()
    sql = "SELECT AVG(img_num) FROM search_history"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(0,len(result)):
        print(result[i])
    db.close()
    print("###########################################################")
          
def mysql_popular():
    db = pymysql.connect("localhost","root","bu","tweetAPI" )
    cursor = db.cursor()
    sql = "SELECT popular_word, COUNT(*) FROM search_history GROUP BY popular_word ORDER BY COUNT(*) DESC;"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in range(0,len(result)):
        print(result[i])
    db.close()




if __name__ == '__main__':
    tweet_id = input("Input the tweeter id you want to search with @: ")
    num = input("Input number of tweets: ")
    num = int(num)
    #pass in the username of the account you want to download
    tag_list, word = get_all_tweets(tweet_id, num)
    print(tag_list)
    
    
    db_type = input("choose database to store history: 1 for mysql, 2 for mongodb, other inputs to exit: ")
    if db_type == '1':
        print("now writing data to mysql database")
        mysql_database(tag_list, tweet_id, num, word)
        keyword = str(input('input keyword to search: '))
        mysql_search(keyword)
        mysql_picsperfeed()
        mysql_popular()
        
    elif db_type == '2':
        print("now writing data to mongodb database")
        mongodb_database(tag_list, tweet_id, num, word)
        keyword = str(input('input keyword to search: '))
        mongodb_search(keyword)
        mongodb_imgperfeed()
        mongodb_popular()
    else:
        pass
    



