# 🚀 Hızlı Başlangıç Kılavuzu

## Docker ile 3 Adımda Çalıştırın

### Adım 1: API Anahtarını Ayarlayın

`.env` dosyası zaten hazır! API anahtarınız içinde:
```bash
GOOGLE_MAPS_API_KEY={{GOOGLE_MAPS_API_KEY}}
```

### Adım 2: Docker Container'ı Başlatın

```bash
docker compose up -d
```

### Adım 3: Tarayıcınızda Açın

http://localhost:8501

---

## Kullanışlı Komutlar

```bash
# Container'ı durdur
docker compose down

# Logları görüntüle
docker compose logs -f

# Yeniden başlat
docker compose restart
```

---

## Proje Hakkında

**Öğrenci:** Samet POLAT (2112729005)  
**Ders:** BLG-307 Yapay Zeka Sistemleri  
**Konu:** Karınca Kolonisi Algoritması ile Yol Optimizasyonu
