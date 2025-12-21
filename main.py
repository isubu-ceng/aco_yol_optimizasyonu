"""
Karınca Kolonisi Algoritması ile Yol Optimizasyonu
Ankara Göletleri Su Numunesi Toplama Rotası
Streamlit Web Uygulaması

Öğrenci: Samet POLAT (2112729005)
Ders: BLG-307 Yapay Zeka Sistemleri
"""

import streamlit as st
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import time

# Proje modülleri
from data.coordinates import get_all_locations, get_location_names, get_coordinates_list
from core.haversine import create_haversine_matrix
from core.matrix_utils import create_distance_matrix_with_google
from core.ant_algorithm import AntColonyOptimizer
from visual.plotting import (
    create_route_map, 
    plot_convergence,
    plot_convergence_matplotlib,
    save_map_as_png,
    display_route_details,
    create_distance_heatmap
)
from config import DEFAULT_ACO_PARAMS, PAGE_CONFIG
import os

# Sayfa konfigürasyonu
st.set_page_config(**PAGE_CONFIG)

# Başlık ve bilgi
st.title("🐜 Karınca Kolonisi Algoritması ile Yol Optimizasyonu")
st.markdown("### Ankara Göletleri Su Numunesi Toplama Rotası")

st.markdown("""
**Senaryo:** Çevre Bakanlığı birimlerinin Ankara'daki 10 farklı göletten su numunesi toplarken 
kullanacağı en kısa rotayı bulmak için Karınca Kolonisi Algoritması (ACO) kullanılmaktadır.
""")

st.markdown("---")

# Sidebar - Parametre Ayarları
st.sidebar.header("⚙️ Algoritma Parametreleri")

# ACO parametreleri
num_ants = st.sidebar.slider(
    "Karınca Sayısı",
    min_value=10,
    max_value=200,
    value=DEFAULT_ACO_PARAMS['num_ants'],
    step=10,
    help="Her iterasyonda çalışan karınca sayısı"
)

num_iterations = st.sidebar.slider(
    "İterasyon Sayısı",
    min_value=50,
    max_value=500,
    value=DEFAULT_ACO_PARAMS['num_iterations'],
    step=10,
    help="Algoritmanın kaç iterasyon çalışacağı"
)

alpha = st.sidebar.slider(
    "Alpha (α) - Feromon Önem Derecesi",
    min_value=0.1,
    max_value=5.0,
    value=DEFAULT_ACO_PARAMS['alpha'],
    step=0.1,
    help="Feromon izinin ne kadar önemli olduğu"
)

beta = st.sidebar.slider(
    "Beta (β) - Mesafe Önem Derecesi",
    min_value=0.1,
    max_value=10.0,
    value=DEFAULT_ACO_PARAMS['beta'],
    step=0.1,
    help="Mesafe bilgisinin ne kadar önemli olduğu"
)

evaporation_rate = st.sidebar.slider(
    "Buharlaşma Oranı (ρ)",
    min_value=0.1,
    max_value=0.9,
    value=DEFAULT_ACO_PARAMS['evaporation_rate'],
    step=0.05,
    help="Feromon buharlaşma hızı (0-1 arası)"
)

st.sidebar.markdown("---")

