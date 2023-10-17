import cv2 
from cvzone.HandTrackingModule import HandDetector  #to detect hands
cap=cv2.VideoCapture(0)  #capture the video image
cap.set(10,245) #height
cap.set(12,245)  #width
detector = HandDetector(maxHands=2)  #to detect hands
myequation = ''
delayCounter = 0

#class
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    #user_define function: draw
    def draw(self,img):
        cv2.rectangle(img, self.pos,
                      (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225 , 225), cv2.FILLED)
        cv2.rectangle(img, self.pos,
                     (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value,(self.pos[0] + 40, self.pos[1] + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width,
                                          self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width,
                                          self.pos[1] + self.height),
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 5)
            return True
        else:
            return False
#drawing button
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 100
        ypos = y * 100 + 100
        buttonList.append(Button((xpos,ypos),100,100,buttonListValues[y][x]))
#loop
while (True):
    success, img = cap.read()  #reading video content
    img = cv2.flip(img,1)  #flip function is used to flip hand position
    hands, img = detector.findHands(img,flipType=False)
    cv2.rectangle(img, (100, 40), (100+400, 40+100), (225,225,0), cv2.FILLED)
    cv2.rectangle(img, (100, 40), (100+400, 40+100), (50, 50, 50), 3)
    #draw a button
    for button in buttonList:
        button.draw(img)
    if hands:
        lmList = hands[0]["lmList"]  #list of 21 Landmark points
        #print(lmList)
        length, info, img = detector.findDistance(lmList[8][0:2], lmList[12][0:2],img)
        print(length)
        x,y = lmList[8][0:2]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkClick(x,y) and delayCounter==0:
                    myvalue = buttonListValues[int(i % 4)][int(i / 4)]
                    #myequation += myvalue
                    if myvalue == '=':
                        myequation = str(eval(myequation))
                    else:
                        myequation += myvalue
                    delayCounter = 1
        #avoid duplicate
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    cv2.putText(img,myequation,(110,90), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("Image",img)  #image show on video
    key = cv2.waitKey(1)  #set waiting time for video
    if key != ord('q'):   #if q is pressed the window/video is closed
        continue
    break
#After the loop release the cap object
cap.release()
#Destroy all the windows
cv2.destroyAllWindows()