import streamlit as st
import subprocess
import os

st.title(f"Tailscale demo")

ephemeral_key = st.text_input("Ephemeral key")

if st.button("Connect"):
    os.system("killall tailscaled")
    os.system("killall tailscale")
    subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking"])
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale"])

#    subprocess.Popen(["/app/tailscale-demo/tailscale",
#        "--socket=/tmp/tailscale.sock",
#        "up",
#        "--authkey=" + ephemeral_key])

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale status")
    os.system("/app/tailscale-demo/tailscale netcheck")
#    st.write("Daemon: " + daemonproc.poll())
#    st.write("Client: " + clientproc.poll())

#    if process.returncode == 0:
#        st.balloons()
#        st.header("You're connected!")
#        # TODO: Disable the button
#        # TODO: Enable a button to query the db
#    else:
#        st.write("Sorry it didn't work for some reason :(")

