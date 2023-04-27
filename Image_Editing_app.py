import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
from io import BytesIO

def apply_enhancements(our_image, enhance_type):
    img = np.array(our_image.convert("RGB"))
    if "Gray-Scale" in enhance_type:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if "Contrast" in enhance_type:
        rate = st.sidebar.slider("Contrast", 0.1, 6.0)  # Use only float numbers
        enhancer = ImageEnhance.Contrast(Image.fromarray(img))
        img = np.array(enhancer.enhance(rate))
    if "Brightness" in enhance_type:
        rate = st.sidebar.slider("Brightness", 0.1, 10.0)
        enhancer = ImageEnhance.Brightness(Image.fromarray(img))
        img = np.array(enhancer.enhance(rate))
    if "Sharpness" in enhance_type:
        rate = st.sidebar.slider("Sharpness", 0.1, 10.0)
        enhancer = ImageEnhance.Sharpness(Image.fromarray(img))
        img = np.array(enhancer.enhance(rate))
    if "Shadow & Blur" in enhance_type:
        alpha = st.sidebar.slider("Shadow intensity", 1.0, 7.0)
        kernel_size = st.sidebar.slider("Blur", 3, 21, step=2)
        kernel = np.zeros((kernel_size, kernel_size), np.float32)
        kernel.fill(1.0 / (kernel_size * kernel_size))
        shadow = cv2.filter2D(img, -1, kernel)
        img = cv2.addWeighted(img, 1 - alpha, shadow, alpha, 0)
    if "Rotate" in enhance_type:
        angle = st.sidebar.slider("Rotation angle",0, 180)
        rows, cols, _ = img.shape
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        img = cv2.warpAffine(img, M, (cols, rows))
    return img


def cannanize_image(our_image):
    new_img = np.array(our_image.convert("RGB"))
    img = cv2.GaussianBlur(new_img, (13, 13), 0)  # 0 is Standard Deviation and Kernel should be odd
    canny = cv2.Canny(img, 100, 150)
    return canny
def cartoonize_image(our_image):
    img = np.array(our_image.convert('RGB'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

st.title('Image Editing App')
st.text("Edit your images in a fast and simple way")
activities = ["Detection", "About"]
choice = st.sidebar.selectbox("Select Activity", activities)

if choice == "Detection":
    st.subheader("Detection")
    image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png","heic"])

    if image_file is not None:
        our_image = Image.open(image_file)
        st.text("Original Image")
        st.image(our_image)

        enhance_type = st.sidebar.multiselect("Enhance type",["Original-Compressed", "Gray-Scale", "Contrast", "Brightness", "Sharpness", "Rotate", "Shadow & Blur"])
        enhanced_img = apply_enhancements(our_image, enhance_type)
        st.text("Enhanced Image")
        st.image(enhanced_img)


    tasks = ["Cartoonize","Edging"]
    feature_choice = st.sidebar.selectbox("Find features", tasks)
    if st.button("Process"):
        if feature_choice == "Cartoonize":
            result_img = cartoonize_image(our_image)
            st.image(result_img)
        elif feature_choice == "Edging":
            result_img = cannanize_image(our_image)
            st.image(result_img)
         

elif choice=="About":
    st.subheader("About the developer")
    st.markdown("Built with streamlit by [Team1]")
    st.text("Our team built this as a Mini-Project for Cloud Computing")
    clou=Image.open("Aboutfor.jpg")
    st.image(clou)
    st.text("We have a basic understanding on Python and C languages")
