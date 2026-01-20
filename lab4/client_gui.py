import socket
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox


class ChatClientGUI:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Lab4 Client")

        # Network
        self.sock: socket.socket | None = None
        self.receiver_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.incoming_queue: queue.Queue[str] = queue.Queue()

        # Top: connection settings
        conn_frame = ttk.Frame(master)
        conn_frame.pack(fill=tk.X, padx=8, pady=6)

        ttk.Label(conn_frame, text="Host:").pack(side=tk.LEFT)
        self.host_var = tk.StringVar(value="127.0.0.1")
        self.host_entry = ttk.Entry(conn_frame, width=16, textvariable=self.host_var)
        self.host_entry.pack(side=tk.LEFT, padx=(4, 10))

        ttk.Label(conn_frame, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="1502")
        self.port_entry = ttk.Entry(conn_frame, width=6, textvariable=self.port_var)
        self.port_entry.pack(side=tk.LEFT, padx=(4, 10))

        ttk.Label(conn_frame, text="Name:").pack(side=tk.LEFT)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(conn_frame, width=16, textvariable=self.name_var)
        self.name_entry.pack(side=tk.LEFT, padx=(4, 10))

        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.connect)
        self.connect_btn.pack(side=tk.LEFT)
        self.disconnect_btn = ttk.Button(conn_frame, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_btn.pack(side=tk.LEFT, padx=(6, 0))

        # Middle: chat log
        text_frame = ttk.Frame(master)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 6))

        self.text = tk.Text(text_frame, height=18, state=tk.DISABLED, wrap=tk.WORD)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(text_frame, command=self.text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text["yscrollcommand"] = scroll.set

        # Bottom: message entry
        bottom = ttk.Frame(master)
        bottom.pack(fill=tk.X, padx=8, pady=(0, 8))
        self.msg_var = tk.StringVar()
        self.msg_entry = ttk.Entry(bottom, textvariable=self.msg_var)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", lambda _e: self.send_message())
        self.send_btn = ttk.Button(bottom, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_btn.pack(side=tk.LEFT, padx=(6, 0))

        # Poll queue for incoming messages
        self.master.after(100, self._drain_incoming_queue)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def log(self, line: str) -> None:
        self.text.configure(state=tk.NORMAL)
        self.text.insert(tk.END, line + "\n")
        self.text.see(tk.END)
        self.text.configure(state=tk.DISABLED)

    def connect(self) -> None:
        if self.sock is not None:
            return
        host = self.host_var.get().strip() or "127.0.0.1"
        try:
            port = int(self.port_var.get().strip() or "1502")
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Введите имя перед подключением")
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except Exception as exc:  # noqa: BLE001
            self.sock = None
            messagebox.showerror("Connection failed", str(exc))
            return

        self.log(f"Connected to {host}:{port}")
        self._set_connected_state(True)
        self.stop_event.clear()
        self.receiver_thread = threading.Thread(target=self._receiver_loop, name="Receiver", daemon=True)
        self.receiver_thread.start()

    def disconnect(self) -> None:
        self.stop_event.set()
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except Exception:  # noqa: BLE001
                pass
            try:
                self.sock.close()
            except Exception:  # noqa: BLE001
                pass
        self.sock = None
        self._set_connected_state(False)
        self.log("Disconnected")

    def _set_connected_state(self, connected: bool) -> None:
        self.connect_btn.configure(state=tk.DISABLED if connected else tk.NORMAL)
        self.disconnect_btn.configure(state=tk.NORMAL if connected else tk.DISABLED)
        self.send_btn.configure(state=tk.NORMAL if connected else tk.DISABLED)

    def send_message(self) -> None:
        if self.sock is None:
            return
        text = self.msg_var.get().strip()
        if not text:
            return
        name = self.name_var.get().strip() or "User"
        msg = f"{name}: {text}".encode()
        try:
            self.sock.sendall(msg)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Send failed", str(exc))
            self.disconnect()
            return
        self.msg_var.set("")

    def _receiver_loop(self) -> None:
        assert self.sock is not None
        try:
            while not self.stop_event.is_set():
                try:
                    data = self.sock.recv(1024)
                except OSError:
                    break
                if not data:
                    break
                self.incoming_queue.put(data.decode(errors="replace"))
        finally:
            # Ensure UI reflects disconnected state
            self.incoming_queue.put("[connection closed]")
            self.master.after(0, lambda: self._set_connected_state(False))

    def _drain_incoming_queue(self) -> None:
        while True:
            try:
                line = self.incoming_queue.get_nowait()
            except queue.Empty:
                break
            self.log(line)
        self.master.after(100, self._drain_incoming_queue)

    def on_close(self) -> None:
        self.disconnect()
        self.master.destroy()


def main() -> None:
    root = tk.Tk()
    ChatClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


