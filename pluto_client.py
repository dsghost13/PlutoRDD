import socket

SERVER_IP = '172.29.234.51'
PORT = 12345
BUFFER_SIZE = 4096

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

def receive():
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            print(data.decode())
        except Exception as e:
            print(f"Connection error: {e}")
            break


if __name__ == "__main__":
    receive()