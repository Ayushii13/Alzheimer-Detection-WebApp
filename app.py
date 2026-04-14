import os
import gdown
MODEL_PATH ="alzheimer_model.h5"
if not os.path.exists(MODEL_PATH):
    url="https://drive.google.com/file/d/1NmA7FzZo4gYitY7td9KK5GXxC1AYcglN"
    gdown.download(url, MODEL_PATH, quite=False)
from flask import Flask, render_template, request
import os
from predict import get_prediction

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded"

    file = request.files["file"]
    filepath = os.path.join("static", file.filename)
    file.save(filepath)

    prediction = get_prediction(filepath)

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
import os
from predict import get_prediction # This links to your predict.py file

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was actually uploaded
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', message='No selected file')

        if file:
            # Save the file to C:\AlzheimerProject\static\uploads
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Get the result from our AI model
            label, confidence = get_prediction(filepath)

            # Send the result back to the website
            return render_template('index.html', 
                                 prediction=label, 
                                 confidence=round(confidence, 2), 
                                 image_path=filepath)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
