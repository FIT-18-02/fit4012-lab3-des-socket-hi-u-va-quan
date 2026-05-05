#!/usr/bin/env bash
set -euo pipefail

# Lấy Port và Message từ tham số dòng lệnh hoặc dùng mặc định
PORT="${1:-6001}"
MESSAGE="${2:-Xin chao FIT4012 - Quan & Hieu}"

echo "[*] Bat dau chay demo Lab 3 tai Port: $PORT"

# 1. Chạy Receiver dưới nền (Background)
# Thêm SENDER_LOG_FILE để CI hoặc script tự lưu log nếu cần
PYTHONUNBUFFERED=1 RECEIVER_HOST=127.0.0.1 RECEIVER_PORT="$PORT" SOCKET_TIMEOUT=10 python receiver.py &
receiver_pid=$!

# Đợi một chút để Receiver kịp khởi tạo socket
sleep 2

# 2. Chạy Sender để gửi tin nhắn
echo "[*] Sender dang gui tin nhan..."
SERVER_IP=127.0.0.1 SERVER_PORT="$PORT" MESSAGE="$MESSAGE" python sender.py

# 3. Đợi một lát để Receiver xử lý xong rồi đóng Receiver
sleep 2
echo "[*] Ket thuc demo, dang dong Receiver (PID: $receiver_pid)..."

# Dung kill thay vi wait de script khong bi treo neu receiver dung vong lap while True
kill "$receiver_pid" || true

echo "[+] Demo hoan tat ruc ro!"
//QH
