import streamlit as st
import subprocess
import os
import psycopg2

st.title(f"Tailscale demo")

if st.button("Initialize Tailscale"):
    subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale",
        "--socks5-server=localhost:1055"])
    subprocess.Popen(["/app/tailscale-demo/tailscale",
        "--socket=/tmp/tailscale.sock",
        "up", "--authkey=" + os.getenv('TAILSCALE_AUTHKEY'),
        "--hostname=tailscale-demo"])

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock status")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock netcheck")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock ip")

st.header("Postgres")
host = st.text_input("Host")
user = st.text_input("User")
password = st.text_input("Password")
if st.button("Connect"):
    conn = psycopg2.connect(host=host, user=user, password=password, connect_timeout=10)
    cursor = conn.cursor()
    cursor.execute("select version()")
    data = cursor.fetchone()
    st.write("Connection established: " + data)


with st.expander("Terminal debugger"):
    command = st.text_input("Command")
    if st.button("Execute"):
        os.system("echo running: " + command)
        os.system(command)

#    st.write("Daemon: " + daemonproc.poll())

#    st.write("Client: " + clientproc.poll())

#    if process.returncode == 0:
#        st.balloons()
#        st.header("You're connected!")
#        # TODO: Disable the button
#        # TODO: Enable a button to query the db
#    else:
#        st.write("Sorry it didn't work for some reason :(")

#if st.button("Start daemon"):
#    os.system("ps aux | grep tailscale")
#    os.system("ls -lah /tmp/tailscale*")
#    subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
#        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale"])
#
#if st.button("Start client"):
#    subprocess.Popen(["/app/tailscale-demo/tailscale",
#        "--socket=/tmp/tailscale.sock",
#        "up",
#        "--authkey=" + ephemeral_key])
#
