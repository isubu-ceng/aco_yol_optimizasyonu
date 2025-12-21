"""
Haversine Formülü ile İki Koordinat Arası Kuş Uçuşu Mesafe Hesaplama
"""

import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    İki nokta arasındaki kuş uçuşu mesafeyi Haversine formülü ile hesaplar.
    
    Parameters:
    -----------
    lat1, lon1 : float
        Birinci noktanın enlem ve boylam değerleri (derece)
    lat2, lon2 : float
        İkinci noktanın enlem ve boylam değerleri (derece)
    
    Returns:
    --------
    float
        İki nokta arası mesafe (kilometre)
    """
    # Dünya yarıçapı (km)
    R = 6371.0
    
    # Dereceyi radyana çevir
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    # Farkları hesapla
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formülü
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    
    return distance

def create_haversine_matrix(coordinates):
    """
    Koordinat listesinden Haversine mesafe matrisi oluşturur.
    
    Parameters:
    -----------
    coordinates : list of tuples
        [(lat1, lon1), (lat2, lon2), ...] formatında koordinat listesi
    
    Returns:
    --------
    numpy.ndarray
        NxN boyutunda mesafe matrisi (N = lokasyon sayısı)
    """
    n = len(coordinates)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                lat1, lon1 = coordinates[i]
                lat2, lon2 = coordinates[j]
                distance_matrix[i][j] = haversine_distance(lat1, lon1, lat2, lon2)
    
    return distance_matrix
