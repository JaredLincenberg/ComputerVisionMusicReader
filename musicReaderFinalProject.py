import cv2
import numpy as np
import os 
import glob
from pdf2image import convert_from_path
import math
import matplotlib.pyplot as plt
MAX_SIZE = 2000
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        param.append((x,y))
        print(param)
def main():
    images = readInFiles("lanative-let")
    # manualSelectTemplateMatch(images)
    for imageName in images:
        a = getImageLines(images[imageName])
        getImageSum(images[imageName])
        # create_named_window("edges", a)
        # cv2.imshow("edges", a)
        # cv2.waitKey(0)
    
def getImageSum(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_img = cv2.bitwise_not(img)
    sumOfRows = np.sum(black_img, axis=1)
    x = np.arange(len(sumOfRows))
    plt.plot(sumOfRows)
    print(len(np.where(sumOfRows<1)[0])) 
    b = []
    x0 = -1
    for x in np.where(sumOfRows<2.5e4)[0]:
        if x0+1 != x:
            b.append(x0)
            x0 = x
            b.append(x)
            
        else:
            x0+=1
    print(b)
    plt.vlines(b,0,1e6,colors='r')
    plt.show()
def getImageLines(image):
    if(image.shape[0]>=MAX_SIZE or image.shape[1]>=MAX_SIZE):
        w = MAX_SIZE/image.shape[0]
        h = MAX_SIZE/image.shape[1]
        image = cv2.resize(image, dsize=None, fx = h, fy = h)
    image_width = image.shape[1]
    image_height = image.shape[0]

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge_img = cv2.Canny(image=img, 
                            apertureSize=3,  
                            threshold1=0.05, 
                            threshold2=3 * 0.05, 
                            L2gradient=True) 
    MIN_HOUGH_VOTES_FRACTION = 0.15
    MIN_LINE_LENGTH_FRACTION = 0.05
    hough_lines = cv2.HoughLines( image = edge_img, 
                                    rho = 1, 
                                    theta = math.pi/180, 
                                    threshold = int(img.shape[1] * MIN_HOUGH_VOTES_FRACTION), 
                                    )
    for i in range(min(100, len(hough_lines))):    
        rho = hough_lines[i][0][0]  # distance from (0,0)
        theta = hough_lines[i][0][1]  # angle in radians
        a = math.cos(theta)  # distance from (0,0)
        b = math.sin(theta) # angle in radians
        x0 = a * rho
        y0 = b * rho
        p1 = (int(x0 + MAX_SIZE * (-b)), int(y0 + MAX_SIZE * (a)))   
        p2 = (int(x0 - MAX_SIZE * (-b)), int(y0 - MAX_SIZE * (a)))   
        print(p1, p2)  
        cv2.line(img=image, pt1=p1, pt2=p2, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    return image
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