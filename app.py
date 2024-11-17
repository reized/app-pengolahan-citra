import streamlit as st
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Image Processing with RGB Sliders and Histogram")

# Sidebar untuk memilih fitur
feature = st.sidebar.selectbox(
    "Choose a feature",
    ("Upload Image", "Grayscale", "Edge Detection", "RGB Adjustment", "Negative", "Smoothing", "Salt & Pepper")
)

# Fungsi untuk meng-upload gambar
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Menampilkan gambar yang di-upload
    image = Image.open(uploaded_file)
    image_array = np.array(image)

    # Fungsi untuk menampilkan histogram
    def plot_histogram(image, title="Histogram"):
        fig, ax = plt.subplots()
        if len(image.shape) == 2:  # Grayscale
            ax.hist(image.ravel(), bins=256, color='gray')
        else:  # RGB
            colors = ('r', 'g', 'b')
            for i, color in enumerate(colors):
                ax.hist(image[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
        ax.set_title(title)
        ax.set_xlabel("Pixel Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # Layout kolom untuk gambar asli dan hasil pengolahan
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image, caption="Original Image", use_column_width=True)
        st.write("Histogram of Original Image")
        plot_histogram(image_array, "Histogram - Original Image")

    # Fitur berdasarkan pilihan pengguna
    if feature == "Grayscale":
        # Konversi ke grayscale
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        with col2:
            st.image(gray_image, caption="Grayscale Image", use_column_width=True)
            st.write("Histogram of Grayscale Image")
            plot_histogram(gray_image, "Histogram - Grayscale")

    elif feature == "Edge Detection":
        # Slider untuk threshold deteksi tepi Canny
        threshold1 = st.sidebar.slider("Threshold 1", min_value=0, max_value=255, value=100)
        threshold2 = st.sidebar.slider("Threshold 2", min_value=0, max_value=255, value=200)

        # Konversi ke grayscale sebelum deteksi tepi
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Deteksi tepi
        edges = cv2.Canny(gray_image, threshold1=threshold1, threshold2=threshold2)
        with col2:
            st.image(edges, caption="Edge Detection", use_column_width=True)
            st.write("Histogram of Edge Detection")
            plot_histogram(edges, "Histogram - Edge Detection")

    elif feature == "RGB Adjustment":
        # Slider untuk mengatur intensitas masing-masing kanal RGB
        r_factor = st.sidebar.slider("Red Intensity", min_value=0, max_value=255, value=255)
        g_factor = st.sidebar.slider("Green Intensity", min_value=0, max_value=255, value=255)
        b_factor = st.sidebar.slider("Blue Intensity", min_value=0, max_value=255, value=255)

        # Mengubah intensitas kanal warna
        adjusted_image = image_array.copy()
        adjusted_image[:, :, 0] = np.clip(adjusted_image[:, :, 0] * (r_factor / 255), 0, 255)
        adjusted_image[:, :, 1] = np.clip(adjusted_image[:, :, 1] * (g_factor / 255), 0, 255)
        adjusted_image[:, :, 2] = np.clip(adjusted_image[:, :, 2] * (b_factor / 255), 0, 255)

        with col2:
            st.image(adjusted_image.astype(np.uint8), caption="RGB Adjusted Image", use_column_width=True)
            st.write("Histogram of RGB Adjusted Image")
            plot_histogram(adjusted_image, "Histogram - RGB Adjusted Image")

    elif feature == "Negative":
        # Membuat efek negatif pada gambar
        negative_image = 255 - image_array
        with col2:
            st.image(negative_image, caption="Negative Image", use_column_width=True)
            st.write("Histogram of Negative Image")
            plot_histogram(negative_image, "Histogram - Negative")


    elif feature == "Smoothing":
        # Slider untuk mengatur ukuran kernel smoothing
        kernel_size = st.sidebar.slider("Kernel Size", min_value=1, max_value=15, value=5, step=2)
    
        # Melakukan smoothing (blur) menggunakan GaussianBlur
        smoothed_image = cv2.GaussianBlur(image_array, (kernel_size, kernel_size), 0)
        
        # Pastikan hasil smoothing tetap dalam tipe uint8
        smoothed_image = np.clip(smoothed_image, 0, 255).astype(np.uint8)
        
        with col2:
            st.image(smoothed_image, caption="Smoothed Image", use_column_width=True)
            st.write("Histogram of Smoothed Image")
            plot_histogram(smoothed_image, "Histogram - Smoothed")


    elif feature == "Salt & Pepper":
        # Slider untuk mengatur proporsi noise
        noise_prob = st.sidebar.slider("Noise Probability", min_value=0.01, max_value=0.1, value=0.05)

        # Menambahkan noise salt & pepper
        noisy_image = image_array.copy()
        total_pixels = noisy_image.size // noisy_image.shape[-1]
        num_salt = int(noise_prob * total_pixels / 2)
        num_pepper = int(noise_prob * total_pixels / 2)

        # Menambahkan salt (putih)
        coords = [np.random.randint(0, i - 1, num_salt) for i in noisy_image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 255

        # Menambahkan pepper (hitam)
        coords = [np.random.randint(0, i - 1, num_pepper) for i in noisy_image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 0

        with col2:
            st.image(noisy_image, caption="Salt & Pepper Noise Image", use_column_width=True)
            st.write("Histogram of Salt & Pepper Image")
            plot_histogram(noisy_image, "Histogram - Salt & Pepper")
