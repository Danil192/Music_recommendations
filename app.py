from flask import Flask, render_template, request, jsonify
import subprocess
import traceback
import os

app = Flask(__name__)

CLIPS_PATH = r"C:\Program Files\CLIPS 6.4\CLIPSDOS.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_clips():
    try:
        data = request.json

        clips_code = f"""
(load "{os.path.join(BASE_DIR, 'music_recs.clp')}")
(reset)
(assert (user_activity (value {data["activity"]})))
(assert (user_popularity (value {data["popularity"]})))
(assert (user_mood (value {data["mood"]})))
(assert (user_language (value {data["language"]})))
(assert (state ready))
(run)
"""

        result = subprocess.run(
            [CLIPS_PATH],
            input=clips_code,
            text=True,
            capture_output=True
        )

        if result.stderr.strip():
            return jsonify({
                "output": "ОШИБКА",
                "error": result.stderr,
                "code": result.stdout
            })

        return jsonify({"output": result.stdout})

    except Exception as e:
        return jsonify({
            "output": "ОШИБКА PYTHON",
            "error": str(e),
            "trace": traceback.format_exc()
        })

if __name__ == "__main__":
    app.run(debug=True)
