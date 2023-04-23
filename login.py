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

deta = Deta("d04dpxd7btb_gg4hbdMzBp3Ed1vjv2nskwfSsgN8YWZZ")

# Create a new database "example-db"
# If you need a new database, just use another name.
db = deta.Base("users_db")


choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign in'])
# Data to be written to Deta Base
if choice == 'Sign in':
    st.write('# Signin')
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button('Create Account'):
        db.put({"email": email, "password": password})
        st.success("Account created successfully")
if choice == 'Login':
    st.write('# Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Check if the username exists in the database
        user = db.get({"email": username})

        if user and user['password'] == password:
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
        


        else:
            st.write('Invalid username or password')
            
