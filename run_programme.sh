pip install tweepy
pip install Pillow
export GOOGLE_APPLICATION_CREDENTIALS="/directory/googlekey.json"

cd /directory_of_the_tweetAPI_programme/
python tweetAPI.py

#use the follwing command to generate the video
#the directory shown is the directory of images
#use -t to set length of your video
#"test" is the name of the video
ffmpeg -y -r 2 -i /home/ece-student/Desktop/601hwk/img/image%04d.jpg -s 1024*540 test.mp4
