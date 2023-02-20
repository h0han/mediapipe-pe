import ssl
import urllib.request

# SSL 인증서 검증을 건너뛰도록 SSLContext 생성
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# URL 오픈 시 SSLContext 전달
response = urllib.request.urlopen(url, context=ssl_context)

import cv2
import mediapipe as mp
import time
import json

class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,
                                     self.detectionCon,self.trackCon)
        
    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        # print(results.pose_landmarks)

        # pose_landmarks_list = []  # Initialize the list for the current frame
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, 
                                    self.mpPose.POSE_CONNECTIONS)

        #     for id, lm in enumerate(results.pose_landmarks.landmark):
        #         h, w, c = img.shape
        #         cx, cy = int(lm.x*w), int(lm.y*h)
        #         cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)

        #         pose_landmarks_list.append({
        #             "id": id,
        #             "x": lm.x,
        #             "y": lm.y,
        #             "z": lm.z,
        #             "visibility": lm.visibility
        #         })

        # with open(f"./omg_pose_landmarks/pose_landmarks_{cap.get(cv2.CAP_PROP_POS_FRAMES)}.json", "w") as f:
        #     json.dump(pose_landmarks_list, f)

        return img
    
    def getPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)
        return lmList


def main():
    cap = cv2.VideoCapture('src/OMG_sml.mp4')
    pTime = 0
    detector = poseDetector(mode=False, upBody=False, smooth=True, 
                            detectionCon=0.5, trackCon=0.5)
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        print(lmList)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3) 

        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
