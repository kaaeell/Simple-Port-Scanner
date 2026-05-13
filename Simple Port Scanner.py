import socket
import datetime
import threading
import json
import time
import random
from queue import Queue

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 3306: "MySQL", 3389: "RDP",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    5432: "PostgreSQL", 6379: "Redis", 27017: "MongoDB",
}

lock = threading.Lock()
scanned_count = 0

# keeping scan history
scan_history = []


def scan_port(host, port, timeout=1, grab_banner=False):

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((host, port))

        banner = ""

        if result == 0 and grab_banner:

            try:
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()

            except:
                banner = "No banner"

        sock.close()

        return result == 0, banner

    except:
        return False, ""


def worker(host, queue, results, total_ports, grab_banner):

    global scanned_count

    while True:

        try:
            port = queue.get_nowait()

        except:
            break

        is_open, banner = scan_port(host, port, grab_banner=grab_banner)

        with lock:

            scanned_count += 1

            progress = (scanned_count / total_ports) * 100

            print(f"\rProgress: {progress:.1f}% ({scanned_count}/{total_ports})", end="")

        if is_open:

            service = COMMON_PORTS.get(port, "Unknown")

            with lock:

                results.append((port, service, banner))

                print(f"\n  ✅ {port:<6} {service:<12} OPEN")

        queue.task_done()


def resolve_host(host):

    try:
        return socket.gethostbyname(host)

    except socket.gaierror:
        return None


def save_results_txt(host, ip, ports, start_time, end_time, filename):

    with open(filename, "w") as f:

        f.write("=" * 50 + "\n")
        f.write("   Port Scanner Report v4.0\n")
        f.write("   by Yaser\n")
        f.write("=" * 50 + "\n")

        f.write(f"\nTarget  : {host}\n")
        f.write(f"IP      : {ip}\n")
        f.write(f"Started : {start_time}\n")
        f.write(f"Finished: {end_time}\n\n")

        for port, service, _ in sorted(ports):

            f.write(f"{port:<8} {service:<15} OPEN\n")


def save_results_json(host, ip, ports, filename):

    data = {
        "target": host,
        "ip": ip,
        "open_ports": [
            {"port": p, "service": s, "banner": b}
            for p, s, b in ports
        ]
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_ports():

    print("\n[1] Common ports")
    print("[2] 1–1024")
    print("[3] Custom range")

    choice = input("Choose: ").strip()

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
            print("invalid input using common ports")
            return list(COMMON_PORTS.keys())

    else:
        return list(COMMON_PORTS.keys())


# random tiny status thing
def random_scan_tip():

    tips = [
        "🛰️ scanning satellites probably",
        "☕ scanner running on caffeine",
        "💻 packets are flying rn",
        "🔍 looking for open doors in the network"
    ]

    print(random.choice(tips))


# NEW simple feature
def scan_rating(open_ports):

    if open_ports > 10:
        print("⚠️ security rating: questionable")

    elif open_ports > 5:
        print("😬 security rating: could be better")

    else:
        print("✅ security rating: decent")


# NEW
def random_hacker_message():

    msgs = [
        "👨‍💻 typing very fast increases scan speed",
        "🕶️ hacker mode activated",
        "🌐 network vibes detected",
        "💀 firewall probably nervous rn"
    ]

    print(random.choice(msgs))


def main():

    startup = [
        "starting scanner...",
        "loading network stuff...",
        "probably scanning legally...",
        "port scanner v4 ready"
    ]

    print("=" * 50)
    print("🔍 Port Scanner v4.1")
    print("by Yaser")
    print("=" * 50)

    print(random.choice(startup))

    targets = input("\nEnter target(s) (comma-separated): ").split(",")

    ports = get_ports()

    grab_banner = input("Grab banners? (y/n): ").lower() == "y"

    save = input("Save results? (y/n): ").lower() == "y"

    for host in targets:

        host = host.strip()

        ip = resolve_host(host)

        if not ip:
            print(f"❌ Could not resolve {host}")
            continue

        print(f"\n🎯 Scanning {host} ({ip})")

        random_scan_tip()

        queue = Queue()

        for port in ports:
            queue.put(port)

        results = []
        threads = []

        global scanned_count

        scanned_count = 0

        start_time = datetime.datetime.now()

        # fake loading vibe
        print("starting scan", end="")

        for i in range(3):
            time.sleep(0.4)
            print(".", end="")

        print()

        for _ in range(min(100, len(ports))):

            t = threading.Thread(
                target=worker,
                args=(ip, queue, results, len(ports), grab_banner)
            )

            t.start()

            threads.append(t)

        for t in threads:
            t.join()

        end_time = datetime.datetime.now()

        print(f"\n✅ Done: {len(results)} open ports")

        scan_history.append((host, len(results)))

        # showing open ports sorted
        if results:

            print("\n📂 Open ports summary:")

            for port, service, _ in sorted(results):
                print(f" - {port} ({service})")

        else:
            print("no open ports found")

        random_hacker_message()

        scan_rating(len(results))

        # random fake danger meter lol
        danger = random.randint(1, 100)

        print(f"🔥 threat level: {danger}%")

        # tiny easter eggs
        secret = input("\nsecret command? (press enter to skip): ")

        if secret.lower() == "admin":
            print("🛠️ admin mode unlocked")

        elif secret.lower() == "root":
            print("💀 root access denied obviously")

        # save results
        if save:

            timestamp = start_time.strftime('%Y%m%d_%H%M%S')

            save_results_txt(
                host,
                ip,
                results,
                start_time,
                end_time,
                f"{host}_{timestamp}.txt"
            )

            save_results_json(
                host,
                ip,
                results,
                f"{host}_{timestamp}.json"
            )

            print("💾 results saved")

    # final stats
    print("\n📊 Scan History:")

    for host, count in scan_history:
        print(f" - {host}: {count} open ports")

    print("\nscanner finished")


if __name__ == "__main__":
    main()
