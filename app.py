from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os
import traceback

app = Flask(__name__)

# путь к CLIPSDOS.exe
CLIPS_PATH = r"C:\Program Files\CLIPS 6.4\CLIPSDOS.exe"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_clips():
    try:
        print("\n========== ЗАПРОС ПОЛУЧЕН ==========\n")

        data = request.json
        print("ДАННЫЕ ОТ КЛИЕНТА:", data)

        # создаём временный CLP файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".clp", mode="w", encoding="utf8") as clp:
            clp_path = clp.name

            print("Создан CLP:", clp_path)

            clp.write(f'(load "{os.path.join(BASE_DIR, "music_recs.clp")}")\n')
            clp.write("(reset)\n")
            clp.write(f'(assert (user_activity (value {data["activity"]})))\n')
            clp.write(f'(assert (user_popularity (value {data["popularity"]})))\n')
            clp.write(f'(assert (user_mood (value {data["mood"]})))\n')
            clp.write(f'(assert (user_language (value {data["language"]})))\n')
            clp.write("(assert (state ready))\n")
            clp.write("(run)\n")

        print("CLP файл успешно записан")

        # формируем команду
        cmd = f'"{CLIPS_PATH}" < "{clp_path}"'
        print("Команда запуска CLIPS:", cmd)

        # запускаем CLIPS через stdin, это 100 процентов работает
        result = subprocess.run(
            ["cmd.exe", "/c", cmd],
            capture_output=True,
            text=True
        )

        print("=== РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ ===")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("RETURN CODE:", result.returncode)

        # удаляем временный CLP файл
        os.remove(clp_path)

        if result.stderr.strip():
            return jsonify({
                "output": "ОШИБКА CLIPS",
                "error": result.stderr,
                "code": result.stdout
            })

        return jsonify({"output": result.stdout})

    except Exception as e:
        print("ОШИБКА PYTHON:", e)
        return jsonify({
            "output": "ОШИБКА PYTHON",
            "error": str(e),
            "trace": traceback.format_exc()
        })


if __name__ == "__main__":
    app.run(debug=True)
