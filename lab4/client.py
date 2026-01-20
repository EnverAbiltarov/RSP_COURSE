import socket

HOST = "127.0.0.1"
PORT = 1502

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    name = input("Введите ваше имя: ")

    while True:
        message = input("Введите сообщение: ")
        s.sendall(f"{name}: {message}".encode())
        data = s.recv(1024)
        print(data.decode())
