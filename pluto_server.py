import socket

HOST_IP = '172.29.234.51'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, PORT))
server_socket.listen(1)
print(f"Server listening on port {PORT}...")

connection, addr = server_socket.accept()
print(f"Client connected from {addr}")

try:
    while True:
        connection.send(bytes(input("> "), "utf-8"))
finally:
    connection.close()