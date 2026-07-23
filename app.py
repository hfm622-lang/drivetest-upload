from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Permitir hasta 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


@app.route("/")
def index():
    return """
<h2>Servidor HTTP funcionando.</h2>

<h3>Download</h3>
https://drivetest-upload.onrender.com/test15mb.bin

<h3>Upload</h3>
https://drivetest-upload.onrender.com/upload
"""


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "GET":
        return "Use POST para realizar el upload.", 405

    print("=" * 70)
    print("NUEVA PETICION")
    print("=" * 70)

    print("\nHEADERS")
    print("-" * 70)

    for k, v in request.headers.items():
        print(f"{k}: {v}")

    print("\nCONTENT LENGTH")
    print("-" * 70)
    print(request.content_length)

    print("\nCONTENT TYPE")
    print("-" * 70)
    print(request.content_type)

    print("\nLEYENDO CUERPO DE LA PETICION...")

    try:
        data = request.get_data(cache=False)

        print("Bytes recibidos:", len(data))

        filename = os.path.join(UPLOAD_FOLDER, "raw_upload.bin")

        with open(filename, "wb") as f:
            f.write(data)

        print("Archivo guardado:", filename)

        return "UPLOAD OK", 200

    except Exception as ex:

        print("EXCEPCION:")
        print(type(ex))
        print(ex)

        return "ERROR", 500


@app.errorhandler(413)
def too_large(e):

    print("\n" + "*" * 70)
    print("ERROR 413")
    print("*" * 70)

    print("Content-Length:", request.content_length)
    print("Exception:", e)

    return "413 Request Entity Too Large", 413


@app.errorhandler(Exception)
def handle_exception(e):

    print("\n" + "*" * 70)
    print("ERROR GENERAL")
    print("*" * 70)

    print(type(e))
    print(e)

    return "ERROR", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
