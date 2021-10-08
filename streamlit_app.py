# Monkeypatch stdlib to use the proxy
import socket
import socks

socks.set_default_proxy(socks.SOCKS5, os.getenv("ALL_PROXY"))
socket.socket = socks.socksocket

import streamlit as st
import subprocess
import os
import psycopg2
import asyncio
import asyncpg

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

if st.button("Check connection"):
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock status")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock netcheck")
    os.system("/app/tailscale-demo/tailscale --socket=/tmp/tailscale.sock ip")

st.header("Postgres")

with st.expander("asyncpg"):
    async def run():
        conn = await asyncpg.connect(user='demo', password='demo',
                                     database='demo', host='fd7a:115c:a1e0:ab12:4843:cd96:6256:7b70')
        values = await conn.fetch(
            'SELECT * FROM people'
        )
        await conn.close()

    def get_or_create_eventloop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError as ex:
            if "There is no current event loop in thread" in str(ex):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    loop = get_or_create_eventloop()
    loop.run_until_complete(run())


with st.expander("psycopg"):
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
