import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Set up the credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Prompt user for the Google Sheet link
sheet_url = input("Enter the Google Sheet link: ")
aum_sheet_url = "https://docs.google.com/spreadsheets/d/1j8jRlbBJi_6GREbj9vhlUvv6SQXAFkZp32M4WLy0Wkk/edit?usp=sharing"

# Prompt user for the path to the JSON key file
json_keyfile_path = "C:\\Aum.Music\\credentials.json"

# Set up the credentials using the provided JSON key file path
creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
client = gspread.authorize(creds)
aum_client = gspread.authorize(creds)

# Open the Google Sheet using the provided link
sheet = client.open_by_url(sheet_url)
aum_sheet = aum_client.open_by_url(aum_sheet_url)

# Select the "artist" column
worksheet = sheet.sheet1
cell = worksheet.find('Artist')

# Select the "artist" column in Aum
aum_worksheet = aum_sheet.worksheet("IG Artist")
aum_artist_values = aum_worksheet.col_values(1)[1:]  # Exclude header row

written_artists = set()

if cell is not None:
    column_index = cell.col
    column_values = worksheet.col_values(column_index)[1:]  # Exclude header row

    # Write artist values to a text file
    with open('artists.txt', 'w') as file:
        for artist in column_values:
            if ',' in artist:
                artists = artist.split(",")
                for a in artists:
                    if a.strip() not in written_artists:
                        if a in aum_artist_values:
                            index = aum_artist_values.index(a) + 2  # Adjust index to account for header row
                            ig_artist = aum_worksheet.cell(index, 4).value
                            file.write(a.strip() + '\n')
                            file.write(f'@{ig_artist}' + '\n')
                            file.write('.\n')
                            written_artists.add(a.strip())
            elif artist.strip() not in written_artists:
                if artist in aum_artist_values:
                    index = aum_artist_values.index(artist) + 2  # Adjust index to account for header row
                    ig_artist = aum_worksheet.cell(index, 4).value
                    file.write(artist.strip() + '\n')
                    file.write(f'@{ig_artist}' + '\n')
                    file.write('.\n')
                    written_artists.add(artist.strip())

    print("Artist values have been written to 'artists.txt' file.")
    os.system('notepad.exe artists.txt')
else:
    print("'Artist' column not found in the worksheet.")
