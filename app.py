from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


@app.route("/")
def index():
    return """
Servidor HTTP funcionando.<br><br>

DL:
https://drivetest-upload.onrender.com/test15mb.bin

<br><br>

UL:
https://drivetest-upload.onrender.com/upload
"""


@app.route("/upload", methods=["POST"])
def upload():

    print("=" * 60)
    print("NUEVA PETICION")
    print("=" * 60)

    print("Headers:")
    for h in request.headers:
        print(h)

    print()

    print("Content-Length:", request.content_length)
    print("Content-Type:", request.content_type)

    print()

    print("FILES:")
    print(request.files)

    print()

    print("FORM:")
    print(request.form)

    print()

    if request.files:

        for key in request.files:

            f = request.files[key]

            print("Campo:", key)
            print("Nombre:", f.filename)
            print("Tipo:", f.content_type)

            filename = secure_filename(f.filename)

            f.save(os.path.join(UPLOAD_FOLDER, filename))

            print("Guardado:", filename)

        return "UPLOAD OK", 200

    data = request.get_data()

    print("RAW DATA SIZE:", len(data))

    with open("uploads/raw_upload.bin", "wb") as f:
        f.write(data)

    print("RAW DATA GUARDADA")

    return "RAW OK", 200


@app.errorhandler(413)
def too_large(e):

    print("ERROR 413")
    print("Content-Length:", request.content_length)

    return "Archivo demasiado grande", 413


if __name__ == "__main__":
    app.run()
