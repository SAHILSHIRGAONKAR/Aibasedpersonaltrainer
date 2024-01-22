from flask import Flask, render_template
from flask_socketio import SocketIO
from ExerciseCheckerModule import FormChecker  # Import your FormChecker class
import cv2
import base64

app = Flask(__name__)
socketio = SocketIO(app)

# Create an instance of the FormChecker class
form_checker = FormChecker()

# Function to generate video frames
def generate():
    cap = cv2.VideoCapture(0)  # Use the appropriate camera index

    while True:
        success, frame = cap.read()
        if not success:
            continue

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Convert the frame to a base64 string
        frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')

        # Send the frame to the HTML page
        socketio.emit('video_frame', {'frame': frame_base64})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Start the video feed when a client connects
    socketio.start_background_task(generate)

@app.route('/execute_bicep_curls')
def execute_bicep_curls():
    form_checker.Start_biceps_tracker()
    return 'Bicep curls started'

if __name__ == '__main__':
    socketio.run(app, debug=True)
