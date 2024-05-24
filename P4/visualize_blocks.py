#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from buscaRyP import read_file

def visualize_block(block):
    fig, ax = plt.subplots()

    # Create a rectangle for each article in the block
    for article in block.articles:
        ax.add_patch(patches.Rectangle((article.x, article.y), article.w, article.h, edgecolor='black', facecolor='none'))

    # Set the limits of the plot to the size of the block
    ax.set_xlim(0, block.W)
    ax.set_ylim(0, block.H)

    plt.gca().invert_yaxis()  # Invert y axis to match the coordinate system in the problem
    plt.show()

if __name__ == '__main__':
    # read file name from command line
    if len(sys.argv) != 2:
        print("Usage: python3 visualize.py <file_name>")
        sys.exit(1)

    file = sys.argv[1]

    # Read the blocks from the file
    blocks = read_file(file)

    # Visualize the first block
    for block in blocks:
        visualize_block(block)
