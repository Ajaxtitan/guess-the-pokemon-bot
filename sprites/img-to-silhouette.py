import numpy as np
from PIL import Image

# do the following code for every image in the directory
for i in range(1, 1011):

    # open image and convert to numpy array
    na = np.array(Image.open(f"{str(i).zfill(3)}.png"))

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
    new_img.convert("RGB").save(f"{str(i).zfill(3)}-dark.png")

