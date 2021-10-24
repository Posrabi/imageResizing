"""
The second step in the seam carving algorithm: finding the energy of the lowest-
energy seam in an image. In this version of the algorithm, only the energy value
of the seam is determined. However, this version of the algorithm still forms
the basis of overall seam carving process.

If you run this module in isolation, the location of the _end_ of the seam will
be visualized:

    python3 seam_v1.py surfer.jpg surfer-seam-energy-v1.png
"""


import sys

from PIL.Image import effect_mandelbrot

from energy import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


def compute_vertical_seam_v1(energy_data):
    """
    Find the lowest-energy vertical seam given the energy of each pixel in the
    input image. The image energy should have been computed before by the
    `compute_energy` function in the `energy` module.

    This is the first version of the seam finding algorithm. You will implement
    the recurrence relation directly, outputting the energy of the lowest-energy
    seam and the x-coordinate where that seam ends.

    This is one of the functions you will need to implement. Expected return
    value: a tuple with two values:

      1. The x-coordinate where the lowest-energy seam ends.
      2. The total energy of that seam.
    """
    cache = {}
    bot_row = []
    for idx, ele in enumerate(energy_data[0]):
        cache[(idx,0)] = ele
    def subproblem (x, y):
        if (x,y) in cache:
            return cache[(x,y)]
        elif x == 0:
            energy = min(subproblem(x,y-1),subproblem(x+1,y-1)) + energy_data[y][x]
        elif x == len(energy_data[0]) - 1:
            energy = min(subproblem(x,y-1), subproblem(x-1, y -1)) + energy_data[y][x]
        else:
            energy = min(subproblem(x,y-1), subproblem(x+1, y-1) , subproblem(x-1, y-1)) + energy_data[y][x]
        cache[(x,y)] = energy
        return energy

    for idx_row, row in enumerate(energy_data[1:]):
        for idx_col in range(len(row)):
            subproblem(idx_col, idx_row+1)
    for idx,ele in enumerate(energy_data[len(energy_data)-1]):
        bot_row.append(cache[(idx,len(energy_data)-1)])
    ans = min(bot_row)
    return (bot_row.index(ans), ans)
    raise NotImplementedError('compute_vertical_seam_v1 is not implemented')


def visualize_seam_end_on_image(pixels, end_x):
    """
    Draws a red box at the bottom of the image at the specified x-coordinate.
    This is done to visualize approximately where a vertical seam ends.

    This is NOT one of the functions you have to implement.
    """

    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    min_x = max(end_x - 5, 0)
    max_x = min(end_x + 5, w - 1)

    min_y = max(h - 11, 0)
    max_y = h - 1

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            new_pixels[y][x] = Color(255, 0, 0)

    return new_pixels


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

    print('Finding the lowest-energy seam...')
    min_end_x, min_seam_energy = compute_vertical_seam_v1(energy_data)

    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_end_on_image(pixels, min_end_x)
    write_array_into_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {min_end_x}')
