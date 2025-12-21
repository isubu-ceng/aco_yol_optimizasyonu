# Python 3.11 slim imajını kullan
FROM python:3.11-slim

# Çalışma dizini oluştur
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Streamlit konfigürasyon dizini oluştur
RUN mkdir -p /root/.streamlit

# Streamlit config dosyası oluştur
RUN echo "\
[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > /root/.streamlit/config.toml

# Port'u aç
EXPOSE 8501

# Health check ekle
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Streamlit uygulamasını çalıştır
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
