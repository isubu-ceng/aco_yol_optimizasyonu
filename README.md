# Karınca Kolonisi Algoritması ile Yol Optimizasyonu
# Ankara Göletleri Su Numunesi Toplama Rotası

**Öğrenci Adı:** Samet POLAT  
**Öğrenci No:** 2112729005  
**Ders:** BLG-307 Yapay Zeka Sistemleri  
**Senaryo:** Senaryo 5 - Çevre Bakanlığı Gölet Su Numunesi Toplama

---

## 📋 Proje Hakkında

Bu proje, Çevre Bakanlığı birimlerinin Ankara'daki 10 farklı göletten su numunesi toplarken kullanacağı en kısa rotayı bulmak için **Karınca Kolonisi Algoritması (ACO)** kullanmaktadır. Zaman kısıtı nedeniyle en optimize rotanın bulunması kritik önem taşımaktadır.

### Kullanılan Teknolojiler
- **Python 3.8+**
- **Streamlit** - İnteraktif web arayüzü
- **Google Maps API** - Gerçek mesafe hesaplamaları
- **NumPy & Pandas** - Veri işleme
- **Folium & Plotly** - Görselleştirme

---

## 🚀 Kurulum

### Kurulum Yöntemleri

Bu projeyi iki farklı şekilde çalıştırabilirsiniz:
1. **🐳 Docker ile (ÖNERİLİR)** - Tüm bağımlılıklar otomatik kurulur
2. **🐍 Manuel Python kurulumu** - Klasik yöntem

---

## 🐳 Yöntem 1: Docker ile Kurulum (ÖNERİLİR)

Docker kullanarak projeyi tüm bağımlılıklarıyla birlikte çalıştırabilirsiniz.

### Gereksinimler
- Docker Desktop (macOS/Windows) veya Docker Engine (Linux)
- Docker Compose

### Adımlar

#### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/isubu-ceng/aco_yol_optimizasyonu.git
cd aco_yol_optimizasyonu
```

#### 2. API Anahtarını Ayarlayın

**Seçenek A: .env dosyası ile**
```bash
cp .env.docker.example .env
# .env dosyasını düzenleyip API anahtarınızı ekleyin
nano .env  # veya favori editörünüz
```

**Seçenek B: secrets.toml ile**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml dosyasını düzenleyip API anahtarınızı ekleyin
nano .streamlit/secrets.toml
```

#### 3. Docker Container'ı Çalıştırın

```bash
# Docker Compose ile çalıştırın
docker compose up -d

# Veya sadece Docker ile
docker build -t aco-app .
docker run -p 8501:8501 --env-file .env aco-app
```

#### 4. Uygulamaya Erişin

Tarayıcınızda şu adresi açın: **http://localhost:8501**

#### Docker Komutları

```bash
# Container'ı başlat
docker compose up -d

# Container'ı durdur
docker compose down

# Logları görüntüle
docker compose logs -f

# Container'ı yeniden başlat
docker compose restart

# Container durumunu kontrol et
docker compose ps
```

---

## 🐍 Yöntem 2: Manuel Python Kurulumu

### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/isubu-ceng/aco_yol_optimizasyonu.git
cd aco_yol_optimizasyonu
```

### 2. Sanal Ortam Oluşturun (Önerilir)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# veya
venv\\Scripts\\activate  # Windows
```

### 3. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Google Maps API Key Ayarlayın

