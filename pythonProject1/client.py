
import socketio
from cryptography.fernet import Fernet

# Buraya server çalıştırılırken bastığı anahtarı yapıştır
key = b"7J2ZDx4BRNJYS_erwh4yRDvw37mZhKZJlY1sQcD7qs8="
cipher = Fernet(key)

sio = socketio.Client()

@sio.event
def connect():
    print("Server'a bağlandı")

@sio.on("message")
def on_message(data):
    decrypted = cipher.decrypt(data.encode()).decode()
    print("Server cevabı:", decrypted)

sio.connect("http://127.0.0.1:5000")

# Mesaj gönder
msg = "Selam, burası client!"
encrypted_msg = cipher.encrypt(msg.encode()).decode()
sio.send(encrypted_msg)

sio.wait()
