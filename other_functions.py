import random
import string


def generate_imagename(extension):
    number_of_characters = 7
    image_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_characters))
    image_name = image_name + '.' + extension
    print(image_name)

    return image_name