# import socket
# import threading
#
# HOST = "0.0.0.0"
# PORT = 1502
#
# clients: set[socket.socket] = set()
# clients_lock = threading.Lock()
#
#
# def broadcast(message: bytes) -> None:
#     to_remove: list[socket.socket] = []
#     with clients_lock:
#         for c in list(clients):
#             try:
#                 c.sendall(message)
#             except Exception:
#                 to_remove.append(c)
#         for c in to_remove:
#             try:
#                 clients.remove(c)
#             except KeyError:
#                 pass
#             try:
#                 c.close()
#             except Exception:
#                 pass
#
#
# def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
#     with conn:
#         print(f"Connected by {addr}")
#         with clients_lock:
#             clients.add(conn)
#         buffer = ""
#         try:
#             while True:
#                 data = conn.recv(1024).decode('utf-8', errors='replace')
#                 if not data:
#                     break
#
#                 buffer += data
#                 lines = buffer.split('\n')
#                 buffer = lines[-1]  # Keep incomplete line in buffer
#
#                 for line in lines[:-1]:
#                     if line.strip():
#                         # Process message based on type
#                         if line.startswith("MSG:"):
#                             # Regular text message - broadcast as is
#                             broadcast((line + '\n').encode())
#                             print(f"Message from {addr}: {line[4:]}")
#                         elif line.startswith("FILE:"):
#                             # File message - broadcast to all clients
#                             broadcast((line + '\n').encode())
#                             print(f"File transfer from {addr}")
#                         else:
#                             # Legacy format (without prefix) - treat as text message
#                             broadcast(("MSG:Unknown: " + line + '\n').encode())
#
#         except ConnectionError:
#             pass
#         except Exception as e:
#             print(f"Error with client {addr}: {e}")
#         finally:
#             with clients_lock:
#                 if conn in clients:
#                     clients.remove(conn)
#             print(f"Disconnected {addr}")
#
#
# def main() -> None:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.bind((HOST, PORT))
#         s.listen()
#         print(f"Server listening on {HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
#             t.start()
#
#
# if __name__ == "__main__":
#     main()
#
# import socket
# import threading
#
# HOST = "0.0.0.0"
# PORT = 1502
#
# clients: set[socket.socket] = set()
# clients_lock = threading.Lock()
#
#
# def broadcast(message: str, sender_socket: socket.socket = None) -> None:
#     """Broadcast message to all clients except sender"""
#     to_remove: list[socket.socket] = []
#     with clients_lock:
#         for client in list(clients):
#             if client != sender_socket:  # Don't send back to sender
#                 try:
#                     client.sendall(message.encode('utf-8'))
#                 except Exception:
#                     to_remove.append(client)
#         # Remove broken connections
#         for client in to_remove:
#             try:
#                 clients.remove(client)
#             except KeyError:
#                 pass
#             try:
#                 client.close()
#             except Exception:
#                 pass
#
#
# def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
#     with conn:
#         print(f"Connected by {addr}")
#         with clients_lock:
#             clients.add(conn)
#
#         try:
#             while True:
#                 data = conn.recv(1024)
#                 if not data:
#                     break
#
#                 message = data.decode('utf-8', errors='replace').strip()
#                 if message:
#                     print(f"Received from {addr}: {message}")
#                     broadcast(f"{message}\n", conn)  # Send to all other clients
#
#         except (ConnectionError, OSError):
#             pass
#         except Exception as e:
#             print(f"Error with client {addr}: {e}")
#         finally:
#             with clients_lock:
#                 if conn in clients:
#                     clients.remove(conn)
#             print(f"Disconnected {addr}")
#
#
# def main() -> None:
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.bind((HOST, PORT))
#         s.listen()
#         print(f"Server listening on {HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
#             t.start()
#
#
# if __name__ == "__main__":
#     main()

import socket
import threading

HOST = "0.0.0.0"
PORT = 1502

clients: set[socket.socket] = set()
clients_lock = threading.Lock()


def broadcast(message: str) -> None:
    """Broadcast message to ALL clients including sender"""
    to_remove: list[socket.socket] = []
    with clients_lock:
        for client in list(clients):
            try:
                client.sendall(message.encode('utf-8'))
            except Exception:
                to_remove.append(client)
        # Remove broken connections
        for client in to_remove:
            try:
                clients.remove(client)
            except KeyError:
                pass
            try:
                client.close()
            except Exception:
                pass


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    with conn:
        print(f"Connected by {addr}")
        with clients_lock:
            clients.add(conn)

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8', errors='replace').strip()
                if message:
                    print(f"Received from {addr}: {message}")
                    broadcast(f"{message}\n")  # Send to ALL clients including sender

        except (ConnectionError, OSError):
            pass
        except Exception as e:
            print(f"Error with client {addr}: {e}")
        finally:
            with clients_lock:
                if conn in clients:
                    clients.remove(conn)
            print(f"Disconnected {addr}")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()


if __name__ == "__main__":
    main()