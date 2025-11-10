import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Pokémon database
url = "https://pokemondb.net/pokedex/all"

# Send a GET request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing Pokémon data
table = soup.find("table", {"id": "pokedex"})

# Extract headers
headers = [th.text for th in table.find("thead").find_all("th")]

# Extract rows of data
rows = []
for tr in table.find("tbody").find_all("tr"):
    cols = [td.text.strip() for td in tr.find_all("td")]
    rows.append(cols)

# Create a DataFrame for easy data handling
pokemon_data = pd.DataFrame(rows, columns=headers)

# Save data to a CSV (optional)
pokemon_data.to_csv("pokemon_data.csv", index=False)

# Print the first few rows to verify
print(pokemon_data.head())
