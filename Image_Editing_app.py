import streamlit as st
import random

# define a dictionary with user details
users = {
    "user1": {"password": "pass123", "otp": None},
    "user2": {"password": "pass456", "otp": None},
    "user3": {"password": "pass789", "otp": None}
}

# define a function to generate OTP
def generate_otp():
    otp = ""
    for i in range(4):
        otp += str(random.randint(1, 9))
    return otp

# define the Streamlit app
def app():
    st.title("Login Page")

    # define a form for user input
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submitted = st.form_submit_button('Login')

        # check if the form is submitted
        if submitted:
            # check if the username exists
            if username in users.keys():
                # check if the password is correct
                if password == users[username]["password"]:
                    # generate and send OTP
                    otp = generate_otp()
                    users[username]["otp"] = otp
                    st.success("Login successful. OTP sent to your registered mobile number.")
                    # display OTP verification form
                    with st.form(key='otp_form'):
                        otp_input = st.text_input("Enter OTP")
                        otp_submitted = st.form_submit_button('Verify OTP')
                        # check if the OTP is verified
                        if otp_submitted:
                            if otp_input == users[username]["otp"]:
                                st.success("OTP verification successful. You are logged in.")
                            else:
                                st.error("Invalid OTP. Please try again.")
                else:
                    st.error("Incorrect password. Please try again.")
            else:
                st.error("Username not found. Please try again.")
