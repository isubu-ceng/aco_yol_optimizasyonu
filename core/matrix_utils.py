"""
Google Maps API ile Gerçek Yol Mesafesi Matrisi Oluşturma
"""

import googlemaps
import numpy as np
import time
from datetime import datetime

def create_distance_matrix_with_google(api_key, locations_dict):
    """
    Google Maps Distance Matrix API kullanarak gerçek yol mesafelerini hesaplar.
    
    Parameters:
    -----------
    api_key : str
        Google Maps API anahtarı
    locations_dict : dict
        {name: {lat: float, lon: float, adres: str}} formatında lokasyon sözlüğü
    
    Returns:
    --------
    tuple
        (distance_matrix, duration_matrix, location_names)
        - distance_matrix: numpy array, km cinsinden mesafeler
        - duration_matrix: numpy array, dakika cinsinden süreler
        - location_names: list, lokasyon isimleri
    """
    # Google Maps client oluştur
    gmaps = googlemaps.Client(key=api_key)
    
    # Lokasyon isimlerini ve koordinatlarını al
    location_names = list(locations_dict.keys())
    n = len(location_names)
    
    # Mesafe ve süre matrisleri oluştur
    distance_matrix = np.zeros((n, n))
    duration_matrix = np.zeros((n, n))
    
    # Her lokasyon çifti için API'ye istek gönder
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            
            # Origin ve destination koordinatları
            origin = (locations_dict[location_names[i]]["lat"], 
                     locations_dict[location_names[i]]["lon"])
            destination = (locations_dict[location_names[j]]["lat"], 
                          locations_dict[location_names[j]]["lon"])
            
            try:
                # Distance Matrix API çağrısı
                result = gmaps.distance_matrix(
                    origins=origin,
                    destinations=destination,
                    mode="driving",  # Araba ile
                    language="tr",
                    units="metric"
                )
                
                # Sonuçları kontrol et
                if result['rows'][0]['elements'][0]['status'] == 'OK':
                    # Mesafe (metre -> kilometre)
                    distance_m = result['rows'][0]['elements'][0]['distance']['value']
                    distance_matrix[i][j] = distance_m / 1000.0
                    
                    # Süre (saniye -> dakika)
                    duration_s = result['rows'][0]['elements'][0]['duration']['value']
                    duration_matrix[i][j] = duration_s / 60.0
                else:
                    print(f"Uyarı: {location_names[i]} -> {location_names[j]} mesafe bulunamadı!")
                    distance_matrix[i][j] = 0
                    duration_matrix[i][j] = 0
                
                # API rate limit'i aşmamak için kısa bekleme
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Hata: {location_names[i]} -> {location_names[j]} - {str(e)}")
                distance_matrix[i][j] = 0
                duration_matrix[i][j] = 0
    
    return distance_matrix, duration_matrix, location_names

def save_matrix_to_file(matrix, location_names, filename):
    """
    Mesafe matrisini dosyaya kaydeder.
    
    Parameters:
    -----------
    matrix : numpy.ndarray
        Mesafe matrisi
    location_names : list
        Lokasyon isimleri
    filename : str
        Kaydedilecek dosya adı
    """
    import pandas as pd
    
    df = pd.DataFrame(matrix, index=location_names, columns=location_names)
    df.to_csv(filename)
    print(f"Mesafe matrisi {filename} dosyasına kaydedildi.")

def load_matrix_from_file(filename):
    """
    Dosyadan mesafe matrisini yükler.
    
    Parameters:
    -----------
    filename : str
        Yüklenecek dosya adı
    
    Returns:
    --------
    tuple
        (matrix, location_names)
    """
    import pandas as pd
    
    df = pd.read_csv(filename, index_col=0)
    matrix = df.values
    location_names = list(df.index)
    
    return matrix, location_names
