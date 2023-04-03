import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os

def main():    
    st.title('Image Processing App')
    st.text("Edit your images in a fast and simple way")
    activities=["Detection","About"]
    choice=st.sidebar.selectbox("Select Activity",activities)
    if choice=="Detection":
        st.subheader("Detection")
        image_file=st.file_uploader("Upload Image",type=["jpg","jpeg","png","bmp","heic"])
        if image_file is not None:
            our_image=Image.open(image_file)
            st.text("Original Image")
            st.image(our_image)
        
            enhance_type=st.sidebar.radio("Enhance type", ["Original-Compressed","Gray-Scale","Contrast","Brightness","Blurring","Sharpness"])
            
        
        
    elif choice=="About":
        st.subheader("About the developer")
        st.markdown("Built with streamlit by [Team1]")
        st.text("Our team built this as a Mini-Project for Cloud Computing")
        clou=Image.open("Aboutfor.jpg")
        st.image(clou)
        st.text("We have a basic understanding on Python and C languages")
if __name__ == '__main__':
    main()
