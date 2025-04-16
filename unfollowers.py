import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service # Atau Firefox/Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# --- Konfigurasi (GANTI DENGAN DATA ANDA & PATH WEBDRIVER) ---
INSTAGRAM_USERNAME = "...."
# PERINGATAN KERAS: Jangan pernah menyimpan password langsung di kode untuk aplikasi nyata!
INSTAGRAM_PASSWORD = "..."
# Ganti dengan path tempat Anda menyimpan chromedriver.exe atau geckodriver.exe
#WEBDRIVER_PATH = '/path/to/your/chromedriver' # Contoh untuk Chrome di Linux/Mac
WEBDRIVER_PATH = 'C:/Users/Admin/Documents/python code/chromedriver-win64/chromedriver.exe' #contoh untuk windows
# Koordinat (SANGAT TIDAK DIREKOMENDASIKAN, MUDAH GAGAL)
FOLLOWING_LIST_X = 934
FOLLOWING_LIST_Y = 194

# Selector Tombol (BISA BERUBAH KAPAN SAJA)
FOLLOWING_BUTTON_SELECTOR = "button._acan._acap._acat._aj1-._ap30" # Tombol "Diikuti" di dalam daftar
UNFOLLOW_CONFIRM_BUTTON_SELECTOR = "button._a9--._ap36._a9-_" # Tombol konfirmasi "Batal mengikuti"

# Jumlah maksimal unfollow dalam satu sesi (untuk mencegah blokir)
MAX_UNFOLLOWS = 1000 # Atur sesuai kebutuhan, jangan terlalu banyak!
# Jeda antar tindakan (dalam detik) - PENTING untuk menghindari blokir
MIN_DELAY = 1
MAX_DELAY = 2
# -----------------------------------------------------------



def login_instagram(driver, username, password):
    """Fungsi untuk login ke Instagram."""
    print("Mencoba login...")
    driver.get("https://www.instagram.com/accounts/login/")
    try:
        # Tunggu hingga input username muncul
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        print("Mengisi username dan password...")
        username_input.send_keys(username)
        password_input.send_keys(password)
        time.sleep(1) # Jeda sebelum klik login

        print("Klik tombol login...")
        login_button.click()

        # Tunggu beberapa saat untuk proses login dan kemungkinan munculnya pop-up
        print("Menunggu proses login selesai...")
        time.sleep(10) # Tunggu agak lama setelah login

        # --- Handle Pop-up (Contoh: "Save Login Info?" / "Turn on Notifications?") ---
        # Pop-up ini bisa berbeda-beda, Anda mungkin perlu menyesuaikan selectornya
        try:
            print("Mencari tombol 'Not Now' (Save Info)...")
            not_now_button_save = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')] | //div[contains(text(), 'Not Now')]"))
                # Atau gunakan selector lain yang lebih spesifik jika tahu
            )
            print("Menutup pop-up 'Save Info'...")
            not_now_button_save.click()
            time.sleep(1)
        except (NoSuchElementException, TimeoutException):
            print("Pop-up 'Save Info' tidak ditemukan atau sudah ditutup.")

        try:
            print("Mencari tombol 'Not Now' (Notifications)...")
            not_now_button_notif = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                # Cari tombol 'Not Now' kedua jika ada
            )
            print("Menutup pop-up 'Notifications'...")
            not_now_button_notif.click()
            time.sleep(1)
        except (NoSuchElementException, TimeoutException):
            print("Pop-up 'Notifications' tidak ditemukan atau sudah ditutup.")

        print("Login berhasil!")
        return True

    except TimeoutException:
        print("Gagal login: Elemen login tidak ditemukan (timeout). Mungkin halaman berubah?")
        return False
    except Exception as e:
        print(f"Terjadi kesalahan saat login: {e}")
        return False

