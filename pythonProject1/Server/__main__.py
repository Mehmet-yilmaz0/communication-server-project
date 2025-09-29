from flask import Flask
from flask_socketio import SocketIO
from cryptography.fernet import Fernet

# Anahtar oluştur (normalde dosyadan okunur)
key = Fernet.generate_key()
cipher = Fernet(key)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return "Server çalışıyor!"

# Mesaj alıcı
@socketio.on("message")
def handle_message(encrypted_msg):
    try:
        # Gelen mesajı çöz
        decrypted = cipher.decrypt(encrypted_msg.encode()).decode()
        print(f"Şifreli mesaj geldi: {encrypted_msg}")
        print(f"Çözülen mesaj: {decrypted}")

        # Cevap gönder
        reply = f"Mesaj alındı: {decrypted}"
        encrypted_reply = cipher.encrypt(reply.encode()).decode()
        socketio.send(encrypted_reply)

    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    print("Şifreleme anahtarını paylaş:", key.decode())
    socketio.run(app, host="127.0.0.1", port=5000)