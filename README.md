# Mahckoor
#### A Twitter account takeover detector.
## Description
It only needs any public API keys for Twitter and OSINT tools to work, then you supply it with Twitter usernames for the account you’d like to be monitored.
It monitors usual signs of takeovers, such as changes in the display name, profile picture, bio, etc.
It also monitors all tweets by the monitored accounts. It will thoroughly analyze the text looking for matches in a blacklist, or if the links tweeted have bad reputation after checking with online OSINT tools like VirusTotal.
Alerts from the tools can be emailed and can also be sent to your SIEM in CEF format via port 514 UDP.
## Requirements
1. Python packages:
   - requests==2.28.1
   - tweepy==4.8.0
   - urlextract==1.6.0
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
