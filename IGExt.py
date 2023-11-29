import spotipy, logging, time, csv, gspread
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from oauth2client.service_account import ServiceAccountCredentials

# Spotify API credentials
CLIENT_ID = 'f8ad5b8eb68940b48b5dac24e5567e2b'
CLIENT_SECRET = 'e2966868aae44b078cb89b4f01577709'
REDIRECT_URI = 'http://localhost:8888/callback'

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='playlist-read-private user-follow-read user-follow-modify'))

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Aum.Music\\credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1j8jRlbBJi_6GREbj9vhlUvv6SQXAFkZp32M4WLy0Wkk"
sheet = client.open_by_url(spreadsheet_url).worksheet("IG Artist")

# Configure logging
log_file_path = 'C:\\Users\\Administrator\\Downloads\\script_log.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_playlist_artists(sp, playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist['name']
    playlist_description = playlist.get('description', '')
    releases_dates = "None"
    genre = "None"

    # Extract release dates from the description
    if "Releases" in playlist_description:
        try:
            releases_dates = playlist_description.split("Releases")[0].strip()
        except Exception as e:
            logging.error(f"Error extracting release dates: {e}")

    # Extract genre from the description
    try:
        if "|" in playlist_description:
            parts = playlist_description.split("|")
            if len(parts) > 2:
                genre = parts[1].strip()
    except Exception as e:
        print(f"Error extracting genre: {e}")

    results = playlist['tracks']
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

    return artists_info, playlist_name, releases_dates, genre

def smooth_scroll(driver, class_name):
    for _ in range(10):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        if driver.find_elements(By.CLASS_NAME, class_name):
            return True
    return False

def check_in_db(username, artist_name):
    try:
        ig_user_col = sheet.col_values(4)  # IG user column
        artist_name_col = sheet.col_values(1)  # Artist Name column
    except:
        return "No"

    # Check if username is in IG user column
    if username in ig_user_col:
        return "Yes"

    # Function to try different name formats
    def try_name_formats(name):
        formats = [
            name.lower(),  # All lowercase
            name.title(),  # First letter of each word capitalized
            name.upper(),  # All uppercase
            ' '.join([name.split()[0].capitalize(), name.split()[1].lower()]) if len(name.split()) > 1 else name  # First name capitalized, last name lowercase
        ]
        for fmt in formats:
            if fmt in artist_name_col:
                index = artist_name_col.index(fmt)
                return sheet.cell(index + 1, 4).value or "No"
        return "No"

    return try_name_formats(artist_name)



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
                in_db = check_in_db(instagram_username, name)
                if in_db == "No":
                    instagram_username = "NONE"
                print(f"{name}: {instagram_username} (In DB: {in_db})")
                key = (name, instagram_username, in_db)
            except (NoSuchElementException, TimeoutException) as e:
                in_db = check_in_db("NONE", name)
                print(f"{name}: None (In DB: {in_db})")
                key = (name, "NONE", in_db)
                logging.warning(f"Element not found or timeout occurred: {e}")

            instagram_accounts[key] = instagram_accounts.get(key, 0) + 1
        else:
            in_db = check_in_db("NONE", name)
            print(f"{name}: None (In DB: {in_db})")
            key = (name, "NONE", in_db)
            instagram_accounts[key] = instagram_accounts.get(key, 0) + 1

    return instagram_accounts

def save_to_csv(instagram_accounts):
    csv_file_path = 'C:\\Users\\Administrator\\Downloads\\instagram_accounts.csv'
    while True:
        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['Artist Name', 'Instagram Username', 'Count', 'In DB'])
                for (name, username, in_db), count in instagram_accounts.items():
                    writer.writerow([name, username, count, in_db])
            logging.info("Instagram accounts successfully saved to CSV file.")
            break  # Break out of the loop if file is successfully written
        except PermissionError as e:
            logging.error(f"PermissionError: Unable to write to the CSV file. Check if the file is open in your computer. Error: {e}")
            print(f"PermissionError: Unable to write to the CSV file. Check if the file is open in your computer. Press Enter to retry.")
            input()  # Wait for user input before retrying

