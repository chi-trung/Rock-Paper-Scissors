"""
Định nghĩa cấu trúc message giữa Client và Server
"""
import json
from datetime import datetime


class Message:
    """Lớp định nghĩa message"""
    
    def __init__(self, msg_type, content, sender):
        """
        Args:
            msg_type: 'MOVE', 'MESSAGE', 'STATUS'
            content: Nội dung message
            sender: Tên người gửi
        """
        self.type = msg_type
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now().isoformat()
    
    def to_json(self):
        """Chuyển đổi thành JSON"""
        return json.dumps({
            'type': self.type,
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp
        })
    
    @staticmethod
    def from_json(json_str):
        """Tạo Message từ JSON"""
        data = json.loads(json_str)
        msg = Message(data['type'], data['content'], data['sender'])
        msg.timestamp = data['timestamp']
        return msg
    
    def __str__(self):
        return f"[{self.type}] {self.sender}: {self.content}"
