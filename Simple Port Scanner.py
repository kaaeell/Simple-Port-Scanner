import socket
import datetime
import threading
from queue import Queue

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

open_ports = []
lock = threading.Lock()

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False

def worker(host, queue, results):
    while not queue.empty():
        port = queue.get()
        is_open = scan_port(host, port)
        if is_open:
            service = COMMON_PORTS.get(port, "Unknown")
            with lock:
                results.append((port, service))
                print(f"  ✅ OPEN  {port:<10} {service}")
        queue.task_done()

def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None

def save_results(host, ip, ports, start_time, end_time, filename):
    with open(filename, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("   Port Scanner Report\n")
        f.write("   by Yaser | github.com/kaaeell\n")
        f.write("=" * 50 + "\n")
        f.write(f"\nTarget  : {host}\n")
        f.write(f"IP      : {ip}\n")
        f.write(f"Started : {start_time}\n")
        f.write(f"Finished: {end_time}\n\n")
        f.write(f"{'PORT':<10} {'SERVICE':<15} STATUS\n")
        f.write("-" * 40 + "\n")
        if ports:
            for port, service in sorted(ports):
                f.write(f"{port:<10} {service:<15} OPEN\n")
        else:
            f.write("No open ports found.\n")
        f.write("-" * 40 + "\n")
        f.write(f"\nTotal open ports: {len(ports)}\n")
    print(f"\n💾 Results saved to: {filename}")

def get_ports(choice):
    if choice == "1":
        return list(COMMON_PORTS.keys())
    elif choice == "2":
        return list(range(1, 1025))
    elif choice == "3":
        try:
            start = int(input("  Start port: "))
            end = int(input("  End port  : "))
            if start < 1 or end > 65535 or start > end:
                print("❌ Invalid range. Using common ports.")
                return list(COMMON_PORTS.keys())
            return list(range(start, end + 1))
        except ValueError:
            print("❌ Invalid input. Using common ports.")
            return list(COMMON_PORTS.keys())
    else:
        print("Invalid choice, scanning common ports by default.")
        return list(COMMON_PORTS.keys())

def main():
    print("=" * 50)
    print("   🔍 Port Scanner v2.0")
    print("   by Yaser | github.com/kaaeell")
    print("=" * 50)

    host = input("\nEnter target host (e.g. scanme.nmap.org): ").strip()

    ip = resolve_host(host)
    if not ip:
        print(f"\n❌ Could not resolve host: {host}")
        return

    print("\n[1] Common ports only (fast)")
    print("[2] Ports 1-1024 (thorough)")
    print("[3] Custom port range")
    choice = input("\nChoose an option (1/2/3): ").strip()
    ports = get_ports(choice)

    save = input("\nSave results to file? (y/n): ").strip().lower()

    start_time = datetime.datetime.now()
    print(f"\n🎯 Target  : {host} ({ip})")
    print(f"⏰ Started : {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔎 Scanning {len(ports)} ports with multithreading...\n")

    queue = Queue()
    for port in ports:
        queue.put(port)

    results = []

    thread_count = min(100, len(ports))
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(ip, queue, results))
        t.daemon = True
        t.start()

    queue.join()

    end_time = datetime.datetime.now()
    duration = (end_time - start_time).seconds

    print("\n" + "-" * 40)
    print(f"\n📊 Scan complete in {duration}s!")
    print(f"   Open ports found : {len(results)}")
    if results:
        print(f"   Open ports       : {', '.join(str(p) for p, _ in sorted(results))}")
    print(f"⏰ Finished : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if save == "y":
        filename = f"scan_{host}_{start_time.strftime('%Y%m%d_%H%M%S')}.txt"
        save_results(host, ip, results, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), filename)

if __name__ == "__main__":
    main()
