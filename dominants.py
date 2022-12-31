import numpy as np
import cv2
import os
import math


def get_dominant_colors(img):

    reshaped = img.reshape((-1, 3))
    # convert to np.float32
    reshaped = np.float32(reshaped)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 3
    _, _, center = cv2.kmeans(reshaped, K, None, criteria, 10,
                              cv2.KMEANS_PP_CENTERS)
    # Now convert back into uint8
    dominants = np.uint8(center)

    return dominants

def bgr_to_hex(dominants):

    color_1, color_2, color_3 = dominants[0], dominants[1], dominants[2]
    c1 = "#{:02x}{:02x}{:02x}".format(color_1[2], color_1[1], color_1[0])
    c2 = "#{:02x}{:02x}{:02x}".format(color_2[2], color_2[1], color_2[0])
    c3 = "#{:02x}{:02x}{:02x}".format(color_3[2], color_3[1], color_3[0])
    hex = f"{c1} \n{c2} \n{c3} \n"
    
    return hex

def paint_colors(dominants, area=50):

    color_1, color_2, color_3 = dominants[0], dominants[1], dominants[2]

    img_w = 3 * area
    img_h = 1 * area

    # Create image
    out_img = np.zeros((img_h, img_w, 3), np.uint8)
    out_img[:, 0:area] = color_1     #(y,x)
    out_img[:, area:area*2] = color_2
    out_img[:, area*2:area*3] = color_3
    return out_img


def process_single_img(path, file):
    try:
        img = cv2.imread(r'{}/{}'.format(path, file))
    except:
        raise ValueError("Please make sure you use a correct path and image file.")
    dominants = get_dominant_colors(img)
    hex = bgr_to_hex(dominants)
    colors_img = paint_colors(dominants, area=50)
    cv2.imwrite(r'{}/dominant colors.jpg'.format(path), colors_img)

    return img, hex


def process_multiple_imgs(path):

    try:
        files = os.listdir(path)
    except:
        raise ValueError("Please use a correct path.")

    hexs = ""
    # img_rows = math.ceil(len(files)/3)
    for i, file in enumerate(files):
        try:
            img = cv2.imread(r'{}/{}'.format(path, file))
        except:
            raise ValueError("Please make sure you use image files.")

        dominants = get_dominant_colors(img)
        hex = bgr_to_hex(dominants)
        hexs += hex
        colors_img = paint_colors(dominants, area=50)

        if i == 0:
            org_img = colors_img
        else:
            org_img = np.concatenate((org_img, colors_img), axis = 0)

    cv2.imwrite(r'{}/dominant colors.jpg'.format(path), org_img)

    return img, hexs
