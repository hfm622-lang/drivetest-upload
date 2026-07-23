from flask import Flask, request
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Permitir hasta 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


@app.route("/")
def index():
    return """
Servidor HTTP funcionando.<br><br>

<h3>Download</h3>
https://drivetest-upload.onrender.com/test15mb.bin

<br><br>

<h3>Upload</h3>
https://drivetest-upload.onrender.com/upload
"""


@app.route("/upload", methods=["POST"])
def upload():

    print("\n" + "=" * 70)
    print("NUEVA PETICION")
    print("=" * 70)

    print("\nHEADERS")
    for k, v in request.headers.items():
        print(f"{k}: {v}")

    print("\nContent-Length:", request.content_length)
    print("Content-Type :", request.content_type)

    print("\nFILES ------------------------------")
    print(request.files)

    if len(request.files) > 0:

        for campo in request.files:

            archivo = request.files[campo]

            print("--------------------------------")
            print("Campo      :", campo)
            print("Nombre     :", archivo.filename)
            print("Tipo       :", archivo.content_type)

            nombre = secure_filename(archivo.filename)

            if nombre == "":
                nombre = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"

            ruta = os.path.join(UPLOAD_FOLDER, nombre)

            archivo.save(ruta)

            print("Guardado en:", ruta)
            print("Tamaño:", os.path.getsize(ruta), "bytes")

    else:
        print("No hay archivos en request.files")

    print("\nFORM -------------------------------")
    print(request.form)

    print("\nVALUES -----------------------------")
    print(request.values)

    print("\nRAW DATA ---------------------------")

    raw = request.get_data(cache=True)

    print("Bytes RAW:", len(raw))

    if len(raw) > 0:

        nombre = f"raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"

        ruta = os.path.join(UPLOAD_FOLDER, nombre)

        with open(ruta, "wb") as f:
            f.write(raw)

        print("RAW guardado en:", ruta)

    else:
        print("No hay datos RAW")

    print("\nFINALIZADO")
    print("=" * 70)

    # Siempre responder OK
    return "OK", 200


@app.errorhandler(413)
def error_413(e):

    print("\n******** ERROR 413 ********")
    print("Content-Length:", request.content_length)

    return "413", 413


@app.errorhandler(Exception)
def error_general(e):

    print("\n******** ERROR GENERAL ********")
    print(type(e))
    print(e)

    return "ERROR", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
