import csv
import time
import random 
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc 

# Tentukan nama file
nama_file_csv = 'data_responden.csv' 
url_form = "link google form sia deung"

# PENGATURAN BROWSER UNTUK LAPTOP (WINDOWS)
driver = uc.Chrome(version_main=147)

print("\n🚀 Bot berjalan dengan mode santai...\n")

with open(nama_file_csv, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file, delimiter=';') 
    
    for baris_data in csv_reader:
        nama_tester = baris_data['nama']
        email_tester = baris_data['email']
        gender_tester = baris_data['jenis_kelamin']
        
        print(f"--- Mengisi data untuk: {nama_tester} | {gender_tester} ---")
        
        try:
            driver.get(url_form)
            # Jeda awal loading form (3 sampai 5 detik)
            time.sleep(random.uniform(3.0, 5.0)) 
            
            # Cari elemen kolom Email dan ketikkan
            kolom_email = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/input')
            kolom_email.send_keys(email_tester)
            time.sleep(random.uniform(0.5, 1.5)) # Jeda ngetik email ke nama
            
            # Cari elemen kolom Nama dan ketikkan
            kolom_nama = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            kolom_nama.send_keys(nama_tester)
            time.sleep(random.uniform(1.0, 2.0))
            
            # --- FUNGSI NINJA ---
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
                        
                        # LOGIKA 1: CEK PERTANYAAN UMUR (Lock 14-29)
                        for opsi in opsi_jawaban:
                            teks_opsi = str(opsi.get_attribute("data-value")).lower()
                            if "14" in teks_opsi and "29" in teks_opsi:
                                jawaban_terpilih = opsi
                                break
                        
                        # LOGIKA 2: CEK PERTANYAAN JENIS KELAMIN
                        if jawaban_terpilih is None and ("laki" in gabungan_teks or "perempuan" in gabungan_teks or "pria" in gabungan_teks or "wanita" in gabungan_teks):
                            for opsi in opsi_jawaban:
                                teks_opsi = str(opsi.get_attribute("data-value")).lower()
                                if target_gender.strip() != "" and target_gender.lower() in teks_opsi:
                                    jawaban_terpilih = opsi
                                    break
                                    
                        # LOGIKA 3: CEK PENDIDIKAN (Lock SMA/SMK/Sederajat)
                        # Pastikan ini pertanyaan pendidikan dengan mendeteksi kata-kata khas pendidikan
                        if jawaban_terpilih is None and ("smp" in gabungan_teks or "sma" in gabungan_teks or "smk" in gabungan_teks or "sarjana" in gabungan_teks or "diploma" in gabungan_teks):
                            for opsi in opsi_jawaban:
                                teks_opsi = str(opsi.get_attribute("data-value")).lower()
                                if "sma" in teks_opsi or "smk" in teks_opsi or "sederajat" in teks_opsi:
                                    jawaban_terpilih = opsi
                                    break
                                    
                        # LOGIKA 4: ACAK SEMUA PILIHAN (LIKERT & SISA DEMOGRAFI)
                        if jawaban_terpilih is None:
                            jawaban_terpilih = random.choice(opsi_jawaban)
                        
                        # Jika bot sudah menentukan pilihan, klik jawabannya
                        if jawaban_terpilih:
                            driver.execute_script("arguments[0].click();", jawaban_terpilih)
                            
                            # JEDA ACAK NATURAL ANTAR JAWABAN (1.5 sampai 3.5 detik)
                            time.sleep(random.uniform(1.5, 3.5))
            
            # Eksekusi isi kuesioner halaman 1
            isi_semua_pilihan_ganda(gender_tester)
            
            # --- LOOPING PINDAH HALAMAN ---
            while True:
                tombol_next = driver.find_elements(By.XPATH, '//span[contains(text(),"Berikutnya") or contains(text(),"Next")]/ancestor::div[@role="button"]')
                
                if len(tombol_next) > 0:
                    driver.execute_script("arguments[0].click();", tombol_next[0])
                    # Jeda agak lama saat pindah halaman (kayak nunggu loading halaman baru)
                    time.sleep(random.uniform(2.5, 4.5)) 
                    isi_semua_pilihan_ganda(gender_tester)
                else:
                    break 
            
            # Tombol Submit
            tombol_submit = driver.find_element(By.XPATH, '//span[contains(text(),"Kirim") or contains(text(),"Submit")]/ancestor::div[@role="button"]')
            time.sleep(random.uniform(1.0, 2.0)) # Jeda mikir bentar sebelum klik kirim
            driver.execute_script("arguments[0].click();", tombol_submit)
            
            time.sleep(3) 
            print(f"✅ Submit sukses!\n")
            
        except Exception as e:
            print(f"❌ Terjadi error: {e}\n")

print("🎉 Semua data selesai diproses!")
driver.quit()