#### API Key Alma Adımları:
1. [Google Cloud Console](https://console.cloud.google.com/) adresine gidin
2. Yeni bir proje oluşturun
3. **APIs & Services** → **Enable APIs and Services** seçin
4. **Distance Matrix API** ve **Maps JavaScript API** aktif edin
5. **Credentials** → **Create Credentials** → **API Key** oluşturun

#### API Key'i Projeye Ekleyin:

**Yöntem 1:** `.streamlit/secrets.toml` dosyası (Önerilir)
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Sonra `.streamlit/secrets.toml` dosyasını açıp API anahtarınızı ekleyin.

**Yöntem 2:** `.env` dosyası
```bash
cp .env.example .env
```
Sonra `.env` dosyasını açıp API anahtarınızı ekleyin.

### 5. Uygulamayı Çalıştırın
```bash
streamlit run main.py
```

---

## 📁 Proje Yapısı

```
aco_yol_optimizasyonu/
│
├── main.py                      # Streamlit ana uygulama dosyası
├── config.py                    # Konfigürasyon parametreleri
├── requirements.txt             # Python bağımlılıkları
│
├── Dockerfile                   # Docker image tanımı
├── docker-compose.yml           # Docker Compose konfigürasyonu
├── .dockerignore                # Docker'a dahil edilmeyecek dosyalar
│
├── data/
│   └── coordinates.py           # Ankara göletlerinin koordinatları
│
├── core/
│   ├── ant_algorithm.py         # ACO algoritması implementasyonu
│   ├── matrix_utils.py          # Mesafe matrisi işlemleri
│   └── haversine.py             # Koordinat mesafe hesaplamaları
│
├── visual/
│   └── plotting.py              # Görselleştirme fonksiyonları
│
├── figure/                      # Algoritma çıktıları (otomatik oluşturulur)
│   ├── convergence.png          # Yakınsama grafiği
│   └── rota.html                # İnteraktif harita
│
├── .streamlit/
│   ├── secrets.toml             # API anahtarı (GİZLİ - git'e eklenmez)
│   └── secrets.toml.example     # API anahtarı şablonu
│
├── .env.example                 # Ortam değişkenleri şablonu
├── .gitignore                   # Git ignore dosyası
└── README.md                    # Bu dosya
```

**Not:** `figure/` klasörü, algoritma çalıştırıldığında otomatik olarak görselleştirme çıktılarını kaydeder.

---

## 🎯 Kullanım

### Uygulamayı Başlatın
```bash
streamlit run main.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

### Arayüz Kullanımı

1. **Kenar Çubuğunda Parametreleri Ayarlayın:**
   - Karınca Sayısı (10-200)
   - İterasyon Sayısı (50-500)
   - Alpha (α) - Feromon önem derecesi
   - Beta (β) - Mesafe önem derecesi
   - Buharlaşma Oranı (0.1-0.9)

2. **"Algoritma Çalıştır" Butonuna Tıklayın**

3. **Sonuçları İnceleyin:**
   - En kısa rota ve toplam mesafe
   - İnteraktif harita üzerinde rota görselleştirmesi
   - İterasyonlara göre yakınsama grafiği

---

## 🗺️ Ankara Göletleri

Projede kullanılan 10 gölet:
1. Eymir Gölü
2. Mogan Gölü
3. Karagöl (Çubuk)
4. Dikilitaş Göleti
5. Çamlıdere Göleti
6. Kurtboğazı Barajı
7. Çubuk Barajı
8. Asartepe Barajı
9. Güvenç Göleti
10. İmrahor Vadisi Göleti

---

## 🐜 Karınca Kolonisi Algoritması (ACO)

### Algoritma Parametreleri

- **α (Alpha):** Feromon izinin önemi
- **β (Beta):** Mesafe bilgisinin (sezgisel) önemi
- **ρ (Rho):** Feromon buharlaşma oranı
- **Q:** Feromon yoğunluğu sabiti
- **m (Karınca sayısı):** Her iterasyonda çalışan karınca sayısı

### Algoritma Akışı

1. Başlangıç feromon değerleri atanır
2. Her iterasyonda:
   - Her karınca bir tur oluşturur
   - Olasılıksal olarak bir sonraki şehri seçer
   - Feromon güncellemesi yapılır
   - En iyi tur kaydedilir
3. Belirlenen iterasyon sayısı kadar tekrarlanır
4. En kısa tur döndürülür

---

## 📊 Çıktılar

### 1. Harita Görselleştirmesi
- İnteraktif Folium haritası
- Göletlerin işaretlenmesi
- Optimal rotanın çizilmesi
- **Otomatik kayıt:** `figure/rota.html`

### 2. Yakınsama Grafiği
- Her iterasyondaki en iyi mesafe
- Algoritmanın öğrenme süreci
- İyileştirme yüzdesi istatistiği
- **Otomatik kayıt:** `figure/convergence.png`

### 3. Rota Detayları
- Ziyaret sırası
- Toplam mesafe (km)
- Tahmini süre

### 4. Figure Klasörü
Algoritma her çalıştırıldığında `figure/` klasörüne şu dosyalar otomatik kaydedilir:
- **convergence.png** - 300 DPI yüksek kaliteli yakınsama grafiği
- **rota.html** - İnteraktif harita (tarayıcıda açılabilir)

Bu dosyalar rapor ve sunumlarda kullanılabilir.

---

## ⚙️ Geliştirme Notları

### Test Etme
```bash
# Bağımlılıkları kontrol et
pip list

# Streamlit versiyonunu kontrol et
streamlit --version
```
