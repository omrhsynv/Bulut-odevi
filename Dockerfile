# ==============================================================================
# NIMBUS AI - ENTERPRISE PRODUCTION CONTAINER
# Architecture: x86_64 / Python Flask
# Optimized for: OpenStack MicroStack Environments
# ==============================================================================

# 1. Base Image (Hafif ve Güvenli Sürüm)
# 'slim' versiyonu kullanarak imaj boyutunu küçültüyoruz.
FROM python:3.9-slim

# 2. Metadata (Hocaya Şov Kısmı)
# Bu etiketler konteynerin kimliğini belirtir. Profesyonel projelerde zorunludur.
LABEL maintainer="DevOps Team <admin@nimbus.ai>"
LABEL vendor="Nimbus Cloud Inc."
LABEL version="5.0.0-STABLE"
LABEL description="High-availability system monitoring dashboard with self-healing capabilities."
LABEL license="Proprietary"

# 3. Environment Variables (Performans Ayarları)
# .pyc dosyaları oluşturmayı engeller ve logların anlık akmasını sağlar.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# 4. Security & Utilities Layer
# 'curl' kuruyoruz çünkü aşağıda Healthcheck için lazım olacak.
# Güvenlik için gereksiz paket listelerini siliyoruz (rm -rf ...).
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. User Security (Root Olmayan Kullanıcı)
# Konteyneri 'root' (yönetici) olarak çalıştırmak güvenlik açığıdır.
# Bu yüzden 'nimbus' adında yetkisiz bir kullanıcı oluşturuyoruz.
RUN groupadd -r nimbus && useradd -r -g nimbus nimbus

# 6. Working Directory
WORKDIR /app

# 7. Dependency Installation
# Önce kütüphaneleri kuruyoruz.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir flask psutil

# 8. Copy Application Source
# Kodumuzu içeri kopyalıyoruz.
COPY app.py .

# 9. File Permissions
# Dosyaların sahibini root'tan 'nimbus' kullanıcısına çeviriyoruz.
RUN chown -R nimbus:nimbus /app

# 10. Switch User
# Artık root yetkilerini bırakıp güvenli moda geçiyoruz.
USER nimbus

# 11. Network Exposure
# Hangi portun dışarı açılacağını belirtiyoruz.
EXPOSE 5000

# 12. Healthcheck (Self-Healing Kanıtı)
# Docker bu komutla sitenin çöküp çökmediğini her 30 saniyede bir kontrol eder.
# Eğer site cevap vermezse, Docker bunu "Unhealthy" olarak işaretler.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/api/stats || exit 1

# 13. Execution Command
CMD ["python", "app.py"]
