from flask import Flask, jsonify, request

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
