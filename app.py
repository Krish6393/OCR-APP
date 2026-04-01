from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/")
def home():
    return "OCR is running"

@app.route("/extract", methods=["POST"])
def extract():
    file = request.files["image"]
    img = Image.open(file.stream)
    text = pytesseract.image_to_string(img)
    return jsonify({"text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
