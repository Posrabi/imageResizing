"""
A re-implementation of the second step in the seam carving algorithm: finding
the lowest-energy seam in an image. In this version of the algorithm, not only
is the energy value of the seam determined, but it's possible to reconstruct the
entire seam from the top to the bottom of the image.

    python3 seam_v2.py surfer.jpg surfer-seam-energy-v2.png
"""


import sys

from energy import compute_energy
from utils import Color, read_image_into_array, write_array_into_image


class SeamEnergyWithBackPointer:
    """
    Represents the total energy of a seam along with a back pointer:

      - Stores the total energy of a seam that ends at some position in the
        image. The position is not stored because it can be inferred from where
        in a 2D grid this object appears.

      - Also stores the x-coordinate for the pixel in the previous row that led
        to this particular seam energy. This is the back pointer from which the
        entire seam can be reconstructed.
    """
    def __init__(self, energy, back,x):
        self.energy = energy
        self.back = back
        self.x = x

    #raise NotImplementedError('SeamEnergyWithBackPointer is not implemented')


def compute_vertical_seam_v2(energy_data):
    """
    Find the lowest-energy vertical seam given the energy of each pixel in the
    input image. The image energy should have been computed before by the
    `compute_energy` function in the `energy` module.

    This is the second version of the seam finding algorithm
    Expected return value: a tuple with two values:

      1. The list of x-coordinates forming the lowest-energy seam, starting at
         the top of the image.
      2. The total energy of that seam.
    """
    cache = {}
    seam =[]
    bot_row = []

    for idx, ele in enumerate(energy_data[0]):
        cache[(idx,0)] = SeamEnergyWithBackPointer(ele, None, idx)

    def subproblem (x, y):
        if (x,y) in cache:
            return cache[(x,y)]
        elif x == 0:
            a = [subproblem(x,y-1), subproblem(x+1,y-1)]
            a = sorted(a, key=lambda x: x.energy)
            energy = a[0].energy + energy_data[y][x]
            back = a[0]
        elif x == len(energy_data[0]) - 1:
            a = [subproblem(x,y-1), subproblem(x-1,y-1)]
            a = sorted(a, key=lambda x: x.energy)
            energy = a[0].energy + energy_data[y][x]
            back = a[0]
        else:
            a = [subproblem(x,y-1), subproblem(x-1,y-1), subproblem(x+1, y-1)]
            a = sorted(a, key=lambda x: x.energy)
            energy = a[0].energy + energy_data[y][x]
            back = a[0]
        return SeamEnergyWithBackPointer(energy, back, x)

    for idx_row, row in enumerate(energy_data[1:]):
        for idx_col in range(len(row)):
            cache[(idx_col, idx_row+1)] = subproblem(idx_col, idx_row+1)
    for idx in range(len(energy_data[0])):
        bot_row.append(cache[(idx, len(energy_data) - 1)]) #store the bottom row(list of objects)
    bot_row = sorted(bot_row, key=lambda x: x.energy) #sort according to enery
    ans = bot_row[0] #take the min after sorting
    while ans:
        seam.append(ans.x)
        ans = ans.back #track back with linked lists
    seam = seam[::-1]
    return (seam, bot_row[0].energy)

    raise NotImplementedError('compute_vertical_seam_v2 is not implemented')


def visualize_seam_on_image(pixels, seam_xs):
    """
    Draws a red line on the image along the given seam. This is done to
    visualize where the seam is.

    This is NOT one of the functions you have to implement.
    """

    h = len(pixels)
    w = len(pixels[0])

    new_pixels = [[p for p in row] for row in pixels]

    for y, seam_x in enumerate(seam_xs):
        min_x = max(seam_x - 2, 0)
        max_x = min(seam_x + 2, w - 1)

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
    seam_xs, min_seam_energy = compute_vertical_seam_v2(energy_data)

    print(f'Saving {output_filename}')
    visualized_pixels = visualize_seam_on_image(pixels, seam_xs)
    write_array_into_image(visualized_pixels, output_filename)

    print()
    print(f'Minimum seam energy was {min_seam_energy} at x = {seam_xs[-1]}')
