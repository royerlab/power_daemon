import pyfirmata2
import socket
import threading
import os
from config import SOCKET_ADDRESS, PORT, PIN

class BoardDaemon:
    def __init__(self):
        self.board = pyfirmata2.Arduino(PORT)
        self.pin = self.board.get_pin(PIN)
        self.pin.write(False)

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            if data == "on":
                self.pin.write(1)
                client_socket.sendall(b"OK: Powered on\n")
            elif data == "off":
                self.pin.write(0)
                client_socket.sendall(b"OK: Powered off\n")
            elif data == "status":
                state = self.pin.read()
                if state is None:
                    client_socket.sendall(b"ERROR: State was 'None'\n")
                else:
                    status = "on" if state == 1 else "off"
                    client_socket.sendall(f"OK: Current state is {status}\n".encode("utf-8"))
            else:
                client_socket.sendall(b"ERROR: Invalid command\n")
        finally:
            client_socket.close()

    def run(self):
        if os.path.exists(SOCKET_ADDRESS):
            os.remove(SOCKET_ADDRESS)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(SOCKET_ADDRESS)
        server.listen(5)
        print("Board daemon is running...")

        try:
            while True:
                client_socket, _ = server.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        finally:
            server.close()
            self.board.exit()
            if os.path.exists(SOCKET_ADDRESS):
                os.remove(SOCKET_ADDRESS)

if __name__ == "__main__":
    daemon = BoardDaemon()
    daemon.run()