def save_to_text(instagram_accounts, playlist_number="None", playlist_name="None", releases_dates="None", genre="None", new_followed_artists=None):
    with open('C:\\Users\\Administrator\\Downloads\\instagram_accounts.txt', mode='w', encoding='utf-8') as file:

        file.write("*ᗆum.Music*\n")
        file.write(f"ᑭしᗩᎩしᏆᔑᎢ *{playlist_number}*\n")
        file.write(f"彡 *{playlist_name}* 彡\n\n")
        file.write(f"{releases_dates} Releases\n.\n")

        # Format and write genre
        genre_parts = genre.split("♩")
        genre_formatted = "\n♩".join(genre_parts[1:])  # Add "♩" before each genre part
        file.write(f"\n♩{genre_formatted}\n\n.\n")

        file.write("*Spotify*\n\n\n")
        file.write("*Apple Music*\n\n\n")
        file.write("*YouTube*\n\n")
        file.write(".\n📸*IG:* @\n")
        file.write("אם בא לכם לעזור לי לקדם את הפרויקט\n")
        file.write("אשמח שתוסיפו לי עוקב באינסטה,\n")
        file.write("זה לוקח שנייה ועוזר לאלגוריתם להתעורר על צד ימין 🙏\n")
        file.write("instagram.com/aum.music\n")
        file.write("\n\n\n\n\n")

        # IG Post
        file.write(f"\n{releases_dates} Releases\n")
        file.write(f"Week #{''.join(filter(str.isdigit, playlist_number))}\n")
        file.write(f"彡 {playlist_name} 彡\n\n")  # Assuming playlist_name is already formatted as "彡 Name 彡"
        file.write("Link in Bio\n.\n")
        genre_formatted = "\n♩".join(genre_parts[1:])  # Add "♩" before each genre part
        file.write(f"\n♩{genre_formatted}\n\n.\n")
        file.write(".\n" * 3)
        file.write("📸@\n")
        file.write(".\n" * 5)  # 5 blank lines
        file.write("#aummusic #aumusic\n")
        file.write("#newmusicrelease #discovermusic #spotifyplaylists\n")
        file.write("#newplaylist #discoverartists #spotifycharts\n")
        file.write("\n" * 5)  # 5 blank lines

        total_artists = len(instagram_accounts)
        found = sum(1 for _, _, in_db in instagram_accounts if in_db == "Yes")
        found_in_db = sum(1 for _, _, in_db in instagram_accounts if in_db != 'No' and in_db != 'Yes')
        not_found = total_artists - found - found_in_db
        for (name, username, in_db), count in instagram_accounts.items():
            username_to_write = username if username != 'NONE' else (in_db if in_db != 'No' else '')
            file.write(f"{name}\n@{username_to_write}\n.\n")

        file.write("\n" * 5)  # 5 blank lines
        file.write(f"Total Artists: {total_artists}\nFound: {found}\nFound in DB: {found_in_db}\nNot Found: {not_found}\n")

        if new_followed_artists:
            file.write("\nNewly Followed Artists on Spotify:\n")
            for artist in new_followed_artists:
                file.write(f"{artist}\n")
            file.write(f"Total Newly Followed: {len(new_followed_artists)}\n")

def main():
    playlist_url = input("Enter the Spotify playlist URL: ")
    artists_info, full_playlist_name, releases_dates, genre = get_playlist_artists(sp, playlist_url)  # Unpack four values

    try:
        # Reformat playlist name if it contains "彡"
        if "彡" in full_playlist_name:
            parts = full_playlist_name.split("彡")
            # Remove empty strings and join the parts with "彡"
            playlist_name = "彡" + "彡".join(part.strip() for part in parts if part.strip()) + "彡"
        else:
            playlist_name = full_playlist_name
    except Exception as e:
        print(f"Error processing playlist name: {e}")
        playlist_name = "None"


    driver = webdriver.Chrome()
    try:
        instagram_accounts = scrape_artist_pages(driver, artists_info)
        found_in_db = sum(1 for _, _, in_db in instagram_accounts if in_db != 'No')
        print(f"\nProcessed {len(artists_info)} artists.")
        print(f"Found Instagram accounts for {found_in_db} artists.")
        print(f"Instagram accounts not found for {len(artists_info) - found_in_db} artists.")

        create_csv = input("Would you like to save the results to a CSV file? (y/n): ").lower()
        if create_csv == 'y':
            save_to_csv(instagram_accounts)
            print("Instagram accounts saved to CSV file.")

        create_text = input("Would you like to save the results to a text file? (y/n): ").lower()
        if create_text == 'y':
            new_artists = None
            follow_artists = input("Would you like to follow the artists from this playlist on Spotify? (y/n): ").lower()
            if follow_artists == 'y':
                new_artists = follow_new_artists_in_playlist(playlist_url)
                if new_artists:
                    print("New artists followed on Spotify:")
                    for artist in new_artists:
                        print(artist)
                else:
                    print("You are already following all the artists in this playlist.")

            save_to_text(instagram_accounts, playlist_number, playlist_name, releases_dates, genre,
                         new_followed_artists=new_artists)
    finally:
        driver.quit()


