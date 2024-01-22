import cv2
import posemodule as pm  # Import your pose detection module

def main():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    while True:
        success, img = cap.read()
        # img = cv2.imread("TestVideosAndImages/img5.jpeg")
        img = detector.findPose(img)
        img = cv2.resize(img, (640, 480))
        lmlist = detector.getPosition(img)

        if len(lmlist) != 0:
            co_ord1 = lmlist[24][1], lmlist[24][2]  # Shoulder coordinates
            co_ord2 = lmlist[26][1], lmlist[26][2]  # Elbow coordinates
            co_ord3 = lmlist[28][1], lmlist[28][2]  # Wrist coordinates

            print("co1:", co_ord1)
            print("co2:", co_ord2)
            print("co3:", co_ord3)

            img = cv2.circle(img, co_ord1, 15, (0, 0, 255), cv2.FILLED)
            img = cv2.circle(img, co_ord2, 15, (0, 255, 0), cv2.FILLED)
            img = cv2.circle(img, co_ord3, 15, (255, 0, 0), cv2.FILLED)

        img = cv2.flip(img, 1)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
