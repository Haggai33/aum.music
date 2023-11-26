import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv

# Spotify API credentials
CLIENT_ID = 'f8ad5b8eb68940b48b5dac24e5567e2b'
CLIENT_SECRET = 'e2966868aae44b078cb89b4f01577709'
REDIRECT_URI = 'http://localhost:8888/callback'

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='playlist-read-private'))

def get_playlist_artists(sp, playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    artists_info = []

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                for artist in track['artists']:
                    artist_info = sp.artist(artist['id'])
                    artists_info.append((artist_info['name'], artist_info['external_urls']['spotify']))

        if results['next']:
            results = sp.next(results)
        else:
            break

    return artists_info

def smooth_scroll(driver, class_name):
    for _ in range(10):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        if driver.find_elements(By.CLASS_NAME, class_name):
            return True
    return False

def scrape_artist_pages(driver, artists_info):
    instagram_accounts = {}
    for name, spotify_url in artists_info:
        driver.get(spotify_url)
        if smooth_scroll(driver, 'uhDzVbFHyCQDH6WrWZaC'):
            try:
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'uhDzVbFHyCQDH6WrWZaC'))).click()
                instagram_link = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.oe0FHRJU7PvjoTnXJmfr[href*="instagram.com"]')))
                instagram_url = instagram_link.get_attribute('href')
                instagram_username = instagram_url.split('instagram.com/')[-1].split('/')[0].split('?')[0]
                print(f"{name}: {instagram_username}")
                key = (name, instagram_username)
            except (NoSuchElementException, TimeoutException):
                print(f"{name}: None")
                key = (name, "NONE")

            instagram_accounts[key] = instagram_accounts.get(key, 0) + 1
        else:
            print(f"{name}: None")
            key = (name, "NONE")
            instagram_accounts[key] = instagram_accounts.get(key, 0) + 1

    return instagram_accounts

def save_to_csv(instagram_accounts):
    with open('C:\\Users\\Administrator\\Downloads\\instagram_accounts.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Artist Name', 'Instagram Username', 'Count'])
        for (name, username), count in instagram_accounts.items():
            writer.writerow([name, username, count])


def main():
    playlist_url = input("Enter the Spotify playlist URL: ")
    artists_info = get_playlist_artists(sp, playlist_url)

    driver = webdriver.Chrome()
    try:
        instagram_accounts = scrape_artist_pages(driver, artists_info)
        print(f"\nProcessed {len(artists_info)} artists.")
        print(f"Found Instagram accounts for {len([acc for acc in instagram_accounts if acc[1] != 'NONE'])} artists.")
        print(f"Instagram accounts not found for {len([acc for acc in instagram_accounts if acc[1] == 'NONE'])} artists.")

        create_csv = input("Would you like to save the results to a CSV file? (y/n): ").lower()
        if create_csv == 'y':
            save_to_csv(instagram_accounts)
            print("Instagram accounts saved to CSV file.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
