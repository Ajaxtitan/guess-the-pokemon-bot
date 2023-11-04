import requests
import shutil

for i in range(1, 1011):
    url = f"https://serebii.net/pokemon/art/{str(i).zfill(3)}.png"
    pic = requests.get(url, stream=True)
    if pic.status_code == 200:
        with open(f"{str(i).zfill(3)}.png", "wb") as file:
            shutil.copyfileobj(pic.raw, file)
        print(f"Pokedex #{i} successfully saved!")