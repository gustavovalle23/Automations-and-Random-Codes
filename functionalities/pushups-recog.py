import cv2
import mediapipe as md

md_drawing = md.solutions.drawing_utils
md_pose = md.solutions.pose

count = 0
position = None

cap = cv2.VideoCapture(0)

with md_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Empty Camera")
          break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Remove cv2.flip() here
        result = pose.process(image)

        inList = [] 
        if result.pose_landmarks:
            md_drawing.draw_landmarks(image, result.pose_landmarks, md_pose.POSE_CONNECTIONS)

            for id, im in enumerate(result.pose_landmarks.landmark):
              h, w, _ = image.shape 
              X, Y = int(im.x * w), int(im.y * h) 
              inList.append([id, X, Y])

        if len(inList) != 0: 
            if ((inList[12][2] - inList[14][2])>=15 and (inList[11][2] - inList[13][2])>=15):
                position = "down"
            if ((inList[12][2] - inList[14][2])<=5 and (inList[11][2] - inList[13][2])<=5) and position == "down":
                position = "up"
                count += 1

        # Display push-up count on the frame
        cv2.putText(image, f'Push-ups: {count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Pushup Counter", image)  # Remove cv2.flip() here
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
