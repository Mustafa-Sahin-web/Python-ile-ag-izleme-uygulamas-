#!/usr/bin/env python3
"""
Test script for network monitoring application
Ağ izleme uygulaması için test scripti
"""
import sys
import tempfile
import os
from network_scanner import NetworkScanner
from excel_exporter import ExcelExporter


def test_network_scanner():
    """NetworkScanner sınıfını test eder"""
    print("=" * 60)
    print("NetworkScanner Test")
    print("=" * 60)
    
    scanner = NetworkScanner(timeout=1)
    
    # Test 1: Ping testi (localhost)
    print("\nTest 1: Localhost ping testi...")
    result = scanner.ping("127.0.0.1")
    print(f"  Sonuç: {'✓ BAŞARILI' if result else '✗ BAŞARISIZ'}")
    
    # Test 2: Port testi (localhost)
    print("\nTest 2: Port kontrolü testi...")
    # Most systems won't have port 9999 open
    result = scanner.check_port("127.0.0.1", 9999)
    print(f"  Port 9999 kapalı: {'✓ BAŞARILI' if not result else '✗ BAŞARISIZ'}")
    
    # Test 3: Host tarama (localhost)
    print("\nTest 3: Host tarama testi (127.0.0.1)...")
    result = scanner.scan_host("127.0.0.1")
    if result:
        print(f"  ✓ Host bulundu:")
        print(f"    - IP: {result['ip']}")
        print(f"    - Hostname: {result['hostname']}")
        print(f"    - Durum: {result['status']}")
    else:
        print("  ✗ Host bulunamadı")
    
    return scanner


def test_excel_exporter(scanner):
    """ExcelExporter sınıfını test eder"""
    print("\n" + "=" * 60)
    print("ExcelExporter Test")
    print("=" * 60)
    
    # Örnek veri oluştur
    test_data = [
        {
            'ip': '127.0.0.1',
            'hostname': 'localhost',
            'status': 'Aktif',
            'open_ports': 'Port bulunamadı'
        }
    ]
    
    # Excel'e aktar
    print("\nTest: Excel dosyası oluşturma...")
    exporter = ExcelExporter()
    filename = os.path.join(tempfile.gettempdir(), "test_results.xlsx")
    success = exporter.export(test_data, filename, "127.0.0.1/32")
    
    if success:
        print(f"  ✓ Excel dosyası başarıyla oluşturuldu: {filename}")
        return True
    else:
        print("  ✗ Excel dosyası oluşturulamadı")
        return False


def test_filtering():
    """Filtreleme fonksiyonunu test eder"""
    print("\n" + "=" * 60)
    print("Filtreleme Test")
    print("=" * 60)
    
    scanner = NetworkScanner()
    
    # Örnek sonuçlar oluştur
    scanner.results = [
        {'ip': '192.168.1.1', 'hostname': 'router', 'status': 'Aktif', 'open_ports': '80, 443'},
        {'ip': '192.168.1.2', 'hostname': 'server', 'status': 'Aktif', 'open_ports': '22, 80'},
        {'ip': '192.168.1.3', 'hostname': 'workstation', 'status': 'Aktif', 'open_ports': '445'},
        {'ip': '192.168.1.4', 'hostname': 'proxy', 'status': 'Aktif', 'open_ports': '8080'},
    ]
    
    # Hostname filtreleme
    print("\nTest 1: Hostname filtreleme (keyword='server')...")
    filtered = scanner.filter_results(keyword='server')
    print(f"  Bulunan: {len(filtered)} sonuç")
    if len(filtered) == 1 and filtered[0]['hostname'] == 'server':
        print("  ✓ BAŞARILI")
    else:
        print("  ✗ BAŞARISIZ")
    
    # Port filtreleme - port 80 (should not match 8080)
    print("\nTest 2: Port filtreleme (port=80, 8080 ile karışmamalı)...")
    filtered = scanner.filter_results(port=80)
    print(f"  Bulunan: {len(filtered)} sonuç")
    # Should find 2 results (router and server), NOT proxy with 8080
    if len(filtered) == 2:
        has_8080 = any('8080' in r['open_ports'] for r in filtered)
        if not has_8080:
            print("  ✓ BAŞARILI - 8080 ile karışmadı")
        else:
            print("  ✗ BAŞARISIZ - 8080 ile karıştı")
    else:
        print("  ✗ BAŞARISIZ")
    
    # Port filtreleme - port 8080
    print("\nTest 3: Port filtreleme (port=8080)...")
    filtered = scanner.filter_results(port=8080)
    print(f"  Bulunan: {len(filtered)} sonuç")
    if len(filtered) == 1 and '8080' in filtered[0]['open_ports']:
        print("  ✓ BAŞARILI")
    else:
        print("  ✗ BAŞARISIZ")


def main():
    """Ana test fonksiyonu"""
    print("\n" + "=" * 60)
    print("     AĞ İZLEME UYGULAMASI TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        # NetworkScanner testleri
        scanner = test_network_scanner()
        
        # ExcelExporter testleri
        test_excel_exporter(scanner)
        
        # Filtreleme testleri
        test_filtering()
        
        print("\n" + "=" * 60)
        print("Tüm testler tamamlandı!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test sırasında hata oluştu: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
