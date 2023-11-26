import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

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
    for _ in range(10):  # Adjust the range as needed
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Adjust sleep time as needed
        if driver.find_elements(By.CLASS_NAME, class_name):
            return True
    return False

def scrape_artist_pages(driver, artists_info):
    for name, spotify_url in artists_info:
        print(f"Scraping for Artist: {name}, Spotify URL: {spotify_url}")
        if isinstance(spotify_url, str):
            driver.get(spotify_url)
        else:
            print(f"Invalid URL for {name}")
            continue

        # Smoothly scroll to find the element
        if smooth_scroll(driver, 'uhDzVbFHyCQDH6WrWZaC'):
            try:
                # Wait and click on the element to reveal social media links
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'uhDzVbFHyCQDH6WrWZaC'))).click()

                # Wait and find Instagram link
                instagram_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.oe0FHRJU7PvjoTnXJmfr[href*="instagram.com"]')))
                instagram_url = instagram_link.get_attribute('href')

                # Extract Instagram username from URL
                instagram_username = instagram_url.split('instagram.com/')[-1].rstrip('/')
                print(f"{name} Instagram: {instagram_username}")

            except (NoSuchElementException, TimeoutException):
                print(f"{name} - Element not found or Instagram link not available")
        else:
            print(f"{name} - Required element for revealing social media links not found")

def main():
    playlist_url = input("Enter the Spotify playlist URL: ")
    artists_info = get_playlist_artists(sp, playlist_url)

    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        scrape_artist_pages(driver, artists_info)
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
