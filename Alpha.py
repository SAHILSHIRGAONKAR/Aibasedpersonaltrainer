from flask import Flask, render_template, jsonify
from ExerciseCheckerModule import FormChecker  # Replace with the actual import statement for your FormChecker class

app = Flask(__name__,static_url_path='/static')

# Create an instance of the FormChecker class
form_checker = FormChecker()

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/execute_bicep_curls', methods=['GET'])
def execute_bicep_curls():
    # Call the Start_biceps_tracker method on the form_checker instance
    form_checker.Start_biceps_tracker()

    # Return a response with a JSON message
    return jsonify({"message": "Bicep curls started"})

@app.route('/execute_squats', methods=['GET'])
def execute_squats():
    # Call the Start_squats_tracker method on the form_checker instance
    form_checker.Start_squats_tracker()

    # Return a response with a JSON message
    return jsonify({"message": "Squats started"})

if __name__ == '__main__':
    app.run(debug=True)
