# Mahckoor
#### A Twitter account takeover detector.
## Description
Mahckoor monitors changes in supplied Twitter accounts and analyzes their tweets, and alerts via email & remote logging to SIEM upon detecting signs of account takeover.
## Features
Current:
1. Support for multi-account monitoring
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
Ideas for the future:
1. Support for multiprocessing/async
2. Utilize machine learning to identify anamoulous tweets
3. Support for analyzing tweet replies to match against a blacklist
4. Analyze text & content in tweeted media
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
   - VirusTotal API (free is fine)
3. Filling the config.ini file.
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
   python main.py
   ```
