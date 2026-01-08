import socket
import threading
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext


class GameClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.player_name = None
        self.connected = False
        
    def connect(self, player_name):
        """Kết nối tới server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.player_name = player_name
            
            # Gửi tên người chơi
            self.socket.send(player_name.encode('utf-8'))
            self.connected = True
            
            # Bắt đầu thread nhận dữ liệu
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
    
    def receive_messages(self):
        """Nhận message từ server"""
        while self.connected:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"[Server]: {message}")
            except:
                break
    
    def send_move(self, move):
        """Gửi nước đi tới server"""
        try:
            message = {
                'type': 'MOVE',
                'content': move,
                'sender': self.player_name
            }
            self.socket.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Lỗi gửi: {e}")
    
    def send_message(self, text):
        """Gửi tin nhắn tới server"""
        try:
            message = {
                'type': 'MSG',
                'content': text,
                'sender': self.player_name
            }
            self.socket.send(json.dumps(message).encode('utf-8'))
        except Exception as e:
            print(f"Lỗi gửi: {e}")
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            self.socket.close()


class ClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors - Client")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.client = None
        self.init_components()
    
    def init_components(self):
        """Khởi tạo các thành phần GUI"""
        # Frame trên - Kết nối
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        tk.Label(top_frame, text="Server: localhost:5000").pack(side=tk.LEFT)
        
        self.connect_button = tk.Button(
            top_frame, 
            text="Kết nối", 
            command=self.on_connect
        )
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(
            top_frame, 
            text="Trạng thái: Chưa kết nối", 
            fg="red"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Frame giữa - Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            height=15, 
            width=70,
            state=tk.DISABLED
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame game buttons
        game_frame = tk.LabelFrame(self.root, text="Chọn nước đi")
        game_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.rock_button = tk.Button(
            game_frame, 
            text="🪨 Rock", 
            width=15,
            command=lambda: self.on_move("ROCK"),
            state=tk.DISABLED
        )
        self.rock_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.paper_button = tk.Button(
            game_frame, 
            text="📄 Paper", 
            width=15,
            command=lambda: self.on_move("PAPER"),
            state=tk.DISABLED
        )
        self.paper_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.scissors_button = tk.Button(
            game_frame, 
            text="✂️ Scissors", 
            width=15,
            command=lambda: self.on_move("SCISSORS"),
            state=tk.DISABLED
        )
        self.scissors_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Frame nhập liệu
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.input_field = tk.Entry(input_frame)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        send_button = tk.Button(
            input_frame, 
            text="Gửi", 
            command=self.on_send_message
        )
        send_button.pack(side=tk.LEFT, padx=5)
    
    def on_connect(self):
        """Xử lý kết nối"""
        player_name = simpledialog.askstring("Kết nối", "Nhập tên của bạn:")
        if player_name:
            self.client = GameClient()
            if self.client.connect(player_name):
                self.append_chat("✓ Kết nối thành công!")
                self.set_connected(True)
            else:
                messagebox.showerror("Lỗi", "Không thể kết nối tới server")
    
    def on_move(self, move):
        """Xử lý nước đi"""
        if self.client:
            self.append_chat(f"Bạn chọn: {move}")
            self.client.send_move(move)
    
    def on_send_message(self):
        """Xử lý gửi tin nhắn"""
        text = self.input_field.get()
        if text and self.client:
            self.append_chat(f"Bạn: {text}")
            self.client.send_message(text)
            self.input_field.delete(0, tk.END)
    
    def append_chat(self, message):
        """Thêm message vào chat area"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def set_connected(self, connected):
        """Cập nhật trạng thái kết nối"""
        if connected:
            self.status_label.config(
                text="Trạng thái: Đã kết nối", 
                fg="green"
            )
            self.connect_button.config(state=tk.DISABLED)
            self.rock_button.config(state=tk.NORMAL)
            self.paper_button.config(state=tk.NORMAL)
            self.scissors_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(
                text="Trạng thái: Chưa kết nối", 
                fg="red"
            )
            self.connect_button.config(state=tk.NORMAL)
            self.rock_button.config(state=tk.DISABLED)
            self.paper_button.config(state=tk.DISABLED)
            self.scissors_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    gui = ClientGUI(root)
    root.mainloop()
