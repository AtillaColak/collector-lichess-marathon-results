import requests
import pandas as pd
import io
import multiprocessing as mp

def get_dataframe(link, year, season):
    response = requests.get(link)
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        df['Year'] = year
        df['Season'] = season
        return df
    else:
        print(f'Error downloading CSV file for {link}: {response.text}')
        return None

seasons = ["spring", "autumn", "summer", "winter"]
dfs = []

def download_csv(link, year, season):
    df = get_dataframe(link, year, season)
    if df is not None:
        return df
    else:
        return pd.DataFrame()

if __name__ == '__main__':
    # I set processes to 2 because the Lichess API doesn't allow more than 2 concurrent requests.
    pool = mp.Pool(processes = 2)
    for year in range(18, 23):
        results = []
        for season in seasons:
            link = f"https://lichess.org/api/tournament/{season}{year}/results?as=csv"
            results.append(pool.apply_async(download_csv, args=(link, year, season)))
        dfs.extend([r.get() for r in results])

    all_data = pd.concat(dfs)
    all_data.to_csv('all_marathons_ranks.csv', index=False)