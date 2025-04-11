import os
import base64
from io import BytesIO
from flask import Flask, request, jsonify, render_template
from PIL import Image
from database import get_connection  # Assuming same DB function

app = Flask(__name__)

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html", name="Flask User")


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    # Extract image data and decode
    image_data = base64.b64decode(data["image"].split(",")[1])
    image = Image.open(BytesIO(image_data))

    filename = f"{data['username']}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)
    image.save(file_path)

    # Insert into MySQL database
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO user (firstName, lastName, email, username, img) VALUES (%s, %s, %s, %s, %s)"
    values = (data["firstName"], data["lastName"], data["email"], data["username"], file_path)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Signup successful!"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # You can implement face match logic here
    return jsonify({"message": "Login route hit!"})


if __name__ == "__main__":
    app.run(debug=True)
