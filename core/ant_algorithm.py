"""
Karınca Kolonisi Optimizasyonu (Ant Colony Optimization - ACO) Algoritması
Gezgin Satıcı Problemi (TSP) için implementasyon
"""

import numpy as np
import random

class AntColonyOptimizer:
    """
    Karınca Kolonisi Algoritması ile TSP çözümü
    """
    
    def __init__(self, distance_matrix, num_ants=50, num_iterations=100, 
                 alpha=1.0, beta=2.0, evaporation_rate=0.5, Q=100):
        """
        Parameters:
        -----------
        distance_matrix : numpy.ndarray
            Şehirler arası mesafe matrisi
        num_ants : int
            Her iterasyonda kullanılacak karınca sayısı
        num_iterations : int
            Algoritmanın kaç iterasyon çalışacağı
        alpha : float
            Feromon izinin önem derecesi
        beta : float
            Mesafe bilgisinin (sezgisel) önem derecesi
        evaporation_rate : float
            Feromon buharlaşma oranı (0-1 arası)
        Q : float
            Feromon yoğunluğu sabiti
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        
        # Feromon matrisi - başlangıçta tüm kenarlar eşit feromon içerir
        self.pheromone = np.ones((self.num_cities, self.num_cities)) / self.num_cities
        
        # En iyi çözümü saklamak için
        self.best_path = None
        self.best_distance = float('inf')
        
        # İterasyon geçmişi
        self.iteration_best_distances = []
        
    def calculate_path_distance(self, path):
        """
        Verilen rotanın toplam mesafesini hesaplar.
        
        Parameters:
        -----------
        path : list
            Ziyaret sırası [0, 3, 1, 2, ...]
        
        Returns:
        --------
        float
            Toplam mesafe
        """
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distance_matrix[path[i]][path[i + 1]]
        # Başlangıç noktasına dönüş
        distance += self.distance_matrix[path[-1]][path[0]]
        return distance
    
    def construct_solution(self):
        """
        Bir karınca için olasılıksal olarak rota oluşturur.
        
        Returns:
        --------
        list
            Oluşturulan rota
        """
        # Rastgele başlangıç şehri (genellikle 0)
        current_city = 0
        unvisited = list(range(1, self.num_cities))
        path = [current_city]
        
        while unvisited:
            # Bir sonraki şehri seç
            next_city = self._select_next_city(current_city, unvisited)
            path.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city
        
        return path
    
    def _select_next_city(self, current_city, unvisited):
        """
        Feromon ve mesafe bilgisine göre bir sonraki şehri seçer.
        
        Parameters:
        -----------
        current_city : int
            Şu anki şehir
        unvisited : list
            Henüz ziyaret edilmemiş şehirler
        
        Returns:
        --------
        int
            Seçilen şehir
        """
        pheromone_values = np.array([self.pheromone[current_city][city] for city in unvisited])
        
        # Mesafe bilgisi (heuristic) - mesafe ne kadar kısaysa o kadar iyi
        # Sıfır mesafeyi önlemek için küçük bir epsilon ekle
        heuristic_values = np.array([
            1.0 / (self.distance_matrix[current_city][city] + 1e-10) 
            for city in unvisited
        ])
        
        # Olasılık hesaplama
        probabilities = (pheromone_values ** self.alpha) * (heuristic_values ** self.beta)
        probabilities = probabilities / probabilities.sum()
        
        # Rulet tekerleği seçimi
        next_city = np.random.choice(unvisited, p=probabilities)
        
        return next_city
    
    def update_pheromones(self, all_paths, all_distances):
        """
        Tüm karıncaların rotalarına göre feromon matrisini günceller.
        
        Parameters:
        -----------
        all_paths : list of lists
            Tüm karıncaların rotaları
        all_distances : list of floats
            Tüm rotaların mesafeleri
        """
        # Buharlaşma
        self.pheromone *= (1 - self.evaporation_rate)
        
        # Her karıncanın katkısı
        for path, distance in zip(all_paths, all_distances):
            # Kısa rotalar daha fazla feromon bırakır
            pheromone_deposit = self.Q / distance
            
            # Rotadaki her kenara feromon ekle
            for i in range(len(path) - 1):
                self.pheromone[path[i]][path[i + 1]] += pheromone_deposit
                self.pheromone[path[i + 1]][path[i]] += pheromone_deposit
            
            # Başlangıç noktasına dönüş
            self.pheromone[path[-1]][path[0]] += pheromone_deposit
            self.pheromone[path[0]][path[-1]] += pheromone_deposit
    
    def optimize(self, verbose=True):
        """
        ACO algoritmasını çalıştırır.
        
        Parameters:
        -----------
        verbose : bool
            İlerleme bilgisi yazdırılsın mı
        
        Returns:
        --------
        tuple
            (best_path, best_distance, iteration_history)
        """
        for iteration in range(self.num_iterations):
            # Tüm karıncalar için rota oluştur
            all_paths = []
            all_distances = []
            
            for ant in range(self.num_ants):
                path = self.construct_solution()
                distance = self.calculate_path_distance(path)
                
                all_paths.append(path)
                all_distances.append(distance)
                
                # En iyi çözümü güncelle
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path.copy()
            
            # Feromonları güncelle
            self.update_pheromones(all_paths, all_distances)
            
            # Bu iterasyondaki en iyi mesafeyi kaydet
            iteration_best = min(all_distances)
            self.iteration_best_distances.append(self.best_distance)
            
            if verbose and (iteration + 1) % 10 == 0:
                print(f"İterasyon {iteration + 1}/{self.num_iterations} - "
                      f"En iyi mesafe: {self.best_distance:.2f} km")
        
        if verbose:
            print(f"\nOptimizasyon tamamlandı!")
            print(f"En iyi mesafe: {self.best_distance:.2f} km")
        
        return self.best_path, self.best_distance, self.iteration_best_distances
    
    def get_results(self):
        """
        Optimizasyon sonuçlarını döndürür.
        
        Returns:
        --------
        dict
            Sonuç bilgileri
        """
        return {
            'best_path': self.best_path,
            'best_distance': self.best_distance,
            'iteration_history': self.iteration_best_distances,
            'num_iterations': self.num_iterations,
            'num_ants': self.num_ants,
            'alpha': self.alpha,
            'beta': self.beta,
            'evaporation_rate': self.evaporation_rate
        }
