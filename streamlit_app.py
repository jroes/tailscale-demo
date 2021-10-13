# 
#
#
##
#

# Note to future me: proxychains won't work because it needs to run the program inside of it
# Unless we really hack it up and like run some piece of python code separately

# Alternative, more easy-mode solution: just use ssh -L / whatever to do a reverse proxy
# Things to do for that:
#  * Generate an ssh keypair on the db server
#  * Set the key as an env var
#  * Find working ssh -L example
# .... Profit?!


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

if st.button("Initialize is this working proxychains"):
    #subprocess.Popen(["/app/tailscale-demo/proxychains4", "-f", "proxychains.conf"])
    os.system("/app/tailscale-demo/proxychains4 socks5 127.0.0.1 1055")

if st.button("Boot SSH tunnel"):
    with open("/tmp/key", "w") as f:
        f.write(st.secrets["SSH_AUTHKEY"])
    os.chmod("/tmp/key", 0o600) # user read/write only
    subprocess.Popen([f"ssh -i /tmp/key -L 5432:{st.secrets['SSH_HOST']}:5432 {st.secrets['SSH_USER']}@{st.secrets['SSH_HOST']}"])
    os.remove("/tmp/key") # no need to keep on disk

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