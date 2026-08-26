import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# المفتاح السري أو الشفرة التي سيرسلها السيرفر للعميل بعد التحقق الناجح
# يمكنك تغيير هذا المفتاح بالمفتاح الحقيقي الخاص بك
MASTER_SECRET_KEY = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
CLIENT_SECRET_TOKEN = "YOUR_SECRET_CLIENT_TOKEN"

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "message": "Titan Security Server is running securely."})

@app.route('/api/get_key', methods=['POST'])
def get_key():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid payload"}), 400
            
        client_token = data.get("token")
        hwid = data.get("hwid")
        
        # التحقق من صحة التوكن المرسل من السكربت العميل
        if client_token == CLIENT_SECRET_TOKEN:
            return jsonify({
                "status": "success",
                "key": MASTER_SECRET_KEY
            })
        
        return jsonify({"status": "unauthorized", "message": "Invalid token"}), 403
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
