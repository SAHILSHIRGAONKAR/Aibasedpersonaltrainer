from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie
import sys
import cv2
import posemodule as pm
from audiocom import text_to_speech
import threading
import concurrent.futures

# Define the FormChecker class
class FormChecker:
    def __init__(self):
        self.detector = pm.poseDetector()
        self.audio_finished_event = threading.Event()
        self.gif_window = None
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)  # Create a thread pool with 1 worker

    def draw_rep_counter(self, img, count):
        # Define the position and size of the square
        square_position = (20, 20)  # Adjust the position as needed
        square_size = (100, 60)  # Adjust the size as needed
        square_color = (0, 255, 0)  # Green color for the square
        rep_color = (0, 0, 255)  # Red color for the rep count text

        # Draw the green square
        cv2.rectangle(img, square_position, (square_position[0] + square_size[0], square_position[1] + square_size[1]),
                      square_color, cv2.FILLED)

        # Display the rep count in the green square
        cv2.putText(
            img,
            f"Reps: {count}",
            (square_position[0] + 10, square_position[1] + 40),  # Adjust text position within the square
            cv2.FONT_HERSHEY_SIMPLEX,
            1,  # Font scale
            rep_color,  # Text color (red)
            2,  # Thickness
            cv2.LINE_AA,  # Line type
        )

    def convert_text_to_speech(self, text):
        text_to_speech(text)
        # self.audio_finished_event.set()  # Signal that audio has finished

    def bicep_curls(self):
        gif_path = "static/TestVideosAndImages/bicep-curls.gif"  # Specify the GIF path here

        instructions_text = "Grab the pair of dumbbells with your palms facing forward. " \
                            "Stand 5 to 7 steps away from the camera. Your feet should be roughly hip-width apart. " \
                            "Keeping your back straight, contract your biceps to curl the dumbbells upwards. " \
                            "Squeeze your biceps hard at the top and pause for a moment. " \
                            "Slowly lower the dumbbells all the way to the starting position. " \
                            "Repeat for the desired number of reps."

        # Convert text to speech for bicep curls instructions in a separate thread
        audio_thread = threading.Thread(target=self.convert_text_to_speech, args=(instructions_text,))
        audio_thread.start()
        # Stop the audio thread
        audio_thread.join()

        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(gif_path)
        ui.setupUi(window)
        window.show()
        self.gif_window = window  # Store the reference to the GIF window



        sys.exit(app.exec_())



    def track_bicep_curls(self):
        # list_threads = []
        cap = cv2.VideoCapture(0)  # 0 is for the default camera
        count = 0
        direction = 0

        while True:
            success, img = cap.read()
            img = cv2.resize(img, (640, 480))
            img = cv2.flip(img, 1)
            img = self.detector.findPose(img, False)
            lmlist = self.detector.getPosition(img, False)

            if len(lmlist) != 0:
                angle1 = self.detector.findAngle(img, 23, 11, 13)
                angle2 = self.detector.findAngle(img, 11, 13, 15)

                # check the curls
                if 15 < angle1 < 24:
                    if angle2 > 100:
                        direction = "down"
                    if angle2 < 41 and direction == 'down' and lmlist[15][1] > lmlist[23][1] and lmlist[15][1] - lmlist[11][1] < 20:
                        direction = "up"
                        count += 1
                        print(count, direction)

                        if int(count) != 0:
                            # print("here")
                            speaker_thread = threading.Thread(
                                target=text_to_speech, args=(str(int(count)),), kwargs={}
                            )
                            # list_threads.append(speaker_thread)
                            self.executor.submit(speaker_thread.start)

            self.draw_rep_counter(img, count)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or 'Esc' key
                break

        cap.release()
        cv2.destroyAllWindows()
        QtCore.QCoreApplication.quit()  # Close all windows

    def squats(self):
        gif_path = "static/TestVideosAndImages/squats.gif"  # Specify the GIF path here

        instructions_text = "Stand with your feet shoulder-width apart. " \
                            "Lower your body by bending your hips and knees until your thighs are parallel to the ground. " \
                            "Make sure that your knees are above or inside your toes "\
                            "Keep your back straight and chest up. " \
                            "Return to the starting position by straightening your hips and knees. " \
                            "Repeat for the desired number of reps."

        # Convert text to speech for bicep curls instructions in a separate thread
        audio_thread = threading.Thread(target=self.convert_text_to_speech, args=(instructions_text,))
        audio_thread.start()
        audio_thread.join()

        app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(gif_path)
        ui.setupUi(window)
        window.show()
        self.gif_window = window  # Store the reference to the GIF window

        sys.exit(app.exec_())

        # Stop the audio thread
        # audio_thread.join()

    def track_squats(self):
        cap = cv2.VideoCapture(0)  # 0 is for the default camera
        count = 0
        direction = 0

        while True:
            success, img = cap.read()
            img = cv2.resize(img, (640, 480))
            img = cv2.flip(img, 1)
            img = self.detector.findPose(img, False)
            lmlist = self.detector.getPosition(img, False)

            if len(lmlist) != 0:
                if len(lmlist) != 0:
                    angle1 = self.detector.findAngle(img, 24, 26, 28)
                    angle2 = self.detector.findAngle(img, 23, 25, 27)

                if angle1 > 90:
                    direction = "up"
                if angle1 < 90 and lmlist[26][1] > lmlist[32][1] and direction == 'up':
                    direction = "down"
                    count += 1
                    print(count, direction)

                    if int(count) != 0:
                        speaker_thread = threading.Thread(
                            target=text_to_speech, args=(str(int(count)),), kwargs={}
                        )
                        self.executor.submit(speaker_thread.start)

            self.draw_rep_counter(img, count)

            cv2.imshow("Image", img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or 'Esc' key
                break

        cap.release()
        cv2.destroyAllWindows()
        QtCore.QCoreApplication.quit()  # Close all windows

    def Start_biceps_tracker(self):
        tracking_thread = threading.Thread(target= self.track_bicep_curls)
        tracking_thread.start()
        # tracking_thread.join()
        # Start bicep curls function
        self.bicep_curls()

    def Start_squats_tracker(self):
        tracking_thread = threading.Thread(target=self.track_squats)
        tracking_thread.start()
        # tracking_thread.join()
        # Start bicep curls function
        self.squats()

    # import argparse

    # def main(self):
    #     parser = argparse.ArgumentParser(description='Fitness Tracker')
    #     parser.add_argument('--function', type=str, required=True, help='Function to run (e.g., bicep_curls, squats)')
    #     args = parser.parse_args()
    #
    #     form_checker = FormChecker()
    #
    #     if args.function == 'Start_biceps_tracker':
    #         form_checker.Start_biceps_tracker()
    #     elif args.function == 'Start_biceps_tracker':
    #         form_checker.Start_squats_tracker()
    #     else:
    #         print("Invalid function specified. Use --function bicep_curls or --function squats.")

class Ui_MainWindow(object):
    def __init__(self, gif_path):
        self.gif_path = gif_path

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(710, 710)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 700, 700))
        self.label.setMinimumSize(QtCore.QSize(680, 680))
        self.label.setMaximumSize(QtCore.QSize(700, 700))
        self.label.setObjectName("label")

        # add label to the main window
        MainWindow.setCentralWidget(self.centralwidget)

        # set qmovie as label
        self.movie = QMovie(self.gif_path)
        self.label.setMovie(self.movie)
        self.movie.start()

if __name__ == "__main__":
    # Create a FormChecker instance and check bicep curls form
    form_checker = FormChecker()

    # Start a separate thread for tracking
    # tracking_thread = threading.Thread(target=form_checker.track_bicep_curls)
    # tracking_thread.start()
    # # tracking_thread.join()
    # # Start bicep curls function
    # form_checker.bicep_curls()
    form_checker.Start_biceps_tracker()

    QtCore.QCoreApplication.exec_()
