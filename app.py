from flask import Flask, render_template, request, jsonify
import traceback
from music_recs import get_formatted_output

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_expert_system():
    try:
        data = request.json
        print("=== ПОЛУЧЕНЫ ДАННЫЕ ===", data)

        # Получаем параметры от пользователя
        activity = data.get("activity", "work")
        popularity = data.get("popularity", "popular")
        mood = data.get("mood", "energetic")
        language = data.get("language", "russian")

        # Запускаем экспертную систему
        output = get_formatted_output(activity, popularity, mood, language)

        print("=== РЕЗУЛЬТАТ ===")
        print(output)

        return jsonify({"output": output})

    except Exception as e:
        return jsonify({
            "output": "ОШИБКА PYTHON",
            "error": str(e),
            "trace": traceback.format_exc()
        })


if __name__ == "__main__":
    app.run(debug=True)
