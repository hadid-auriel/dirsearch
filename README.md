# dirsearch
4Pentesting
Cara pakai di Windows:

Install Python (kalau belum ada) dan requests:
   pip install requests
Taruh pydirsearch.py dan wordlist.txt di folder yang sama, lalu jalankan:
   python pydirsearch.py -u http://target.local -w wordlist.txt
Kalau mau coba ekstensi tertentu (sesuai placeholder %EXT% di wordlist kamu):
   python pydirsearch.py -u http://target.local -w wordlist.txt -e php,html,txt

Fitur yang ada: multithreading, filter status code (default sembunyikan 404), timeout, opsi matikan SSL verify, dan simpan hasil ke file (-o hasil.txt).

Pakai ini cuma di target yang memang izin kamu scan ya (lab sekolah, aplikasi sendiri, atau yang sudah disetujui dosen/instruktur)
