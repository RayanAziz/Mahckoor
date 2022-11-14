import datetime
import time
import tweepy
import tweepy.asynchronous
import asyncio
import requests
import re
import json
import os
import profile
import threading
from osint import *
from os.path import exists
from config import config
from notifier import emailer, siem
from printer import *

print_logo("V1.0")
  
# Load Twitter API info from the config
bearer_token = config['twitter api']['bearer_token']

client = tweepy.Client(wait_on_rate_limit=True, bearer_token=bearer_token)

class TweetStreamer(tweepy.StreamingClient):

    def on_connect(self):
        print(INFO + time_now() + "Connected to Twitter and now monitoring:")
        for profile in self.get_rules().data:
            print(grey("                               - ") + green("@{}   {}".format(str(profile.tag.split(",")[0]), str(profile.tag.split(",")[1]))))
        print("========================================================================")
    def on_tweet(self, tweet):
        username = client.get_user(id=tweet.author_id).data.username
        tweets_monitor(username, tweet)
    def on_disconnect(self):
        print(ERROR + time_now() + "Disconnected from Twitter")
        # Attempt to reconnect
    def on_connection_error(self):
        print(ERROR + time_now() + "Connection to Twitter lost")
    def on_exception(self, exception):
        print(ERROR + time_now() + str(exception))
        # Handle the exception
    #def on_keep_alive(self):
        # Say nothing
    def on_request_error(self, status_code):
        match status_code:
            case 429:
                print(ERROR + time_now() + "[" + str(status_code) + "] Did you fully close the previous connection? Attempting connection again...")
            case 504:
                print(ERROR + time_now() + "[" + str(status_code) + "] Twitter servers are unavailable")
            case 401:
                print(ERROR + time_now() + "[" + str(status_code) + "] Invalid Twitter bearer token. Terminating...")
                exit()

if not os.path.exists("data"):
    os.mkdir("data")

is_blacklist_enabled = False

if os.path.isfile("data/blacklist.txt"):
    with open('data/blacklist.txt', 'r+', encoding='UTF8') as f:
        blacklist = [line.strip() for line in f]
    is_blacklist_enabled = True
else:
    print(WARNING + time_now() + "No blacklist.txt was found in ./data/")

instances = [] # Array of account profile instances

def main():
    stream = TweetStreamer(bearer_token, daemon=True, wait_on_rate_limit=True)
    usernames = config['twitter accounts']['user_name'].split(",") # Import usernames to a list
    # Clean the usernames
    for i in range(len(usernames)):
        usernames[i] = re.sub('[^a-zA-Z.\d_]', '', usernames[i])
    delay = len(usernames) * 2 + 2 # Twitter API v2 rate limit is 900 lookups/15 min = 1/sec
    old_rules = stream.get_rules()
    if not (old_rules[0] == None) :
        for rule in old_rules.data:
            stream.delete_rules(rule.id) # Delete old rules saved in the stream
    for username in usernames:
        profile = client.get_user(username=username, user_fields=['name', 'username']).data
        stream.add_rules(tweepy.StreamRule(value="from:" + username, tag=(profile.username + ","  + profile.name)))
    stream.filter(tweet_fields=['id','text', 'created_at', 'author_id', 'attachments', 'in_reply_to_user_id', 'referenced_tweets', 'lang', 'possibly_sensitive', 'reply_settings', 'source'], user_fields=['name', 'username', 'description', 'location', 'pinned_tweet_id', 'profile_image_url', 'url'],media_fields=['type', 'url'], threaded=True)
    load_users(usernames)
    while(True):
        for instance in instances:
            thread = threading.Thread(target = instance.compare, daemon=True)
            thread.start()
            thread.join()
        time.sleep(delay)
     
     
def load_users(usernames):
    # Fetch all users
    user_objects = client.get_users(usernames=usernames,  user_fields=['id', 'name', 'username', 'description', 'location', 'url', 'profile_image_url', 'pinned_tweet_id', 'public_metrics'])
    if(user_objects.errors): # Username is wrong or doesn't exist
        print(ERROR + time_now() + user_objects.errors[0]['detail'])
        exit()
    for user_object in user_objects:
        for user_profile in user_object:
            instances.append(create_instance(user_profile)) # For threading
     
     
def create_instance(user_profile):
    return profile.Profile(user_profile, client)


# Sends tweets for analysis and takes decision on them
def tweets_monitor(username, tweet):
    analysis = analyze_tweet(username, tweet.text)
    if (analysis):
        tweet_link = "https://twitter.com/{}/status/{}".format(username, str(tweet.id))
        siem(tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'), analysis, None, tweet_link, username)
        emailer(tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'), analysis, None, tweet_link, username)    
    
    
# Is fed a tweet to analyze with blacklists and VT and returns a verdit array
def analyze_tweet(username, text):
    tweet_verdict = [] # Array of dictionaries of alerts
    if (is_blacklist_enabled):
        for word in blacklist:
            if word in text:
                print(ALERT + time_now() + "Found a blacklisted word in a tweet by {}: {} ".format(green("@" + username), red(word)))
                tweet_verdict.append({"Blacklisted Word": word})
    urls = get_urls(text)
    for url in urls:
        if (get_exapnded_url(url)):
            url = get_exapnded_url(url)
        else: continue
        print(INFO + time_now() + "Found a link in a tweet by {}: {}".format(green("@" + username), blue(url)))
        if (is_blacklist_enabled):
            for word in blacklist:
                if word in url:
                    print(ALERT + time_now() + "Found a blacklisted word in the tweeted link: {}".format(red(word)))
                    tweet_verdict.append({"Blacklisted Word": word})
        try:
            vt_result =  check_vt(url)
            if (vt_result > 0):
                tweet_verdict.append({"VT Bad Reputation": url + "," + str(vt_result)})
        except:
            print(WARNING + time_now() + "Skipped VT URL analysis")
    return tweet_verdict
        
# main()
    
try:
    main()

except KeyboardInterrupt:
    print(WARNING + time_now() + "[CTRL + C]? OK...")
    
except tweepy.errors.Unauthorized:
    print(ERROR + time_now() + "Invalid or invalidated Twitter bearer token")

except Exception as e:
    print(ERROR + time_now() + "Unknown error: " + str(e))
    
# Alerts upon a program termination
# finally:
    # print(WARNING + time_now() + "Tool terminated. Sending notifications...")
    # try:
        # emailer(time_now(raw=True), "Machkoor Stopped Working", None, None, None)
    # except:
        # print(ERROR + time_now() + "Could not email about the termination")
    # try:
        # trigger = [{"Machkoor Stopped Working": True}]
        # siem(time_now(raw=True), trigger, None, None, None)          
    # except:
        # print(ERROR + time_now() + "Could not an alert to the SIEM about the termination")
            
 