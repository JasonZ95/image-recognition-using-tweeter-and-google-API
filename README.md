image-recognition-using-tweeter-and-google-API
==============================================
Instruction
-----------

  This is a python programme that download user's tweeter images and convert it to a video. On each of the pictures, there are several tags to describe the object on it. To realize the function described above, I apply two APIs:
  
  'Tweepy': The API provided by tweeter official to access any user's tweet messages, which is used to download the images for our programme.

   'Google Vision': An API with powerful image recognition capabilities provided by Google. It can output tags to describe the object in the pictures.

   'FFMPEG': To convert images into a video in mp4 format.

  I also use PIL image library to attach the text message to the pictures, which make the output more friendly.

Preparation
-----------

  There are several things you need to do before using the programme.

   *Apply for a tweeter developer account to get the key for the tweepy API. The website is 

     https://tweepy.readthedocs.io/en/v3.5.0/

   *Get access for the google cloud platform to get the authentication file (.json) to get access for the API.

   *install relavent resourses(tweepy & PIL), using the following command:
   ```Bash
   pip install tweepy
   ```
   ```Bash
   pip install Pillow
   ```
  
   *Before running the programme, you need to execute following command:
   ```Bash
   export GOOGLE_APPLICATION_CREDENTIALS="/directory/googlekey.json"
   ```
   (This command allows you to use the google vision API.)
  
  * After running the programme, you can find some pics in the file you specified. Now you can use following command to convert images to video:
  ```Bash
  ffmpeg -f image2 -r 2  -i /directory/image%04d.jpg -vcodec libx264  -t 40 test.mp4
  ```
     
  # image-recognition-using-tweeter-and-google-API
  
  In this part, I create two databases for users to store their search history. In this part the user can use the API to realize:
  
  *Detail information of every transaction the user may run using the API
  
  *Store all relevant information for everytime a user uses the application
  
  By using search functions, users can also:
  
  *Search for certain words and retrieve which user/session that has this work in it.  For example, search for ‘basketball”, and get results of which user had Basketball in their sessions.
  
  *Collective statistics about overall usage of the system:
  
    *Number of images per feed
    
    *Most popular descriptors

  
