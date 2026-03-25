# 🔍 Simple Port Scanner

A lightweight command-line port scanner built with Python. Scans a target host for open ports, identifies running services, and saves results to a file.

---

## 🚀 Features

- ⚡ Multithreaded scanning (blazing fast)
- Resolves hostnames to IP addresses
- Scans common ports, full range (1–1024), or custom range
- Identifies services (SSH, HTTP, FTP, MySQL, etc.)
- 💾 Saves results to a timestamped `.txt` report
- Pure Python — no external libraries needed

---

## 📸 Preview

```
==================================================
   🔍 Port Scanner v2.0
   by Yaser | github.com/kaaeell
==================================================

Enter target host: scanme.nmap.org

[1] Common ports only (fast)
[2] Ports 1-1024 (thorough)
[3] Custom port range

Choose an option: 1
Save results to file? (y/n): y

🎯 Target  : scanme.nmap.org (45.33.32.156)
⏰ Started : 2025-03-25 14:22:01
🔎 Scanning 16 ports with multithreading...

  ✅ OPEN  22         SSH
  ✅ OPEN  80         HTTP

----------------------------------------

📊 Scan complete in 2s!
   Open ports found : 2
   Open ports       : 22, 80
💾 Results saved to: scan_scanme.nmap.org_20250325_142201.txt
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

```bash
python port_scanner.py
```

You'll be asked to:
1. Enter a target host (domain or IP)
2. Choose scan mode:
   - **Option 1** — Common ports only (fast)
   - **Option 2** — Ports 1–1024 (thorough)
   - **Option 3** — Custom port range
3. Choose whether to save results to a `.txt` file

---

## 🧪 Safe Testing

Use this free legal test server:

```
scanme.nmap.org
```

> ⚠️ **Disclaimer:** Only scan hosts you own or have explicit permission to scan. Unauthorized port scanning may be illegal in your country.

---

## 📚 What I Learned

- How TCP sockets work in Python
- What ports and services are
- How multithreading speeds up network tasks
- How tools like Nmap work under the hood
- Basic network reconnaissance concepts

---

## 🗺️ Roadmap

- [x] Scan common ports
- [x] Multithreading for faster scans
- [x] Save results to `.txt` file
- [x] Custom port range
- [ ] Banner grabbing (detect software versions)
- [ ] Export to `.json`
- [ ] Scan multiple hosts at once

---

## 📄 License

MIT License — free to use, modify and share.
