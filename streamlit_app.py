import streamlit as st
import subprocess

st.title(f"Tailscale demo")

ephemeral_key = st.text_input("Ephemeral key")

if st.button("Connect"):
    process = subprocess.run("connect.sh", capture_output, { "TS_KEY": ephemeral_key })
    st.write(process.stdout)
    st.write(process.stderr)
    if process.returncode == 0:
        st.balloons()
        st.header("You're connected!")
        # TODO: Disable the button
        # TODO: Enable a button to query the db
    else:
        st.write("Sorry it didn't work for some reason :(")

