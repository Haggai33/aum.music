+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|  Spotify API     +----->  Google Sheets   +----->  Selenium for    |
|  (spotipy)       |     |  (gspread)       |     |  Instagram       |
|                  |     |                  |     |  (webdriver)     |
+---------+--------+     +---------+--------+     +---------+--------+
          |                        |                        |
          |                        |                        |
          |                        |                        |
          |                        |                        |
          v                        v                        v
+---------+--------+     +---------+--------+     +---------+--------+
|                  |     |                  |     |                  |
| get_playlist_    |     | check_in_db      |     | scrape_artist_   |
| artists          |     |                  |     | pages            |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
          |                        |                        |
          |                        |                        |
          |                        |                        |
          |                        |                        |
          v                        v                        v
+---------+--------+     +---------+--------+     +---------+--------+
|                  |     |                  |     |                  |
| save_to_csv      |     | save_to_text     |     | follow_new_      |
|                  |     |                  |     | artists_in_      |
|                  |     |                  |     | playlist         |
+------------------+     +------------------+     +------------------+




README for Script Version 11.0 IG + WhatsApp
Description:
This Python script is designed to automate the process of gathering information about artists from a Spotify playlist, checking their presence in a Google Sheets database, and scraping their Instagram usernames from their Spotify artist pages. The script also generates formatted text and CSV files with the collected data for use in Instagram and WhatsApp communications.

Features
Spotify Integration: Connects to the Spotify API to fetch artist information from a specified playlist.
Google Sheets Integration: Checks if the artists are already present in a Google Sheets database.
Instagram Scraping: Visits each artist's Spotify page to scrape their Instagram username.
Data Export: Generates a formatted text file and a CSV file with artist details, suitable for Instagram and WhatsApp posts.
Follow Artists: Option to follow new artists from the playlist on Spotify.
Error Handling
The script includes error handling for various scenarios:

Spotify API Connection: Handles errors related to Spotify API authentication and data retrieval.
Google Sheets Access: Manages exceptions when accessing or reading data from Google Sheets.
Web Scraping: Catches exceptions during the scraping process, such as elements not found or timeouts.
File Operations: Ensures safe reading/writing operations for CSV and text files.
