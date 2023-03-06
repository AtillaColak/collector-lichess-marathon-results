import time
import timeit
import matplotlib.pyplot as plt
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
        time.sleep(0.1)  # Add a delay of 1 second
        return df
    else:
        print(f'Error downloading CSV file for {link}: {response.text}')
        return None



def download_csv(link, year, season):
    df = get_dataframe(link, year, season)
    time.sleep(0.2)  # wait for .2 a second before making the next request
    if df is not None:
        return df
    else:
        return pd.DataFrame()

def version1():

    seasons = ["spring", "autumn", "summer", "winter"]
    dfs = []

    if __name__ == '__main__':
        pool = mp.Pool(processes = 2)
        for year in range(18, 23):
            results = []
            for season in seasons:
                link = f"https://lichess.org/api/tournament/{season}{year}/results?as=csv"
                results.append(pool.apply_async(download_csv, args=(link, year, season)))
            dfs.extend([r.get() for r in results])

        all_data = pd.concat(dfs)
        all_data.to_csv('all_marathons_ranks.csv', index=False)
    pass

def version2():

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
    pass

list_v1 = []
list_v2 = []
for i in range(10):
    t1 = timeit.timeit(version1, number=1)
    list_v1.append(t1)
    t2 = timeit.timeit(version2, number=1)
    list_v2.append(t2)

plt.plot(list_v1, list_v2)
plt.title('Execution time comparison')
plt.xlabel('Execution time (seconds) Multiprocessing')
plt.ylabel('Execution time (seconds) Standard')
plt.show()
