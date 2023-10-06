import cv2
import mediapipe as mp
import time
import random

# class creationopen
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # it gives small dots onhands total 20 landmark points

    def findHands(self,img,draw=True):
        # Send rgb image to hands
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) # process the frame
    #     print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    #Draw dots and connect them
                    self.mpDraw.draw_landmarks(img,handLms,
                                                self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self,img, handNo=0, draw=True):
        """Lists the position/type of landmarks
        we give in the list and in the list ww have stored
        type and position of the landmarks.
        List has all the lm position"""

        lmlist = []

        # check wether any landmark was detected
        if self.results.multi_hand_landmarks:
            #Which hand are we talking about
            myHand = self.results.multi_hand_landmarks[handNo]
            # Get id number and landmark information
            for id, lm in enumerate(myHand.landmark):
                # id will give id of landmark in exact index number
                # height width and channel
                h,w,c = img.shape
                #find the position
                cx,cy = int(lm.x*w), int(lm.y*h) #center
                # print(id,cx,cy)
                lmlist.append([id,cx,cy])

                # Draw circle for 0th landmark
                if draw:
                    cv2.circle(img,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return lmlist

class Shape():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
    
def rescaler(height, width, frame):
    dimensions = (width, height)
    frame = cv2.resize(frame, dimensions, interpolation= cv2.INTER_AREA)

def enemy_creation(img, enemy_color):
    x_coord = random.randint(0, img.shape[1])
    y_coord = 0

    x2_coord = x_coord+100
    y2_coord = y_coord+80

    cv2.rectangle(img, (x_coord, y_coord),(x2_coord, y2_coord) , enemy_color, cv2.FILLED)

def enemy_spawn(frame, color):
    for i in range(0,10):
        enemy_creation(frame, color)
        time.sleep(5)

    
def main():  

    colorR = (0, 0, 255) #blue
    enemy_color = (255, 0, 0) #red

    cap = cv2.VideoCapture(1)
    detector = handDetector()

    cap.set(3, 1280)
    cap.set(4, 1280)

    cx, cy, w, h = 100,100,200,200

    while True:
        success,img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            cursor = lmList[8]
            if cx-w//2<cursor[1] < cx+w//2 and cy-h//2<cursor[2]< cy+h//2:
                colorR = (0 ,255, 0)  #green
                cx, cy = cursor[1], cursor[2]
            else:
                colorR = (255, 0, 255)  #purple

        #user rectangle
        #start point = 0,0 and end point is 200,200
        cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED)



        #enemy_spawn(img, enemy_color)
     

        #Final Display
        cv2.imshow("Video",img)
        key = cv2.waitKey(20)
        if(key==ord("x")):
            break


    

if __name__ == "__main__":
    main()