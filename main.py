import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

myColors=[[135,36,82,171,210,176],[77,78,118,88,204,206]]   # HSV codes
myColorValues=[[102,0,102],[255,255,153]]    # BGR codes
myPoints=[]   #[x,y,colorId,thickness]
brushThickness = 10  # Default brush thickness

def findColor(img,myColors, myColorValues,brushThickness):   # identifies specific colors in img and returns a list called newPoints
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0    # for detecting color
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED) # for visualizing detected points
        if x!=0 and y!=0:
            newPoints.append([x,y,count,brushThickness])
        count+=1
        #cv2.imshow(str(color[0]), mask)
    return newPoints
def getContours(img):    # finds contours of mask and returns a center point to detected color region
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)    # less corners at contour
            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),point[3],myColorValues[point[2]],cv2.FILLED)

def clearCanvas(imgResult):
    imgResult[:] = 0


while True:

    success, img = cap.read()
    imgResult = img.copy()   # we make our changes at not exact img, we make changes at copy of it
    newPoints = findColor(img, myColors, myColorValues, brushThickness)
    if len(newPoints) !=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorValues)

    imgResult = cv2.flip(imgResult, 1)

    cv2.imshow('Result', imgResult)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        myPoints = []  # Tüm noktaları temizle
        clearCanvas(imgResult)
    elif key == ord('8') and brushThickness < 15:
        brushThickness+=1
    elif key == ord('2') and brushThickness > 5 :
        brushThickness-=1

cap.release()
cv2.destroyAllWindows()