def unfollow_users(driver, username, max_unfollows):
    """Fungsi untuk melakukan proses unfollow."""
    unfollowed_count = 0
    for i in range(max_unfollows):
        print(f"\n--- Iterasi Unfollow ke-{i + 1} ---")
        try:
            # 1. Buka halaman profil sendiri (diperlukan sebelum klik koordinat/link)
            print(f"Navigasi ke profil: https://www.instagram.com/{username}/")
            driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(1) # Tunggu halaman profil load

            # 2. Buka daftar "Following"
            print(f"Mencoba membuka daftar 'Following'...")

            # === CARA 1: Klik Koordinat (TIDAK STABIL) ===
            try:
                print(f"Mengklik koordinat X:{FOLLOWING_LIST_X}, Y:{FOLLOWING_LIST_Y} (Tidak Direkomendasikan)...")
                actions = ActionChains(driver)
                # Pindah ke elemen body dulu (offset relatif terhadap viewport)
                body = driver.find_element(By.TAG_NAME, 'body')
                actions.move_to_element_with_offset(body, 0, 0) # Reset ke pojok kiri atas viewport
                actions.move_by_offset(FOLLOWING_LIST_X, FOLLOWING_LIST_Y).click().perform()
                print("Koordinat diklik.")
                time.sleep(1) # Tunggu modal following muncul
            except Exception as e:
                 print(f"Gagal mengklik koordinat: {e}. Mencoba cara alternatif...")
                 # === CARA 2: Klik Link "Following" (LEBIH STABIL) ===
                 try:
                     print("Mencari link 'following'...")
                     # Selector ini mungkin perlu disesuaikan jika Instagram berubah
                     following_link_xpath = f"//a[contains(@href,'/{username}/following/')]"
                     following_link = WebDriverWait(driver, 15).until(
                         EC.element_to_be_clickable((By.XPATH, following_link_xpath))
                     )
                     print("Link 'following' ditemukan, mengklik...")
                     following_link.click()
                     print("Daftar 'Following' dibuka via link.")
                     time.sleep(1) # Tunggu modal following muncul
                 except (NoSuchElementException, TimeoutException) as e_link:
                     print(f"Gagal menemukan atau mengklik link 'following': {e_link}")
                     print("Tidak bisa membuka daftar following. Iterasi dibatalkan.")
                     continue # Lanjut ke iterasi berikutnya jika gagal buka daftar

            # 3. Cari tombol "Following" / "Diikuti" di dalam modal/list
            print(f"Mencari tombol 'Diikuti' dengan selector: {FOLLOWING_BUTTON_SELECTOR}")
            # Mungkin perlu scroll sedikit jika tombol pertama tidak terlihat
            # driver.execute_script("window.scrollBy(0, 250);") # Contoh scroll
            # time.sleep(1)

            # Cari tombol PERTAMA yang cocok di dalam modal yang muncul
            following_button = WebDriverWait(driver, 20).until(
                 # Pastikan mencari di dalam konteks modal jika memungkinkan,
                 # atau gunakan selector yang lebih spesifik.
                 # Untuk sekarang, kita cari di seluruh halaman setelah modal terbuka.
                 EC.element_to_be_clickable((By.CSS_SELECTOR, FOLLOWING_BUTTON_SELECTOR))
            )
            print("Tombol 'Diikuti' ditemukan.")
            time.sleep(1)

            # 4. Klik tombol "Following" / "Diikuti"
            print("Mengklik tombol 'Diikuti'...")
            following_button.click()
            time.sleep(1) # Tunggu pop-up konfirmasi muncul

            # 5. Cari tombol konfirmasi "Unfollow" / "Batal mengikuti"
            print(f"Mencari tombol konfirmasi 'Batal mengikuti' dengan selector: {UNFOLLOW_CONFIRM_BUTTON_SELECTOR}")
            unfollow_confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, UNFOLLOW_CONFIRM_BUTTON_SELECTOR))
            )
            print("Tombol konfirmasi 'Batal mengikuti' ditemukan.")
            time.sleep(1)

            # 6. Klik tombol konfirmasi "Unfollow" / "Batal mengikuti"
            print("Mengklik tombol konfirmasi 'Batal mengikuti'...")
            unfollow_confirm_button.click()
            unfollowed_count += 1
            print(f"Berhasil unfollow 1 orang. Total: {unfollowed_count}")

            # 7. Refresh Halaman (Sesuai Permintaan - Tidak Efisien)
            print("Merefresh halaman...")
            driver.refresh()
            print("Menunggu halaman refresh...")
            time.sleep(1) # Beri jeda panjang setelah refresh

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Gagal pada iterasi {i+1}: Elemen tidak ditemukan atau timeout.")
            print(f"Error: {e}")
            print("Mungkin selector perlu diperbarui atau halaman tidak memuat dengan benar.")
            print("Mencoba refresh dan lanjut ke iterasi berikutnya...")
            driver.refresh() # Coba refresh jika gagal di tengah jalan
            time.sleep(1)
            continue # Lanjut ke iterasi berikutnya
        except Exception as e:
            print(f"Terjadi kesalahan tidak terduga pada iterasi {i+1}: {e}")
            print("Mencoba refresh dan lanjut...")
            driver.refresh()
            time.sleep(1)
            continue

    print(f"\nSelesai. Total {unfollowed_count} orang di-unfollow dalam sesi ini.")

# --- Main Execution ---
if __name__ == "__main__":
    # Setup WebDriver
    service = Service(WEBDRIVER_PATH)
    options = webdriver.ChromeOptions() # Ganti ke FirefoxOptions jika pakai GeckoDriver
    # options.add_argument("--headless")  # Jalankan tanpa membuka jendela browser (opsional)
    # options.add_argument("--disable-gpu") # Terkadang diperlukan di beberapa sistem
    # options.add_argument("--no-sandbox") # Terkadang diperlukan di Linux
    # options.add_argument("--disable-dev-shm-usage") # Mengatasi masalah resource terbatas

    driver = None # Inisialisasi driver
    try:
        driver = webdriver.Chrome(service=service, options=options) # Ganti ke Firefox jika perlu
        driver.implicitly_wait(5) # Waktu tunggu implisit singkat
        driver.maximize_window()

        # Login
        if login_instagram(driver, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD):
            # Jeda setelah login berhasil
            time.sleep(1)
            # Mulai proses unfollow
            unfollow_users(driver, INSTAGRAM_USERNAME, MAX_UNFOLLOWS)
        else:
            print("Login gagal. Skrip dihentikan.")

    except Exception as e:
        print(f"Terjadi kesalahan utama: {e}")

    finally:
        # Selalu tutup browser di akhir
        if driver:
            print("Menutup browser...")
            driver.quit()
        print("Skrip selesai.")
