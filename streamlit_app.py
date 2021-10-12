import os
import streamlit as st
import subprocess
import psycopg2

st.title(f"Tailscale demo")

if st.button("Initialize Tailscale"):
    subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale",
        "--socks5-server=localhost:1055"])
    subprocess.Popen(["/app/tailscale-demo/tailscale",
        "--socket=/tmp/tailscale.sock",
        "up",
        "--authkey=" + os.getenv('TAILSCALE_AUTHKEY'),
        "--hostname=tailscale-demo"])

host = st.text_input("Host", value="fd7a:115c:a1e0:ab12:4843:cd96:6256:7b70")
user = st.text_input("Username", value="demo")
password = st.text_input("Password", value="demo", type="password")

if st.button("Initialize proxychains"):
    subprocess.Popen(["/app/tailscale-demo/proxychains4", "-f", "proxychains.conf"])

#if st.button("Boot SSH tunnel"):
    # TODO: Put passwordless private key in a secret
#    subprocess.Popen(["ssh -L 5432:remote.server.com:5432 myuser@remote.server.com"])

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock status")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock netcheck")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock ip")

st.header("Postgres")

with st.expander("psycopg"):
    if st.button("Connect"):
        conn = psycopg2.connect(host="localhost", user=user, port=54321, password=password, connect_timeout=10)
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        st.write("Connection established: " + data)


with st.expander("Terminal debugger"):
    command = st.text_input("Command")
    if st.button("Execute"):
        os.system("echo running: " + command)
        os.system(command)