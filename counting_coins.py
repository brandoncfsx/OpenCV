import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Path to the image.')
args = vars(ap.parse_args())

# Convert to grayscale and apply a large blurring size, making it easier for the edge detector to find the outline of the coins.
image = cv2.imread(args['image'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
cv2.imshow('Image', image)

edged = cv2.Canny(blurred, 30, 150)
cv2.imshow('Edges', edged)

# Args: edged image (use a copy since this function alters the image passed in), type of contours (RETR_EXTERNAL: retrieves only the outermost contours, can pass in RETR_LIST to grab all contours, there are also RETR_COMP and RETR_TREE for hierarchical contours), and the last arg is how we want to approximate the contour (CHAIN_APPROX_SIMPLE compresses horizontal, vertical and diagonal segments into their endpoints only - saves computation and memory, can pass in CHAIN_APPROX_NONE if we want all points without compression).
# Return values of findContours function is: Contours (a list) and hierarchy of the contours.
(cnts,hierarchy) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(f'Found {len(cnts)} coins in this image.')

# Create a copy of the image since we want to preserve the original.
coins = image.copy()
# Args: image we want to draw on, list of contours, contour index (-1 indicates that we want all contours), color, and thickness of line.
cv2.drawContours(coins, cnts, -1, (0, 255, 0), 2)
cv2.imshow('Coins', coins)
cv2.waitKey(0)