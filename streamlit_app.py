import os
import streamlit as st
import subprocess
import psycopg2
import pandas.io.sql as psql

def init_tunnel():
    os.system(f"mkdir -p ~/.ssh && chmod 700 ~/.ssh")
    with open("/home/appuser/.ssh/key", "w") as f:
        f.write(st.secrets["SSH_AUTHKEY"])
    os.chmod("/home/appuser/.ssh/key", 0o600) # user read/write only
    os.system(f"mkdir -p ~/.ssh && ssh-keyscan -H {st.secrets['SSH_HOST']} >> ~/.ssh/known_hosts")
    subprocess.Popen(["ssh", "-i", "~/.ssh/key", "-4", "-N", "-L", f"54321:localhost:5432", f"{st.secrets['SSH_USER']}@{st.secrets['SSH_HOST']}"])
    #os.remove("~/.ssh/key") # no need to keep on disk

st.title(f"Tailscale & SSH demo")

st.header("Postgres")
with st.expander("Connection details"):
    host = st.text_input("Host", value="localhost")
    user = st.text_input("Username", value="demo")
    password = st.text_input("Password", value="demo", type="password")


if st.button("Initialize SSH tunnel"):
    init_tunnel()

@st.experimental_singleton
def connect():
    return psycopg2.connect(host="localhost", user=user, port=54321, password=password, connect_timeout=10)

if st.button("Query database"):
    conn = connect()
    df = psql.read_sql('SELECT * from people;', conn)
    st.dataframe(df)

## Tailscale stuff

if st.button("Initialize Tailscale"):
    subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale",
        "--socks5-server=localhost:1055"])
    subprocess.Popen(["/app/tailscale-demo/tailscale",
        "--socket=/tmp/tailscale.sock",
        "up",
        "--authkey=" + os.getenv('TAILSCALE_AUTHKEY'),
        "--hostname=tailscale-demo"])

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock status")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock netcheck")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock ip")

with st.expander("Terminal debugger"):
    command = st.text_input("Command")
    if st.button("Execute"):
        os.system("echo running: " + command)
        os.system(command)
