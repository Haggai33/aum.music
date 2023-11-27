Spotify Artist Scraper and Follower
Overview
This script is designed to interact with Spotify playlists, scrape artist information, check for Instagram accounts, and optionally follow artists on Spotify. It integrates with Google Sheets to cross-reference data and can export results to CSV and text files.

Features
Scrape Spotify Playlist: Extracts artist information from a given Spotify playlist URL.
Instagram Account Search: Searches for Instagram accounts of artists and checks if they are already in a Google Sheet database.
Follow Artists on Spotify: Offers an option to follow artists from the playlist on Spotify.
Export Data: Saves the scraped data to CSV and text files, including a summary of found Instagram accounts and newly followed artists on Spotify.
Usage Scenarios
Extracting Artist Data: Input a Spotify playlist URL to get artist names and their Spotify URLs.
Instagram Account Search: The script scrapes each artist's Spotify page for an Instagram account link. If not found, it checks a Google Sheet database for a match.
Following Artists: You can choose to follow artists from the playlist who are not already followed on Spotify.
Data Export: After processing, you have the option to save the data in CSV or text format. The text file includes a summary of total artists, found Instagram accounts, accounts found in the database, and accounts not found. It also lists newly followed artists on Spotify if that option was chosen.
Requirements
Python environment with necessary libraries (spotipy, selenium, gspread, etc.).
Spotify API credentials.
Google Sheets API setup with a service account.
Chrome WebDriver for Selenium.
Note
Ensure all credentials and URLs are correctly set up in the script before running it. The script is interactive and will prompt for inputs and choices during execution.
