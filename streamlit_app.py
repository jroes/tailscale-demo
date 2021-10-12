import os
import streamlit as st
import subprocess
import psycopg2

st.title(f"Tailscale demo")

procs = []

if st.button("Initialize Tailscale"):
    procs.append(subprocess.Popen(["/app/tailscale-demo/tailscaled", "--tun=userspace-networking",
        "--socket=/tmp/tailscale.sock", "--state=/tmp/tailscale",
        "--socks5-server=localhost:1055"]))
    procs.append(subprocess.Popen(["/app/tailscale-demo/tailscale",
        "--socket=/tmp/tailscale.sock",
        "up",
        "--authkey=" + os.getenv('TAILSCALE_AUTHKEY'),
        "--hostname=tailscale-demo"]))

host = st.text_input("Host", value="fd7a:115c:a1e0:ab12:4843:cd96:6256:7b70")
user = st.text_input("Username", value="demo")
password = st.text_input("Password", value="demo", type="password")

if st.button("Initialize proxychains"):
    procs.append(subprocess.Popen(["proxychains4"]))

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

# TODO: Enable better process management
st.write(procs)

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
