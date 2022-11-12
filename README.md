NOTE: WORKS ONLY ON PYTHON 3.10 and newer.
# Mahckoor
Twitter account hijacking detection and alerting.
## Description
Mahckoor monitors changes in supplied Twitter accounts and analyzes their tweets. It alerts upon detecting changes on the profile or when suspicious tweets are tweeted. Alerts are sent via email & remote logging to SIEM (so far).
## Features
### Current features:
1. Support for monitroing up to 5 accounts concurrently.
2. Periodically monitor changes in profile properties:
   - Username
   - Display Name
   - Profile Picture
   - Bio
   - URL
   - Location
   - Pinned Tweet
3. Stream real-time tweets from monitored accounts and analyze them.
4. Support for detecing custom blacklisted words.
5. Support for sending tweeted links to OSINT for analysis (only VT so far).
6. Intelligently set Twitter API query frequency to avoid hitting rate limits.
7. Sending alerts via email & remote logging to SIEM on UDP port 514 in CEF.
8. Easy to configure and deploy
### Features in mind:
1. Detect malformed config.ini.
2. Log to a local file.
3. Give options to ignore alerting on some monitors (e.g. don't alert for changes in the profile picture).
4. Support for matching against the blacklist regardless of character case to reduce size.
5. Utilize machine/deep learning to detect anamoulous and malicious tweets.
6. Support for analyzing tweet replies to phishing.
7. Alert if sensitive media is tweeted, and OCR text in it.
8. Support for more TI & OSINT platforms (urlscan integration with nice features is upcoming).
## Requirements
1. Python packages:
   - requests==2.28.1
      ```
      pip3 install requests
      ```
   - tweepy==4.8.0
      ```
      pip3 install tweepy
      ```
   - urlextract==1.6.0
      ```
      pip3 install urlextract
      ```
2. API keys:
   - Twitter bearer, consumer & access tokens with secrets (free elevated access or better is preferred)
      - [How to get](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2)
   - VirusTotal API (free is fine)
      - [How to get](https://support.virustotal.com/hc/en-us/articles/115002088769-Please-give-me-an-API-key)
3. Filling out the config.ini file.
   - Required configs:
      - [twitter accounts]
      - [twitter api]
      - [frequency]
   - Optional configs:
      - [virus total api]
      - [email]
      - [siem]
## Deployment
   ```
   python mahckoor.py
   ```
