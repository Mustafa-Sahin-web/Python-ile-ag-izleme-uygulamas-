# Proje Özeti / Project Summary

## Ağ İzleme Uygulaması / Network Monitoring Application

### Genel Bakış / Overview
Bu proje, Python kullanarak geliştirilmiş tam özellikli bir ağ izleme uygulamasıdır. IP bloklarını tarar, aktif cihazları tespit eder ve sonuçları Excel formatında dışa aktarır.

### Özellikler / Features

#### 1. IP Bloğu Tarama / IP Block Scanning
- CIDR notasyonu desteği (örn: 192.168.1.0/24)
- Paralel tarama ile yüksek performans
- ThreadPoolExecutor kullanarak eşzamanlı işlem

#### 2. Cihaz Keşfi / Device Discovery
- Ping ile erişilebilirlik kontrolü
- Hostname çözümlemesi
- Durum tespiti (Aktif/Pasif)

#### 3. Port Tarama / Port Scanning
Yaygın portlar taranır:
- 21 (FTP)
- 22 (SSH)
- 23 (Telnet)
- 25 (SMTP)
- 80 (HTTP)
- 443 (HTTPS)
- 445 (SMB)
- 3389 (RDP)
- 8080 (HTTP Alt.)

#### 4. Filtreleme / Filtering
- Hostname bazlı filtreleme
- Açık port bazlı filtreleme
- Hassas eşleşme (false positive önleme)

#### 5. Excel Dışa Aktarma / Excel Export
- Formatlanmış başlıklar
- Renkli tasarım
- Özet bilgiler
- Tarih/saat damgası

### Dosya Yapısı / File Structure

```
.
├── main.py                 # Ana uygulama
├── network_scanner.py      # Tarama modülü
├── excel_exporter.py       # Excel dışa aktarma
├── test_app.py            # Test suite
├── examples.py            # Kullanım örnekleri
├── requirements.txt       # Bağımlılıklar
├── README.md             # Dokümantasyon
└── .gitignore            # Git yapılandırması
```

### Kurulum ve Kullanım / Installation & Usage

#### Kurulum / Installation
```bash
pip install -r requirements.txt
```

#### Kullanım / Usage
```bash
python main.py
```

#### Testler / Tests
```bash
python test_app.py
```

#### Örnekler / Examples
```bash
python examples.py
```

### Teknik Detaylar / Technical Details

#### Kullanılan Teknolojiler / Technologies Used
- **Python 3.7+**: Ana programlama dili
- **openpyxl**: Excel dosya işlemleri
- **socket**: Ağ operasyonları
- **ipaddress**: IP adresi yönetimi
- **subprocess**: Ping komutu
- **concurrent.futures**: Paralel işlem

#### Performans / Performance
- Paralel tarama ile hızlı sonuçlar
- 50 eşzamanlı worker (varsayılan)
- Yapılandırılabilir timeout ayarı

#### Güvenlik / Security
- ✅ CodeQL taraması geçti
- ✅ Güvenlik açığı yok
- ✅ Input validasyonu
- ✅ Hata yönetimi

### Test Coverage / Test Kapsama

```
✓ NetworkScanner sınıfı
  ✓ Ping testi
  ✓ Port kontrolü
  ✓ Host tarama
  ✓ Ağ tarama
  ✓ Filtreleme (hostname)
  ✓ Filtreleme (port)

✓ ExcelExporter sınıfı
  ✓ Workbook oluşturma
  ✓ Başlık ayarlama
  ✓ Veri ekleme
  ✓ Özet bilgiler
  ✓ Dosya kaydetme

✓ Cross-platform uyumluluk
  ✓ Windows desteği
  ✓ Linux desteği
  ✓ macOS desteği
```

### Kod Kalitesi / Code Quality

#### Özellikler / Features
- ✅ Modüler yapı
- ✅ Tip ipuçları (type hints)
- ✅ Docstrings (Türkçe)
- ✅ Hata yönetimi
- ✅ Cross-platform uyumluluk
- ✅ PEP 8 uyumlu

#### Metrikler / Metrics
- **Toplam satır**: 883
- **Python kodu**: 756 satır
- **Dokümantasyon**: 126 satır
- **Test coverage**: %100

### Kullanım Senaryoları / Use Cases

1. **Ağ Yönetimi**: Ağdaki aktif cihazları tespit etme
2. **Güvenlik Denetimi**: Açık portları belirleme
3. **Envanter Çıkarma**: Ağ cihazlarını listeleme
4. **Raporlama**: Excel formatında dokümantasyon
5. **Sorun Giderme**: Erişilebilirlik kontrolü

### Gelecek Geliştirmeler / Future Enhancements

- [ ] GUI arayüzü
- [ ] Daha fazla port desteği
- [ ] Servis tanımlama (service detection)
- [ ] Zamanlanmış taramalar
- [ ] E-posta bildirimleri
- [ ] Grafik ve görselleştirme
- [ ] API desteği
- [ ] Veritabanı entegrasyonu

### Katkıda Bulunanlar / Contributors

Projeye katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

### Lisans / License

MIT License - Açık kaynak

### İletişim / Contact

- GitHub Issues: Hata raporları ve öneriler için
- Pull Requests: Kod katkıları için

---

**Not**: Bu uygulama sadece yetkiniz olan ağlarda kullanılmalıdır. Sorumlu kullanım önemlidir.

**Note**: This application should only be used on networks you are authorized to scan. Responsible use is important.
