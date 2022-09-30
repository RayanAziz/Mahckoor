# Mahckoor
#### A Twitter account takeover detector.
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
4. Setting a custom frequency for the periodic check to avoid hitting API rate limits & quotas.
5. Sending alerts via email & remote logging to SIEM on UDP port 514 in CEF.  
### Features in mind:
1. Detect absent or malformed config.ini.
2. Support for multiprocessing/async.
3. Give options to ignore alerting on some monitors (e.g. don't alert for changes in the profile picture).
4. Utilize machine/deep learning to detect anamoulous and malicious tweets.
5. Support for analyzing tweet replies to match against a blacklist.
6. Analyze text & content in tweeted media.
7. Log to a local file.
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
   - Required fields:
      - [twitter accounts]
      - [twitter api]
      - [frequency]
   - Optional fields:
      - [virus total api]
      - [email]
      - [siem]
## Usage
   ```
   python mahckoor.py
   ```
