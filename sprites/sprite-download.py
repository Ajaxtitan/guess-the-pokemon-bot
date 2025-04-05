import shutil

import requests

from config import Config

if __name__ == "__main__":
    for dex_num in range(1, Config.LARGEST_POKEDEX_NUMBER + 1):
        url = f"https://serebii.net/pokemon/art/{str(dex_num).zfill(3)}.png"
        pic = requests.get(url, stream=True)
        if pic.status_code == 200:
            with open(f"{str(dex_num).zfill(3)}.png", "wb") as file:
                shutil.copyfileobj(pic.raw, file)
            print(f"Pokedex #{dex_num} successfully saved!")
