import numpy as np
from PIL import Image

from config import Config

if __name__ == "__main__":
    # do the following code for every image in the directory
    for dex_num in range(1, Config.LARGEST_POKEDEX_NUMBER + 1):
        sprite_file_name = f"{str(dex_num).zfill(3)}.png"
        silhouette_file_name = f"{str(dex_num).zfill(3)}-dark.png"

        # open image and convert to numpy array
        na = np.array(Image.open(Config.SPRITE_CACHE_DIR/sprite_file_name))

        # make every pixel, of every row of every column black in RGB channels, i.e. channel 0, 1, 2
        na[:, :, :3] = 0

        # make boolean True/False mask of all alphas >200
        mask = na[:, :, 3] > 200

        # set alpha channel to 255 wherever mask is True, and 0 elsewhere
        na[:, :, 3] = mask * 255

        # convert back from numpy array to PIL Image
        img = Image.fromarray(na)
        new_img = Image.new("RGBA", img.size, "WHITE")
        new_img.paste(img, (0, 0), img)
        new_img.convert("RGB").save(Config.SPRITE_CACHE_DIR/silhouette_file_name)
