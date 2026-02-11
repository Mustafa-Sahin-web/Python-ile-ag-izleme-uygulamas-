import subprocess
import platform
import socket
import time
import os
import re
import msvcrt
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- RENK AYARLARI ---
class Renk:
    YESIL = '\033[92m'
    KIRMIZI = '\033[91m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    TURKUAZ = '\033[96m'
    BITIR = '\033[0m'

# --- KÜTÜPHANE KONTROLÜ VE YÜKLEME ---
def kutuphane_kontrol():
    global pd, EXCEL_DESTEGI
    try:
        import pandas as pd
        EXCEL_DESTEGI = True
    except ImportError:
        print(f"{Renk.SARI}[!] Excel kaydı için gerekli 'pandas' kütüphanesi eksik.{Renk.BITIR}")
        onay = input(f"{Renk.MAVI}Gerekli kütüphaneler otomatik yüklensin mi? (e/h): {Renk.BITIR}").lower()
        if onay == 'e':
            print(f"{Renk.TURKUAZ}Kütüphaneler yükleniyor, lütfen bekleyin...{Renk.BITIR}")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
                import pandas as pd
                EXCEL_DESTEGI = True
                print(f"{Renk.YESIL}✅ Kütüphaneler başarıyla yüklendi!{Renk.BITIR}\n")
                time.sleep(2)
            except Exception as e:
                print(f"{Renk.KIRMIZI}❌ Yükleme sırasında hata oluştu: {e}{Renk.BITIR}")
                EXCEL_DESTEGI = False
        else:
            print(f"{Renk.SARI}[!] Excel özelliği devre dışı bırakıldı.{Renk.BITIR}\n")
            EXCEL_DESTEGI = False

# Program başlamadan kütüphaneleri kontrol et
kutuphane_kontrol()

def kendi_ip_bul():
    """Bilgisayarın yerel ağdaki IP adresini öğrenir."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Kendi IP'mizi bir kez alalım
KENDI_IP = kendi_ip_bul()
kapalilari_goster = True

def cihaz_adi_bul(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Bilinmiyor"

def excele_aktar(veriler, filtre_adi):
    if not EXCEL_DESTEGI:
        print(f"\n{Renk.KIRMIZI}[HATA] Excel için kütüphaneler yüklü değil!{Renk.BITIR}")
        return
    if not veriler:
        print(f"\n{Renk.SARI}[UYARI] Kaydedilecek veri bulunamadı.{Renk.BITIR}")
        return

    zaman_damgasi = datetime.now().strftime("%H%M%S")
    dosya_adi = f"ag_raporu_{filtre_adi}_{zaman_damgasi}.xlsx"
    
    df = pd.DataFrame(veriler, columns=["IP Adresi", "Durum", "Cihaz Adi", "Zaman"])
    
    try:
        df.to_excel(dosya_adi, index=False)
        print(f"\n{Renk.YESIL}[KAYIT TAMAM] Dosya oluşturuldu: {dosya_adi}{Renk.BITIR}")
    except Exception as e:
        print(f"\n{Renk.KIRMIZI}[HATA] Kayıt yapılamadı: {e}{Renk.BITIR}")

def ping_at(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    komut = ["ping", param, "1", "-w", "800", ip]
    try:
        sonuc = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return ip, sonuc.returncode == 0, cihaz_adi_bul(ip) if sonuc.returncode == 0 else "Erisilemez"
    except:
        return ip, False, "Hata"

def girdi_dogrula():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    print(f"{Renk.TURKUAZ}=== AG PANEL YAPILANDIRMA ==={Renk.BITIR}")
    print(f"{Renk.SARI}Bilgisayarınızın IP Adresi: {KENDI_IP}{Renk.BITIR}\n")
    
    # --- 1. BLOK KONTROLÜ (Boş ve Geçersiz Giriş) ---
    while True:
        blog = input(f"{Renk.MAVI}IP Bloğu (Örn: 172.16.180): {Renk.BITIR}").strip()
        if not blog:
            print(f"{Renk.KIRMIZI}Hata: IP bloğu boş bırakılamaz!{Renk.BITIR}")
            continue
        parcalar = blog.split('.')
        if len(parcalar) == 3:
            try:
                if all(0 <= int(p) <= 255 for p in parcalar): break
            except ValueError: pass
        print(f"{Renk.KIRMIZI}Hata: Geçersiz blok! (0-255 arası 3 hane olmalı){Renk.BITIR}")

    # --- 2. BAŞLANGIÇ IP KONTROLÜ (Boş ve Sayı Girişi) ---
    while True:
        bas_input = input(f"{Renk.MAVI}Başlangıç IP (0-255): {Renk.BITIR}").strip()
        if not bas_input:
            print(f"{Renk.KIRMIZI}Hata: Başlangıç IP boş bırakılamaz!{Renk.BITIR}")
            continue
        try:
            bas = int(bas_input)
            if 0 <= bas <= 255: break
            print(f"{Renk.KIRMIZI}Hata: 0-255 arası bir değer girin!{Renk.BITIR}")
        except ValueError: print(f"{Renk.KIRMIZI}Sadece rakam girin!{Renk.BITIR}")

    # --- 3. BİTİŞ IP KONTROLÜ (Boş ve Mantık Kontrolü) ---
    while True:
        bit_input = input(f"{Renk.MAVI}Bitiş IP (0-255): {Renk.BITIR}").strip()
        if not bit_input:
            print(f"{Renk.KIRMIZI}Hata: Bitiş IP boş bırakılamaz!{Renk.BITIR}")
            continue
        try:
            bit = int(bit_input)
            if 0 <= bit <= 255:
                if bit >= bas: break
                else: print(f"{Renk.KIRMIZI}Hata: Bitiş IP, Başlangıçtan ({bas}) küçük olamaz!{Renk.BITIR}")
            else: print(f"{Renk.KIRMIZI}Hata: 0-255 arası bir değer girin!{Renk.BITIR}")
        except ValueError: print(f"{Renk.KIRMIZI}Sadece rakam girin!{Renk.BITIR}")

    # --- 4. SÜRE KONTROLÜ ---
    while True:
        try:
            sure_input = input(f"{Renk.MAVI}Tekrar Süresi (Saniye): {Renk.BITIR}").strip()
            if not sure_input:
                print(f"{Renk.KIRMIZI}Hata: Süre boş bırakılamaz!{Renk.BITIR}")
                continue
            sure = int(sure_input)
            if sure > 0: break
            print(f"{Renk.KIRMIZI}Hata: Süre 0'dan büyük olmalı!{Renk.BITIR}")
        except ValueError: print(f"{Renk.KIRMIZI}Geçersiz süre girişi!{Renk.BITIR}")
            
    return blog, bas, bit, sure

def monitor():
    global kapalilari_goster
    blog, bas, bit, bekleme = girdi_dogrula()

    while True:
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')
        zaman = datetime.now().strftime("%H:%M:%S")
        
        print(f"{Renk.SARI}[IZLEME] {blog}.{bas}-{bit} | SAAT: {zaman}{Renk.BITIR}")
        print(f"MOD: {'TÜM LİSTE' if kapalilari_goster else 'SADECE AKTİFLER'}")
        print("-" * 85)
        print(f"{'IP ADRESI':<30} | {'DURUM':<12} | {'SISTEM ADI'}")
        print("-" * 85)

        ip_listesi = [f"{blog}.{i}" for i in range(bas, bit + 1)]
        tum_sonuclar, aktifler, kapalilar = [], [], []
        ayakta = 0

        with ThreadPoolExecutor(max_workers=100) as executor:
            sonuclar = list(executor.map(ping_at, ip_listesi))

        for ip, durum, isim in sonuclar:
            ip_etiketi = f"{ip} (Sizin IP Adresiniz)" if ip == KENDI_IP else ip
            durum_metni = "ONLINE" if durum else "OFFLINE"
            veri = [ip, durum_metni, isim, zaman]
            tum_sonuclar.append(veri)
            
            if durum:
                print(f"{Renk.YESIL}{ip_etiketi:<30} | [OK] ONLINE | {isim}{Renk.BITIR}")
                aktifler.append(veri)
                ayakta += 1
            else:
                kapalilar.append(veri)
                if kapalilari_goster:
                    print(f"{Renk.KIRMIZI}{ip_etiketi:<30} | [!!] OFFLINE | -{Renk.BITIR}")

        print("-" * 85)
        print(f"OZET: {ayakta} Aktif | {len(ip_listesi)-ayakta} Kapalı.")
        print(f"\n{Renk.TURKUAZ}KAYIT: [T] Tümünü Kaydet | [A] Aktifleri Kaydet | [K] Kapalıları Kaydet")
        print(f"DIREKTIF: [P] Duraklat (İncelemek için) | [H] Gizle | [R] Yenile | [Q] Çıkış{Renk.BITIR}")

        bekle_bitis = time.time() + bekleme
        duraklatildi = False
        
        while time.time() < bekle_bitis or duraklatildi:
            if msvcrt.kbhit():
                tus = msvcrt.getch().decode().lower()
                if tus == 'p': 
                    duraklatildi = not duraklatildi
                    if duraklatildi: print(f"\n{Renk.TURKUAZ}>>> DURAKLATILDI. Yukarı çıkıp inceleyebilirsiniz. Devam için 'P' basın.{Renk.BITIR}")
                if tus == 't': excele_aktar(tum_sonuclar, "TUM_LISTE")
                if tus == 'a': excele_aktar(aktifler, "AKTIFLER")
                if tus == 'k': excele_aktar(kapalilar, "KAPALILAR")
                if tus == 'h':
                    kapalilari_goster = not kapalilari_goster
                    break 
                if tus == 'r': break
                if tus == 'q': return

            if not duraklatildi:
                kalan = int(bekle_bitis - time.time())
                print(f"Yeni tarama: {max(0, kalan)}sn... ('P' ile duraklat)    ", end='\r')
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nKapatıldı.")