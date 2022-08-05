import feedparser
import smtplib
import time
import pytz
from datetime import datetime
import os

UTC = pytz.utc
FEED_URL = os.getenv('FEED_URL')
DELAY = int(os.getenv('DELAY'))
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))


def email(msg):
    
    BODY = "\r\n".join((
        f"From: {EMAIL_FROM}",
        f"To: {EMAIL_TO}",
        f"Subject: [RSS Tracker] Change detected!",
        "",
        msg))
    
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], BODY)
    server.quit()
        
    print(f'Sent msg: {msg}')
    
    
def notify(feed):
    msg = "New changes detected:" + "\n--------\n"
    for entry in feed.entries:
        
        # Get current time
        currentTime = datetime.now(UTC)

        # Matching day/hour
        if (entry['published_parsed'].tm_mday == currentTime.day) and abs(((entry['published_parsed'].tm_hour - currentTime.hour)) <= 1) and abs(((entry['published_parsed'].tm_min - currentTime.minute)) <= 5):
            title = entry['title']
            link = entry['link']
            published = entry['published']
            
            # Build the message to send later
            msg = msg + title + "\n" + link + "\n" + published + "\n------------\n"
            
    email(msg)


def main():
    # Get the data
    feed = feedparser.parse(FEED_URL)

    # Get latest changes made
    default = feed.entries[0].published

    print("Start!")
    print(f"Target FEEDURL: {FEED_URL}")
    print("." + "\n" + "." + "\n" + "." + "\n")

    while True:
        try:
            print("Monitoring the RSS...")
            time.sleep(DELAY)
            # Update current time
            currentTime = datetime.now(UTC)
            currentTime = currentTime.strftime("%H:%M:%S")

            # Get new data
            feed = feedparser.parse(FEED_URL)

            # Get the lastest published time again to check for any changes
            check = feed.entries[0].published

            # Different published time means the RSS was updated with new data.
            if check != default:
                notify(feed)
                print(f"--->Changes detected! Message sent at {currentTime}<---")
                print("--------------------------\n")
                print('For debugging: ')
                print(f'Default (before changed): {default}')
                print(f'Check: {check}')

                # Update default with new changes
                default = check
                
            else:
                print(f'No detected changes at {currentTime}')
                print("--------------------------")

        except Exception as e:
            print("---------- WARNING ----------")
            print("Error occured! Check below:")
            print("Exception: {}".format(type(e).__name__))
            print("Exception message: {}".format(e))
            print("-----------------------------")
            

if __name__ == "__main__":
    main()
