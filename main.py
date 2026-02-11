"""
Network Monitoring Application
Ağ İzleme Uygulaması - Ana Program
"""
import sys
from network_scanner import NetworkScanner
from excel_exporter import ExcelExporter


def print_banner():
    """Uygulama başlığını yazdırır"""
    print("=" * 60)
    print("     AĞ İZLEME UYGULAMASI - NETWORK MONITORING APP")
    print("=" * 60)
    print()


def get_ip_block():
    """Kullanıcıdan IP bloğu girişi alır"""
    print("IP Bloğu Örnekleri:")
    print("  - 192.168.1.0/24  (192.168.1.1 - 192.168.1.254)")
    print("  - 10.0.0.0/24     (10.0.0.1 - 10.0.0.254)")
    print("  - 172.16.0.0/24   (172.16.0.1 - 172.16.0.254)")
    print()
    
    while True:
        ip_block = input("Taranacak IP bloğunu girin (CIDR formatında): ").strip()
        if ip_block:
            return ip_block
        print("Geçerli bir IP bloğu girin!")


def get_filter_options():
    """Kullanıcıdan filtreleme seçeneklerini alır"""
    print("\nFiltreleme seçenekleri:")
    print("1. Hostname'e göre filtrele")
    print("2. Açık porta göre filtrele")
    print("3. Filtreleme yapma")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == "1":
        keyword = input("Aranacak hostname kelimesini girin: ").strip()
        return {"keyword": keyword}
    elif choice == "2":
        try:
            port = int(input("Aranacak port numarasını girin: ").strip())
            return {"port": port}
        except ValueError:
            print("Geçersiz port numarası!")
            return {}
    
    return {}


def display_results(results):
    """Tarama sonuçlarını ekrana yazdırır"""
    if not results:
        print("\nHiç aktif host bulunamadı!")
        return
    
    print("\n" + "=" * 80)
    print(f"{'IP Adresi':<15} {'Hostname':<30} {'Durum':<10} {'Açık Portlar'}")
    print("=" * 80)
    
    for result in results:
        print(f"{result['ip']:<15} {result['hostname']:<30} "
              f"{result['status']:<10} {result['open_ports']}")
    
    print("=" * 80)
    print(f"Toplam: {len(results)} aktif host")
    print()


def main():
    """Ana program fonksiyonu"""
    print_banner()
    
    # IP bloğunu al
    ip_block = get_ip_block()
    
    # Tarayıcıyı oluştur ve taramayı başlat
    scanner = NetworkScanner(timeout=1)
    results = scanner.scan_network(ip_block)
    
    if not results:
        print("\nHiç aktif host bulunamadı. Program sonlandırılıyor.")
        return
    
    # Sonuçları göster
    display_results(results)
    
    # Filtreleme seçenekleri
    filter_opts = get_filter_options()
    
    if filter_opts:
        filtered_results = scanner.filter_results(
            keyword=filter_opts.get('keyword'),
            port=filter_opts.get('port')
        )
        print(f"\nFiltreleme sonrası {len(filtered_results)} host bulundu.")
        display_results(filtered_results)
        results = filtered_results
    
    # Excel'e aktarma
    export_choice = input("\nSonuçları Excel'e aktarmak ister misiniz? (E/H): ").strip().upper()
    
    if export_choice == 'E':
        filename = input("Dosya adı girin (örn: sonuclar.xlsx): ").strip()
        
        if not filename:
            filename = "network_scan_results.xlsx"
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        exporter = ExcelExporter()
        exporter.export(results, filename, ip_block)
    
    print("\nProgram tamamlandı. İyi günler!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Beklenmeyen hata: {e}")
        sys.exit(1)
