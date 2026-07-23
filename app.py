from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Drive Test Upload Server OK"

@app.route("/upload", methods=["POST"])
def upload():

    filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    if request.files:
        file = list(request.files.values())[0]

        name = filename + "_" + file.filename

        path = os.path.join(UPLOAD_FOLDER, name)

        file.save(path)

        return jsonify({
            "status":"OK",
            "filename":name,
            "size":os.path.getsize(path)
        })

    data = request.get_data()

    name = filename + ".bin"

    path = os.path.join(UPLOAD_FOLDER,name)

    with open(path,"wb") as f:
        f.write(data)

    return jsonify({
        "status":"OK",
        "filename":name,
        "size":len(data)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)