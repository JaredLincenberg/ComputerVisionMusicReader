import cv2
import numpy as np
import os 
import glob
from pdf2image import convert_from_path

def main():
     
    images = readInFiles("toccatina-let.pdf")
    for imageName in images:
        cv2.cvtColor(images[imageName], cv2.COLOR_BGR2GRAY)

    # Apply Methods
def readInFiles(pdfFileName):
    # https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
    pages = convert_from_path(pdfFileName, 500)
    images = {}
    for page, i  in zip(pages, range(len(pages))):
        filename = "toccatina-let_"+str(i)+".jpg"
      
        # Save the image of the page in system 
        page.save(filename, 'JPEG') 

        # Read in image
        pageImg = cv2.imread("toccatina-let_"+str(i)+".jpg")

        # Save Filename and image to Dictionary
        images["toccatina-let_"+str(i)+".jpg"] = pageImg

        # Make large images viewable
        create_named_window("toccatina-let_"+str(i)+".jpg", pageImg)
        cv2.imshow("toccatina-let_"+str(i)+".jpg", pageImg)
    cv2.waitKey(0)
    return images

def convertGrayScale():
    return cv2.cvtColor(imageCCC,cv2.COLOR_BGR2GRAY)


# Taken from Slides
def create_named_window(window_name, image):
    # WINDOW_NORMAL allows resize; use WINDOW_AUTOSIZE for no resize.
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    h = image.shape[0]  # image height
    w = image.shape[1]  # image width    \
    # Shrink the window if it is too big (exceeds some maximum size).
    WIN_MAX_SIZE = 1000
    if max(w, h) > WIN_MAX_SIZE:        
        scale = WIN_MAX_SIZE / max(w, h)
    else:        
        scale = 1
    cv2.resizeWindow(winname=window_name, width=int(w * scale), height=int(h * scale))
if __name__ == "__main__":
    main()