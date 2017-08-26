import requests
import requests.auth
import re
import time
import sys
import random
import csv

start_time = time.time()

# OAuth info
client_id = sys.argv[3]
secret = sys.argv[4]
access_token = ''

# Request a token
client_auth = requests.auth.HTTPBasicAuth(client_id, secret)
post_data = {"grant_type": "password", "username": sys.argv[1], "password": sys.argv[2]}
headers = {"User-Agent": "redditNetworkGraph/0.1 by standard_thrownaway"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
access_token=response.json()['access_token']
print(response.json())

output = open('search_output.csv', 'w')
past_subreddits = []
subreddits_list = ['buddhism', 'opensource', 'brasil']
for i in range(0, 100000000):
    # Get a random subreddit name from subreddits_list
    subreddit = str(random.choice(subreddits_list))
    subreddits_list.remove(subreddit)
    if(subreddit in past_subreddits):
        continue
    past_subreddits.append(subreddit)

    # Get related subreddits from sidebar
    headers = {"Authorization": "bearer "+access_token, "User-Agent": "redditNetworkGraph/0.1 by standard_thrownaway"}
    response = requests.get("https://oauth.reddit.com/r/"+subreddit+"/about/.json", headers=headers)
    if(response.status_code != 200):
        try:
            print(response.json()['reason'])
        except:
            pass
        print("Code != 200. subreddit:" +subreddit)
        continue;

    # Skip if not able to get description and subscribers
    try:
        subreddit_description = response.json()['data']['description']
        subreddit_subscribers = response.json()['data']['subscribers']
    except:
        continue

    if(subreddit_subscribers < 10000):
        continue

    subreddits_regex = re.compile(r'r[\/](\w+)')
    related_subreddits = subreddits_regex.findall(subreddit_description)
    related_subreddits =  [x.lower() for x in related_subreddits]
    related_subreddits = list(set(related_subreddits)) #remove duplicates
    subreddits_list.extend(related_subreddits)
    subreddits_list = list(set(subreddits_list)) #remove duplicates
    print(subreddit + ' / ' + 'past_subreddits_size: '+str(len(past_subreddits))  + ' / ' +  'subreddits_list_size: '+str(len(subreddits_list))  + ' / ' +  'running_time: '+str(round(time.time() - start_time, 1)))
    
    output.write(subreddit + ',' + str(subreddit_subscribers) + ',' + ",".join(related_subreddits) + '\n')
    output.flush()

output.close()

