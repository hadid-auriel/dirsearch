# dirsearch

Dibuat untuk keperluan belajar / tugas sekolah mata kuliah Cyber Security.

## ⚠️ Disclaimer

Tool ini hanya boleh digunakan pada target yang **kamu miliki izin eksplisit** untuk diuji — misalnya lab sekolah, aplikasi milik sendiri, environment latihan (DVWA, OWASP Juice Shop, dsb.), atau target CTF resmi. Melakukan scanning terhadap sistem milik orang lain tanpa izin dapat melanggar hukum (di Indonesia diatur antara lain dalam UU ITE). Penulis tidak bertanggung jawab atas penyalahgunaan tool ini.

## Fitur

- Brute-force directory & file menggunakan wordlist custom
- Mendukung format wordlist dirsearch asli (placeholder `%EXT%`)
- Substitusi ekstensi otomatis (`-e php,html,txt`)
- Multithreading untuk scan lebih cepat
- Filter status code (default sembunyikan `404`)
- Simpan hasil scan ke file
- Opsi matikan verifikasi SSL (untuk target self-signed cert)

## Requirements

- Python 3.7+
- Library `requests`

## Instalasi

```bash
git clone https://github.com/<username>/pydirsearch.git
cd pydirsearch
pip install -r requirements.txt
```

Atau langsung:

```bash
pip install requests
```

## Cara Pakai

Scan dasar:

```bash
python pydirsearch.py -u http://target.local -w wordlist.txt
```

Dengan ekstensi tertentu:

```bash
python pydirsearch.py -u http://target.local -w wordlist.txt -e php,html,txt
```

Contoh lebih lengkap:

```bash
python pydirsearch.py -u http://target.local -w wordlist.txt \
  -e php,html,txt \
  -t 50 \
  -x 404,403 \
  --timeout 5 \
  -o hasil_scan.txt
```

## Opsi

| Flag | Deskripsi | Default |
|---|---|---|
| `-u`, `--url` | URL target (wajib) | - |
| `-w`, `--wordlist` | Path ke file wordlist (wajib) | - |
| `-e`, `--extensions` | Daftar ekstensi dipisah koma | *(kosong)* |
| `-t`, `--threads` | Jumlah thread paralel | `20` |
| `-x`, `--exclude` | Status code yang disembunyikan, pisah koma | `404` |
| `--timeout` | Timeout request (detik) | `10` |
| `-o`, `--output` | Simpan hasil ke file | *(tidak disimpan)* |
| `--no-ssl-verify` | Matikan verifikasi SSL | *(aktif/verify)* |

## Contoh Output

```
[*] Target     : http://target.local/
[*] Wordlist   : wordlist.txt
[*] Extensions : ['php', 'html']
[*] Threads    : 20
[*] Exclude    : [404]
------------------------------------------------------------
[200] http://target.local/admin/  (size: 4521)
[301] http://target.local/images  (size: 0)
[403] http://target.local/.htaccess  (size: 278)
------------------------------------------------------------
[*] Selesai dalam 12.4 detik. Ditemukan 3 path.
```

## Lisensi

MIT License - bebas digunakan dan dimodifikasi untuk keperluan edukasi.
