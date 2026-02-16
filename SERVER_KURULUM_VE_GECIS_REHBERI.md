# 🚀 Sunucu Kurulum, Yönetim ve Geçiş Rehberi (Adım Adım)

Bu belge, projenizi (`avrasya-university-site`) kendi sunucunuza (1TB Fiziksel Sunucu) kurmanız, yönetmeniz ve mevcut domaininizi (`avrasya.edu.tr`) yönlendirmeniz için gereken **tüm adımları** en ince detayına kadar anlatır.

---

## **BÖLÜM 1: Projenin Sunucuya Hazırlanması (Lokalde Yapılacaklar)**

Sunucuya kodları göndermeden önce, projemizin sunucu ortamında sorunsuz çalışması için bazı dosyaları düzenlememiz gerekmektedir. Bu adımları "Uygula" dediğinizde ben otomatik yapacağım ancak planımızda bulunması şarttır.

### **1.1. `.gitignore` Dosyasının Düzenlenmesi**
Sunucuya gereksiz veya güvenlik riski taşıyan dosyaların gitmemesi için `.gitignore` dosyasını güncelleyeceğiz.
*   **Eklenecekler:** `.env` (şifreler içerir), `venv/` (sanal ortam), `__pycache__` (gereksiz derlenmiş dosyalar), `db.sqlite3` (lokal veritabanı), `media/` (kullanıcı yüklemeleri sunucuda ayrı tutulur).

### **1.2. `settings.py` Veritabanı Ayarı (PostgreSQL Entegrasyonu)**
Projenin hem bilgisayarınızda (SQLite) hem de sunucuda (PostgreSQL) sorunsuz çalışması için veritabanı ayarlarını şu şekilde güncelleyeceğiz:
```python
import os
import dj_database_url

# Mevcut SQLite ayarını koruyup, sunucuda DATABASE_URL varsa PostgreSQL kullanacak yapı:
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}
```

### **1.3. Gerekli Kütüphanelerin Eklenmesi (`requirements.txt`)**
Sunucuda PostgreSQL ve web sunucusu için gerekli paketlerin `requirements.txt` dosyasında olduğundan emin olacağız:
*   `psycopg2-binary` (PostgreSQL adaptörü)
*   `gunicorn` (Uygulama sunucusu)
*   `dj-database-url` (Veritabanı URL yapılandırması)

---

## **BÖLÜM 2: Sunucuya Bağlanma (SSH)**

Sunucunuzu yönetmek için "SSH" (Secure Shell) protokolü kullanılır. Bu, sunucunun kara ekranına (terminaline) uzaktan bağlanmanızı sağlar.

### **Seçenek A: Windows İçin (PuTTY Programı İle)**
1.  **İndirme:** [PuTTY İndir](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) adresinden uygulamayı indirip kurun.
2.  **Ayarlar:**
    *   PuTTY'yi açın.
    *   **Host Name (or IP address)** kutusuna sunucunuzun IP adresini yazın (Örn: `192.168.1.100`).
    *   **Port** kısmının `22` olduğundan emin olun.
    *   **Open** butonuna tıklayın.
3.  **Giriş Yapma:**
    *   Karşınıza siyah bir ekran ve `login as:` yazısı gelecek.
    *   Buraya **`root`** yazın ve Enter'a basın.
    *   `Password:` sorusu gelecek.
        *   ⚠️ **DİKKAT:** Şifrenizi yazarken ekranda hiçbir karakter (yıldız vs.) çıkmaz, imleç ilerlemez. Bu bir güvenlik önlemidir. Siz şifrenizi doğruca yazıp **Enter**'a basın.

### **Seçenek B: Windows PowerShell veya Mac/Linux Terminal İle (Program İndirmeden)**
1.  Bilgisayarınızda **PowerShell** (Windows) veya **Terminal** (Mac) uygulamasını açın.
2.  Şu komutu yazın:
    ```bash
    ssh root@SUNUCU_IP_ADRESI
    ```
    *(Örnek: `ssh root@192.168.1.100`)*
