import feedparser
import os
import ftplib
import time
import re

# Set the URLs of the RSS feeds
feed_urls = ["FEED1.rss", "FEED2.rss"]

# Set the download location and FTP credentials
download_path = "/Where/You/Want/Saved"
ftp_host = "ftp.host.com"
ftp_username = "username"
ftp_password = "password"

def download_and_upload(feed_url):
  # Parse the RSS feed
  feed = feedparser.parse(feed_url)

  # Get the most recent item (i.e., the most recent episode)
  latest_item = feed["items"][0]

  # Use a regular expression to search for the file URL in the description element
  file_url_match = re.search(r'https://.+\.mp3', latest_item["description"])

  # Check if the regular expression found a match
  if file_url_match:
    # Get the file URL from the match
    file_url = file_url_match.group(0)

    # Download the file
    os.system("curl -L -o {}/{} {}".format(download_path, file_url.split("/")[-1], file_url))

    # Connect to the FTP server
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_username, ftp_password)

    # Upload the file
    with open("{}/{}".format(download_path, file_url.split("/")[-1]), "rb") as f:
      ftp.storbinary("STOR {}".format(file_url.split("/")[-1]), f)

    # Close the FTP connection
    ftp.quit()
  else:
    print("No file URL found in description element for item in feed {}".format(feed_url))


# Run the function for each RSS feed every hour
while True:
  for feed_url in feed_urls:
    download_and_upload(feed_url)
  time.sleep(3600)
