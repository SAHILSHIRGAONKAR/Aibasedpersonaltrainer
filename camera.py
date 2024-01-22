import cv2
#video feed
#capture frames from the [default camera (index 0)] and convert them into JPEG format.
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)


#capture a frame from the camera and return it as a JPEG-encoded byte string
    def get_frame(self):
        while self.video.isOpened():
            ret, img = self.video.read()
            cv2.imshow("Image", img)
            ret, jpeg = cv2.imencode('.jpg', img) #convert the frame to JPEG format and store it in the variable jpeg
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            return jpeg.tobytes()  #returns the JPEG-encoded frame as bytes


#         self.video.release()
#         cv2.destroyAllWindows()
# vc = VideoCamera()
# vc.get_frame()