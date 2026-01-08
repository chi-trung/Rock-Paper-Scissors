import socket
import threading
import json
from datetime import datetime

class GameServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.clients_lock = threading.Lock()
        self.games = {}  # Lưu trữ các trận đấu
        
    def start(self):
        """Khởi động server"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[SERVER] Khởi động tại {self.host}:{self.port}")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVER] Client mới kết nối: {address}")
                
                # Tạo thread xử lý client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"[SERVER] Lỗi: {e}")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, address):
        """Xử lý kết nối từ một client"""
        client_name = None
        client_data = {'socket': client_socket, 'address': address, 'name': None}
        
        try:
            # Nhận tên client
            message = client_socket.recv(1024).decode('utf-8')
            client_name = message.strip()
            client_data['name'] = client_name
            
            with self.clients_lock:
                self.clients.append(client_data)
            
            print(f"[{client_name}] Đã kết nối")
            
            # Gửi thông báo tới tất cả client
            self.broadcast(f"{client_name} đã vào phòng", exclude=client_socket)
            
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                self.process_message(message, client_name)
                
        except Exception as e:
            print(f"[{client_name}] Lỗi: {e}")
        finally:
            with self.clients_lock:
                self.clients = [c for c in self.clients if c['socket'] != client_socket]
            
            print(f"[{client_name}] Ngắt kết nối")
            self.broadcast(f"{client_name} đã rời phòng")
            client_socket.close()
    
    def process_message(self, message, sender):
        """Xử lý message từ client"""
        msg_type = message.get('type')
        
        if msg_type == 'MOVE':
            # TODO: Xử lý nước đi game
            print(f"[{sender}] Move: {message.get('content')}")
            
        elif msg_type == 'MSG':
            # Broadcast message
            self.broadcast(f"{sender}: {message.get('content')}")
    
    def broadcast(self, message, exclude=None):
        """Gửi message tới tất cả client"""
        with self.clients_lock:
            for client in self.clients:
                if exclude and client['socket'] == exclude:
                    continue
                try:
                    client['socket'].send(message.encode('utf-8'))
                except:
                    pass


if __name__ == "__main__":
    server = GameServer()
    server.start()
