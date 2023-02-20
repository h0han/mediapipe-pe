import cv2
import mediapipe as mp
import time
import json

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture('src/OMG_sml.mp4')
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)

    pose_landmarks_list = []  # Initialize the list for the current frame

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)

            pose_landmarks_list.append({
                "id": id,
                "x": lm.x,
                "y": lm.y,
                "z": lm.z,
                "visibility": lm.visibility
            })

    with open(f"./omg_pose_landmarks/pose_landmarks_{cap.get(cv2.CAP_PROP_POS_FRAMES)}.json", "w") as f:
        json.dump(pose_landmarks_list, f)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3) 

    cv2.imshow('Image', img)
    cv2.waitKey(1)

def main():
    


if __name__ == '__main__':
    main()
