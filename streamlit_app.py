import os
import streamlit as st
import psycopg2
import pandas.io.sql as psql
import time
from ssh_tunnel import SSHTunnel

def render_tunnel_state():
    st.header("SSH Tunnel")
    if 'tunnel' not in st.session_state:
        st.session_state.tunnel = SSHTunnel(st.secrets['SSH_AUTHKEY'], st.secrets['SSH_USER'], st.secrets['SSH_HOST'])

    def on_connect():
        st.session_state.tunnel.connect()

    def on_disconnect():
        st.session_state.tunnel.disconnect()

    tunnel = st.session_state.tunnel

    if tunnel.is_connected():
        st.button("Disconnect", on_click=on_disconnect)
    else:
        if tunnel.is_failed():
            st.error("Tunnel failed to connect: " + tunnel.get_output())

        st.button("Connect to SSH tunnel", on_click=on_connect)

    if st.button("Check tunnel status"):
        tunnel.evaluate_state()
        st.markdown("Tunnel state: " + str(tunnel.state))
        if tunnel.is_failed():
            st.write("Tunnel failed to connect.")

@st.experimental_singleton
def connect():
    return psycopg2.connect(host="localhost", user=user, port=54321, password=password, connect_timeout=10)

st.title(f"Tailscale & SSH demo")

render_tunnel_state()

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
