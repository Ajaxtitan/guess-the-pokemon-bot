import requests
from bs4 import BeautifulSoup

url = "https://www.serebii.net/pokemon/nationalpokedex.shtml"
data = requests.get(url)

soup = BeautifulSoup(data.content, "html.parser")

results = soup.find("table", class_="dextable")
lst = results.find_all("tr")[2:]

ALL_POKEMON = []

# cleaning up the data
for pokemon in lst:
    name = pokemon.find_all("td")
    if len(name) < 2:
        continue
    ALL_POKEMON.append(name[3].text.strip())