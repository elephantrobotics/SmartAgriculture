import socketserver
import logging
import time
import socket
import threading

logging.basicConfig(level=logging.INFO)
'''
class TcpServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address):
        super().__init__(server_address, TcpRequestHandler)
        # 果子参数
        self.good_fruit_str = "apple"
        self.bad_fruit_str = "orange"
        self.invalid_fruit_str = "none"

        self.target = self.invalid_fruit_str
        self.target_copy = self.target

    def good_fruit(self, fruit_type):
        return fruit_type == self.good_fruit_str

    def bad_fruit(self, fruit_type):
        return fruit_type == self.bad_fruit_str

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target

    def get_target_copy(self):
        return self.target_copy

    def set_target_copy(self, copy):
        self.target_copy = copy

    def clear(self):
        self.set_target(self.invalid_fruit_str)
        self.set_target_copy(self.invalid_fruit_str)

class TcpRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client_address = self.client_address[0]
        logging.info(f"[NEW CONNECTION] {client_address} connected.")

        while True:
            try:
                server = self.server
                target = server.get_target()

                if server.good_fruit(target):
                    logging.info("good fruit:", server.good_fruit_str)
                    self.request.sendall(server.good_fruit_str.encode())
                elif server.bad_fruit(target):
                    logging.info("bad fruit:", server.bad_fruit_str)
                    self.request.sendall(server.bad_fruit_str.encode())
                else:
                    # logging.info("invalid fruit:", server.invalid_fruit_str)
                    self.request.sendall(server.invalid_fruit_str.encode())

                server.set_target_copy(target)
                server.set_target(server.invalid_fruit_str)
                print(" service is Running ")
                data = self.request.recv(1024)
                print("\n\n\n\n")
                print(data)
                print("\n\n\n\n")
                
                if not data:
                    break

                time.sleep(0.1)
            except ConnectionResetError as e:
                print(e)
                break

        logging.info(f"[DISCONNECTED] {client_address} disconnected.")

if __name__ == "__main__":
    server_address = ('127.0.0.1', 12345)
    server = TcpServer(server_address)
    logging.info(f"[LISTENING] Server is listening on {server_address[0]}:{server_address[1]}")
    server.serve_forever()
'''


class TcpServer(threading.Thread):
    def __init__(self, server_address) -> None:
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(server_address)
        print("server Binding succeeded!")
        self.s.listen(1)
        self.connected_obj = None

        # 果子参数
        self.good_fruit_str = "apple"
        self.bad_fruit_str = "orange"
        self.invalid_fruit_str = "none"

        self.target = self.invalid_fruit_str
        self.target_copy = self.target
        self.start_move = False

    def good_fruit(self, fruit_type):
        return fruit_type == self.good_fruit_str

    def bad_fruit(self, fruit_type):
        return fruit_type == self.bad_fruit_str

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target

    def get_target_copy(self):
        return self.target_copy

    def set_target_copy(self, copy):
        self.target_copy = copy

    def clear(self):
        self.set_target(self.invalid_fruit_str)
        self.set_target_copy(self.invalid_fruit_str)

    def R2_action_done(self):
        self.start_move = False
        self.send_info("1")

    def send_info(self, data):
        self.connected_obj.sendall(data.encode())

    def run(self):
        while True:
            # try:
            print("waiting connect!------------------")
            self.connected_obj, addr = self.s.accept()
            while True:
                # try:
                print("waiting data--------")
                data = self.connected_obj.recv(1024)
                command = data.decode('utf-8')
                print(command)
                self.start_move = True


if __name__ == "__main__":
    server_address = ('127.0.0.1', 12345)
    server = TcpServer(server_address)
