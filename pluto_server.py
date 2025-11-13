import socket
import adi

SAMPLE_RATE = 1e6       # e.g., 1e6 for 1 MSPS
CENTER_FREQ = 2.4e9     # e.g., 2.4 GHz
BUFFER_SIZE = 1024      # number of samples per send

HOST = ''               # Listen on all interfaces
PORT = 12345            # TCP port to stream to client

pluto = adi.Pluto()
pluto.sample_rate = SAMPLE_RATE
pluto.rx_lo = CENTER_FREQ

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on port {PORT}...")

conn, addr = server_socket.accept()
print(f"Client connected from {addr}")

try:
    while True:
        iq_samples = pluto.rx()
        conn.sendall(iq_samples.tobytes())
finally:
    conn.close()