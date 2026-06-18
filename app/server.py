import socket
import threading
from flask import Flask, Response

TCP_OUT_PORT = 5912
TCP_IN_PORT = 6000
WEB_PORT = 5913

clients = []
buffer = []

# ---- INPUT SERVER (port 6000) ----
def input_server():
    server = socket.socket()
    server.bind(("0.0.0.0", TCP_IN_PORT))
    server.listen(5)

    print(f"[+] INPUT server listening on {TCP_IN_PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Input connected: {addr}")
        threading.Thread(target=handle_input, args=(conn,), daemon=True).start()

def handle_input(conn):
    global clients, buffer
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            text = data.decode(errors="ignore").strip()
            if not text:
                continue

            buffer.append(text)
            if len(buffer) > 300:
                buffer.pop(0)

            for c in clients[:]:
                try:
                    c.sendall((text + "\n").encode())
                except:
                    clients.remove(c)

        except:
            break

    conn.close()

# ---- OUTPUT SERVER (port 5912) ----
def output_server():
    server = socket.socket()
    server.bind(("0.0.0.0", TCP_OUT_PORT))
    server.listen(5)

    print(f"[+] OUTPUT server on port {TCP_OUT_PORT}")

    while True:
        client, addr = server.accept()
        print(f"[+] Client connected: {addr}")
        clients.append(client)

# ---- WEB UI ----
app = Flask(__name__)

@app.route("/")
def web():
    def stream():
        last = 0
        while True:
            if len(buffer) > last:
                for line in buffer[last:]:
                    yield line + "<br>\n"
                last = len(buffer)
    return Response(stream(), mimetype="text/html")

# ---- MAIN ----
def main():
    threading.Thread(target=input_server, daemon=True).start()
    threading.Thread(target=output_server, daemon=True).start()

    print(f"[+] Web UI: http://0.0.0.0:{WEB_PORT}")
    app.run(host="0.0.0.0", port=WEB_PORT)

if __name__ == "__main__":
    main()
