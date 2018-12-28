import numpy as np
from PIL import Image
import random
import matplotlib.pyplot as plt


def create_random_image(width, height):
    data = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            data[y, x] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    return data


image = create_random_image(1920, 1080)

imgplot = plt.imshow(image)

