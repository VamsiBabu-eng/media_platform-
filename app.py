import streamlit as st
from db_c import conn,cursor
st.title("Media Platform")

login,signup = st.tabs(
    ["Login","SignUp"]
)

with login:
    st.header("Login")
    with st.form("Login_Form"):
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")
        btn=st.form_submit_button("Login")


with signup:
    st.header("SignUp")

    with st.form("SignUp_Form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        btn = st.form_submit_button("SignUp")

        if btn:
          query = """
          INSERT INTO users(name,email,password)
          VALUES(%s,%s,%s) """
          values = (name,email,password)
          cursor.execute(query,values)
          conn.commit()
          st.success("User Registered Successfully")
          cursor.execute("SELECT * FROM users")
          data = cursor.fetchall()
          st.write(data)
           