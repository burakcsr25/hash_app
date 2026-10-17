# Hash Analiz (Hash Analyzer) 🔍

Modern, hızlı ve kullanıcı dostu bir arayüzle dosyalarınızın MD5 hash değerlerini, boyutlarını, tarihlerini ve medya dosyalarının sürelerini hesaplayan; yinelenen (duplicate) dosyaları akıllı renk kodlamasıyla anında görselleştiren PyQt6 tabanlı masaüstü uygulaması.

---

## 🚀 Öne Çıkan Özellikler

- 📂 **Sürükle & Bırak Desteği:** Tekil dosyaları veya doğrudan klasörleri pencereye sürükleyip bırakarak (tüm alt klasörlerle birlikte) anında tarayın.
- ⚡ **Asenkron & Çok Kanallı (Multi-Threaded):** Hash ve video/ses süresi hesaplamaları arka planda bağımsız `QThread` iş parçacıklarıyla yürütülür; arayüz işlem sırasında asla donmaz veya takılmaz.
- 🎨 **Akıllı Çift (Duplicate) Dosya Tespiti:** MD5 özetleri aynı olan dosyalar otomatik olarak gruplanır ve soft pastel renk paletiyle renklendirilerek tabloda hemen göze çarpar.
- ⏱️ **Gelişmiş Medya Süresi Analizi:** `TinyTag` ve `OpenCV` entegrasyonu ile hem ses hem de video (`.mp4`, `.mkv`, `.avi`, `.mov`, `.mts`, `.flv` vb.) dosyalarının sürelerini doğru şekilde tespit eder.
- 🔢 **Özel Sayısal Sıralama:** Boyut sütunu (MB bazında) standart metin sıralaması yerine sayısal büyüklüğe göre sıralanır.
- 📊 **Canlı Sayaç:** Durum çubuğunda (status bar) yüklenen toplam dosya adedini gerçek zamanlı takip edebilirsiniz.

---

## 🛠️ Kurulum

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/burakcsr25/hash_app.git
cd hash_app
```

### 2. Gerekli Paketleri Yükleyin
Sisteminizde Python 3.8 veya üzeri yüklü olduğundan emin olun:
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
python hash_app.py
```

---

## 📦 Bağımsız Çalıştırılabilir (.EXE) Oluşturma

Projeyi Python kurulu olmayan bilgisayarlarda da çalıştırmak üzere tek bir `.exe` dosyası haline getirmek için PyInstaller kullanabilirsiniz:

```bash
pyinstaller hash_app.spec
```

İşlem tamamlandığında `dist/` klasörü altında `hash_app.exe` oluşacaktır.

---

## 📁 Proje Dosya Yapısı

```plaintext
hash_app/
├── hash_app.py        # Ana uygulama ve PyQt6 arayüz kodları
├── hash_app.spec      # PyInstaller derleme ayar dosyası
├── icon.ico           # Uygulama simgesi
├── requirements.txt   # Python bağımlılıkları
├── .gitignore         # Git takip dışı dosyalar listesi
└── README.md          # Proje dokümantasyonu
```

---

## 🇬🇧 English Summary

**Hash Analyzer** is a lightweight, responsive desktop tool built with Python & PyQt6. It allows users to quickly calculate MD5 checksums, file sizes, modification dates, and media durations via simple Drag & Drop.

### Key Highlights:
- **Drag & Drop:** Drop files or entire folders to analyze recursively.
- **Duplicate File Highlighting:** Automatically matches identical MD5 hashes and groups them with distinctive pastel background colors.
- **Media Duration Calculation:** Supports audio and video formats using `TinyTag` and `OpenCV`.
- **Non-blocking UI:** Employs `QThread` workers for responsive background processing.
- **PyInstaller Ready:** Build configuration included to generate standalone Windows binaries.

---

## 📜 Lisans

Bu proje açık kaynak olarak sunulmuştur. Dilediğiniz gibi kullanabilir, katkıda bulunabilir ve geliştirebilirsiniz.
