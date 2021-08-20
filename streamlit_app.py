import streamlit as st
import subprocess

st.title(f"Tailscale demo")

ephemeral_key = st.text_input("Ephemeral key")

self.daemonproc = None
self.clientproc = None
if st.button("Connect"):
    self.daemonproc = subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale"])

    self.clientproc = subprocess.Popen(["/app/tailscale-demo/tailscale", "--socket=/tmp/tailscale.sock", "up",
        "--authkey=" + ephemeral_key])

if st.button("Check connection"):
    st.write("Daemon: " + self.daemonproc.poll())
    st.write("Client: " + self.clientproc.poll())

#    if process.returncode == 0:
#        st.balloons()
#        st.header("You're connected!")
#        # TODO: Disable the button
#        # TODO: Enable a button to query the db
#    else:
#        st.write("Sorry it didn't work for some reason :(")

