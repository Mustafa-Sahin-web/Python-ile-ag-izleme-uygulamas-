#!/usr/bin/env python3
"""
Example usage script for network monitoring application
Demonstrates different features and use cases
"""
import tempfile
import os
from network_scanner import NetworkScanner
from excel_exporter import ExcelExporter


def example_1_basic_scan():
    """Example 1: Basic network scan of localhost"""
    print("\n" + "=" * 70)
    print("ÖRNEK 1: Temel Ağ Taraması (Localhost)")
    print("=" * 70)
    
    scanner = NetworkScanner(timeout=1)
    
    # Scan single IP (localhost as /32)
    print("\n127.0.0.1/32 bloğu taranıyor...")
    results = scanner.scan_network("127.0.0.1/32")
    
    if results:
        print(f"\n✓ {len(results)} aktif host bulundu:")
        for result in results:
            print(f"  - IP: {result['ip']}, Hostname: {result['hostname']}")
    
    return results


def example_2_filtering():
    """Example 2: Demonstrates filtering capabilities"""
    print("\n" + "=" * 70)
    print("ÖRNEK 2: Filtreleme Özellikleri")
    print("=" * 70)
    
    scanner = NetworkScanner()
    
    # Create sample data for demonstration
    scanner.results = [
        {
            'ip': '192.168.1.1',
            'hostname': 'router.local',
            'status': 'Aktif',
            'open_ports': '80, 443'
        },
        {
            'ip': '192.168.1.10',
            'hostname': 'server01.local',
            'status': 'Aktif',
            'open_ports': '22, 80, 443'
        },
        {
            'ip': '192.168.1.20',
            'hostname': 'workstation.local',
            'status': 'Aktif',
            'open_ports': '445, 3389'
        },
        {
            'ip': '192.168.1.30',
            'hostname': 'server02.local',
            'status': 'Aktif',
            'open_ports': '22, 3306'
        }
    ]
    
    print(f"\nToplam {len(scanner.results)} örnek sonuç")
    
    # Filter by hostname
    print("\n--- Hostname filtreleme (keyword='server') ---")
    filtered = scanner.filter_results(keyword='server')
    print(f"Bulunan: {len(filtered)} sonuç")
    for result in filtered:
        print(f"  - {result['ip']}: {result['hostname']}")
    
    # Filter by port
    print("\n--- Port filtreleme (port=80) ---")
    filtered = scanner.filter_results(port=80)
    print(f"Bulunan: {len(filtered)} sonuç")
    for result in filtered:
        print(f"  - {result['ip']}: {result['open_ports']}")
    
    return scanner.results


def example_3_excel_export(results):
    """Example 3: Export results to Excel"""
    print("\n" + "=" * 70)
    print("ÖRNEK 3: Excel'e Aktarma")
    print("=" * 70)
    
    if not results:
        print("\nAktarılacak veri yok!")
        return
    
    exporter = ExcelExporter()
    filename = os.path.join(tempfile.gettempdir(), "example_scan_results.xlsx")
    
    print(f"\nSonuçlar '{filename}' dosyasına aktarılıyor...")
    success = exporter.export(results, filename, "192.168.1.0/24")
    
    if success:
        print("\n✓ Excel dosyası özellikleri:")
        print("  - Formatlanmış başlıklar")
        print("  - Otomatik sütun genişlikleri")
        print("  - Özet bilgiler sayfası")
        print("  - Tarama tarihi ve saati")
    
    return success


def example_4_common_ports():
    """Example 4: Demonstrate common port scanning"""
    print("\n" + "=" * 70)
    print("ÖRNEK 4: Yaygın Port Taraması")
    print("=" * 70)
    
    scanner = NetworkScanner(timeout=1)
    
    print("\nTaranan yaygın portlar:")
    ports_info = {
        21: "FTP (File Transfer Protocol)",
        22: "SSH (Secure Shell)",
        23: "Telnet",
        25: "SMTP (Email)",
        80: "HTTP (Web)",
        443: "HTTPS (Secure Web)",
        445: "SMB (Windows File Sharing)",
        3389: "RDP (Remote Desktop)",
        8080: "HTTP Alternative"
    }
    
    for port, description in ports_info.items():
        print(f"  - Port {port}: {description}")
    
    print("\nLocalhost üzerinde port taraması yapılıyor...")
    open_ports = scanner.scan_common_ports("127.0.0.1")
    
    if open_ports:
        print(f"\n✓ {len(open_ports)} açık port bulundu: {', '.join(map(str, open_ports))}")
    else:
        print("\n✓ Localhost'ta yaygın portlar kapalı (güvenli)")


def main():
    """Main example runner"""
    print("=" * 70)
    print("  AĞ İZLEME UYGULAMASI - KULLANIM ÖRNEKLERİ")
    print("=" * 70)
    
    try:
        # Example 1: Basic scanning
        results = example_1_basic_scan()
        
        # Example 2: Filtering
        sample_results = example_2_filtering()
        
        # Example 3: Excel export
        example_3_excel_export(sample_results)
        
        # Example 4: Port scanning
        example_4_common_ports()
        
        print("\n" + "=" * 70)
        print("Tüm örnekler başarıyla tamamlandı!")
        print("=" * 70)
        print("\nGerçek kullanım için 'python main.py' komutunu çalıştırın.")
        
    except Exception as e:
        print(f"\n✗ Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
