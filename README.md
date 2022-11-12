# Mahckoor
Twitter account hijacking detection and alerting tool.
## Overview
### Description
Mahckoor monitors changes in supplied Twitter accounts and analyzes their tweets. It alerts upon detecting changes on the profile or when suspicious tweets are tweeted. Alerts are sent via email & remote logging to SIEM (so far).
### Use Case
Automatic monitoring for organaization Twitter accounts to expediate incident response and to fulfill regulation requirements.
## Features
### Current features:
1. Support for monitroing up to 5 accounts concurrently (Twitter API limit, workaround possible if userbase needed it).
2. Periodically monitor changes in profile properties:
   - Username
   - Display Name
   - Profile Picture
   - Bio
   - URL
   - Location
   - Pinned Tweet
3. Stream real-time tweets from monitored accounts and analyze them.
   a. Support for detecing custom blacklisted words.
   b. Support for sending tweeted links to OSINT for analysis (only VT so far).
6. Intelligently set Twitter API query frequency to avoid hitting API rate limits.
7. Maximum detection delay: 12 seconds (it's 10 seconds but Twitter rate limits are inconsistent sometimes).
8. Sending alerts via email & remote logging to SIEM on UDP in CEF.
9. Easy to configure and deploy
### Ideas in mind:
1. Detect malformed config.ini.
2. Log to a local file.
3. Give options to ignore alerting on some monitors (e.g. don't alert for changes in the profile picture).
4. Support for matching against the blacklist regardless of character case to reduce list size.
5. Utilize machine/deep learning to detect anamoulous and malicious tweets.
6. Support for analyzing tweet replies to phishing.
7. Alert if sensitive media as per Twitter judgement is tweeted, and OCR text in it.
8. Support for more than 5 accounts with 1 Twitter bearer token workaround.
9. Support for more TI & OSINT platforms (urlscan integration with nice features is upcoming).
## Requirements
1. Python packages:
   - colorama==0.4.6
   - requests==2.28.1
   - tweepy==4.12.1
   - urlextract==1.7.1
2. API keys:
   - Twitter bearer token (any access is fine)
      - [How to get](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2)
   - VirusTotal API (free is fine)
      - [How to get](https://support.virustotal.com/hc/en-us/articles/115002088769-Please-give-me-an-API-key)
3. Filling out the config.ini file.
   - Required configs:
      - [twitter accounts]
      - [twitter api]
   - Optional configs:
      - [virustotal api]
      - [email]
      - [siem]
## Deployment
   ```
   python mahckoor.py
   ```
### Disclaimer
Logo asset owned by [rexcanor](https://www.vecteezy.com/members/rexcanor).
