

# 1. Base Image (Hafif ve Güvenli Sürüm)
# 'slim' versiyonu kullanarak imaj boyutunu küçültüyoruz.
FROM python:3.9-slim

LABEL maintainer="DevOps Team <admin@nimbus.ai>"
LABEL vendor="Nimbus Cloud Inc."
LABEL version="5.0.0-STABLE"
LABEL description="High-availability system monitoring dashboard with self-healing capabilities."
LABEL license="Proprietary"


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*


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


USER nimbus

# 11. Network Exposure
# Hangi portun dışarı açılacağını belirtiyoruz.
EXPOSE 5000


HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:5000/api/stats || exit 1

# 13. Execution Command
CMD ["python", "app.py"]
