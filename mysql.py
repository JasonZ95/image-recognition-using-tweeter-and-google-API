import pymysql

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