def get_all_followed_artists():
    """Retrieve all artists the user is currently following."""
    followed_artists = set()
    results = sp.current_user_followed_artists(limit=50)

    while results:
        artists = results['artists']
        for item in artists['items']:
            followed_artists.add(item['id'])

        if artists['next']:
            results = sp.next(artists)
        else:
            break

    return followed_artists

def get_playlist_artist_ids(playlist_id):
    """Retrieve all artist IDs from a playlist."""
    artist_ids = set()
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                for artist in track['artists']:
                    artist_ids.add(artist['id'])

        if results['next']:
            results = sp.next(results)
        else:
            break

    return artist_ids

def follow_new_artists_in_playlist(playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    followed_artist_ids = get_all_followed_artists()
    playlist_artist_ids = get_playlist_artist_ids(playlist_id)

    new_artists = []
    for artist_id in playlist_artist_ids:
        if artist_id not in followed_artist_ids:
            sp.user_follow_artists([artist_id])
            artist_info = sp.artist(artist_id)
            new_artists.append(artist_info['name'])

    return new_artists

def main():
    playlist_url = input("Enter the Spotify playlist URL: ")
    artists_info, full_playlist_name, releases_dates, genre = get_playlist_artists(sp, playlist_url)  # Unpack four values

    # Process playlist name to extract name and number
    try:
        if "彡" in full_playlist_name:
            parts = full_playlist_name.split("彡")
            playlist_name = "" + parts[1].strip() + ""  # Assuming the name is always between 彡 symbols
            playlist_number = parts[-1].strip()  # Assuming the number is after the last 彡
        else:
            playlist_name = full_playlist_name  # Default to the full name if 彡 not found
            playlist_number = "None"
    except Exception as e:
        print(f"Error processing playlist name: {e}")
        playlist_name = "None"
        playlist_number = "None"
        logging.error(f"Error in main function: {e}")


    driver = webdriver.Chrome()
    try:
        instagram_accounts = scrape_artist_pages(driver, artists_info)
        found_in_db = sum(1 for _, _, in_db in instagram_accounts if in_db != 'No')
        print(f"\nProcessed {len(artists_info)} artists.")
        print(f"Found Instagram accounts for {found_in_db} artists.")
        print(f"Instagram accounts not found for {len(artists_info) - found_in_db} artists.")

        create_csv = input("Would you like to save the results to a CSV file? (y/n): ").lower()
        if create_csv == 'y':
            save_to_csv(instagram_accounts)
            print("Instagram accounts saved to CSV file.")

        create_text = input("Would you like to save the results to a text file? (y/n): ").lower()
        if create_text == 'y':
            new_artists = None
            follow_artists = input("Would you like to follow the artists from this playlist on Spotify? (y/n): ").lower()
            if follow_artists == 'y':
                new_artists = follow_new_artists_in_playlist(playlist_url)
                if new_artists:
                    print("New artists followed on Spotify:")
                    for artist in new_artists:
                        print(artist)
                else:
                    print("You are already following all the artists in this playlist.")

            save_to_text(instagram_accounts, playlist_number, playlist_name, releases_dates, genre, new_followed_artists=new_artists)


            print("Instagram accounts saved to text file.")

    finally:
        driver.quit()


if __name__ == "__main__":
    logging.info("Script started")
    main()
    logging.info("Script finished")
