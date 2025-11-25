from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import traceback

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
        print("=== ПОЛУЧЕНЫ ДАННЫЕ ===", data)

        # создаём временный CLP файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".clp", mode="w", encoding="cp1251") as clp:
            clp_path = clp.name

            clp.write(f'(load "{os.path.join(BASE_DIR, "music_recs.clp")}")\n')
            clp.write("(reset)\n")
            clp.write(f'(assert (user_activity (value {data["activity"]})))\n')
            clp.write(f'(assert (user_popularity (value {data["popularity"]})))\n')
            clp.write(f'(assert (user_mood (value {data["mood"]})))\n')
            clp.write(f'(assert (user_language (value {data["language"]})))\n')
            clp.write("(assert (state ready))\n")
            clp.write("(run)\n")

        cmd = f'"{CLIPS_PATH}" < "{clp_path}"'

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
            encoding="cp866"
        )

        os.remove(clp_path)

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
