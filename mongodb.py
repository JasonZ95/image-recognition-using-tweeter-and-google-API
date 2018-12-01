import pymongo
from collections import Counter

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
