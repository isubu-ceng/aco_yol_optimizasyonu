"""
ACO Parametreleri ve Konfigürasyon Ayarları
"""

# ACO Algoritması Parametreleri
DEFAULT_ACO_PARAMS = {
    'num_ants': 50,              # Karınca sayısı
    'num_iterations': 100,       # İterasyon sayısı
    'alpha': 1.0,                # Feromon önem derecesi
    'beta': 2.0,                 # Mesafe önem derecesi
    'evaporation_rate': 0.5,     # Buharlaşma oranı (0-1 arası)
    'Q': 100                     # Feromon yoğunluğu sabiti
}

# Streamlit Sayfa Ayarları
PAGE_CONFIG = {
    'page_title': 'ACO Yol Optimizasyonu - Ankara Göletler',
    'page_icon': '🐜',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Harita Ayarları
MAP_CONFIG = {
    'ankara_center': [39.9334, 32.8597],  # Ankara merkez koordinatları
    'zoom_start': 11
}
