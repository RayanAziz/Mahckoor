import requests
import json
import re
from config import config
from urlextract import URLExtract
from printer import *

vt_url = "https://www.virustotal.com/vtapi/v2/url/report"
vt_api = config['virustotal api']['api_key']

def check_vt(url):
    parameters = {'apikey': vt_api, 'resource': url}
    response = requests.get(url=vt_url, params=parameters)
    if (response.status_code == 204): 
        print(WARNING + time_now() + "VT API rate limit reached".format(response))
        return
    try:
        json_response = json.loads(response.text)
        if json_response['response_code'] <= 0:
            print(INFO + time_now() + "No results for the link in VirusTotal")
            return 0
        elif json_response['response_code'] >= 1:
            if json_response['positives'] <= 0:
                print(INFO + time_now() + "Link is clean")
            else:
                print(ALERT + time_now() + "The link is malicious according to {} security vendor(s)".format(str(json_response['positives'])))
            return json_response['positives']
    except ValueError as e:
        print(ERROR + time_now() + "VT API key is not specified or invalid")

# Takes a tweet text and returns a list of URLs in it
def get_urls(text):
    return URLExtract().find_urls(text)
       
# Takes a t.co URL and returns the actual URL
def get_exapnded_url(twitter_url):
    if not (twitter_url):
        return None
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'} # This must be a browser agent to avoid issues
    url = re.search("(?P<url>https?://[^\s]+)\"", requests.get(url=twitter_url, headers=headers).text).group("url")
    if (url.find("twitter.com") == -1 and url.find("twimg.com") == -1): # Don't need to analyze Twitter links (media & quote tweets)
        return url
    else:
        return None