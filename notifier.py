import smtplib
import email
import socket
from config import config
from urllib.parse import urlparse
from printer import *

# Email alerts options
enable = ['True', 'true', 'TRUE', 'Yes', 'yes', 'YES']
is_email_enabled = config['email']['enable']
if (is_email_enabled in enable):
    mail_server = config['email']['mail_server']
    smtp_port   = int(config['email']['smtp_port'])
    email_user  = config['email']['email_user']
    email_name  = config['email']['email_name']
    email_pass  = config['email']['email_pass']
    recipients  = config['email']['recipients']
    is_email_enabled = True
    print(INFO + time_now() + "Email notifications are enabled to {}".format(green(recipients)))
else:
    is_email_enabled = False
    print(WARNING + time_now() + "Email notifications are disabled")
# SIEM alerts options
is_siem_enabled = config['siem']['enable']
if (is_siem_enabled in ['True', 'true', 'TRUE', 'Yes', 'yes', 'YES']):
    siem_info = (config['siem']['host'], int(config['siem']['port']))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    is_siem_enabled = True
    print(INFO + time_now() + "Remote log alerting is enabled to {}".format(green(config['siem']['host'] + ":" + str(config['siem']['port']))))
else:
    print(WARNING + time_now() + "Remote log alerting is disabled")
    is_siem_enabled = False

vt_api = config['virustotal api']['api_key']
        
def emailer(time, trigger, old_value, new_value, username):
    if not (is_email_enabled):
        return
    message = email.message.Message()
    message['To'] = recipients
    message['From'] = '{} <{}>'.format(email_name, email_user)
    server = smtplib.SMTP(mail_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_pass)
    if (username):
        profile_link = "https://twitter.com/" + username
    if ("Change" in trigger):
        message['Subject'] = "Twitter Account @{} Profile Change Alert".format(username)
        body = \
            '''
Time: {}
Alert(s): {}
Old Value(s): {}
New Value(s): {}
Profile Link: {}
'''.format(time, trigger, old_value, new_value, profile_link)

    elif ("Stopped Working" in trigger): # Stopped working alerts
        message['Subject'] = "Mahckoor Stopped Working Alert"
        body = \
            '''
Time: {}
Alert: {}
'''.format(time, trigger)

    elif ("Deleted" in trigger): # Deleted account alert
        message['Subject'] = "Twitter Account @{} Deleted Alert".format(username, profile_link)
        body = \
            '''
Time: {}
Alert: {}
Missing Profile Link: {}
'''.format(time, trigger)

    else: # Tweet alerts, needs special handling
        message['Subject'] = "Twitter Account @{} Suspicious Tweet Alert".format(username)
        alert = "" # Emptry alert string to build
        for pair in trigger:
            for key, value in pair.items():
                match key:
                    case "VT Bad Reputation":
                        vt = value.split(",")
                        alert = alert + "\n    • " + key + ": \"" + mask_url(vt[0]) + "\" flagged by " + vt[1] + " security vendor(s)"
                    #case "Screenshot":
                        #screenshot_pair = value.split(",")
                        #alert = alert + "\n" + key + ": \"" + screenshot_pair[1] + "\"" # Print only the link, not the png data
                    case _: # Default case
                        #print(ALERT + time_now() + "Else: " + key)
                        alert = alert + "\n    • " + key + ": \"" + value + "\""
        body = \
            '''
Time: {}
Alert(s):{}
Tweet Link: {}
Profile Link: {}
'''.format(time, alert, new_value, profile_link)
    message.set_payload(body, 'utf-8')
    try:
        server.sendmail(email_user, recipients, message.as_string())
        print(INFO + time_now() + "Notification email sent to {}".format(green(recipients)))
    except Exception as e:
        print(ERROR + time_now() + "Sending notification email failed")
        print(ERROR + time_now() + e)
        print(ERROR + time_now() + "Attempting reconnection to the server and trying one more time")
        try:
            server = smtplib.SMTP(mail_server, smtp_port)
            server.ehlo()
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, recipients, message.as_string())
            print(INFO + time_now() + "Alert email sent to {}".format(green(recipients)))
        except:
            print(ERROR + time_now() + "Sending notification email failed again")

# Sends remote alert logs to the SIEM in CEF on the specified IP and port
def siem(time, trigger, value1, value2, username):
    if not (is_siem_enabled):
        return
    if (username):
        profile_link = "https://twitter.com/" + username
    # Remove png data from tweet alerts
    if not (value1): # value1 is None in tweet alerts
        for pair in trigger:        
            for key, value in pair.items():
                if (key == "Screenshot"):
                    screenshot_pair = value.split(",")
                    trigger.update({"Screenshot": screenshot_pair[1]}) # Remove screenshot png data and keep the link
    if ("Change" in trigger):
        trigger = "CEF:0|Rayan Aziz|Mahckoor|1.0|Mahckoor Alert|suser={}|start={}|msg={}|oldvalue={}|newvalue={}|url=https://twitter.com/{}".format(username, time, trigger, value1, value2, username)
    elif ("Stopped Working" in trigger):
        trigger = "CEF:0|Rayan Aziz|Mahckoor|1.0|Mahckoor Alert|start={}|msg={}".format(time, trigger)
    else:
        trigger = "CEF:0|Rayan Aziz|Mahckoor|1.0|Mahckoor Alert|suser=@{}|start={}|msg={}|url={}".format(username, time, trigger, value2)

    try:
        sock.sendto(trigger.encode(), siem_info)
    except:
        print(ERROR + time_now() + "Sending alert to SIEM failed, check the configs")
        return
        
    print(INFO + time_now() + "Alert log sent to {}".format(str(green(config['siem']['host'] + ":" + str(config['siem']['port'])))))
    

# Makes URLs impossible to open undeliberately
def mask_url(url):
    return url.replace(urlparse(url).netloc, urlparse(url).netloc.replace(".", "[.]")).replace("http", "hXXp")