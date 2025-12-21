"""
Ankara Göletleri Koordinatları ve Bilgileri
Senaryo 5: Çevre Bakanlığı Su Numunesi Toplama Rotası
"""

# Ankara'daki 10 göletin koordinatları (lat, lon)
ANKARA_GOLETLER = {
    "Eymir Gölü": {
        "lat": 39.8244,
        "lon": 32.8261,
        "adres": "Eymir Gölü, ODTÜ, Çankaya/Ankara"
    },
    "Mogan Gölü": {
        "lat": 39.7636,
        "lon": 32.7920,
        "adres": "Mogan Gölü, Gölbaşı/Ankara"
    },
    "Karagöl": {
        "lat": 40.4121,
        "lon": 32.9123,
        "adres": "Karagöl, Çubuk/Ankara"
    },
    "Dikilitaş Göleti": {
        "lat": 39.5195,
        "lon": 32.7208,
        "adres": "Dikilitaş Göleti, Çankaya/Ankara"
    },
    "Çamlıdere Göleti": {
        "lat": 40.3933,
        "lon": 32.3956,
        "adres": "Çamlıdere Barajı, Çamlıdere/Ankara"
    },
    "Kurtboğazı Barajı": {
        "lat": 40.2782,
        "lon": 32.7016,
        "adres": "Kurtboğazı Barajı, Çubuk/Ankara"
    },
    "Çubuk Barajı": {
        "lat": 40.0030,
        "lon": 32.9279,
        "adres": "Çubuk Barajı, Çubuk/Ankara"
    },
    "Asartepe Barajı": {
        "lat": 40.1453,
        "lon": 32.3968,
        "adres": "Asartepe Barajı, Elmadağ/Ankara"
    },
    "Güvenç Göleti": {
        "lat": 40.1361,
        "lon": 32.7474,
        "adres": "Güvenç Göleti, Çankırı Yolu/Ankara"
    },
    "İmrahor Vadisi Göleti": {
        "lat": 39.8359,
        "lon": 32.8503,
        "adres": "İmrahor Vadisi, Keçiören/Ankara"
    }
}

# Başlangıç noktası: Çevre ve Şehircilik Bakanlığı Ankara
BASLANGIC_NOKTA = {
    "Çevre Bakanlığı (Başlangıç)": {
        "lat": 39.9156,
        "lon": 32.8518,
        "adres": "Çevre ve Şehircilik Bakanlığı, Üniversiteler Mahallesi, Çankaya/Ankara"
    }
}

def get_all_locations():
    """Tüm lokasyonları birleştirilmiş sözlük olarak döndürür"""
    all_locations = {}
    all_locations.update(BASLANGIC_NOKTA)
    all_locations.update(ANKARA_GOLETLER)
    return all_locations

def get_location_names():
    """Sadece lokasyon isimlerinin listesini döndürür"""
    all_locs = get_all_locations()
    return list(all_locs.keys())

def get_coordinates_list():
    """Koordinatları liste formatında döndürür [(lat, lon), ...]"""
    all_locs = get_all_locations()
    return [(loc["lat"], loc["lon"]) for loc in all_locs.values()]

def get_location_by_name(name):
    """İsme göre lokasyon bilgilerini döndürür"""
    all_locs = get_all_locations()
    return all_locs.get(name, None)
