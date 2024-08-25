# Ipyzhov Kg23


## Sorting images by heat
The project is a tool for analyzing images and determining their "warmth" based on the analysis of color pixels. In this README you will find information about how to use the project, its structure and dependencies.

## Description
The project consists of a Python script that analyzes images in the HSL color model, determines which of them have dominant "warm" colors, and creates an HTML page that displays images sorted by warmth level. You can also adjust the "warmth" threshold to lower or increase the amount of warmth to display on the output HTML page. Input data: a folder with images in any quantity

## How to use
1. Make sure you have Python and the Pillow Library (PIL), which is used for image processing, installed.
2. Create a folder "images" and place the images you want to analyze there.Make sure the folder is in the same directory as the script.
3. Run the Python script main.py, which parses the images and produces an HTML page with the results.
4. Open the "output.html" file in your web browser. You will see a grid with images sorted by their warmth level.

## Project structure
'main.py': The project's main script that parses images and creates an HTML page.

'images/': Folder in which to place images for analysis.

'output.html': The generated HTML page with the results.

## Dependencies
The project uses the following dependencies:

- Python 3

- Pillow Library (PIL) for working with images

## Notes
This project determines the "warmth" of an image based on its color palette and whether the hue in the HSL color model matches a specific range.

Your web browser must support displaying HTML pages.
