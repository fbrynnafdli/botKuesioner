import csv
import time
import random 
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 

# Tentukan nama file
nama_file_csv = 'data_siswa.csv' 
url_form = "https://docs.google.com/forms/d/e/1FAIpQLSdwq8GHLdZ3GKCuAKlo4vzdu6qrlfb81nanTeGdo36aO27vxw/viewform?usp=dialog"

# Buka browser menggunakan undetected-chromedriver
driver = uc.Chrome(version_main=147)

# Buka halaman login / form
driver.get(url_form)

# --- TRIK JEDA LOGIN ---
print("\n" + "="*50)
print("BROWSER SEDANG TERBUKA!")
print("1. Silakan login ke akun Google kamu secara manual di browser.")
print("2. Jika sudah berhasil login dan FORM SUDAH MUNCUL, kembali ke layar hitam ini.")
print("3. Tekan ENTER di sini untuk mulai menjalankan bot!")
print("="*50 + "\n")

input("Tekan ENTER jika sudah siap...") 

# Buka dan baca file CSV 
with open(nama_file_csv, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter=';') 
    
    for baris_data in csv_reader:
        nama_tester = baris_data['nama']
        email_tester = baris_data['email']
        
        print(f"--- Mengisi data untuk: {nama_tester} ---")
        
        try:
            # Cari elemen kolom Email dan ketikkan
            kolom_email = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input')
            kolom_email.send_keys(email_tester)
            
            # Cari elemen kolom Nama dan ketikkan
            kolom_nama = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            kolom_nama.send_keys(nama_tester)
            
            # --- FUNGSI NINJA ACAK JAWABAN (UPGRADE LIKERT 4-5 & UMUR) ---
            def isi_semua_pilihan_ganda():
                time.sleep(1) # Tunggu elemen muncul
                # Cari semua blok pertanyaan di halaman aktif
                semua_pertanyaan = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]')
                for pertanyaan in semua_pertanyaan:
                    # Cari bulatan jawaban di dalam pertanyaan
                    opsi_jawaban = pertanyaan.find_elements(By.XPATH, './/div[@role="radio"]')
                    
                    if opsi_jawaban:
                        jawaban_terpilih = None
                        
                        # LOGIKA 1: CEK PERTANYAAN UMUR (Pilihan Ganda)
                        # Mencari opsi yang kata-katanya mengandung angka "14" dan "29"
                        for opsi in opsi_jawaban:
                            teks_opsi = str(opsi.get_attribute("data-value")).lower()
                            if "14" in teks_opsi and "29" in teks_opsi:
                                jawaban_terpilih = opsi
                                break
                        
                        # LOGIKA 2: SKALA LIKERT ATAU DEMOGRAFI LAINNYA
                        if jawaban_terpilih is None:
                            jumlah_opsi = len(opsi_jawaban)
                            
                            # Jika opsinya ada 4 atau 5 (Biasanya Skala Likert)
                            if jumlah_opsi >= 4:
                                # Ambil 2 opsi paling akhir saja (opsi 4 atau 5)
                                jawaban_terpilih = random.choice(opsi_jawaban[-2:])
                            else:
                                # Jika opsinya sedikit (misal Jenis Kelamin 2 opsi), acak semua
                                jawaban_terpilih = random.choice(opsi_jawaban)
                        
                        # Klik jawaban yang terpilih
                        driver.execute_script("arguments[0].click();", jawaban_terpilih)
                        time.sleep(0.2)
            
            # Eksekusi isi jawaban untuk halaman pertama
            isi_semua_pilihan_ganda()
            
            # --- LOOPING PINDAH HALAMAN ---
            while True:
                # Cek apakah ada tombol "Berikutnya" (Next)
                tombol_next = driver.find_elements(By.XPATH, '//span[contains(text(),"Berikutnya") or contains(text(),"Next")]/ancestor::div[@role="button"]')
                
                if len(tombol_next) > 0:
                    # Klik tombol Berikutnya
                    driver.execute_script("arguments[0].click();", tombol_next[0])
                    time.sleep(1.5) # Tunggu loading halaman baru
                    
                    # Isi otomatis di halaman baru ini
                    isi_semua_pilihan_ganda()
                else:
                    break # Berhenti kalau sudah mentok di halaman terakhir
            
            # Cari dan klik tombol Submit/Kirim di halaman paling akhir
            tombol_submit = driver.find_element(By.XPATH, '//span[contains(text(),"Kirim") or contains(text(),"Submit")]/ancestor::div[@role="button"]')
            driver.execute_script("arguments[0].click();", tombol_submit)
            
            time.sleep(2) # Tunggu loading submit selesai
            print(f"Submit sukses untuk {nama_tester}!\n")
            
            # Kembali ke halaman form kosong untuk data selanjutnya
            driver.get(url_form)
            time.sleep(2)
            
        except Exception as e:
            print(f"Terjadi error saat memproses {nama_tester}: {e}\n")
            driver.get(url_form)
            time.sleep(2)

print("Semua data selesai diproses!")
driver.quit()