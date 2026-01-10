# Trò Chơi Kéo-Búa-Bao

## Tổng Quan

Dự án này triển khai một trò chơi Kéo-Búa-Bao nhiều người chơi sử dụng Python. Hệ thống bao gồm kiến trúc server và client, cho phép người chơi kết nối và chơi với nhau theo thời gian thực. Logic trò chơi tuân theo các quy tắc truyền thống của Kéo-Búa-Bao.

## Tính Năng

- **Server**: Quản lý kết nối client, phát tin nhắn và xử lý logic trò chơi.
- **Client**: Cung cấp giao diện đồ họa (GUI) để người chơi tương tác với trò chơi.
- **Quy Tắc Trò Chơi**: Triển khai logic để xác định người chiến thắng dựa trên các lượt chơi của người chơi.
- **Tin Nhắn**: Sử dụng tin nhắn định dạng JSON để giao tiếp giữa server và client.

## Cấu Trúc Dự Án

```
Rock-Paper-Scissors/
├── README.md
├── requirements.txt
├── src/
│   ├── client/
│   │   └── client.py       # Triển khai phía client
│   ├── common/
│   │   ├── game_rules.py   # Logic và quy tắc trò chơi
│   │   └── message.py      # Cấu trúc tin nhắn để giao tiếp
│   └── server/
│       └── server.py       # Triển khai phía server
```

## Cách Chạy

### Yêu Cầu

- Python 3.6 hoặc cao hơn
- Không cần thư viện bên ngoài (sử dụng các thư viện có sẵn như `socket`, `threading`, và `tkinter`)

### Các Bước

1. Clone repository:
   ```bash
   git clone <repository-url>
   cd Rock-Paper-Scissors
   ```
2. Chạy server:
   ```bash
   python src/server/server.py
   ```
3. Chạy client:
   ```bash
   python src/client/client.py
   ```
4. Nhập tên người chơi và kết nối đến server.

## Quy Tắc Trò Chơi

- Người chơi chọn một trong ba lượt chơi: Kéo, Búa, hoặc Bao.
- Người chiến thắng được xác định như sau:
  - Kéo thắng Bao
  - Bao thắng Búa
  - Búa thắng Kéo
- Nếu cả hai người chơi chọn cùng một lượt, trò chơi hòa.
