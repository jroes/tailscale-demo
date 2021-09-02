import streamlit as st
import subprocess
import os
import psycopg2

st.title(f"dpkg demo")

if st.button("Install dpkg"):
    os.system("dpkg -i *.deb")

command = st.text_input("Command")
if st.button("Execute"):
    os.system("echo running: " + command)
    os.system(command)
