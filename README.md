# Rock-Paper-Scissors Game - Multi Client-Server

## 📝 Mô tả dự án
Game Rock-Paper-Scissors sử dụng Socket programming với kiến trúc Multi Client-Server sử dụng **Python**.

## 📁 Cấu trúc project

```
src/
├── server/
│   └── server.py           # Server chính (xử lý multi-client)
├── client/
│   └── client.py           # Client GUI + Socket connection
└── common/
    ├── game_rules.py       # Logic game
    └── message.py          # Định nghĩa cấu trúc message
```

## 🛠️ Công nghệ sử dụng
- **Python 3.x**: Ngôn ngữ lập trình
- **Socket**: Giao tiếp Client-Server
- **Tkinter**: GUI cho client
- **Threading**: Xử lý đa client đồng thời
- **JSON**: Định dạng message

## ✨ Tính năng cơ bản
- [x] Cấu trúc sườn project
- [ ] Kết nối Server-Client
- [ ] GUI cho người chơi
- [ ] Logic tính điểm game
- [ ] Match-making giữa các client
- [ ] Hiển thị kết quả trận đấu
- [ ] Chat giữa các player
- [ ] Bảng xếp hạng

## 👥 Phân công công việc (3 thành viên)
- **Nhánh feature/server**: Xử lý Server (socket, threading), match-making, quản lý phòng/điểm, gửi kết quả và broadcast.
- **Nhánh feature/client**: Client GUI Tkinter, kết nối socket, hiển thị đối thủ/kết quả/điểm, chat đơn giản, xử lý gửi MOVE/MSG.
- **Nhánh feature/common**: Logic game (win/lose/draw), format message JSON, cấu trúc dữ liệu chung, chuẩn giao thức (type, payload), viết helper validate move.

## 🚀 Hướng dẫn chạy

### Yêu cầu
```bash
pip install -r requirements.txt
```

### Chạy Server:
```bash
python src/server/server.py
```

### Chạy Client (mở nhiều terminal):
```bash
python src/client/client.py
```

## 📋 File cần hoàn thiện

### server.py
- [ ] Xử lý logic match-making
- [ ] Lưu thông tin trận đấu
- [ ] Tính điểm
- [ ] Gửi kết quả lại client

### client.py
- [ ] Cải thiện UI
- [ ] Hiển thị đối thủ
- [ ] Hiển thị kết quả
- [ ] Hiển thị điểm

### game_rules.py
- [x] Cơ bản hoàn thành

## 🎮 Luật chơi
- Rock thắng Scissors
- Scissors thắng Paper
- Paper thắng Rock
- Cùng nước thì hòa

## 📊 Message Format
```json
{
    "type": "MOVE",
    "content": "ROCK",
    "sender": "Player1",
    "timestamp": "2026-01-08T10:30:00"
}
```

## 🔧 TODO List
- [ ] Hoàn thiện Server logic
- [ ] Hoàn thiện Client GUI
- [ ] Test kết nối
- [ ] Thêm match-making
- [ ] Thêm system bảng xếp hạng
- [ ] Thêm database SQLite
- [ ] Thêm phản hồi âm thanh
