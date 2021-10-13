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
    os.system(f"mkdir -p ~/.ssh && chmod 700 ~/.ssh")
    with open("/home/appuser/.ssh/key", "w") as f:
        f.write(st.secrets["SSH_AUTHKEY"])
    os.chmod("/home/appuser/.ssh/key", 0o600) # user read/write only
    os.system(f"mkdir -p ~/.ssh && ssh-keyscan -H {st.secrets['SSH_HOST']} >> ~/.ssh/known_hosts")
    subprocess.Popen(["ssh", "-i", "~/.ssh/key", "-4", "-N", "-L", f"54321:localhost:5432", f"{st.secrets['SSH_USER']}@{st.secrets['SSH_HOST']}"])
    #os.remove("~/.ssh/key") # no need to keep on disk

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock status")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock netcheck")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock ip")

st.header("Postgres")

conn = None
with st.expander("psycopg"):
    if st.button("Connect"):
        conn = psycopg2.connect(host="localhost", user=user, port=54321, password=password, connect_timeout=10)

if st.button("Query database"):
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("select version()")
        data = cursor.fetchone()
        st.write(data)


with st.expander("Terminal debugger"):
    command = st.text_input("Command")
    if st.button("Execute"):
        os.system("echo running: " + command)
        os.system(command)