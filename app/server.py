import threading, socket, subprocess
from flask import Flask, Response

TCP_PORT = 5912
WEB_PORT = 5913

clients = []
buffer = []

# ✅ Replace input source here
def input_stream():
    # Option 1: listen to another TCP source
    return subprocess.Popen("nc localhost 6000", shell=True, stdout=subprocess.PIPE)

def tcp_server():
    s = socket.socket()
    s.bind(("0.0.0.0", TCP_PORT))
    s.listen(5)
    while True:
        c,_ = s.accept()
        clients.append(c)

def broadcast(proc):
    while True:
        line = proc.stdout.readline()
        if not line:
            continue
        t = line.decode(errors="ignore").strip()
        if not t:
            continue
        buffer.append(t)
        if len(buffer)>300:
            buffer.pop(0)
        for c in clients[:]:
            try:
                c.sendall((t+"\n").encode())
            except:
                clients.remove(c)

app = Flask(__name__)

@app.route("/")
def web():
    def stream():
        last=0
        while True:
            if len(buffer)>last:
                for l in buffer[last:]:
                    yield l+"<br>\n"
                last=len(buffer)
    return Response(stream(), mimetype="text/html")

def main():
    proc = input_stream()
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=broadcast, args=(proc,), daemon=True).start()
    app.run(host="0.0.0.0", port=WEB_PORT)

if __name__ == "__main__":
    main()
