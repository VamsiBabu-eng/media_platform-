import streamlit as st

from auth import signup_user, login_user
from upload import upload_file
from db import cursor_obj, conn_obj

st.title("Media Platform")

# SESSION STATE
if "user" not in st.session_state:
    st.session_state.user = None

# SIGNUP
def signup_page():

    st.header("Signup")

    with st.form("signup_form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        btn = st.form_submit_button("Signup")

        if btn:

            signup_user(
                name,
                email,
                password
            )

            st.success("Account Created")

# LOGIN
def login_page():

    st.header("Login")

    with st.form("login_form"):

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        btn = st.form_submit_button("Login")

        if btn:

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.user = user

                st.rerun()

            else:
                st.error("Invalid Credentials")

# DASHBOARD
def dashboard():

    st.sidebar.success(
        f"Welcome {st.session_state.user['name']}"
    )

    option = st.sidebar.selectbox(
        "Choose Option",
        ["Upload","View Files","Logout"]
    )

    # UPLOAD
    if option == "Upload":

        file = st.file_uploader(
            "Choose File",
            type=[
                "jpg",
                "jpeg",
                "png",
                "mp4",
                "mp3",
                "pdf"
            ]
        )

        if file:

            if "image" in file.type:
                st.image(file)

            elif "video" in file.type:
                st.video(file)

            elif "audio" in file.type:
                st.audio(file)

            if st.button("Upload File"):

                url = upload_file(file)

                query = """
                INSERT INTO files(
                    user_id,
                    file_name,
                    file_type,
                    file_url
                )
                VALUES(%s,%s,%s,%s)
                """

                values = (
                    st.session_state.user["id"],
                    file.name,
                    file.type,
                    url
                )

                cursor_obj.execute(query,values)

                conn_obj.commit()

                st.success("Uploaded Successfully")

    # VIEW FILES
    elif option == "View Files":

        query = """
        SELECT * FROM files
        WHERE user_id=%s
        """

        values = (
            st.session_state.user["id"],
        )

        cursor_obj.execute(query,values)

        files = cursor_obj.fetchall()

        for file in files:

            st.write(file["file_name"])

            if "image" in file["file_type"]:
                st.image(file["file_url"])

            elif "video" in file["file_type"]:
                st.video(file["file_url"])

            elif "audio" in file["file_type"]:
                st.audio(file["file_url"])

    # LOGOUT
    elif option == "Logout":

        st.session_state.user = None

        st.rerun()

# MAIN FLOW
if st.session_state.user == None:

    login_tab, signup_tab = st.tabs(
        ["Login","Signup"]
    )

    with login_tab:
        login_page()

    with signup_tab:
        signup_page()

else:
    dashboard()