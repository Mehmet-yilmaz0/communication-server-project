# 🚀 Sistem Kurulum Rehberi

Bu rehber, backend (Python/Flask/PostgreSQL) ve frontend (React) sistemini adım adım ayağa kaldırmanızı sağlar.

---

## 📋 Ön Gereksinimler

### Gerekli Yazılımlar:
1. **Python 3.8+** - [İndir](https://www.python.org/downloads/)
2. **Node.js 14+ ve npm** - [İndir](https://nodejs.org/)
3. **PostgreSQL** - [İndir](https://www.postgresql.org/download/)
4. **Git** (opsiyonel)

---

## 🔧 ADIM 1: PostgreSQL Veritabanı Kurulumu

### 1.1 PostgreSQL'i Başlat
```bash
# Windows (PostgreSQL servisi otomatik başlar)
# Veya Services panelinden "postgresql-x64-XX" servisini başlat

# Linux/Mac
sudo systemctl start postgresql
# veya
brew services start postgresql
```

### 1.2 Veritabanı Oluştur
```bash
# PostgreSQL'e bağlan
psql -U postgres

# Veritabanı oluştur
CREATE DATABASE communication_db;

# Çıkış
\q
```

**Not:** Eğer PostgreSQL şifresi sorarsa, varsayılan şifre genellikle `postgres` veya kurulum sırasında belirlediğiniz şifredir.

---

## 🔧 ADIM 2: Backend Kurulumu

### 2.1 Backend Klasörüne Git
```bash
cd backend
```

### 2.2 Python Sanal Ortamı Oluştur (Önerilir)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 2.4 .env Dosyası Oluştur
`backend` klasöründe `.env` dosyası oluşturun:

```bash
# Windows (PowerShell)
New-Item -Path .env -ItemType File

# Linux/Mac
touch .env
```

`.env` dosyasına şu içeriği ekleyin:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/communication_db
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
FLASK_ENV=development
FLASK_DEBUG=True
```

**Önemli:** 
- `DATABASE_URL` içindeki `postgres:postgres` kısmını kendi PostgreSQL kullanıcı adı ve şifrenizle değiştirin
- `JWT_SECRET` değerini güvenli bir rastgele string ile değiştirin

### 2.5 Backend'i Başlat
```bash
python app.py
```

**Başarılı olursa şunu göreceksiniz:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

Backend artık `http://localhost:5000` adresinde çalışıyor! ✅

---

## 🔧 ADIM 3: Frontend Kurulumu

### 3.1 Frontend Klasörüne Git
Yeni bir terminal açın ve:

```bash
cd my-frontend
```

### 3.2 Bağımlılıkları Yükle
```bash
npm install
```

### 3.3 Frontend'i Başlat
```bash
npm start
```

**Başarılı olursa:**
- Tarayıcı otomatik açılır: `http://localhost:3000`
- Veya manuel olarak `http://localhost:3000` adresine gidin

Frontend artık çalışıyor! ✅

---

## 🧪 ADIM 4: Sistem Testi

### 4.1 Backend Health Check
Tarayıcıda veya Postman'de:
```
GET http://localhost:5000/api/health
```

**Beklenen Response:**
```json
{
  "status": "ok"
}
```

### 4.2 Kullanıcı Kaydı (Postman veya curl)
```bash
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "123456"
}
```

**Beklenen Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```

### 4.3 Frontend'den Test
1. Frontend açık olmalı: `http://localhost:3000`
2. Tarayıcı console'unu açın (F12)
3. Hata olmamalı

---

## 🐛 Sorun Giderme

### Backend Çalışmıyor

**Hata: "ModuleNotFoundError"**
```bash
# Sanal ortam aktif mi kontrol et
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Tekrar yükle
pip install -r requirements.txt
```

**Hata: "psycopg2" hatası**
```bash
# Windows için özel kurulum gerekebilir
pip install psycopg2-binary --force-reinstall
```

**Hata: "DATABASE_URL" hatası**
- `.env` dosyasının `backend` klasöründe olduğundan emin olun
- `.env` içindeki PostgreSQL bilgilerini kontrol edin

**Hata: "Port 5000 already in use"**
```bash
# Port'u değiştir (app.py son satırı)
app.run(debug=True, host='0.0.0.0', port=5001)  # 5001 kullan
```

### Frontend Çalışmıyor

**Hata: "npm install" hatası**
```bash
# node_modules'ü sil ve tekrar yükle
rm -rf node_modules package-lock.json
npm install
```

**Hata: "Port 3000 already in use"**
```bash
# Farklı port kullan
PORT=3001 npm start
```

**Hata: "Cannot connect to backend"**
- Backend'in çalıştığından emin olun (`http://localhost:5000/api/health`)
- Tarayıcı console'unda CORS hatası varsa, backend'de CORS ayarlarını kontrol edin

### PostgreSQL Sorunları

**PostgreSQL bağlantı hatası:**
```bash
# PostgreSQL servisinin çalıştığından emin olun
# Windows: Services panelinden kontrol et
# Linux: sudo systemctl status postgresql

# Veritabanının var olduğunu kontrol et
psql -U postgres -l
```

**Şifre hatası:**
- `pg_hba.conf` dosyasını düzenleyerek şifre gereksinimini kaldırabilirsiniz
- Veya `.env` dosyasındaki `DATABASE_URL`'de doğru şifreyi kullanın

---

## 📝 Hızlı Başlangıç (Özet)

```bash
# 1. PostgreSQL'de veritabanı oluştur
psql -U postgres
CREATE DATABASE communication_db;
\q

# 2. Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
# .env dosyası oluştur ve düzenle
python app.py

# 3. Frontend (yeni terminal)
cd my-frontend
npm install
npm start
```

---

## ✅ Başarı Kontrolü

Sistem başarıyla çalışıyorsa:

1. ✅ Backend: `http://localhost:5000/api/health` → `{"status": "ok"}`
2. ✅ Frontend: `http://localhost:3000` → React uygulaması açılıyor
3. ✅ Database: PostgreSQL'de `communication_db` veritabanı var
4. ✅ API: Postman'de register/login endpoint'leri çalışıyor

---

## 🎯 Sonraki Adımlar

1. **Kullanıcı Kaydı:** Frontend'den veya Postman'den kullanıcı kaydedin
2. **Login:** Kullanıcı ile giriş yapın ve token alın
3. **Mesaj Gönderme:** Token ile mesaj gönderin
4. **Mesajları Görüntüleme:** Mesajları listeleyin ve decrypt edin

**Not:** Frontend'de henüz login/register UI yoksa, token'ı manuel olarak localStorage'a kaydedebilirsiniz:

```javascript
// Browser console'da
localStorage.setItem('access_token', 'YOUR_TOKEN_HERE');
```

---

## 📞 Yardım

Sorun yaşarsanız:
1. Terminal/console hatalarını kontrol edin
2. Backend ve frontend loglarını inceleyin
3. PostgreSQL servisinin çalıştığından emin olun
4. Port'ların (5000, 3000) kullanılabilir olduğundan emin olun

