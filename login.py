import streamlit as st
from deta import Deta
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os


def cartoonize_image(our_image):
    new_img=np.array(our_image.convert("RGB"))
    img=cv2.GaussianBlur(new_img,(13,13),0)#0 is Standard Deviation and Kernel should be odd
    canny=cv2.Canny(img,100,150)
    return canny

# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["data_key"])

# Create a new database "example-db"
# If you need a new database, just use another name.
db = deta.Base("users")


choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])
# Data to be written to Deta Base
if choice == 'Sign up':
    with st.form("form"):
        name = st.text_input("Username")
        email = st.number_input("email-Id")
        password=st.number_input("password")
        submitted = st.form_submit_button("Create my account")
    if submitted:
        db.put({"username": name, "email": email, "password": password})
        st.success('Your account is created suceesfully!')
if choice == 'Login':
    with st.form("form"):
        email = st.number_input("email-Id")
        password=st.number_input("password")
        submitted = st.form_submit_button("Login")
        if submitted:
                st.title('Image Editing App')
                st.text("Edit your images in a fast and simple way")
                activities=["Detection","About"]
                choice=st.sidebar.selectbox("Select Activity",activities)
                if choice=="Detection":
                    st.subheader("Detection")
                    image_file=st.file_uploader("Upload Image",type=["jpg","jpeg","png"])
                    if image_file is not None:
                        our_image=Image.open(image_file)
                        st.text("Original Image")
                        st.image(our_image)

                        enhance_type=st.sidebar.radio("Enhance type", ["Original-Compressed","Gray-Scale","Contrast","Brightness","Blurring","Sharpness"])
                        if enhance_type=="Original-Compressed":
                            st.image(our_image,width=300)
                        elif enhance_type=="Gray-Scale":
                            img=np.array(our_image.convert("RGB"))
                            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                            st.text("Gray-Scaled Image")
                            st.image(gray)
                        elif enhance_type=="Contrast":
                            rate=st.sidebar.slider("Contrast",0.1,6.0)#Use only float numbers
                            enhancer=ImageEnhance.Contrast(our_image)
                            enhanced_img=enhancer.enhance(rate)
                            st.text("Contrasted Image")
                            st.image(enhanced_img)
                        elif enhance_type=="Brightness":
                            rate=st.sidebar.slider("Brightness",0.1,10.0)
                            enhancer=ImageEnhance.Brightness(our_image)
                            brighted_img=enhancer.enhance(rate)
                            st.text("Brighted Image")
                            st.image(brighted_img)
                        elif enhance_type=="Blurring":
                            rate=st.sidebar.slider("Blur",0.1,10.0)
                            blurred_img=cv2.GaussianBlur(np.array(our_image),(17,15),rate)#Use only odd numbers
                            st.text("Blurred Image")
                            st.image(blurred_img)
                        elif enhance_type=="Sharpness":
                            rate=st.sidebar.slider("Sharpness",0.1,10.0)
                            enhancer=ImageEnhance.Sharpness(our_image)
                            sharpened_img=enhancer.enhance(rate)
                            st.text("Sharpened Image")
                            st.image(sharpened_img)
                    else:
                        st.image(our_image)
                    tasks=["Cartoonize"]
                    feature_choice=st.sidebar.selectbox("Find features",tasks)
                    if st.button("Process"):
                        if feature_choice=="Cartoonize":
                            result_img = cartoonize_image(our_image)
                            st.image(result_img)
                elif choice=="About":
                    st.subheader("About the developer")
                    st.markdown("Built with streamlit by [Team1]")
                    st.text("Our team built this as a Mini-Project for Cloud Computing")
                    clou=Image.open("Aboutfor.jpg")
                    st.image(clou)
                    st.text("We have a basic understanding on Python and C languages")
            

