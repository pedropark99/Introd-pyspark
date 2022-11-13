#!/bin/bash


# Convert is used to concatenate (or append, or merge) two images together
# This command put the python logo in the center of a background of a certain color
# The -extent component defines the size of the final image (or the size of the background if you prefer to understand in this way)
magick convert Images/python.png -gravity center -background '#164E80' -extent 2000x2000 Images/test.png

# Mogrify is used to modify (or replace) the color of all pixels that match a certain color
# The command below I am replacing all white pixels by a pixel of color "#164E80"
magick mogrify Images/test.png -fill "#164E80" -fuzz 15% -opaque "#FFFFFF" Images/test.png


# The command below I am replacing all black pixels by a null (or empty) pixel
magick mogrify Images/test.png -fill none -fuzz 15% -opaque "#000000" Images/test.png


