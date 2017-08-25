import requests
import requests.auth
import re
import time
import sys

# OAuth info
client_id=sys.argv[3]
secret=sys.argv[4]
access_token=''

# Request a token
client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
post_data = {"grant_type": "password", "username": sys.argv[1], "password": sys.argv[2]}
headers = {"User-Agent": "redditNetworkGraph/0.1 by standard_thrownaway"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
access_token=response.json()['access_token']
print(response.json())

past_subreddits = []
def search_subreddits(subreddit, counter):
    past_subreddits.append(subreddit.lower())
    headers = {"Authorization": "bearer "+access_token, "User-Agent": "redditNetworkGraph/0.1 by standard_thrownaway"}
    response = requests.get("https://oauth.reddit.com/r/"+subreddit+"/about/.json", headers=headers)

    if(response.status_code != 200):
        try:
            print(response.json()['reason'])
        except:
            pass
        print("Code != 200. subreddit:" +subreddit)
        return;

    # give up (return) if not able to get description and subscribers
    try:
        subreddit_description = response.json()['data']['description']
        subreddit_subscribers = response.json()['data']['subscribers']
    except:
        return

    if(subreddit_subscribers < 10000):
        return

    subreddits_regex = re.compile(r'r[\/](\w+)')
    subreddits_list = subreddits_regex.findall(subreddit_description)
    subreddits_list = list(set(subreddits_list)) #remove duplicates
   
    print(subreddit)
    counter = counter -1
    for i in subreddits_list:
        if(i.lower() not in past_subreddits and counter > 0):
            time.sleep(0) # to respect API request limits 
            search_subreddits(i, counter)
    
search_subreddits('Games', 1000)
