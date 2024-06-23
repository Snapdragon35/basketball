import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get the HTML content of a given URL
def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching the URL: {url}\n{e}")
        return None

# Function to parse player stats from the given HTML content using pandas
def parse_player_stats(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'per_game_stats'})
    if table:
        try:
            df = pd.read_html(str(table))[0]
            return df
        except ValueError as e:
            print(f"Error parsing the table: {e}")
            return None
    else:
        print("Error: Table with id 'per_game_stats' not found.")
        return None

# Function to save the stats to a CSV file
def save_to_csv(df, filename='nba_player_stats.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to scrape NBA player stats
def scrape_nba_stats(url):
    html_content = get_html_content(url)
    if html_content:
        player_stats_df = parse_player_stats(html_content)
        if player_stats_df is not None:
            save_to_csv(player_stats_df)

# URL of the page to scrape
url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'

# Scrape and save the NBA player stats
scrape_nba_stats(url)
