# Mahckoor
A Twitter account takeover detection tool.
## Description
Mahckoor monitors changes in supplied Twitter accounts and analyzes their tweets. It alerts upon detecting changes or suspicious tweets via email & remote logging to SIEM.  
## Features
### Current features:
1. Support for multi-account monitoring.
2. Periodically monitoring changes in account properties:
   - Username
   - Display Name
   - Profile Picture
   - Bio
   - URL
   - Location  
3. Periodically fetch new tweets ana analyzed them.
4. Support for detecing custom blacklisted words.
5. Setting a custom frequency for the periodic check to avoid hitting API rate limits & quotas.
6. Sending alerts via email & remote logging to SIEM on UDP port 514 in CEF.
7. Easy deployment and handles most user errors.  
### Features in mind:
1. Detect absent or malformed config.ini.
2. Log to a local file.
3. Give options to ignore alerting on some monitors (e.g. don't alert for changes in the profile picture).
4. Support for matching against the blacklist regardless of character case.
5. Utilize machine/deep learning to detect anamoulous and malicious tweets.
6. Support for analyzing tweet replies to match against a blacklist.
7. Analyze text & content in tweeted media.
8. Support for more TI & OSINT platforms.
9. Recode to support multiprocessing/async.
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
