import streamlit as st
from api import login, register

def auth_page():

    option = st.radio(
        "Choose",
        ["Login", "Sign Up"]
    )

    #  ---------------- LOGIN ----------------
if st.session_state.token is None:

    option = st.radio(
        "Choose",
        ["Login", "Sign Up"]
    )

    # ---------------- LOGIN ----------------

    if option == "Login":

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            response = login(email, password)

            if response.status_code == 200:

                st.session_state.token = response.json()["access_token"]

                st.success("Login Successful")

                st.rerun()

            else:

                st.error(response.text)

    # ---------------- SIGNUP ----------------

    else:

        name = st.text_input("Full Name")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Role",
            [
                "admin",
                "cashier"
            ]
        )

        if st.button("Create Account"):

            response = register(
                name,
                email,
                password,
                role
            )

            if response.status_code == 200:

                st.success(
                    "Account Created Successfully!"
                )

            else:

                st.error(response.text)