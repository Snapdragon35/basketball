from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

url = 'https://en.wikipedia.org/wiki/NBA_Most_Valuable_Player_Award'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
table = soup.find("table", { "class" : "wikitable plainrowheaders sortable" })
df = pd.read_csv('nba_player_stats_1997_2022.csv')

players = []
seasons = []
for i in range(42,len(range(1996,2021))+43):
    row = table.findAll("tr")[i]
    headers = row.findAll("th")
    cells = row.findAll("td")
    name = ""
    year = 1000
    if cells[0].find(text=True)[0] in '12':
        year = int(str(cells[0].find(text=True))[:4]) + 1
        name = str(headers[0].find("a").find(text=True))
    else:
        year = int(str(headers[0].find("a").find(text=True))[:4]) + 1
        name = str(headers[1].find("a").find(text=True))
    if name == "Nikola Jokić":
        name = "Nikola Jokic"
    for j in range(0,len(df.index)-1):
        if (year == df['Season'].iloc[j]) and (name == df['PLAYER_NAME'].iloc[j]):
            players.append(name)
            seasons.append(year)

MVP_awards = pd.DataFrame({'PLAYER_NAME' : players, 'Season' : seasons, 'MVPFlag' : 1})

full_mvp_data = pd.merge(df, MVP_awards, on=['PLAYER_NAME', 'Season'], how='left')
full_mvp_data['MVPFlag'] = full_mvp_data['MVPFlag'].fillna(0)
full_mvp_data.to_csv('mvp_data_1997_2022.csv', index=False)
print(players)
print(seasons)