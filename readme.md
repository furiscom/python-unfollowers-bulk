# Instagram Unfollow Automation Script (Educational Purposes Only)

![Warning Banner](https://img.shields.io/badge/⚠️%20WARNING-Use%20At%20Your%20Own%20Risk-red)
![Violates ToS Banner](https://img.shields.io/badge/📜%20WARNING-Violates%20Instagram%20ToS-orange)
![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![Selenium Version](https://img.shields.io/badge/Selenium-4.x-green.svg)

**🚨🚨🚨 PERINGATAN SANGAT PENTING 🚨🚨🚨**

**PENGGUNAAN SCRIPT INI DAPAT MENYEBABKAN AKUN INSTAGRAM ANDA DIBATASI, DIBLOKIR SEMENTARA, ATAU BAHKAN DINONAKTIFKAN SECARA PERMANEN.**

Mengotomatiskan tindakan di Instagram, terutama tindakan massal seperti *unfollowing*, secara eksplisit **MELANGGAR Ketentuan Layanan (Terms of Service - ToS)** Instagram. Script ini disediakan **HANYA UNTUK TUJUAN EDUKASI DAN DEMONSTRASI TEKNIS** untuk menunjukkan bagaimana otomatisasi browser menggunakan Selenium dapat dilakukan.

**PENULIS TIDAK BERTANGGUNG JAWAB ATAS PENYALAHGUNAAN SCRIPT INI ATAU KONSEKUENSI APAPUN (TERMASUK KEHILANGAN AKUN) YANG TIMBUL DARI PENGGUNAANNYA.**

**GUNAKAN DENGAN RISIKO ANDA SENDIRI. SANGAT TIDAK DISARANKAN UNTUK DIGUNAKAN PADA AKUN PENTING ATAU UTAMA.**

---

## Deskripsi

Script Python ini menggunakan library `Selenium` untuk mengotomatiskan proses *unfollowing* akun di Instagram. Script ini akan:
1.  Membuka browser (Chrome secara default dalam contoh kode).
2.  Login ke akun Instagram Anda.
3.  Menavigasi ke halaman profil Anda.
4.  Membuka daftar "Following" (Mengikuti).
5.  Secara berulang mengklik tombol "Following" di samping pengguna pertama dalam daftar.
6.  Mengklik tombol konfirmasi "Unfollow".
7.  Merefresh halaman (sesuai logika kode, meskipun ini tidak efisien).
8.  Mengulangi proses hingga batas `MAX_UNFOLLOWS` tercapai atau terjadi error.

## Fitur Utama

*   Login otomatis ke Instagram.
*   Navigasi ke daftar "Following".
*   Otomatisasi klik tombol "Following" dan konfirmasi "Unfollow".
*   Konfigurasi jumlah maksimum unfollow per sesi (`MAX_UNFOLLOWS`).
*   Konfigurasi jeda waktu acak antar tindakan (`MIN_DELAY`, `MAX_DELAY`) untuk mencoba meniru perilaku manusia (meskipun masih berisiko).
*   Penanganan dasar untuk pop-up setelah login (mungkin perlu disesuaikan).

## Prasyarat

Sebelum menjalankan script ini, Anda memerlukan:
1.  **Python 3.x** terinstal di sistem Anda.
2.  **Pip** (package installer for Python).
3.  Web browser **Google Chrome** (atau browser lain yang didukung Selenium seperti Firefox, Edge).
4.  **WebDriver** yang sesuai dengan browser dan versi browser Anda (misalnya, `chromedriver` untuk Chrome).

## Instalasi & Setup

1.  **Clone Repositori (atau Unduh Kode):**
    ```bash
    git clone [URL Repositori GitHub Anda]
    cd [nama-folder-repositori]
    ```
    Atau unduh file `.py` secara manual.

2.  **Instal Library Python yang Diperlukan:**
    Buka terminal atau command prompt di direktori tempat Anda menyimpan file `.py`, lalu jalankan:
    ```bash
    pip install selenium
    ```
    *(Library `time` dan `random` sudah bawaan Python)*

3.  **Unduh WebDriver:**
    *   Unduh WebDriver yang sesuai untuk browser Anda. Untuk **Chrome**, unduh `chromedriver` dari: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
    *   **PENTING:** Pastikan versi `chromedriver` **sesuai** dengan versi browser Google Chrome yang terinstal di komputer Anda.
    *   Letakkan file executable WebDriver (misalnya `chromedriver.exe` di Windows) di lokasi yang mudah diakses.

## Konfigurasi Script

Buka file script Python (`nama_file_anda.py`) dengan editor teks dan ubah bagian konfigurasi berikut:

```python
# --- Konfigurasi (GANTI DENGAN DATA ANDA & PATH WEBDRIVER) ---
INSTAGRAM_USERNAME = "USERNAME_ANDA" # Ganti dengan username Instagram Anda

# PERINGATAN KERAS: Jangan pernah menyimpan password langsung di kode!
# Pertimbangkan menggunakan input() atau environment variables untuk keamanan.
INSTAGRAM_PASSWORD = "PASSWORD_ANDA" # Ganti dengan password Instagram Anda

# Ganti dengan path LENGKAP tempat Anda menyimpan chromedriver.exe
WEBDRIVER_PATH = 'C:/path/lengkap/ke/chromedriver.exe' # Contoh Windows
# WEBDRIVER_PATH = '/path/lengkap/ke/chromedriver' # Contoh Linux/Mac

# Koordinat (SANGAT TIDAK DIREKOMENDASIKAN, MUDAH GAGAL)
# Biarkan saja jika Anda lebih memilih metode klik link (lebih baik)
FOLLOWING_LIST_X = 934
FOLLOWING_LIST_Y = 194

# Selector Tombol (BISA BERUBAH KAPAN SAJA oleh Instagram)
FOLLOWING_BUTTON_SELECTOR = "button._acan._acap._acat._aj1-._ap30"
UNFOLLOW_CONFIRM_BUTTON_SELECTOR = "button._a9--._ap36._a9-_"

# Jumlah maksimal unfollow dalam satu sesi (untuk mencegah blokir)
MAX_UNFOLLOWS = 20 # Mulai dengan angka KECIL untuk testing! Jangan > 50-100 per hari.
# Jeda antar tindakan (dalam detik) - PENTING untuk menghindari blokir
MIN_DELAY = 5   # Tingkatkan jeda untuk lebih aman
MAX_DELAY = 15  # Tingkatkan jeda untuk lebih aman
# -----------------------------------------------------------
