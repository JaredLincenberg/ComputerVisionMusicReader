import random
import numpy as np
import math
import cv2
import os
import sys
from PIL import Image


def random_color():
    levels = range(32,256,32)
    return tuple(random.choice(levels) for _ in range(3))

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def main():
    images = np.array(load_images_from_folder(os.getcwd()))

    img= cv2.imread("Sheet.JPG")  #read image

    height=img.shape[0]  #calculate image size
    width=img.shape[1]
    count = 0  # initialize a count
    notes=[]

    for i in range(0, len(images)):
        template=images[i] #pre loaded image of 'a'

        threshold=0.90   #variable threshold to get the best matches in the text
        correlation=cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED) #calculate correlation scores
        cv2.imshow('correlation', correlation) #show correlation score image
        matches = np.where(correlation >= threshold)  #show the location of 'a' matches


        past_locations=np.array([[0, 0]])  #initialize an array of previous a locations

        color = random_color()

        for (x,y) in zip(matches[1], matches[0]):   #go through each point in the locations of a
            cv2.rectangle(img, (x, y), (x + 30, y + 80), color, 2)  #draw a rectangle about the point
            # print(x, y)  #show the point
            count = count + 1 #add to the count





    # print(count) #show count

    cv2.imshow("final", img) #show edited image

    cv2.imwrite("results/result.jpg", img)

    cv2.waitKey(0)



if __name__ == '__main__':
    main()
