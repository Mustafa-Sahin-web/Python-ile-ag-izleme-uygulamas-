# Python ile Ağ İzleme Uygulaması / Network Monitoring Application

Python kullanarak geliştirilmiş ağ izleme uygulaması. Bu uygulama IP bloklarını tarayarak aktif cihazları tespit eder, filtreleme yapar ve sonuçları Excel dosyasına aktarır.

## Özellikler

- ✅ IP bloğu bazında ağ tarama (CIDR notasyonu)
- ✅ Ping ile cihaz aktiflik kontrolü
- ✅ Yaygın portların taranması (21, 22, 23, 25, 80, 443, 445, 3389, 8080)
- ✅ Hostname tespiti
- ✅ Sonuçları filtreleme (hostname veya port bazında)
- ✅ Excel'e dışa aktarma
- ✅ Paralel tarama (hızlı sonuçlar)

## Gereksinimler

- Python 3.7 veya üzeri
- openpyxl kütüphanesi

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/Mustafa-Sahin-web/Python-ile-ag-izleme-uygulamas-.git
cd Python-ile-ag-izleme-uygulamas-
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

Uygulamayı çalıştırmak için:

```bash
python main.py
```

### Adım Adım Kullanım

1. **IP Bloğu Girişi**: Program başladığında, taramak istediğiniz IP bloğunu CIDR formatında girin.
   - Örnek: `192.168.1.0/24` (192.168.1.1 - 192.168.1.254 arası tüm IP'leri tarar)

2. **Tarama**: Uygulama otomatik olarak belirtilen IP bloğundaki tüm adresleri tarayacaktır.
   - Ping ile erişilebilirlik kontrolü
   - Hostname tespiti
   - Açık port taraması

3. **Filtreleme** (İsteğe bağlı):
   - Hostname'e göre: Belirli bir kelimeyi içeren cihazları filtreleyin
   - Porta göre: Belirli bir portu açık olan cihazları filtreleyin
   - Filtreleme yapmadan devam edebilirsiniz

4. **Excel'e Aktarma**: Sonuçları Excel dosyasına kaydetmek isterseniz, dosya adını belirtin.
   - Varsayılan: `network_scan_results.xlsx`

## Örnek Kullanım

```
============================================================
     AĞ İZLEME UYGULAMASI - NETWORK MONITORING APP
============================================================

IP Bloğu Örnekleri:
  - 192.168.1.0/24  (192.168.1.1 - 192.168.1.254)
  - 10.0.0.0/24     (10.0.0.1 - 10.0.0.254)
  - 172.16.0.0/24   (172.16.0.1 - 172.16.0.254)

Taranacak IP bloğunu girin (CIDR formatında): 192.168.1.0/24

192.168.1.0/24 bloğu taranıyor...
Toplam 254 adres taranacak.

İlerleme: 10/254 adres tarandı
  ✓ Aktif host bulundu: 192.168.1.1 (router.local)
İlerleme: 20/254 adres tarandı
  ✓ Aktif host bulundu: 192.168.1.5 (desktop-pc)
...

Tarama tamamlandı. Toplam 5 aktif host bulundu.
```

## Modüller

### network_scanner.py
Ağ tarama işlemlerini gerçekleştiren ana modül.

**Sınıf: NetworkScanner**
- `ping(ip)`: IP adresini ping ile kontrol eder
- `check_port(ip, port)`: Belirtilen portu kontrol eder
- `scan_common_ports(ip)`: Yaygın portları tarar
- `scan_host(ip)`: Tek bir hostu tarar
- `scan_network(ip_block)`: IP bloğunu tarar
- `filter_results(keyword, port)`: Sonuçları filtreler

### excel_exporter.py
Tarama sonuçlarını Excel formatında dışa aktaran modül.

**Sınıf: ExcelExporter**
- `create_workbook()`: Yeni Excel çalışma kitabı oluşturur
- `set_headers()`: Başlıkları ayarlar
- `add_data(results)`: Sonuçları ekler
- `add_summary(ip_block, total_hosts)`: Özet bilgileri ekler
- `export(results, filename, ip_block)`: Excel dosyasına aktarır

### main.py
Uygulamanın ana giriş noktası ve kullanıcı arayüzü.

## Güvenlik Notları

- Bu uygulamayı sadece yetkiniz olan ağlarda kullanın
- Ağ taraması bazı güvenlik sistemlerini tetikleyebilir
- Sorumlu kullanım önemlidir

## Lisans

Bu proje açık kaynak kodludur ve MIT lisansı altında dağıtılmaktadır.

## Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

## İletişim

Sorularınız için issue açabilirsiniz.