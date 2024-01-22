import cv2
import mediapipe as mp
import math


class poseDetector():

    def __init__(self,static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):

        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.min_detection_confidence, self.min_tracking_confidence)

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        self.results = self.pose.process(imgRGB)
        imgRGB.flags.writeable = True
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img, draw=True):
        self.lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy,])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
        return self.lmlist

    def findAngle(self, img, p1, p2, p3, draw=True):
        #get land marks
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        x3, y3 = self.lmlist[p3][1:]

        #calculate angles
        # angle_rad = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        # angle_deg = math.degrees(angle_rad)
        # angle_deg = (angle_deg + 360) % 180  # Normalize the angle to be in the range [0, 360]
        # print(angle_deg)

        # Calculate vectors from (x1, y1) to (x2, y2) and from (x2, y2) to (x3, y3)
        vector1 = [x2 - x1, y2 - y1]
        vector2 = [x2 - x3, y2 - y3]

        # Calculate the cross product of the two vectors
        cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]

        # Calculate the dot product of the two vectors
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        # Calculate the magnitude of the two vectors
        magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

        # Calculate the angle in radians
        angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))

        # Calculate the angle in degrees and ensure it is positive and in the range [0, 180] by using abs
        angle_deg = abs(math.degrees(angle_rad))

        # ensure that calculated angle is in range of [0,180] by subtracting from 360
                                                    # if the calculated angle is between [180,360]
        # if angle_deg > 180.0:
        #     angle_deg = 360.0 - angle_deg

        if draw:
            cv2.line(img, (x1, y1),(x2, y2),(0,255,0), 3)
            cv2.line(img, (x3, y3), (x2, y2), (0,255,0), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle_deg)), (x2 - 50, y2 + 60),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2, cv2.LINE_AA)
        #
        return angle_deg

def main():
    # giving video as input
    # for live camera set cv2.VideoCapture(0)

    cap = cv2.VideoCapture(0)

    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        #to mark perticular point set draw = false &
        #cv2.circle(img, (lmlist[14][1], lmlist[14][2]), 15, (0, 0, 255), cv2.FILLED)
        lmlist = detector.getPosition(img)
        if len(lmlist) != 0:
            # left arm
            detector.findAngle(img, 11, 13, 15)
            # right arm
            detector.findAngle(img, 12, 14, 16)
        print(lmlist)

        img = cv2.flip(img, 1)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): #use 27 in place of q to qive esc as close/stop button
                                              # or -1 to stop when window is closed
            break


if __name__ == "__main__":
    main()
