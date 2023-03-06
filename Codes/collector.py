import requests
import pandas as pd
import io
# This code is unoptimized and runs slower while iterating over 20 files.
# example links of the csv files: https://lichess.org/api/tournament/winter22/results?as=csv

# creates 2 new columns "year", "season" (to the csv requested in link) using the given year and season values.
def get_dataframe(link, year, season):
    response = requests.get(link)
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        # create a file-like object from a string of CSV
        df = pd.read_csv(io.StringIO(csv_data))
        df['Year'] = year
        df['Season'] = season
        return df
    else:
        print(f'Error downloading CSV file for {link}: {response.text}')
        return None

seasons = ["spring", "autumn", "summer", "winter"]
dfs = []

# loop through the marathon link combinations.
for year in range(18, 23):
    for season in seasons:
        link = f"https://lichess.org/api/tournament/{season}{year}/results?as=csv"
        df = get_dataframe(link, year, season)
        if df is not None:
            dfs.append(df)

# concatenate all files and convert it to csv.
all_data = pd.concat(dfs)
all_data.to_csv('all_marathons_ranks.csv', index=False)
