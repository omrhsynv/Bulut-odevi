**Ders:** ISE 465 - Bulut Bilişim | **Dönem:** 2025-2026 Güz

## 1. Proje ve Uygulama Açıklaması
**Uygulama Adı:** Nimbus AI Enterprise Dashboard
**Amaç:** Bu proje, mikroservis mimarisine uygun, kendi kendini iyileştirebilen (self-healing) ve yüksek erişilebilirliğe sahip bir bulut izleme (monitoring) platformunun simülasyonunu gerçekleştirmektir.
**Seçilen Uygulama:** Python Flask tabanlı, CPU/RAM metriklerini görselleştiren, stres testi ve çökme simülasyonları yapabilen interaktif bir web uygulaması.

## 2. Kullanılan Teknolojiler ve Bulut Platformu
* **Bulut Sağlayıcı:** OpenStack (MicroStack) - IaaS (Infrastructure as a Service) olarak kullanıldı.
* **Sanallaştırma:** Ubuntu 22.04 LTS Sanal Makine (OpenStack üzerinde).
* **Konteynerizasyon:** Docker & Dockerfile (Pro sürüm).
* **Yazılım Dili:** Python (Flask), HTML5/CSS3 (Custom Framework), JavaScript (Canvas API).
* **Metrik Takibi:** Psutil kütüphanesi.

## 3. Uygulama Mimari Şeması
Proje aşağıdaki katmanlardan oluşmaktadır:
1.  **İstemci (Client):** Web Tarayıcısı.
2.  **Bulut Katmanı:** OpenStack (MicroStack) Gateway.
3.  **Sanal Sunucu:** Ubuntu Instance (IP: 10.20.20.45).
4.  **Uygulama Katmanı:** Docker Konteyneri (nimbus-ultimate-v5).
    * *Restart Policy:* Always (Self-Healing için).

## 4. Adım Adım Kurulum ve Dağıtım Süreci
1.  **OpenStack Kurulumu:** Yerel makineye `microstack` (beta) kurulumu yapıldı ve `init` ile başlatıldı.
2.  **Sanal Makine (Instance):** OpenStack Dashboard üzerinden Ubuntu 22.04 imajı, m1.small flavor ile başlatıldı.
3.  **Ağ Ayarları:** SSH (22) ve HTTP (80) portları için Security Group kuralları tanımlandı. Floating IP atandı.
4.  **Docker Ortamı:** Instance içine bağlanılarak Docker Engine kuruldu.
5.  **Uygulama Geliştirme:** `app.py` ve `Dockerfile` sunucu üzerinde oluşturuldu.
6.  **Build & Deploy:**
    ```bash
    sudo docker build -t nimbus-ultimate:v5 .
    sudo docker run -d -p 80:5000 --restart always --name monitor nimbus-ultimate:v5
    ```

## 5. Otomasyon Kod Parçacıkları (Dockerfile)
Projede "Enterprise-Grade" bir Dockerfile kullanılmıştır. Güvenlik ve sağlık kontrolleri içerir:

```dockerfile
FROM python:3.9-slim
LABEL maintainer="DevOps Team"
# Güvenlik için root olmayan kullanıcı
RUN useradd -m nimbus
WORKDIR /app
COPY app.py .
# Self-Healing Sağlık Kontrolü
HEALTHCHECK --interval=30s CMD curl --fail http://localhost:5000/api/stats || exit 1
CMD ["python", "app.py"]
