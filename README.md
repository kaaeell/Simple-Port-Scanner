# 🔍 Simple Port Scanner

A lightweight command-line port scanner built with Python. This was my first cybersecurity project — it scans a target host for open ports and identifies the services running on them.

---

## 🚀 Features

- Resolves hostnames to IP addresses
- Scans common ports or full range (1–1024)
- Identifies services (SSH, HTTP, FTP, MySQL, etc.)
- Displays clean results with timestamps
- Pure Python — no external libraries needed

---

## 📸 Preview

```
==================================================
   🔍 Simple Port Scanner
   by Yaser | github.com/kaaeell
==================================================

🎯 Target  : scanme.nmap.org
🌐 IP      : 45.33.32.156
⏰ Started : 2024-03-24 14:22:01
🔎 Scanning 16 ports...

PORT       SERVICE         STATUS
----------------------------------------
22         SSH             ✅ OPEN
80         HTTP            ✅ OPEN
443        HTTPS           ❌ closed
3306       MySQL           ❌ closed
----------------------------------------

📊 Scan complete!
   Open ports found : 2
   Open ports       : 22, 80
```

---

## 🛠️ Installation

No installation needed! Just make sure you have Python 3 installed.

```bash
git clone https://github.com/kaaeell/py-port-scanner
cd py-port-scanner
python port_scanner.py
```

---

## 💻 Usage

Run the script and follow the prompts:

```bash
python port_scanner.py
```

You'll be asked to:
1. Enter a target host (domain or IP)
2. Choose scan mode:
   - **Option 1** — Scan common ports only (fast)
   - **Option 2** — Scan ports 1–1024 (thorough)

---

## 🧪 Safe Testing

To test legally and safely, use:

```
scanme.nmap.org
```

This is a server maintained by the Nmap team specifically for testing port scanners.

> ⚠️ **Disclaimer:** Only scan hosts you own or have explicit permission to scan. Unauthorized port scanning may be illegal in your country.

---

## 📚 What I Learned

- How TCP sockets work in Python
- What ports and services are
- How tools like Nmap work under the hood
- Basic network reconnaissance concepts

---

## 🗺️ Roadmap

- [ ] Add multithreading for faster scans
- [ ] Export results to a `.txt` or `.json` file
- [ ] Add banner grabbing (detect software versions)
- [ ] Add OS detection
- [ ] Build a simple GUI

---

## 📄 License

MIT License — free to use, modify and share.
