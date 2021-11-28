"""
The third and final step in the seam carving process: removing the lowest-energy
seam from an image. By doing so iteratively, the size of the image can be
reduced (in one dimension) by multiple pixels.
Run this module in isolation to resize your image!

    python3 carve.py surfer.jpg 10 surfer-resized.png
"""


import sys

from energy import compute_energy
from seam_v2 import compute_vertical_seam_v2, visualize_seam_on_image
from utils import Color, read_image_into_array, write_array_into_image


def remove_seam_from_image(image, seam_xs):
    """
    Remove pixels from the given image, as indicated by each of the
    x-coordinates in the input. The x-coordinates are specified from top to
    bottom and span the entire height of the image.

    """
    for idx,_ in enumerate(image):
        i = seam_xs[idx]
        del image[idx][i]

    return image

    raise NotImplementedError('remove_seam_from_image is not implemented')


def remove_n_lowest_seams_from_image(image, num_seams_to_remove):
    """
    Iteratively:

    1. Find the lowest-energy seam in the image.
    2. Remove that seam from the image.

    """
    for i in range(num_seams_to_remove):
        energy_data = compute_energy(image) # this must be in here to create new energy_data each new iteration
        seam_xs = compute_vertical_seam_v2(energy_data)[0]
        image = remove_seam_from_image(image,seam_xs)
    return image
    raise NotImplementedError(
        'remove_n_lowest_seams_from_image is not implemented')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'USAGE: {__file__} <input> <num-seams-to-remove> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    num_seams_to_remove = int(sys.argv[2])
    output_filename = sys.argv[3]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print(f'Saving {output_filename}')
    resized_pixels = \
        remove_n_lowest_seams_from_image(pixels, num_seams_to_remove)
    write_array_into_image(resized_pixels, output_filename)
