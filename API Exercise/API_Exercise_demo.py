import time
import random
import requests
import pandas as pd
from requests_oauthlib import OAuth1
key_words=["Object Detection","YOLO","Machine Learning"]
auth = OAuth1("R3HqOpqIo6AcKjDYKD1tpsBzQ", "hw1X2Hv7IlND6eKewSFbFa7SgQ70OpEHKKr7wzvtFDPlFuffVe",f"AAAAAAAAAAAAAAAAAAAAAPnOhgEAAAAAtGmcPuNuqE%2FTStZkA1wcHCmpY%2Bw%3Dn9KHHdFYQJEyBy5sDYNchbCDqiFV5JBRNTtKPPNWpAE9aJ8uyY")
def bearer_oauth(r):
    r.headers["Authorization"]="Bearer {}".format(f"AAAAAAAAAAAAAAAAAAAAAPnOhgEAAAAAtGmcPuNuqE%2FTStZkA1wcHCmpY%2Bw%3Dn9KHHdFYQJEyBy5sDYNchbCDqiFV5JBRNTtKPPNWpAE9aJ8uyY")
    r.headers["User-Agent"]="Mozilla/5.0"
    
    return r
query_params={'query': 'Python',
             'tweet.fields': 'author_id',
             'expansions':'author_id',
             'max_results': '100',
             'user.fields':'created_at,entities,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
             }
url = "https://api.twitter.com/2/tweets/search/recent"#API url
query_params_two=query_params.copy() # next page header
id_had_lst=[]# looped user
user_info_lst=[]# result
key_word_num=0
next=False # flip page
pageNum=0
while key_word_num<len(key_words):
    
    query_params['query']= key_words[key_word_num]
    query_params_two['query']= key_words[key_word_num]
    print("now we are in",query_params['query'])
    time.sleep(random.random()*10)
    if next:# the second page of now searching key word
        r = requests.get(url,auth=bearer_oauth,params=query_params_two)
    else:# the first page of the now searching key word
        
        r = requests.get(url,auth=bearer_oauth,params=query_params)
    js = r.json()
    print(js)
    for one_user in js["includes"]["users"]:
        if one_user["id"] in id_had_lst: #pass the already looped users
            continue
        id_had_lst.append(one_user["id"])
        user_info_lst.append(one_user)
    print("Done one page!")
    if "next_token" not in js["meta"]: #if we have data in next page
        key_word_num+=1
        next=False
        print("finish the {} key word".format(key_word_num))
        continue
    else:
        pageNum+=1
        if pageNum>9:
            key_word_num+=1
            pageNum=0
            next=False
            print("finish the {} key word".format(key_word_num))
            continue
        query_params_two["next_token"] = js["meta"]["next_token"]
        next=True
        continue
pd.DataFrame(user_info_lst).to_csv(r"twitter.csv")
