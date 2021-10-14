import os
import streamlit as st
import subprocess
import psycopg2
import pandas.io.sql as psql

class SSHTunnel():
    def __init__(self):
        self.proc = None

    def connect(self):
        os.system(f"mkdir -p ~/.ssh && chmod 700 ~/.ssh")
        with open("/home/appuser/.ssh/key", "w") as f:
            f.write(st.secrets["SSH_AUTHKEY"])
        os.chmod("/home/appuser/.ssh/key", 0o600) # user read/write only
        os.system(f"mkdir -p ~/.ssh && ssh-keyscan -H {st.secrets['SSH_HOST']} >> ~/.ssh/known_hosts")
        self.proc = subprocess.Popen(["ssh", "-i", "~/.ssh/key", "-4", "-N", "-L", f"54321:localhost:5432", f"{st.secrets['SSH_USER']}@{st.secrets['SSH_HOST']}"])
        #os.remove("~/.ssh/key") # no need to keep on disk
    
    def disconnect(self):
        self.proc.kill()

    def is_connected(self):
        if self.proc is not None:
            return True
        else:
            return False

@st.experimental_singleton
def connect():
    return psycopg2.connect(host="localhost", user=user, port=54321, password=password, connect_timeout=10)

st.title(f"Tailscale & SSH demo")

def draw_tunnel_status():
    if 'tunnel' not in st.session_state:
        st.session_state['tunnel'] = SSHTunnel()

    tunnel = st.session_state['tunnel']

    st.header("SSH tunnel")
    st.write(tunnel.proc)
    if st.button("Disconnect"):
        tunnel.disconnect()
    if st.button("Connect to SSH tunnel"):
        tunnel.connect()
        while not tunnel.is_connected():
            with st.spinner("Connecting..."):
                time.sleep(0.1)
        st.success("Connected!")

draw_tunnel_status()

st.header("Playing with the database")
with st.expander("Connection details"):
    host = st.text_input("Host", value="localhost")
    user = st.text_input("Username", value="demo")
    password = st.text_input("Password", value="demo", type="password")

if st.button("Query database"):
    conn = connect()
    df = psql.read_sql('SELECT * from people;', conn)
    st.dataframe(df)

with st.expander("Terminal debugger"):
    command = st.text_input("Command")
    if st.button("Execute"):
        os.system("echo running: " + command)
        os.system(command)
