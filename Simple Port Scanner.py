import socket
import datetime
import threading
from queue import Queue

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

lock = threading.Lock()


def scan_port(host, port, timeout=1, grab_banner=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((host, port))

        banner = ""
        if result == 0 and grab_banner:
            try:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No banner"

        sock.close()

        return result == 0, banner

    except:
        return False, ""


def worker(host, queue, results, grab_banner):
    while True:
        try:
            port = queue.get_nowait()
        except:
            break

        is_open, banner = scan_port(host, port, grab_banner=grab_banner)

        if is_open:
            service = COMMON_PORTS.get(port, "Unknown")
            with lock:
                results.append((port, service, banner))
                print(f"  ✅ {port:<6} {service:<12} OPEN")

        queue.task_done()


def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def save_results(host, ip, ports, start_time, end_time, filename):
    with open(filename, "w") as f:
        f.write("=" * 50 + "\n")
        f.write("   Port Scanner Report v3.0\n")
        f.write("   by Yaser | github.com/kaaeell\n")
        f.write("=" * 50 + "\n")

        f.write(f"\nTarget  : {host}\n")
        f.write(f"IP      : {ip}\n")
        f.write(f"Started : {start_time}\n")
        f.write(f"Finished: {end_time}\n\n")

        f.write(f"{'PORT':<8} {'SERVICE':<15} {'STATUS'}\n")
        f.write("-" * 40 + "\n")

        if ports:
            for port, service, _ in sorted(ports):
                f.write(f"{port:<8} {service:<15} OPEN\n")
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
            start = int(input("Start port: "))
            end = int(input("End port  : "))
            return list(range(start, end + 1))
        except:
            print("❌ Invalid range. Using common ports.")
            return list(COMMON_PORTS.keys())
    else:
        return list(COMMON_PORTS.keys())


def main():
    print("=" * 50)
    print("   🔍 Port Scanner v3.0")
    print("   by Yaser")
    print("=" * 50)

    host = input("\nEnter target (domain/IP): ").strip()
    ip = resolve_host(host)

    if not ip:
        print("❌ Could not resolve host.")
        return

    print("\n[1] Common ports (fast)")
    print("[2] 1–1024 (standard)")
    print("[3] Custom range")

    choice = input("Choose: ").strip()
    ports = get_ports(choice)

    grab_banner = input("Grab banners? (y/n): ").lower() == "y"
    save = input("Save results? (y/n): ").lower() == "y"

    start_time = datetime.datetime.now()

    print(f"\n🎯 Target: {host} ({ip})")
    print(f"🔎 Scanning {len(ports)} ports...\n")

    queue = Queue()
    for port in ports:
        queue.put(port)

    results = []
    threads = []

    thread_count = min(100, len(ports))

    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(ip, queue, results, grab_banner))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "-" * 40)
    print(f"📊 Done in {duration:.2f}s")
    print(f"Open ports: {len(results)}")

    if results:
        print("Ports:", ", ".join(str(p) for p, _, _ in sorted(results)))

    if save:
        filename = f"scan_{host}_{start_time.strftime('%Y%m%d_%H%M%S')}.txt"
        save_results(
            host,
            ip,
            results,
            start_time.strftime('%Y-%m-%d %H:%M:%S'),
            end_time.strftime('%Y-%m-%d %H:%M:%S'),
            filename,
        )


if __name__ == "__main__":
    main()
