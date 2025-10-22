from flask import Flask, jsonify, request
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
    # 這裡可以呼叫你的原本 Python 腳本函式，例如更新資料庫
    return jsonify({"status": "success", "received": data})

if __name__ == "__main__":
    # 只有在本地測試時使用
    app.run(host="0.0.0.0", port=10000, debug=True)


@app.route("/McDonald", methods=["GET"])
def run_mcdonald():
    try:
        # ✅ 建立物件並執行爬蟲
        m = McDonald()
        m.start_driver()  # 執行爬蟲主程式

        return jsonify({
            "status": "ok",
            "message": "McDonald 爬蟲已執行完成，已生成 McDonald.json"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })