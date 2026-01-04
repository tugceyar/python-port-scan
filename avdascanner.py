import os
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 0.3
RESULTS = []

def banner():
    print("""
 █████╗ ██╗   ██╗██████╗  █████╗ 
██╔══██╗██║   ██║██╔══██╗██╔══██╗
███████║██║   ██║█     █╔███████║
██╔══██║╚██╗ ██╔╝██╔══██╗██╔══██║
██║  ██║ ╚████╔╝ ██████╔╝██║  ██║
╚═╝  ╚═╝  ╚═══╝  ╚═════╝ ╚═╝  ╚═╝

        AVDA Network Scanner
""")

def ping(ip):
    command = f"ping -c 1 {ip} > /dev/null 2>&1"
    return os.system(command) == 0

def scan_ports(ip):
    open_ports = []
    for port in range(1, 65536):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

def scan_host(ip):
    ip = str(ip)
    if ping(ip):
        ports = scan_ports(ip)
        port_text = ",".join(map(str, ports)) if ports else "-"
        RESULTS.append((ip, "AKTİF", port_text))
    else:
        RESULTS.append((ip, "PASİF", "-"))

def scan_network(network):
    print(f"\n Taranan Network: {network}\n")
    with ThreadPoolExecutor(max_workers=20) as executor:
        for ip in ipaddress.IPv4Network(network, strict=False):
            executor.submit(scan_host, ip)

def print_table():
    print("\n{:<16} {:<10} {:<30}".format("IP ADRESİ", "DURUM", "AÇIK PORTLAR"))
    print("-" * 65)
    for ip, status, ports in RESULTS:
        print("{:<16} {:<10} {:<30}".format(ip, status, ports))

if __name__ == "__main__":
    banner()
    network = input("Network gir (örnek: 10.10.10.0/24): ")
    scan_network(network)
    print_table()
