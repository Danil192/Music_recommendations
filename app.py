from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

CLIPS_PATH = "C:\\Program Files\\SSS\\CLIPS 6.4.2\\CLIPSDOS.exe"
CLP_FILE = "music_recs.clp"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_clips():
    data = request.json

    with tempfile.NamedTemporaryFile(delete=False, suffix=".clp", mode="w", encoding="utf8") as temp:
        temp_path = temp.name

        temp.write('(assert (mode web))\n')
        temp.write(f'(load "{CLP_FILE}")\n')

        temp.write(f'(assert (user_activity (value {data["activity"]})))\n')
        temp.write(f'(assert (user_popularity (value {data["popularity"]})))\n')
        temp.write(f'(assert (user_mood (value {data["mood"]})))\n')
        temp.write(f'(assert (user_language (value {data["language"]})))\n')

        temp.write('(assert (state ready))\n')
        temp.write('(reset)\n')
        temp.write('(run)\n')

    result = subprocess.run(
        [CLIPS_PATH, temp_path],
        capture_output=True,
        text=True
    )

    os.remove(temp_path)

    return jsonify({"output": result.stdout})

if __name__ == "__main__":
    app.run(debug=True)
