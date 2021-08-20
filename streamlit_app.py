import streamlit as st
import subprocess
import os

cwd = os.path.dirname(os.path.realpath(__file__))
st.write(cwd)

st.title(f"Tailscale demo")

ephemeral_key = st.text_input("Ephemeral key")

daemonproc = None
clientproc = None
if st.button("Connect"):
    daemonproc = subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state /tmp/tailscale"])

    clientproc = subprocess.Popen(["/app/tailscale-demo/tailscale", "--socket=/tmp/tailscale.sock", "up",
        "--authkey=" + ephemeral_key])

if st.button("Check connection"):
    st.write("Daemon: " + daemonproc.poll())
    st.write("Client: " + clientproc.poll())

#    if process.returncode == 0:
#        st.balloons()
#        st.header("You're connected!")
#        # TODO: Disable the button
#        # TODO: Enable a button to query the db
#    else:
#        st.write("Sorry it didn't work for some reason :(")

