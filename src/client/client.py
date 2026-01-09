import socket
import threading
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext


class GameClient:
    def __init__(self, host='localhost', port=5000, gui=None):
        self.host = host
        self.port = port
        self.socket = None
        self.player_name = None
        self.connected = False
        self.gui = gui  # tham chiếu GUI để cập nhật giao diện
        self.opponent = None
        
    def connect(self, player_name):
        """Kết nối tới server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.player_name = player_name

            # Gửi tên người chơi (handshake đơn giản)
            self.socket.send(player_name.encode('utf-8'))
            self.connected = True
            self.opponent = None

            # Bắt đầu thread nhận dữ liệu
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

            if self.gui:
                self.gui.set_opponent(None)
            return True
        except Exception as e:
            print(f"Lỗi kết nối: {e}")
            return False
    
    def receive_messages(self):
        """Nhận message từ server (newline-delimited JSON)"""
        buffer = ''
        while self.connected:
            try:
                raw = self.socket.recv(4096).decode('utf-8')
                if not raw:
                    break
                buffer += raw
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line.strip():
                        continue
                    try:
                        message = json.loads(line)
                        self.handle_server_message(message)
                    except json.JSONDecodeError:
                        if self.gui:
                            self.gui.run_on_ui(self.gui.append_chat, f"Server: {line}")
            except OSError:
                break
        self.connected = False
        if self.gui:
            self.gui.run_on_ui(self.gui.set_connected, False)

    def handle_server_message(self, message):
        """Xử lý message nhận từ server"""
        msg_type = message.get('type')
        content = message.get('content')
        sender = message.get('sender', 'Server')

        if not self.gui:
            return

        if msg_type == 'SYSTEM':
            self.gui.run_on_ui(self.gui.append_chat, f"[SYSTEM] {content}")
        elif msg_type == 'MATCH':
            opponent = content.get('opponent') if isinstance(content, dict) else content
            self.opponent = opponent
            self.gui.run_on_ui(self.gui.set_opponent, opponent)
            self.gui.run_on_ui(self.gui.append_chat, f"Đã ghép cặp với {opponent}")
        elif msg_type in ('CHAT', 'MSG'):
            self.gui.run_on_ui(self.gui.append_chat, f"{sender}: {content}")
        elif msg_type == 'RESULT':
            if isinstance(content, dict):
                self.gui.run_on_ui(self.gui.show_result, content)
        elif msg_type == 'OPPONENT_LEFT':
            self.opponent = None
            self.gui.run_on_ui(self.gui.append_chat, content)
            self.gui.run_on_ui(self.gui.set_opponent, None)
        elif msg_type == 'ERROR':
            self.gui.run_on_ui(self.gui.append_chat, f"[Lỗi] {content}")
        else:
            self.gui.run_on_ui(self.gui.append_chat, f"{sender}: {content}")
    
    def send_move(self, move):
        """Gửi nước đi tới server"""
        if not self.connected:
            return
        try:
            message = {
                'type': 'MOVE',
                'content': move,
                'sender': self.player_name
            }
            self.socket.send((json.dumps(message) + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Lỗi gửi: {e}")
    
    def send_message(self, text):
        """Gửi tin nhắn tới server"""
        if not self.connected:
            return
        try:
            message = {
                'type': 'MSG',
                'content': text,
                'sender': self.player_name
            }
            self.socket.send((json.dumps(message) + "\n").encode('utf-8'))
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
        self.current_opponent = None
        self.init_components()
    
    def init_components(self):
        """Khởi tạo các thành phần GUI"""
        # Frame trên - Kết nối
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.server_label = tk.Label(top_frame, text="Server: (chưa chọn)")
        self.server_label.pack(side=tk.LEFT)
        
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

        self.opponent_label = tk.Label(
            top_frame,
            text="Đối thủ: (chưa có)",
            fg="blue"
        )
        self.opponent_label.pack(side=tk.LEFT, padx=10)
        
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

        # Kết quả gần nhất
        self.result_label = tk.Label(self.root, text="Kết quả: -")
        self.result_label.pack(fill=tk.X, padx=10)
        
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
        if not player_name:
            return

        host = simpledialog.askstring("Kết nối", "Nhập server (IP hoặc hostname):", initialvalue="localhost")
        if not host:
            return
        port = simpledialog.askinteger("Kết nối", "Nhập port:", initialvalue=5000, minvalue=1, maxvalue=65535)
        if not port:
            return

        self.client = GameClient(host=host, port=port, gui=self)
        if self.client.connect(player_name):
            self.server_label.config(text=f"Server: {host}:{port}")
            self.append_chat("✓ Kết nối thành công!")
            self.set_connected(True)
        else:
            messagebox.showerror("Lỗi", "Không thể kết nối tới server")
    
    def on_move(self, move):
        """Xử lý nước đi"""
        if self.client and self.client.connected:
            self.append_chat(f"Bạn chọn: {move}")
            self.client.send_move(move)
    
    def on_send_message(self):
        """Xử lý gửi tin nhắn"""
        text = self.input_field.get()
        if text and self.client and self.client.connected:
            self.append_chat(f"Bạn: {text}")
            self.client.send_message(text)
            self.input_field.delete(0, tk.END)
    
    def append_chat(self, message):
        """Thêm message vào chat area"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def run_on_ui(self, func, *args, **kwargs):
        """Đảm bảo cập nhật UI an toàn từ thread khác"""
        self.root.after(0, lambda: func(*args, **kwargs))

    def set_opponent(self, opponent_name):
        """Cập nhật thông tin đối thủ và bật/tắt nút chơi"""
        self.current_opponent = opponent_name
        if opponent_name:
            self.opponent_label.config(text=f"Đối thủ: {opponent_name}")
            self.set_play_enabled(True)
        else:
            self.opponent_label.config(text="Đối thủ: (chưa có)")
            self.set_play_enabled(False)

    def show_result(self, content: dict):
        """Hiển thị kết quả trận"""
        your_move = content.get('your_move')
        opp_move = content.get('opponent_move')
        result_text = content.get('result_text', '')
        opponent = content.get('opponent', 'Đối thủ')
        line = f"Kết quả: {result_text} (Bạn: {your_move} - {opponent}: {opp_move})"
        self.result_label.config(text=line)
        self.append_chat(line)
    
    def set_connected(self, connected):
        """Cập nhật trạng thái kết nối"""
        if connected:
            self.status_label.config(
                text="Trạng thái: Đã kết nối", 
                fg="green"
            )
            self.connect_button.config(state=tk.DISABLED)
            self.set_play_enabled(self.current_opponent is not None)
        else:
            self.status_label.config(
                text="Trạng thái: Chưa kết nối", 
                fg="red"
            )
            self.connect_button.config(state=tk.NORMAL)
            self.set_play_enabled(False)
            self.set_opponent(None)

    def set_play_enabled(self, enabled: bool):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.rock_button.config(state=state)
        self.paper_button.config(state=state)
        self.scissors_button.config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    gui = ClientGUI(root)
    root.mainloop()
