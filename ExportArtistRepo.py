from oauth2client.service_account import ServiceAccountCredentials
import os, csv, re, gspread

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

try:
    # Open the Google Sheet using the provided link
    sheet = client.open_by_url(sheet_url)
    aum_sheet = client.open_by_url(aum_sheet_url)
except Exception as e:
    print("Error opening sheets:", str(e))
    exit()

# Select the "artist" column
worksheet = sheet.sheet1
try:
    cell = worksheet.find('Artist')
except Exception as e:
    print("'Artist' column not found in the worksheet.", str(e))
    exit()

# Select the "artist" column in Aum
aum_worksheet = aum_sheet.worksheet("IG Artist")
aum_artist_values = aum_worksheet.col_values(1)[1:]  # Exclude header row
aum_artist_values_lower = [item.lower() for item in aum_artist_values]  # Convert all to lowercase outside the loop

written_artists = set()

if cell is not None:
    column_index = cell.col
    column_values = worksheet.col_values(column_index)[1:]  # Exclude header row

    total_artists = 0
    found_ig_artists = 0
    not_found_artists = 0

    # Write artist values to a text file
    with open('artists.txt', 'w') as file:
        for artist in column_values:
            if ',' in artist:
                artists = artist.split(",")
            else:
                artists = [artist]

            for a in artists:
                a_lower = a.strip().lower()  # Convert to lowercase and strip whitespaces
                total_artists += 1
                if a_lower not in written_artists:
                    # Remove non-alphabetic characters from the artist name
                    a_only_alphabets = re.sub('[^a-zA-Z]', '', a_lower)

                    # Perform an exact check first
                    if a_lower in aum_artist_values_lower:
                        ig_artist = aum_worksheet.cell(aum_artist_values_lower.index(a_lower) + 2, 4).value
                        found_ig_artists += 1
                    # Check again with the modified artist name
                    elif a_only_alphabets in aum_artist_values_lower:
                        ig_artist = aum_worksheet.cell(aum_artist_values_lower.index(a_only_alphabets) + 2, 4).value
                        found_ig_artists += 1
                    else:
                        ig_artist = ''
                        not_found_artists += 1

                    file.write(a.strip() + '\n')
                    file.write(f'@{ig_artist}' + '\n')
                    file.write('.\n')
                    written_artists.add(a_lower)  # Add the lowercased, stripped artist name to the set

        file.write('\n')  # A line break before the statistics
        file.write(f"Total artists: {total_artists}\n")
        file.write(f"Found IG artists: {found_ig_artists}\n")
        file.write(f"Not found IG artists: {not_found_artists}\n")

    print(f"Total artists: {total_artists}")
    print(f"Found IG artists: {found_ig_artists}")
    print(f"Not found IG artists: {not_found_artists}")
    print("Artist values have been written to 'artists.txt' file.")
    os.system('notepad.exe artists.txt')
else:
    print("'Artist' column not found in the worksheet.")
