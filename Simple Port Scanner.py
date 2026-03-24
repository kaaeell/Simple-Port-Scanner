import socket
import datetime

# Common ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    5432: "PostgreSQL",
    6379: "Redis",
    27017: "MongoDB",
}

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0  # True if open
    except socket.error:
        return False

def resolve_host(host):
    try:
        ip = socket.gethostbyname(host)
        return ip
    except socket.gaierror:
        return None

def scan(host, ports):
    print("=" * 50)
    print("   🔍 Simple Port Scanner")
    print("   by Yaser | github.com/kaaeell")
    print("=" * 50)

    ip = resolve_host(host)
    if not ip:
        print(f"\n❌ Could not resolve host: {host}")
        return

    print(f"\n🎯 Target  : {host}")
    print(f"🌐 IP      : {ip}")
    print(f"⏰ Started : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔎 Scanning {len(ports)} ports...\n")
    print(f"{'PORT':<10} {'SERVICE':<15} {'STATUS'}")
    print("-" * 40)

    open_ports = []

    for port in ports:
        is_open = scan_port(ip, port)
        service = COMMON_PORTS.get(port, "Unknown")
        status = "✅ OPEN" if is_open else "❌ closed"

        if is_open:
            open_ports.append(port)
            print(f"{port:<10} {service:<15} {status}")
        else:
            print(f"{port:<10} {service:<15} {status}")

    print("-" * 40)
    print(f"\n📊 Scan complete!")
    print(f"   Open ports found : {len(open_ports)}")
    if open_ports:
        print(f"   Open ports       : {', '.join(map(str, open_ports))}")
    print(f"⏰ Finished : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    print("=" * 50)
    print("   🔍 Simple Port Scanner")
    print("   by Yaser | github.com/kaaeell")
    print("=" * 50)

    host = input("\nEnter target host (e.g. scanme.nmap.org): ").strip()
    print("\n[1] Scan common ports only (fast)")
    print("[2] Scan ports 1-1024 (thorough)")
    choice = input("\nChoose an option (1 or 2): ").strip()

    if choice == "1":
        ports = list(COMMON_PORTS.keys())
    elif choice == "2":
        ports = list(range(1, 1025))
    else:
        print("Invalid choice, scanning common ports by default.")
        ports = list(COMMON_PORTS.keys())

    scan(host, ports)


if __name__ == "__main__":
    main()