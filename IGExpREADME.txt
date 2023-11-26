Spotify Playlist Instagram Scraper
This Python script allows you to scrape Instagram usernames of artists from a Spotify playlist. 
It uses the Spotify Web API to fetch artist details from a given Spotify playlist URL and then 
uses Selenium WebDriver to scrape Instagram usernames from each artist's Spotify page.

Requirements
Python 3.x
spotipy (Spotify Web API Python client)
selenium (Web scraping tool)
Chrome WebDriver (for Selenium)
A Spotify Client ID and Client Secret
Setup
Install Required Python Libraries:

bash
Copy code
pip install spotipy selenium
Download Chrome WebDriver:
Download the Chrome WebDriver from here and place it in a known directory.

Spotify API Credentials:
You need to have a Spotify Developer account. Create an app at Spotify Developer Dashboard to get your CLIENT_ID and CLIENT_SECRET.

Usage
Set Spotify API Credentials:
Replace CLIENT_ID and CLIENT_SECRET in the script with your own credentials.

Run the Script:
Execute the script in your Python environment.

bash
Copy code
python spotify_playlist_instagram_scraper.py
Enter Spotify Playlist URL:
When prompted, enter the full URL of the Spotify playlist you want to scrape.

CSV File Generation:
After the script finishes running, you will be asked if you want to save the results to a CSV file. Type 'y' for yes or 'n' for no.

Output
The script will output the Instagram usernames of the artists in the terminal. If you choose to save the results, a CSV file named instagram_accounts.csv will be created in the C:\Users\Administrator\Downloads directory. This file contains the artist names, their Instagram usernames, and the count of occurrences (useful for duplicate entries).

Notes
The script uses Selenium WebDriver to automate a web browser. Ensure that the version of Chrome WebDriver matches your Chrome browser's version.
The script is configured for Windows paths. If you are using a different OS, please adjust the file paths accordingly.
The script's performance and accuracy depend on the structure of the Spotify web pages. Any significant changes in their layout may require adjustments to the script.