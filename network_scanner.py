"""
Network Scanner Module
Ağ tarama işlemleri için modül
"""
import socket
import ipaddress
import subprocess
import platform
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class NetworkScanner:
    """IP bloklarını tarayan ve cihazları tespit eden sınıf"""
    
    def __init__(self, timeout: int = 1):
        """
        NetworkScanner başlatıcı
        
        Args:
            timeout: Bağlantı zaman aşımı (saniye)
        """
        self.timeout = timeout
        self.results = []
    
    def ping(self, ip: str) -> bool:
        """
        Bir IP adresini ping ile kontrol eder
        
        Args:
            ip: Kontrol edilecek IP adresi
            
        Returns:
            bool: IP erişilebilir ise True, değilse False
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w' if platform.system().lower() == 'windows' else '-W', 
                   str(self.timeout), ip]
        
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.timeout + 1
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, Exception):
            return False
    
    def check_port(self, ip: str, port: int) -> bool:
        """
        Belirtilen IP ve portu kontrol eder
        
        Args:
            ip: IP adresi
            port: Port numarası
            
        Returns:
            bool: Port açık ise True, değilse False
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def scan_common_ports(self, ip: str) -> List[int]:
        """
        Yaygın portları tarar
        
        Args:
            ip: Taranacak IP adresi
            
        Returns:
            List[int]: Açık portların listesi
        """
        common_ports = [21, 22, 23, 25, 80, 443, 445, 3389, 8080]
        open_ports = []
        
        for port in common_ports:
            if self.check_port(ip, port):
                open_ports.append(port)
        
        return open_ports
    
    def scan_host(self, ip: str) -> Optional[Dict]:
        """
        Tek bir hostu tarar
        
        Args:
            ip: Taranacak IP adresi
            
        Returns:
            Optional[Dict]: Host bilgileri veya None
        """
        ip_str = str(ip)
        
        if self.ping(ip_str):
            try:
                hostname = socket.gethostbyaddr(ip_str)[0]
            except (socket.herror, socket.gaierror):
                hostname = "Bilinmiyor"
            
            open_ports = self.scan_common_ports(ip_str)
            
            return {
                'ip': ip_str,
                'hostname': hostname,
                'status': 'Aktif',
                'open_ports': ', '.join(map(str, open_ports)) if open_ports else 'Port bulunamadı'
            }
        
        return None
    
    def scan_network(self, ip_block: str, max_workers: int = 50) -> List[Dict]:
        """
        Bir IP bloğunu tarar
        
        Args:
            ip_block: CIDR notasyonunda IP bloğu (örn: 192.168.1.0/24)
            max_workers: Maksimum paralel işlem sayısı
            
        Returns:
            List[Dict]: Bulunan hostların listesi
        """
        try:
            network = ipaddress.ip_network(ip_block, strict=False)
        except ValueError as e:
            print(f"Geçersiz IP bloğu: {e}")
            return []
        
        self.results = []
        print(f"\n{ip_block} bloğu taranıyor...")
        print(f"Toplam {network.num_addresses} adres taranacak.\n")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.scan_host, ip): ip for ip in network.hosts()}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"İlerleme: {completed}/{len(futures)} adres tarandı")
                
                result = future.result()
                if result:
                    self.results.append(result)
                    print(f"  ✓ Aktif host bulundu: {result['ip']} ({result['hostname']})")
        
        print(f"\nTarama tamamlandı. Toplam {len(self.results)} aktif host bulundu.\n")
        return self.results
    
    def filter_results(self, keyword: Optional[str] = None, 
                       port: Optional[int] = None) -> List[Dict]:
        """
        Sonuçları filtreler
        
        Args:
            keyword: Hostname'de aranacak anahtar kelime
            port: Aranacak açık port
            
        Returns:
            List[Dict]: Filtrelenmiş sonuçlar
        """
        filtered = self.results
        
        if keyword:
            filtered = [r for r in filtered 
                       if keyword.lower() in r['hostname'].lower()]
        
        if port:
            filtered = [r for r in filtered 
                       if str(port) in r['open_ports']]
        
        return filtered
