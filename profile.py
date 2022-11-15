### Each user profile creates an instance of this class 

import datetime
import time
import requests
import re
from osint import get_exapnded_url
from notifier import emailer, siem
from printer import *

class Profile():

    def __init__(self, user, client):
        self.client = client
        self.user_id = user.id
        self.username = user.username
        self.display_name = user.name
        self.bio = user.description
        self.location = user.location
        self.url = user.url
        self.profile_image = user.profile_image_url
        self.pinned_tweet_id = user.pinned_tweet_id
        self.tweets_count = user.public_metrics['tweet_count']
        self.followers_count = user.public_metrics['followers_count']
        self.following_count = user.public_metrics['following_count']
        self.isDeleted = False
        
            
    # Fetch the live user profile and compare to the stored, retuns
    def compare(self):
        self.changes = [] # Array of dictionaries of triggers
        try:
            live_user = self.client.get_user(username=self.username, user_fields=['id', 'name', 'username', 'description', 'location', 'url', 'profile_image_url', 'pinned_tweet_id', 'public_metrics'])
        except: # TODO: specific exceptions
            print(ERROR + time_now() + "Failed to query a live user profile for {}".format(self.username))
            return
        if (live_user.errors): # Oh shi* the account is gone?
            if (self.isDeleted): # If it was reported deleted before don't trigger again
                return
            print(ALERT + time_now() + "Account {} got deleted".format(green("@" + self.username)))
            self.changes = [{"Account Deleted": True}]
            self.isDeleted = True
            #return self.changes
        else:
            self.isDeleted = False
            comparison_self = [self.username, self.display_name, self.bio, self.location, self.url, self.profile_image, self.pinned_tweet_id]
            comparison_live = [live_user.data.username, live_user.data.name,live_user.data.description,live_user.data.location,live_user.data.url,live_user.data.profile_image_url,live_user.data.pinned_tweet_id]
            if (comparison_live != comparison_self):
            
                if (live_user.data.username != self.username):
                    self.changes.append({"Username Change": self.username + "," + live_user.data.username})
                    print(ALERT + time_now() + "Account {} username changed to {}".format(green("@" + self.username), "@" + red(live_user.data.username)))
                    self.username = live_user.data.username
                    
                if (live_user.data.name != self.display_name):
                    self.changes.append({"Display Name Change": self.display_name + "," + live_user.data.name})
                    print(ALERT + time_now() + "Account {} display name changed from {} to {}".format(green("@" + self.username), green(self.display_name), red(live_user.data.name)))
                    self.display_name = live_user.data.name
                    
                if (live_user.data.description != self.bio):
                    self.changes.append({"Bio Change": self.bio + "," + live_user.data.description})
                    print(ALERT + time_now() + "Account {} bio changed from {} to {}".format(green("@" + self.username), green(self.bio), red(live_user.data.description)))
                    self.bio = live_user.data.description
                    
                if (live_user.data.location != self.location):
                    self.changes.append({"Location Change": str(self.location) + "," + str(live_user.data.location)})
                    print(ALERT + time_now() + "Account {} location changed from {} to {}".format(green("@" + self.username), green(str(self.location)), red(str(live_user.data.location))))
                    self.location = live_user.data.location
                    
                if (live_user.data.url != self.url):
                    expanded_live_url = get_exapnded_url(live_user.data.url)
                    expanded_stored_url = get_exapnded_url(self.url)
                    if (expanded_live_url != expanded_stored_url):
                        self.changes.append({"URL Change": str(expanded_stored_url) + "," + str(expanded_live_url)})
                        print(ALERT + time_now() + "Account {} URL changed from {} to {}".format(green("@" + self.username), blue(str(expanded_stored_url)), blue(str(expanded_live_url))))
                        self.url = live_user.data.url
                    
                if (live_user.data.profile_image_url != self.profile_image):
                    self.changes.append({"Profile Image Change": self.profile_image + "," + live_user.data.profile_image_url})
                    print(ALERT + time_now() + "Account {} profile image updated".format(green("@" + self.username)))
                    self.profile_image = live_user.data.profile_image_url
                    
                if (live_user.data.pinned_tweet_id != self.pinned_tweet_id):
                    try:
                        old_tweet = self.client.get_tweet(id = self.pinned_tweet_id).data.text
                    except:
                        old_tweet = "[unable to retreive tweet]"
                    try:
                        new_tweet = self.client.get_tweet(id = live_user.data.pinned_tweet_id).data.text
                    except:
                        new_tweet = "[unable to retreive tweet]"
                    self.changes.append({"Pinned Tweet Change":  str(old_tweet) + "," + str(new_tweet)})
                    print(ALERT + time_now() + "Account {} pinned tweet updated: \"{}\"".format(green("@" + self.username), red(new_tweet)))
                    self.pinned_tweet_id = live_user.data.pinned_tweet_id
                    
            if (self.changes):
                trigger = "" # Empty string to build
                froms = "" # Empty string to build
                tos = "" # Empty string to build
                for pair in self.changes:
                    for key, value in pair.items():
                        if (trigger): trigger = trigger + ", " + key
                        else: trigger = key # trigger string is empty, do not insert a comma
                        
                        values = value.split(",")
                        
                        if (froms): froms = froms + ", " + values[0]
                        else: froms = values[0] # froms string is empty, do not insert a comma
                        
                        if (tos): tos = tos + ", " + values[1]
                        else: tos = values[1] # tos string is empty, do not insert a comma
                    
                siem(time_now(raw = True), trigger, froms, tos, self.username)
                emailer(time_now(raw = True), trigger, froms, tos, self.username)        
