# **Image Processing App**

Aplikasi ini memungkinkan pengguna untuk mengunggah gambar, memprosesnya dengan berbagai efek seperti Grayscale, Edge Detection, Sharpness, dan lainnya, serta menampilkan histogram gambar asli dan hasil pemrosesan. Aplikasi ini juga menyediakan opsi untuk mengakses kamera langsung dan memproses gambar secara real-time.

## **Fitur**
- Unggah gambar untuk pemrosesan
- Akses kamera langsung untuk pemrosesan real-time
- Pilihan efek pemrosesan gambar (Grayscale, Edge Detection, Negative, Gaussian Blur, RGB Adjustment, dan banyak lagi)
- Tampilan histogram untuk gambar asli dan hasil pemrosesan
- Download hasil pemrosesan sebagai gambar

## **Prasyarat**
Pastikan Anda memiliki dependensi berikut untuk menjalankan aplikasi ini:
- Python 3.x
- Streamlit
- OpenCV
- Pillow
- Matplotlib

### **Cara Install**

1. **Clone repository** atau download project ini:
   ```bash
   git clone https://github.com/reized/app-pengolahan-citra.git
   cd app-pengolahan-citra
   ```

2. Set Up a **Virtual Environment**:
    ```bash
    python -m venv venv

    # On Windows
    venv\Scripts\activate
    ```

3. **Install dependensi** dengan pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan aplikasi**:
    ```bash
    streamlit run app.py
    ```

## **Cara Menggunakan Aplikasi**

### 1. **Tab Upload Image**
- Klik tombol **"Choose an image..."** untuk mengunggah gambar dari perangkat Anda.
- Setelah gambar diunggah, aplikasi akan memproses gambar tersebut sesuai dengan efek yang dipilih dari sidebar (misalnya, Grayscale, Edge Detection, dll).
- Gambar asli dan gambar yang sudah diproses akan ditampilkan berdampingan, serta histogram dari kedua gambar.
- Anda dapat mendownload hasil pemrosesan gambar dengan menekan tombol **Download**.

### 2. **Tab Live Camera**
- Pilih checkbox **"Start Camera"** untuk mengakses kamera perangkat Anda.
- Kamera akan mulai menampilkan video langsung, dan gambar yang ditangkap akan diproses sesuai dengan efek yang dipilih.
- Gambar asli dan gambar yang sudah diproses akan ditampilkan bersama histogram secara real-time.
- Pastikan Anda memberikan izin akses kamera pada browser jika diminta.

### 3. **Fitur Sidebar**
- Pilih efek pemrosesan yang diinginkan dari dropdown di sidebar:
  - **Grayscale**
  - **Edge Detection**
  - **Negative**
  - **Gaussian Blur**
  - **Salt & Pepper**
  - **RGB Adjustment**
  - **Brightness**
  - **Sharpness**
  - **Equalization**
  - **Rotate**
  - **Flip**
- Beberapa efek juga memiliki parameter tambahan seperti threshold atau ukuran kernel yang dapat diatur menggunakan slider.

---

## **Akses Kamera**
- Jika Anda mengakses aplikasi melalui browser, pastikan Anda memberikan izin untuk menggunakan kamera perangkat.

---

## **Download Hasil Gambar**
- Setelah gambar diproses, Anda dapat mengunduhnya dengan menekan tombol **Download** yang akan mengunduh gambar hasil pemrosesan ke komputer Anda.