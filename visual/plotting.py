"""
Görselleştirme Fonksiyonları
Harita ve grafik oluşturma
"""

import folium
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def create_route_map(locations_dict, route_indices, location_names):
    """
    Folium ile interaktif harita oluşturur ve rotayı çizer.
    
    Parameters:
    -----------
    locations_dict : dict
        Lokasyon bilgileri sözlüğü
    route_indices : list
        Rota indeksleri [0, 3, 1, 2, ...]
    location_names : list
        Lokasyon isimleri
    
    Returns:
    --------
    folium.Map
        Oluşturulan harita objesi
    """
    # Ankara merkezinde harita oluştur
    ankara_center = [39.9334, 32.8597]
    route_map = folium.Map(
        location=ankara_center,
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Rota koordinatlarını al
    route_coords = []
    for idx in route_indices:
        name = location_names[idx]
        loc = locations_dict[name]
        route_coords.append([loc['lat'], loc['lon']])
    
    # Başlangıç noktasına dön
    route_coords.append(route_coords[0])
    
    # Rotayı çiz
    folium.PolyLine(
        route_coords,
        color='blue',
        weight=3,
        opacity=0.7,
        popup='Optimal Rota'
    ).add_to(route_map)
    
    # Her lokasyona marker ekle
    for i, idx in enumerate(route_indices):
        name = location_names[idx]
        loc = locations_dict[name]
        
        # Renk kodlaması: Başlangıç yeşil, diğerleri kırmızı
        color = 'green' if i == 0 else 'red'
        
        # Marker oluştur
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=f"<b>{i}. {name}</b><br>{loc.get('adres', '')}",
            tooltip=f"{i}. {name}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(route_map)
    
    return route_map

def save_map_as_png(route_map, filename='figure/rota.png'):
    """
    Folium haritasını PNG olarak kaydeder.
    
    Parameters:
    -----------
    route_map : folium.Map
        Kaydedilecek harita
    filename : str
        Dosya yolu
    """
    try:
        # HTML olarak kaydet
        html_path = filename.replace('.png', '.html')
        route_map.save(html_path)
        print(f"✅ Harita {html_path} olarak kaydedildi")
        
        # PNG'ye çevirme için selenium gerekli (opsiyonel)
        # Basit çözüm: HTML'i kaydediyoruz
        return html_path
    except Exception as e:
        print(f"⚠️ Harita kaydedilemedi: {e}")
        return None

def plot_convergence(iteration_history):
    """
    İterasyonlara göre en iyi mesafe grafiğini çizer.
    
    Parameters:
    -----------
    iteration_history : list
        Her iterasyondaki en iyi mesafe değerleri
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Oluşturulan grafik
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(1, len(iteration_history) + 1)),
        y=iteration_history,
        mode='lines+markers',
        name='En İyi Mesafe',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title='ACO Yakınsama Grafiği',
        xaxis_title='İterasyon',
        yaxis_title='En İyi Mesafe (km)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_convergence_matplotlib(iteration_history, save_path='figure/convergence.png'):
    """
    Matplotlib ile yakınsama grafiği çizer ve kaydeder.
    
    Parameters:
    -----------
    iteration_history : list
        Her iterasyondaki en iyi mesafe değerleri
    save_path : str
        Grafiği kaydetmek için dosya yolu (varsayılan: figure/convergence.png)
    
    Returns:
    --------
    str
        Kaydedilen dosyanın yolu
    """
    # Figure klasörünün var olduğundan emin ol
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.figure(figsize=(12, 7))
    plt.plot(range(1, len(iteration_history) + 1), iteration_history, 
             'b-', linewidth=2.5, marker='o', markersize=4)
    plt.xlabel('İterasyon', fontsize=14, fontweight='bold')
    plt.ylabel('En İyi Mesafe (km)', fontsize=14, fontweight='bold')
    plt.title('ACO Algoritması Yakınsama Grafiği\nAnkara Göletleri Su Numunesi Toplama Rotası', 
              fontsize=16, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # İstatistik bilgileri ekle
    best_distance = min(iteration_history)
    worst_distance = max(iteration_history)
    improvement = ((worst_distance - best_distance) / worst_distance * 100)
    
    stats_text = f'En İyi: {best_distance:.2f} km\nİyileştirme: {improvement:.1f}%'
    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=11, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    try:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Yakınsama grafiği {save_path} dosyasına kaydedildi.")
        plt.close()
        return save_path
    except Exception as e:
        print(f"⚠️ Grafik kaydedilemedi: {e}")
        return None

def create_distance_heatmap(distance_matrix, location_names):
    """
    Mesafe matrisini ısı haritası olarak görselleştirir.
    
    Parameters:
    -----------
    distance_matrix : numpy.ndarray
        Mesafe matrisi
    location_names : list
        Lokasyon isimleri
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Isı haritası
    """
    # Kısa isimler oluştur (ilk 20 karakter)
    short_names = [name[:20] + '...' if len(name) > 20 else name 
                   for name in location_names]
    
    fig = go.Figure(data=go.Heatmap(
        z=distance_matrix,
        x=short_names,
        y=short_names,
        colorscale='RdYlGn_r',
        text=np.round(distance_matrix, 1),
        texttemplate='%{text} km',
        textfont={"size": 8},
        colorbar=dict(title="Mesafe (km)")
    ))
    
    fig.update_layout(
        title='Lokasyonlar Arası Mesafe Matrisi',
        xaxis_title='Hedef Lokasyon',
        yaxis_title='Başlangıç Lokasyonu',
        height=600,
        width=700
    )
    
    return fig

def display_route_details(route_indices, location_names, distance_matrix):
    """
    Rota detaylarını tablo formatında döndürür.
    
    Parameters:
    -----------
    route_indices : list
        Rota indeksleri
    location_names : list
        Lokasyon isimleri
    distance_matrix : numpy.ndarray
        Mesafe matrisi
    
    Returns:
    --------
    list of dict
        Her adım için bilgiler
    """
    route_details = []
    total_distance = 0
    
    for i in range(len(route_indices)):
        current_idx = route_indices[i]
        next_idx = route_indices[(i + 1) % len(route_indices)]
        
        current_name = location_names[current_idx]
        next_name = location_names[next_idx]
        
        segment_distance = distance_matrix[current_idx][next_idx]
        total_distance += segment_distance
        
        route_details.append({
            'Adım': i + 1,
            'Başlangıç': current_name,
            'Hedef': next_name,
            'Mesafe (km)': round(segment_distance, 2)
        })
    
    return route_details, total_distance
