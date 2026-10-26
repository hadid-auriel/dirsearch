#!/usr/bin/env python3
"""
pydirsearch.py - Dirsearch sederhana berbasis Python (untuk tugas sekolah / belajar cyber security)

PENTING: Gunakan HANYA pada target yang memang kamu punya izin untuk diuji
(misalnya lab sekolah, aplikasi milik sendiri, atau target yang sudah diizinkan
secara tertulis/CTF). Scanning target orang lain tanpa izin bisa melanggar hukum.

Cara pakai dasar:
    python pydirsearch.py -u http://target.local -w wordlist.txt

Dengan ekstensi (otomatis isi placeholder %EXT% di wordlist, dan juga
dicoba ke kata yang tidak punya %EXT%):
    python pydirsearch.py -u http://target.local -w wordlist.txt -e php,html,txt

Opsi lain:
    -t / --threads     jumlah thread paralel (default 20)
    -x / --exclude     status code yang disembunyikan, pisah koma (default 404)
    --timeout          timeout request dalam detik (default 10)
    -o / --output      simpan hasil ke file
    --no-ssl-verify    matikan verifikasi SSL (untuk target self-signed cert)
"""

import argparse
import concurrent.futures
import sys
import time
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Modul 'requests' belum terpasang. Install dulu dengan:")
    print("    pip install requests")
    sys.exit(1)

requests.packages.urllib3.disable_warnings() if hasattr(requests, "packages") else None


def load_wordlist(path, extensions):
    """Baca wordlist dan hasilkan daftar path final yang akan dicoba."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    paths = []
    for word in raw_lines:
        if "%EXT%" in word:
            if extensions:
                for ext in extensions:
                    paths.append(word.replace("%EXT%", ext))
            # kalau tidak ada ekstensi yang dipilih, skip baris %EXT% (tidak valid tanpa ekstensi)
            continue
        paths.append(word)
        # juga coba word + ekstensi, kalau user minta ekstensi dan wordnya belum punya titik
        if extensions and "." not in word:
            for ext in extensions:
                paths.append(f"{word}.{ext}")

    # hilangkan duplikat tapi jaga urutan
    seen = set()
    unique_paths = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            unique_paths.append(p)
    return unique_paths


def scan_one(base_url, path, session, timeout, exclude_codes, verify_ssl):
    url = urljoin(base_url, path)
    try:
        resp = session.get(url, timeout=timeout, verify=verify_ssl, allow_redirects=False)
        if resp.status_code not in exclude_codes:
            return (url, resp.status_code, len(resp.content))
    except requests.RequestException:
        return None
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Dirsearch sederhana berbasis Python (untuk tujuan edukasi / tugas sekolah)."
    )
    parser.add_argument("-u", "--url", required=True, help="URL target, contoh: http://target.local")
    parser.add_argument("-w", "--wordlist", required=True, help="Path ke file wordlist")
    parser.add_argument("-e", "--extensions", default="", help="Daftar ekstensi dipisah koma, contoh: php,html,txt")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Jumlah thread paralel (default 20)")
    parser.add_argument("-x", "--exclude", default="404", help="Status code yang disembunyikan, pisah koma (default 404)")
    parser.add_argument("--timeout", type=float, default=10, help="Timeout request per detik (default 10)")
    parser.add_argument("-o", "--output", default=None, help="Simpan hasil ke file teks")
    parser.add_argument("--no-ssl-verify", action="store_true", help="Matikan verifikasi SSL")
    args = parser.parse_args()

    base_url = args.url if args.url.endswith("/") else args.url + "/"
    extensions = [e.strip().lstrip(".") for e in args.extensions.split(",") if e.strip()]
    exclude_codes = {int(c.strip()) for c in args.exclude.split(",") if c.strip()}

    print(f"[*] Target     : {base_url}")
    print(f"[*] Wordlist   : {args.wordlist}")
    print(f"[*] Extensions : {extensions if extensions else '(tidak ada)'}")
    print(f"[*] Threads    : {args.threads}")
    print(f"[*] Exclude    : {sorted(exclude_codes)}")
    print("-" * 60)

    paths = load_wordlist(args.wordlist, extensions)
    print(f"[*] Total path yang akan dicoba: {len(paths)}")
    print("-" * 60)

    session = requests.Session()
    session.headers.update({"User-Agent": "pydirsearch/1.0 (school cybersec assignment)"})

    found = []
    start = time.time()
    done_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(scan_one, base_url, p, session, args.timeout, exclude_codes, not args.no_ssl_verify): p
            for p in paths
        }
        for future in concurrent.futures.as_completed(futures):
            done_count += 1
            result = future.result()
            if result:
                url, status, size = result
                found.append(result)
                print(f"[{status}] {url}  (size: {size})")
            if done_count % 200 == 0:
                print(f"    ... {done_count}/{len(paths)} dicoba", file=sys.stderr)

    elapsed = time.time() - start
    print("-" * 60)
    print(f"[*] Selesai dalam {elapsed:.1f} detik. Ditemukan {len(found)} path.")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for url, status, size in sorted(found):
                f.write(f"[{status}] {url} (size: {size})\n")
        print(f"[*] Hasil disimpan ke {args.output}")


if __name__ == "__main__":
    main()
