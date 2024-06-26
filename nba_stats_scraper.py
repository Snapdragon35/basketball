from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import time

# List of seasons you want to fetch data for
seasons = [f'{year}-{str(year+1)[-2:]}' for year in range(1996, 2022)]
full_player_data = pd.DataFrame()

for season in seasons:
    print(f'Fetching data for {season} season...')
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
    df = player_stats.get_data_frames()[0]
    df['Season'] = int(season[:2] + season[5:])  # Add a season column to the DataFrame
    full_player_data = pd.concat([full_player_data, df], ignore_index=True)

# Display the first few rows of the combined DataFrame
print(full_player_data.head())

# Save the combined DataFrame to a CSV file
full_player_data.to_csv('nba_player_stats_1997_2022.csv', index=False)
