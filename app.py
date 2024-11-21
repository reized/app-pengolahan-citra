import streamlit as st
import cv2
import io
from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Image Processing App")

# Pilih tab upload atau kamera
tabs = st.tabs(["Upload Image", "Live Camera"])

# Sidebar untuk memilih fitur
feature = st.sidebar.selectbox(
    "Choose a feature",
    ("Default", "Grayscale", "Edge Detection", "Negative", "Gaussian Blur", "Salt & Pepper", "RGB Adjustment", "Brightness", "Sharpness", "Equalization", "Rotate", "Flip")
)

# Parameter sidebar
params = {}
if feature == "Edge Detection":
    params["threshold1"] = st.sidebar.slider("Threshold 1", 0, 255, 100, key="threshold1_edge")
    params["threshold2"] = st.sidebar.slider("Threshold 2", 0, 255, 200, key="threshold2_edge")
elif feature in ["Gaussian Blur"]:
    params["kernel_size"] = st.sidebar.slider("Kernel Size", 3, 15, step=2, value=5, key="kernel_size_blur")
elif feature == "Salt & Pepper":
    params["noise_prob"] = st.sidebar.slider("Noise Probability", 0.01, 0.1, 0.05, key="noise_prob_salt_pepper")
elif feature == "RGB Adjustment":
    params["r_factor"] = st.sidebar.slider("Red Intensity", 0, 255, 255, key="red_intensity")
    params["g_factor"] = st.sidebar.slider("Green Intensity", 0, 255, 255, key="green_intensity")
    params["b_factor"] = st.sidebar.slider("Blue Intensity", 0, 255, 255, key="blue_intensity")
elif feature == "Brightness":
    params["brightness_factor"] = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, key="brightness_factor")
elif feature == "Sharpness":
    params["sharpness_factor"] = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0, key="sharpness_factor")
elif feature == "Rotate":
    params["angle"] = st.sidebar.slider("Rotation Angle", 0, 360, 0, key="rotation_angle")
elif feature == "Flip":
    params["flip_type"] = st.sidebar.selectbox("Flip Type", ["Horizontal", "Vertical", "Both"], key="flip_type")

# Fungsi untuk memproses gambar
def process_image(image, feature, params=None):
    if feature == "Default":
        return image
    elif feature == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif feature == "Edge Detection":
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return cv2.Canny(gray_image, params["threshold1"], params["threshold2"])
    elif feature == "Negative":
        return 255 - image
    elif feature in ["Gaussian Blur"]:
        return cv2.GaussianBlur(image, (params["kernel_size"], params["kernel_size"]), 0)
    elif feature == "Salt & Pepper":
        noisy_image = image.copy()
        total_pixels = noisy_image.size // noisy_image.shape[-1]
        num_salt = int(params["noise_prob"] * total_pixels / 2)
        num_pepper = int(params["noise_prob"] * total_pixels / 2)
        coords = [np.random.randint(0, i - 1, num_salt) for i in noisy_image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 255
        coords = [np.random.randint(0, i - 1, num_pepper) for i in noisy_image.shape[:2]]
        noisy_image[coords[0], coords[1], :] = 0
        return noisy_image
    elif feature == "RGB Adjustment":
        adjusted_image = image.copy()
        adjusted_image[:, :, 0] = np.clip(adjusted_image[:, :, 0] * (params["r_factor"] / 255), 0, 255)
        adjusted_image[:, :, 1] = np.clip(adjusted_image[:, :, 1] * (params["g_factor"] / 255), 0, 255)
        adjusted_image[:, :, 2] = np.clip(adjusted_image[:, :, 2] * (params["b_factor"] / 255), 0, 255)
        return adjusted_image
    elif feature == "Brightness":
        enhancer = ImageEnhance.Brightness(Image.fromarray(image))
        return np.array(enhancer.enhance(params["brightness_factor"]))
    elif feature == "Sharpness":
        enhancer = ImageEnhance.Sharpness(Image.fromarray(image))
        return np.array(enhancer.enhance(params["sharpness_factor"]))
    elif feature == "Equalization":
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return cv2.equalizeHist(gray_image)
    elif feature == "Rotate":
        return np.array(Image.fromarray(image).rotate(params["angle"]))
    elif feature == "Flip":
        flip_type = params["flip_type"]
        if flip_type == "Horizontal":
            return cv2.flip(image, 1)
        elif flip_type == "Vertical":
            return cv2.flip(image, 0)
        elif flip_type == "Both":
            return cv2.flip(image, -1)

# Fungsi untuk menampilkan histogram
def show_histogram(image, title=None):
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

# Tab 1: Upload Image
with tabs[0]:
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        image_array = np.array(image)
        processed_image = process_image(image_array, feature, params)

        col1, col2 = st.columns(2)
        with col1:
            st.write("Original Image")
            st.image(image, use_container_width=True)
            st.write("Histogram - Original Image")
            show_histogram(image_array, title="Histogram - Original Image")
        with col2:
            st.write(f"Processed Image - {feature}")
            if len(processed_image.shape) == 2:  # Grayscale
                st.image(processed_image, use_container_width=True, clamp=True, channels="GRAY")
            else:
                st.image(processed_image, use_container_width=True) 
            st.write(f"Histogram - {feature}")
            show_histogram(processed_image, title=f"Histogram - {feature}")

        # Tombol download menggunakan BytesIO
        processed_image_pil = Image.fromarray(processed_image)
        buf = io.BytesIO()
        processed_image_pil.save(buf, format="PNG")
        buf.seek(0)

        st.download_button(
            label="Download Processed Image",
            data=buf,
            file_name=f"processed_image_{feature}.png",
            mime="image/png"
        )

# Tab 2: Live Camera
with tabs[1]:
    run_camera = st.checkbox("Start Camera")

    if run_camera:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Cannot access the camera.")
        else:
            placeholder = st.empty()

            while run_camera:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to capture image from the camera.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                processed_frame = process_image(frame_rgb, feature, params)

                with placeholder.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Original Image")
                        st.image(frame_rgb, channels="RGB", use_container_width=True)
                        st.write("Histogram - Original Image")
                        show_histogram(frame_rgb, title="Histogram - Original Image")
                    with col2:
                        st.write(f"Processed Image - {feature}")
                        if len(processed_frame.shape) == 2:  # Grayscale
                            st.image(processed_frame, use_container_width=True, clamp=True, channels="GRAY")
                        else:
                            st.image(processed_frame, channels="RGB", use_container_width=True)
                        st.write(f"Histogram - {feature}")
                        show_histogram(processed_frame, title=f"Histogram - {feature}")

            cap.release()

            # Tombol download untuk frame terakhir yang diproses menggunakan BytesIO
            if processed_frame is not None:
                processed_frame_pil = Image.fromarray(processed_frame)
                buf = io.BytesIO()
                processed_frame_pil.save(buf, format="PNG")
                buf.seek(0)

                st.download_button(
                    label="Download Last Processed Frame",
                    data=buf,
                    file_name=f"processed_frame_{feature}.png",
                    mime="image/png"
                )

            st.stop()