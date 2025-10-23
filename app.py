from flask import Flask, jsonify, request, send_file
from McDonald import McDonald

app = Flask(__name__)

# 測試根路由
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello from MealWorkout Python API!"})


# 範例 API 路由
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    return jsonify({"status": "success", "received": data})


# ✅ 麥當勞爬蟲執行
@app.route("/McDonald", methods=["GET"])
def run_mcdonald():
    try:
        # 執行爬蟲
        m = McDonald()
        m.start_driver()  # 產生 McDonald.json

        return jsonify({
            "status": "ok",
            "message": "McDonald 爬蟲已執行完成，已生成 McDonald.json"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ✅ 提供下載 JSON
@app.route("/download", methods=["GET"])
def download_json():
    return send_file(
        "McDonald.json",
        mimetype="application/json",
        as_attachment=True
    )


# 🚫 不要在雲端執行 app.run()，Render 會自動管理伺服器
if __name__ == "__main__":
    # 這段只在你本機測試時執行
    app.run(host="0.0.0.0", port=10000, debug=True)
