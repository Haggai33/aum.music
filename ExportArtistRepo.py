import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Prompt user for the Google Sheet link
sheet_url = input("Enter the Google Sheet link: ")

# Prompt user for the path to the JSON key file
json_keyfile_path = "C:\\Aum.Music\\credentials.json"

# Set up the credentials using the provided JSON key file path
creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
client = gspread.authorize(creds)

# Open the Google Sheet using the provided link
sheet = client.open_by_url(sheet_url)

# Select the "artist" column
worksheet = sheet.sheet1
cell = worksheet.find('Artist')

if cell is not None:
    column_index = cell.col
    column_values = worksheet.col_values(column_index)

    # Exclude the header row (assuming the first row is the header)
    artist_values = column_values[1:]

    # Write artist values to a text file
    with open('artists.txt', 'w') as file:
        for artist in artist_values:
            if ',' in artist:
                artists = artist.split(",")
                for a in artists:
                    file.write(a.strip() + '\n')
                    file.write('@\n.\n')
            else:
                file.write(artist.strip() + '\n')
                file.write('@\n.\n')

    print("Artist values have been written to 'artists.txt' file.")
else:
    print("'artist' column not found in the worksheet.")
