"""
The first step in the seam carving algorithm: computing the energy of an image.

    python3 energy.py surfer.jpg surfer-energy.png
"""


import sys

from utils import Color, read_image_into_array, write_array_into_image


def energy_at(pixels, x, y):
    """
    Compute the energy of the image at the given (x, y) position.

    """
    energy = 0
    if y == len(pixels) - 1 or y ==0 or x == len(pixels[0]) - 1 or x == 0:
        energy = pow(pixels[y][x].r,2)+ pow(pixels[y][x].g,2) + pow(pixels[y][x].b,2)
    else:
        delta_x_r = pow((pixels[y][x+1].r - pixels[y][x-1].r),2)
        delta_x_g = pow((pixels[y][x+1].g - pixels[y][x-1].g),2)
        delta_x_b = pow((pixels[y][x+1].b - pixels[y][x-1].b),2)
        delta_y_r = pow((pixels[y+1][x].r - pixels[y-1][x].r),2)
        delta_y_g = pow((pixels[y+1][x].g - pixels[y-1][x].g),2)
        delta_y_b = pow((pixels[y+1][x].b - pixels[y-1][x].b),2)
        delta_x = delta_x_r + delta_x_g + delta_x_b
        delta_y = delta_y_r + delta_y_g + delta_y_b
        energy = delta_x + delta_y
    return energy
    raise NotImplementedError('energy_at is not implemented')

def compute_energy(pixels):
    """
    Compute the energy level at each individual pixels
    """
    grid = [[None for _ in row] for row in pixels]
    for y in range(len(pixels)):
        for x in range(len(pixels[y])):
            grid[y][x] = energy_at(pixels, x, y)
    return grid
    raise NotImplementedError('compute_energy is not implemented')


def energy_data_to_colors(energy_data):
    """
    Convert the energy values at each pixel into colors that can be used to
    visualize the energy of the image. The steps to do this conversion are:

      1. Normalize the energy values to be between 0 and 255.
      2. Convert these values into grayscale colors, where the RGB values are
         all the same for a single color.

    """

    colors = [[0 for _ in row] for row in energy_data]

    max_energy = max(
        energy
        for row in energy_data
        for energy in row
    )

    for y, row in enumerate(energy_data):
        for x, energy in enumerate(row):
            energy_normalized = round(energy / max_energy * 255)
            colors[y][x] = Color(
                energy_normalized,
                energy_normalized,
                energy_normalized
            )

    return colors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'USAGE: {__file__} <input> <output>')
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    print(f'Reading {input_filename}...')
    pixels = read_image_into_array(input_filename)

    print('Computing the energy...')
    energy_data = compute_energy(pixels)
    energy_pixels = energy_data_to_colors(energy_data)

    print(f'Saving {output_filename}')
    write_array_into_image(energy_pixels, output_filename)
