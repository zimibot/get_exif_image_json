## Nama Proyek

Script Python untuk Mendapatkan Informasi EXIF dari Gambar dan Menyimpannya dalam Format JSON

## Deskripsi

Script ini adalah sebuah program Python yang digunakan untuk mendapatkan informasi EXIF (Exchangeable Image File Format) dari gambar dengan ekstensi `.jpg`, `.jpeg`, `.png`, dan `.webp`. Informasi EXIF yang diambil meliputi metadata seperti nama file, ukuran file, ukuran gambar, mode gambar, dan koordinat geografis jika tersedia.

Setelah mengumpulkan informasi EXIF dari semua gambar yang ditemukan dalam direktori, script akan mengelompokkan informasi tersebut berdasarkan ekstensi file dan metode yang digunakan (exifread, piexif, Pillow, dan OpenCV). Hasilnya akan disimpan dalam format JSON dan tersedia dalam direktori "output" di direktori saat ini.

## Cara Penggunaan

1. Pastikan Python telah terinstal di sistem Anda.
2. Clone repositori ini ke direktori lokal Anda atau unduh sebagai ZIP dan ekstrak ke direktori lokal.
3. Buka terminal atau command prompt dan pindah ke direktori proyek.

### Menyiapkan Lingkungan

4. Buat virtual environment baru (opsional):

   ```bash
   python -m venv env
   ```

5. Aktifkan virtual environment (opsional):

   - Windows:

     ```bash
     env\Scripts\activate
     ```

   - macOS/Linux:

     ```bash
     source env/bin/activate
     ```

### Instalasi Dependensi

6. Install dependensi yang dibutuhkan:

   ```bash
   pip install -r requirements.txt
   ```

### Menjalankan Script

7. Pastikan Anda memiliki gambar dengan ekstensi `.jpg`, `.jpeg`, `.png`, atau `.webp` dalam direktori "gambar".
8. Jalankan script dengan perintah berikut:

   ```bash
   python image_exif_info.py
   ```

9. Script akan menampilkan nama-nama gambar yang ditemukan dan informasi EXIF yang diambil dari setiap gambar.
10. Setelah selesai, informasi gambar yang dikelompokkan akan disimpan dalam file JSON dengan nama "example_result.json" di direktori "output".

## Kontribusi

Kontribusi terbuka untuk perbaikan atau peningkatan skrip ini. Jika Anda ingin berkontribusi, silakan buat *pull request* pada repositori ini.
