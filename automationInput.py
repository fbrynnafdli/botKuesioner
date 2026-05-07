import csv
import time
import random 
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 

# Tentukan nama file
nama_file_csv = 'data_siswa.csv' 
url_form = "link google form sia deung"

# PENGATURAN BROWSER UNTUK LAPTOP (WINDOWS)
driver = uc.Chrome(version_main=147)

print("\n🚀 Bot mulai berjalan...\n")

# Buka dan baca file CSV 
with open(nama_file_csv, mode='r', encoding='utf-8') as file:
    # delimiter sesuaikan dengan komputermu, bisa titik koma (;) atau koma (,)
    csv_reader = csv.DictReader(file, delimiter=';') 
    
    for baris_data in csv_reader:
        nama_tester = baris_data['nama']
        email_tester = baris_data['email']
        
        # Mengambil data jenis kelamin dari CSV (Pastikan nama kolomnya benar 'jenis_kelamin')
        gender_tester = baris_data['jenis_kelamin']
        
        print(f"--- Mengisi data untuk: {nama_tester} | {gender_tester} ---")
        
        try:
            driver.get(url_form)
            time.sleep(3) # Tunggu form termuat
            
            # Cari elemen kolom Email dan ketikkan
            kolom_email = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input')
            kolom_email.send_keys(email_tester)
            
            # Cari elemen kolom Nama dan ketikkan
            kolom_nama = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            kolom_nama.send_keys(nama_tester)
            
            # --- FUNGSI NINJA ACAK & DETEKSI GENDER ---
            # Kita melempar data gender_tester ke dalam fungsi ini
            def isi_semua_pilihan_ganda(target_gender):
                time.sleep(1) 
                semua_pertanyaan = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]')
                for pertanyaan in semua_pertanyaan:
                    opsi_jawaban = pertanyaan.find_elements(By.XPATH, './/div[@role="radio"]')
                    
                    if opsi_jawaban:
                        jawaban_terpilih = None
                        
                        # Ambil semua teks opsi di pertanyaan ini untuk dicek
                        teks_semua_opsi = [str(opsi.get_attribute("data-value")).lower() for opsi in opsi_jawaban]
                        gabungan_teks = " ".join(teks_semua_opsi)
                        
                        # LOGIKA 1: CEK PERTANYAAN UMUR
                        for opsi in opsi_jawaban:
                            teks_opsi = str(opsi.get_attribute("data-value")).lower()
                            if "14" in teks_opsi and "29" in teks_opsi:
                                jawaban_terpilih = opsi
                                break
                        
                        # LOGIKA 2: CEK PERTANYAAN JENIS KELAMIN
                        # Jika di pertanyaan ini ada kata laki/perempuan/pria/wanita
                        if jawaban_terpilih is None and ("laki" in gabungan_teks or "perempuan" in gabungan_teks or "pria" in gabungan_teks or "wanita" in gabungan_teks):
                            for opsi in opsi_jawaban:
                                teks_opsi = str(opsi.get_attribute("data-value")).lower()
                                # Tambahkan pengecekan apakah target_gender tidak kosong
                                if target_gender.strip() != "" and target_gender.lower() in teks_opsi:
                                    jawaban_terpilih = opsi
                                    break
                                    
#                        LOGIKA 3: ACAK SEMUA PILIHAN (LIKERT & DEMOGRAFI)
                        if jawaban_terpilih is None:
                            jawaban_terpilih = random.choice(opsi_jawaban)
                        # Jika bot sudah menentukan pilihan, klik jawabannya
                        if jawaban_terpilih:
                            driver.execute_script("arguments[0].click();", jawaban_terpilih)
                            time.sleep(0.2)
            
            # Eksekusi isi kuesioner sambil membawa data target gender
            isi_semua_pilihan_ganda(gender_tester)
            
            # --- LOOPING PINDAH HALAMAN ---
            while True:
                tombol_next = driver.find_elements(By.XPATH, '//span[contains(text(),"Berikutnya") or contains(text(),"Next")]/ancestor::div[@role="button"]')
                
                if len(tombol_next) > 0:
                    driver.execute_script("arguments[0].click();", tombol_next[0])
                    time.sleep(1.5) 
                    isi_semua_pilihan_ganda(gender_tester)
                else:
                    break 
            
            # Tombol Submit
            tombol_submit = driver.find_element(By.XPATH, '//span[contains(text(),"Kirim") or contains(text(),"Submit")]/ancestor::div[@role="button"]')
            driver.execute_script("arguments[0].click();", tombol_submit)
            
            time.sleep(2) 
            print(f"✅ Submit sukses!\n")
            
        except Exception as e:
            print(f"❌ Terjadi error: {e}\n")

print("🎉 Semua data selesai diproses!")
driver.quit()