"""Attempting question 1 computer vision"""

import cv2
import numpy as np
import os

blue_color_range = [(200,0,0),(255,60,60)] # row
red_color_range = [(0,0,200),(40,40,255)]  # column, adjusted values a little
TEST_FILE_NAME = "Validation"                 # Modify file name here, switch between Validation & Test
FOLDER_NAME = "/map"                   # Modify testing folder here, switch between whatever image file you need
SAVE_NAME = "/".join(FOLDER_NAME.split('/')) + ".jpg"
SAVE_OUTPUT_FILE = "outputs"

# Loading images
def load_images_from_folder(folder):
    images = []
    image_names = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            image_names.append(filename)
    return images, image_names

def get_jigsaw_puzzle(images, images_name):
    jigsaw = {}
    for i in range(len(images)):
        position = []
        for lower,upper in [blue_color_range,red_color_range]:
            output = images[i].copy()
            mask = cv2.inRange(output,lower,upper) 
            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            index = len(cnts)
            position.append(index)
            jigsaw[images_name[i]] = position      
    return jigsaw

def concat_tile(im_list_2d):
    tiled = cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])
    cv2.imshow('output',tiled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(SAVE_OUTPUT_FILE + SAVE_NAME, tiled)
    return tiled

def solve_jigsaw(jigsaw):
    sorted_jigsaw = {k: v for k, v in sorted(jigsaw.items(), key=lambda item: item[1])}
    square = max(sorted_jigsaw.values(),key=lambda sub: sub[1])[1]
    row_tile = []
    result = []
    count = 1
    for file_name, position in sorted_jigsaw.items():
        img = cv2.imread(os.path.join(folder,file_name))
        row_tile.append(img)
        if count == square:
            result.append(row_tile)
            row_tile = []
            count = 1
        else:
            count += 1
    return concat_tile(result)


folder = TEST_FILE_NAME + FOLDER_NAME
images,images_name = load_images_from_folder(folder)
jigsaw = get_jigsaw_puzzle(images,images_name)
result = solve_jigsaw(jigsaw)