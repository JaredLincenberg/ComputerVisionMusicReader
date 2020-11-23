import cv2
import numpy as np
import os 
import glob
from pdf2image import convert_from_path

def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        param.append((x,y))
        print(param)
def main():
    images = readInFiles("lanative-let")
    manualSelectTemplateMatch(images)
    
    # Apply Methods
def manualSelectTemplateMatch(images):
    for imageName in images:
        current_image = images[imageName]
        cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)
        
        ret, current_image = cv2.threshold(current_image,150,255,cv2.THRESH_BINARY)
        cv2.imshow(imageName, current_image)
        x=[]
        # imageCopy = current_image.copy()
        cv2.setMouseCallback(imageName, get_xy, param =x)
        while(len(x)<2):
            if cv2.waitKey(20) & 0xFF == 27:
                break
            if(len(x)==1):
                pass
                # cv2.circle(current_image, x[0], 4, (0,0,255), thickness=-1, lineType=8, shift=0)
                # cv2.imshow(imageName+str(1), current_image)
        print("left Loop")
        sub = current_image[x[0][1]:x[1][1], x[0][0]:x[1][0]]
        cv2.imshow("img", sub)
        C = cv2.matchTemplate(current_image, sub, cv2.TM_CCOEFF_NORMED)
        loc = np.where( C >= 0.95)

        # Loop through locations place a rectangle and count the number of 'a's
        letterACount=0
        subWidth = sub.shape[1]
        subHeight= sub.shape[0]
        print(sub.shape)
        for pt in zip(*loc[::-1]):
            letterACount +=1
            cv2.rectangle(current_image,pt,(pt[0]+subWidth, pt[1]+subHeight),(0,0,255), thickness=8, lineType=8, shift=0)
        print(letterACount)
        cv2.imshow(imageName, current_image)
        cv2.waitKey(0)
        break
    cv2.waitKey(0)
def readInFiles(pdfFileName):
    # https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/
    pages = convert_from_path(pdfFileName+".pdf", 500)
    images = {}
    for page, i  in zip(pages, range(len(pages))):
        filename = pdfFileName+'_'+str(i)+".jpg"
      
        # Save the image of the page in system 
        page.save(filename, 'JPEG') 

        # Read in image
        pageImg = cv2.imread(pdfFileName+'_'+str(i)+".jpg")

        # Save Filename and image to Dictionary
        images[pdfFileName+'_'+str(i)+".jpg"] = pageImg

        # Make large images viewable
        create_named_window(pdfFileName+'_'+str(i)+".jpg", pageImg)
        # cv2.imshow(pdfFileName+'_'+str(i)+".jpg", pageImg)
    # cv2.waitKey(0)
    return images




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