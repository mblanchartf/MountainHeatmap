# -*- coding: utf-8 -*-
from math import ceil
from gps.utils import get_pixel_position
import cv2


def draw_coordinate(img, draw_coord, starting_coord, previous_coord,
                    zoom=15, px_error=30):

    x, y = get_pixel_position(draw_coord, starting_coord, zoom)

    x_1, y_1 = get_pixel_position(previous_coord, starting_coord, zoom)

    dx, dy = abs(ceil(x-x_1)), abs(ceil(y-y_1))

    if dx < px_error and dy < px_error:
        if img.item(x, y, 0) != 0 and img.item(x, y, 1) != 0:
            # First time access
            cv2.line(img, (y, x), (y_1, x_1), (0, 0, 255), 2)
        elif img.item(x, y, 2) == 5:
            # Minimum pixel value was reached
            cv2.line(img, (y, x), (y_1, x_1), (0, 0, 5), 2)
        else:
            # Decrease red pixel value
            cv2.line(img, (y, x), (y_1, x_1), (0, 0, img.item(x, y, 2)-25), 2)

    return img


def create_heatmap(img, img_0, colorMap=cv2.COLORMAP_HOT):

    r, c, ch = img.shape

    # Remove red color from all the image except the track
    for row in range(0, r):
        for col in range(0, c):
            if img.item(row, col, 0) != 0:
                img.itemset((row, col, 2), 0)

    # Get the red color
    red = img[:, :, 2]

    # Get the heatmap
    heatmap_img_red = cv2.applyColorMap(red, colorMap)

    # Obtain the mask
    masked_img = cv2.bitwise_and(heatmap_img_red, heatmap_img_red, mask=red)

    # Obtain heatmap
    result = apply_mask(img_0, masked_img)

    return result


def apply_mask(img1, img2):

    # Directly extract form OpenCV documentation: Section Application of Mask
    # Load two images

    rows, cols, channels = img2.shape
    roi = img1[0:rows, 0:cols]

    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 5, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    img1[0:rows, 0:cols] = dst

    return img1