3.  İlk bağlantıda "Are you sure you want to continue connecting?" sorusu gelirse **`yes`** yazıp Enter'a basın.
4.  Şifrenizi girin (yine ekranda görünmeyecektir) ve Enter'a basın.

---

## **BÖLÜM 3: Sunucunun Hazırlanması (Sıfır Kurulum)**

Bağlandıktan sonra sırasıyla şu komutları uygulayacağız:

### **3.1. Güncellemeler ve Paket Kurulumları**
```bash
# Sunucuyu güncelle
sudo apt update && sudo apt upgrade -y

# Gerekli programları kur (Python, PostgreSQL, Nginx, Git vb.)
sudo apt install python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git -y
```

### **3.2. Veritabanının Oluşturulması**
```bash
# Postgres kullanıcısına geç
sudo -u postgres psql

# (SQL Komut Satırı Açılacak)
CREATE DATABASE avrasya_db;
CREATE USER avrasya_admin WITH PASSWORD 'GUCLU_BIR_SIFRE_BELIRLEYIN';
ALTER ROLE avrasya_admin SET client_encoding TO 'utf8';
ALTER ROLE avrasya_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE avrasya_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE avrasya_db TO avrasya_admin;
\q
```

---

## **BÖLÜM 4: Projenin Sunucuya Çekilmesi**

### **4.1. Kodları İndirme**
```bash
# Proje klasörünü oluştur
sudo mkdir -p /var/www/avrasya_site
sudo chown -R $USER:$USER /var/www/avrasya_site

# GitHub'dan projeyi çek
git clone https://github.com/raminentezar-rgb/avrasya-university-site.git /var/www/avrasya_site

cd /var/www/avrasya_site
```

### **4.2. Sanal Ortam ve Kurulum**
```bash
# Sanal ortam oluştur
python3 -m venv venv

# Aktif et
source venv/bin/activate

# Kütüphaneleri yükle
pip install -r requirements.txt
```

### **4.3. Gizli Ayarlar (.env Dosyası)**
Sunucuda `.env` dosyası oluşturup gizli bilgileri gireceğiz.
```bash
nano .env
```
**İçerik:**
```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=BURAYA_UZUN_RASTGELE_BIR_ANAHTAR_YAZIN
DJANGO_ALLOWED_HOSTS=avrasya.edu.tr,www.avrasya.edu.tr,SUNUCU_IP_ADRESI
DATABASE_URL=postgres://avrasya_admin:SIFRENIZ@localhost/avrasya_db
```
*(Kaydetmek için: `CTRL + O`, `Enter`. Çıkmak için: `CTRL + X`)*

### **4.4. Yayına Hazırlık**
```bash
# Statik dosyaları topla
python manage.py collectstatic --noinput

# Veritabanını kur
python manage.py migrate
```

---

## **BÖLÜM 5: Servislerin Kurulumu**

### **5.1. Gunicorn (Uygulama Sunucusu)**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
**İçerik:**
```ini
[Unit]
Description=gunicorn daemon for Avrasya Site
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/avrasya_site
ExecStart=/var/www/avrasya_site/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/avrasya_site/avrasya.sock avrasya_site.wsgi:application

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### **5.2. Nginx (Web Sunucusu)**
```bash
sudo nano /etc/nginx/sites-available/avrasya
```
**İçerik:**
```nginx
server {
    listen 80;
    server_name avrasya.edu.tr www.avrasya.edu.tr;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/avrasya_site/staticfiles/;
    }

    location /media/ {
        alias /var/www/avrasya_site/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/avrasya_site/avrasya.sock;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/avrasya /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## **BÖLÜM 6: Güvenlik ve Domain**

### **6.1. Domain Yönlendirme**
Natro panelinden, DNS Yönetimi sayfasından `A Record` kaydını bulup sunucunuzun IP adresini girin.

### **6.2. SSL (HTTPS) Sertifikası**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d avrasya.edu.tr -d www.avrasya.edu.tr
```

---

## **BÖLÜM 7: Bakım ve Komutlar**

Projeyi güncellediğinizde sunucuda şu komutları çalıştırın:
```bash
cd /var/www/avrasya_site
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```
