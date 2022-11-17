#### First introduced at Black Hat MEA 2022 Briefings & Arsenal.
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/media/logo-dark.png" width="342" height="240">
  <source media="(prefers-color-scheme: light)" srcset="/media/logo-white.png" width="373" height="240">
  <img alt="Logo" src="/media/mahckoor-white.png" width="373" height="240">
</picture>  

# Mahckoor
Twitter account hijacking detection and alerting tool.
## Overview
### Description
**Mahckoor** monitors changes in supplied Twitter accounts and analyzes their tweets. It alerts upon detecting changes on the profile or when suspicious tweets are tweeted. Alerts are sent via email & remote logging to SIEM <sup>so far.</sup>
### Use Case
Automatic monitoring for organaization Twitter accounts to expediate incident response and to fulfill regulation requirements.
## Features
### Current features:
1. Support for monitroing up to 5 accounts concurrently <sup>Twitter API limit, workaround possible if the userbase needed it.</sup>
2. Periodically monitor changes in profile properties:
   - Username
   - Display Name
   - Profile Picture
   - Bio
   - URL
   - Location
   - Pinned Tweet
3. Stream real-time tweets from monitored accounts and analyze them.
   - Support for detecing custom blacklisted words.
   - Support for sending tweeted links to OSINT for analysis <sup>only VT so far.</sup>
6. ِAuto setting the frequency for Twitter API queries based on the number of monitored accounts to avoid hitting API rate limits.
7. Maximum detection delay: 12 seconds.
8. Sending alerts via email & remote logging to SIEM on UDP in CEF.
9. Easy to configure and deploy
### Ideas in mind:
1. Detect malformed *config.ini*.
2. Log to a local file.
3. Give options to ignore alerting on some monitors <sup>e.g. don't alert for changes in the profile picture.</sup>
4. Support for matching against the blacklist regardless of character case to reduce list size.
5. Utilize machine/deep learning to detect anamoulous and malicious tweets.
6. Support for analyzing tweet replies to phishing.
7. Alert if sensitive media <sup>as per Twitter judgement</sup> is tweeted, and OCR text in it.
8. Support for more than 5 accounts with 1 Twitter bearer token workaround.
9. Support for more TI & OSINT platforms <sup>urlscan integration with nice features is upcoming.</sup>
## Requirements
1. <ins>Python 3.10 or newer</ins>. If you're hit with a syntax error on match-case statements, this's why.
2. Install required packages:
  ```
  pip install -r requirements.txt
  ```
3. API keys:
   - Twitter bearer token <sup>any access is fine</sup>
      - [How to get](https://developer.twitter.com/en/docs/tutorials/step-by-step-guide-to-making-your-first-request-to-the-twitter-api-v2)
   - VirusTotal API <sup>free is fine</sup>
      - [How to get](https://support.virustotal.com/hc/en-us/articles/115002088769-Please-give-me-an-API-key)
4. Filling out the *config.ini* file
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
## Contact
Please reach out to me directly about suggestions for **Mahckoor** at *0xMahckoor\[at]gmail\[dot]com*.
### Disclaimer
Logo asset made by [rexcanor](https://www.vecteezy.com/members/rexcanor).