# Mesafe hesaplama yöntemi
distance_method = st.sidebar.radio(
    "Mesafe Hesaplama Yöntemi",
    ["Google Maps API (Gerçek Yol)", "Haversine (Kuş Uçuşu)"],
    index=0,
    help="Google Maps API gerçek yol mesafelerini, Haversine kuş uçuşu mesafeyi hesaplar"
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Öğrenci:** Samet POLAT  
**No:** 2112729005  
**Ders:** BLG-307 Yapay Zeka Sistemleri
""")

# Ana içerik
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 Ankara Göletleri")
    locations = get_all_locations()
    location_names = get_location_names()
    
    # Lokasyon listesi
    location_df = pd.DataFrame([
        {"Sıra": i, "Gölet Adı": name, "Adres": locations[name].get('adres', '')}
        for i, name in enumerate(location_names, 1)
    ])
    st.dataframe(location_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🔧 Algoritma Bilgileri")
    st.markdown(f"""
    - **Karınca Sayısı:** {num_ants}
    - **İterasyon Sayısı:** {num_iterations}
    - **Alpha (α):** {alpha}
    - **Beta (β):** {beta}
    - **Buharlaşma Oranı (ρ):** {evaporation_rate}
    - **Mesafe Yöntemi:** {'Google Maps API' if 'Google' in distance_method else 'Haversine'}
    """)

st.markdown("---")

# Algoritma Çalıştır Butonu
if st.button("🚀 Algoritmayı Çalıştır", type="primary", use_container_width=True):
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # 1. Mesafe matrisini oluştur
        status_text.text("📊 Mesafe matrisi oluşturuluyor...")
        progress_bar.progress(10)
        
        if "Google" in distance_method:
            # Google Maps API kullan
            try:
                api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
                distance_matrix, duration_matrix, loc_names = create_distance_matrix_with_google(
                    api_key, locations
                )
                st.success("✅ Google Maps API ile gerçek yol mesafeleri alındı!")
            except Exception as e:
                st.error(f"❌ Google Maps API hatası: {str(e)}")
                st.warning("⚠️ Haversine formülü ile kuş uçuşu mesafeler kullanılacak.")
                coordinates = get_coordinates_list()
                distance_matrix = create_haversine_matrix(coordinates)
                loc_names = location_names
        else:
            # Haversine formülü kullan
            coordinates = get_coordinates_list()
            distance_matrix = create_haversine_matrix(coordinates)
            loc_names = location_names
            st.info("ℹ️ Haversine formülü ile kuş uçuşu mesafeler kullanıldı.")
        
        progress_bar.progress(30)
        
        # 2. ACO algoritmasını çalıştır
        status_text.text("🐜 Karınca Kolonisi Algoritması çalıştırılıyor...")
        
        aco = AntColonyOptimizer(
            distance_matrix=distance_matrix,
            num_ants=num_ants,
            num_iterations=num_iterations,
            alpha=alpha,
            beta=beta,
            evaporation_rate=evaporation_rate,
            Q=DEFAULT_ACO_PARAMS['Q']
        )
        
        # Optimizasyonu çalıştır
        best_path, best_distance, iteration_history = aco.optimize(verbose=False)
        
        progress_bar.progress(80)
        status_text.text("📈 Sonuçlar görselleştiriliyor...")
        
        # Figure klasörünü oluştur
        os.makedirs('figure', exist_ok=True)
        
        # Görselleri kaydet
        try:
            # Yakınsama grafiğini kaydet
            plot_convergence_matplotlib(iteration_history, save_path='figure/convergence.png')
            
            # Haritayı oluştur ve kaydet
            route_map = create_route_map(locations, best_path, loc_names)
            save_map_as_png(route_map, filename='figure/rota.html')
            
            st.success("💾 Görselleştirmeler figure/ klasörüne kaydedildi!")
        except Exception as e:
            st.warning(f"⚠️ Görsel kaydetme hatası: {e}")
        
        # 3. Sonuçları göster
        progress_bar.progress(100)
        status_text.text("✅ Optimizasyon tamamlandı!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"🎉 **En kısa rota bulundu! Toplam mesafe: {best_distance:.2f} km**")
        
        # Sonuç bölümleri
        st.markdown("---")
        st.header("📊 Optimizasyon Sonuçları")
        
        # Tab'lar oluştur
        tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Rota Haritası", "📈 Yakınsama Grafiği", "📋 Rota Detayları", "🔥 Mesafe Matrisi"])
        
        with tab1:
            st.subheader("Optimal Rota Haritası")
            route_map = create_route_map(locations, best_path, loc_names)
            folium_static(route_map, width=800, height=600)
            
            # Rota sırası
            st.markdown("**Ziyaret Sırası:**")
            route_order = " → ".join([f"{i+1}. {loc_names[idx]}" for i, idx in enumerate(best_path)])
            route_order += f" → {loc_names[best_path[0]]}"
            st.info(route_order)
        
        with tab2:
            st.subheader("Algoritma Yakınsama Grafiği")
            convergence_fig = plot_convergence(iteration_history)
            st.plotly_chart(convergence_fig, use_container_width=True)
            
            st.markdown(f"""
            **Yakınsama İstatistikleri:**
            - Başlangıç Mesafesi: {iteration_history[0]:.2f} km
            - Final Mesafe: {iteration_history[-1]:.2f} km
            - İyileştirme: {((iteration_history[0] - iteration_history[-1]) / iteration_history[0] * 100):.1f}%
            """)
        
        with tab3:
            st.subheader("Detaylı Rota Bilgileri")
            route_details, total_distance = display_route_details(best_path, loc_names, distance_matrix)
            
            route_df = pd.DataFrame(route_details)
            st.dataframe(route_df, use_container_width=True, hide_index=True)
            
            st.metric("Toplam Mesafe", f"{total_distance:.2f} km")
            
            # Tahmini süre (ortalama 50 km/saat)
            estimated_time = (total_distance / 50) * 60  # dakika
            st.metric("Tahmini Süre", f"{estimated_time:.0f} dakika (~{estimated_time/60:.1f} saat)")
        
        with tab4:
            st.subheader("Lokasyonlar Arası Mesafe Matrisi")
            heatmap_fig = create_distance_heatmap(distance_matrix, loc_names)
            st.plotly_chart(heatmap_fig, use_container_width=True)
        
        # İndirme butonları
        st.markdown("---")
        st.subheader("💾 Sonuçları İndir")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rota CSV
            route_csv = pd.DataFrame(route_details).to_csv(index=False)
            st.download_button(
                label="📥 Rota Detaylarını İndir (CSV)",
                data=route_csv,
                file_name="ankara_goletleri_rota.csv",
                mime="text/csv"
            )
        
        with col2:
            # Mesafe matrisi CSV
            matrix_csv = pd.DataFrame(
                distance_matrix, 
                index=loc_names, 
                columns=loc_names
            ).to_csv()
            st.download_button(
                label="📥 Mesafe Matrisini İndir (CSV)",
                data=matrix_csv,
                file_name="mesafe_matrisi.csv",
                mime="text/csv"
            )
        
    except Exception as e:
        st.error(f"❌ Bir hata oluştu: {str(e)}")
        st.exception(e)

else:
    st.info("👆 Yukarıdaki butona tıklayarak algoritmayı başlatın.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><strong>Karınca Kolonisi Algoritması ile Yol Optimizasyonu</strong></p>
    <p>Samet POLAT (2112729005) - BLG-307 Yapay Zeka Sistemleri</p>
    <p>Bartın Üniversitesi - Bilgisayar Mühendisliği</p>
</div>
""", unsafe_allow_html=True)
