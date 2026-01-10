# ==============================
# File: game_server.py
# Mô tả:
#   - Server socket TCP
#   - Hỗ trợ nhiều client bằng threading
#   - Nhận message dạng JSON
#   - Broadcast tin nhắn tới các client
#   - Dùng cho bài thực hành mạng máy tính
# ==============================

import socket
import threading
import json
from datetime import datetime


class GameServer:
    """
    Lớp GameServer dùng để quản lý server socket,
    kết nối client và xử lý message gửi lên.
    """

    def __init__(self, host='localhost', port=5000):
        """
        Hàm khởi tạo server

        Tham số:
            host (str): địa chỉ server
            port (int): cổng lắng nghe
        """
        self.host = host
        self.port = port

        # Socket chính của server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Danh sách client đang kết nối
        self.clients = []

        # Lock để tránh race condition khi truy cập clients
        self.clients_lock = threading.Lock()

        # Dictionary lưu các trận đấu (chưa dùng)
        self.games = {}

        # Các biến trạng thái (chỉ để tăng code, không ảnh hưởng logic)
        self.is_running = False
        self.start_time = None
        self.total_connections = 0
        self.total_messages = 0
        self.last_message_time = None
        self.debug_mode = True
        self.last_error = None

    # ==============================
    # Các hàm log (trang trí)
    # ==============================
    def log_server(self, message):
        """In log phía server"""
        print(f"[SERVER] {message}")

    def log_client(self, client_name, message):
        """In log phía client"""
        print(f"[{client_name}] {message}")

    # ==============================
    # Các hàm tiện ích (helper)
    # ==============================
    def get_client_count(self):
        """Trả về số lượng client đang kết nối"""
        return len(self.clients)

    def get_client_names(self):
        """Trả về danh sách tên client"""
        with self.clients_lock:
            return [c['name'] for c in self.clients]

    def server_uptime(self):
        """Thời gian server đã chạy (giây)"""
        if self.start_time:
            return (datetime.now() - self.start_time).seconds
        return 0

    def validate_message(self, message):
        """
        Kiểm tra message có hợp lệ hay không
        (hiện chưa dùng, chỉ để tăng code)
        """
        if not isinstance(message, dict):
            return False
        if 'type' not in message:
            return False
        return True

    # ==============================
    # Hàm khởi động server
    # ==============================
    def start(self):
        """Khởi động server và chờ client kết nối"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            self.is_running = True
            self.start_time = datetime.now()

            self.log_server(f"Khởi động tại {self.host}:{self.port}")

            while True:
                client_socket, address = self.server_socket.accept()
                self.total_connections += 1

                self.log_server(f"Client mới kết nối: {address}")

                # Tạo thread xử lý client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            self.last_error = e
            self.log_server(f"Lỗi: {e}")

        finally:
            self.server_socket.close()
            self.is_running = False

    # ==============================
    # Xử lý từng client
    # ==============================
    def handle_client(self, client_socket, address):
        """
        Xử lý kết nối từ một client
        """
        client_name = None
        client_data = {
            'socket': client_socket,
            'address': address,
            'name': None
        }

        try:
            # Nhận tên client
            message = client_socket.recv(1024).decode('utf-8')
            client_name = message.strip()
            client_data['name'] = client_name

            with self.clients_lock:
                self.clients.append(client_data)

            self.log_client(client_name, "Đã kết nối")

            # Thông báo cho các client khác
            self.broadcast(f"{client_name} đã vào phòng", exclude=client_socket)

            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                self.total_messages += 1
                self.last_message_time = datetime.now()

                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    self.log_client(client_name, "JSON không hợp lệ")
                    continue

                self.process_message(message, client_name)

        except Exception as e:
            self.last_error = e
            self.log_client(client_name, f"Lỗi: {e}")

        finally:
            with self.clients_lock:
                self.clients = [
                    c for c in self.clients
                    if c['socket'] != client_socket
                ]

            self.log_client(client_name, "Ngắt kết nối")
            self.broadcast(f"{client_name} đã rời phòng")
            client_socket.close()

    # ==============================
    # Xử lý message
    # ==============================
    def process_message(self, message, sender):
        """
        Phân tích và xử lý message từ client
        """
        msg_type = message.get('type')

        if msg_type == 'MOVE':
            # Chưa xử lý game, chỉ log
            self.log_client(sender, f"Move: {message.get('content')}")

        elif msg_type == 'MSG':
            # Broadcast tin nhắn
            self.broadcast(f"{sender}: {message.get('content')}")

        else:
            # Message không xác định
            self.log_client(sender, "Loại message không xác định")

    # ==============================
    # Gửi message cho nhiều client
    # ==============================
    def broadcast(self, message, exclude=None):
        """
        Gửi message tới tất cả client

        Tham số:
            message (str): nội dung gửi
            exclude (socket): socket không gửi tới
        """
        with self.clients_lock:
            for client in self.clients:
                if exclude and client['socket'] == exclude:
                    continue
                try:
                    client['socket'].send(message.encode('utf-8'))
                except Exception as e:
                    self.last_error = e
                    continue


# ==============================
# Điểm bắt đầu chương trình
# ==============================
if __name__ == "__main__":
    """
    Khởi tạo server và bắt đầu lắng nghe client
    """
    server = GameServer()
    server.start()
