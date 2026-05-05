#!/usr/bin/env bash
set -euo pipefail

# 1. Cấu hình tham số
PORT="${1:-6001}"
MESSAGE="${2:-Xin chao FIT4012}"
HOST="127.0.0.1"

echo "=== Đang khởi động demo trên Port: $PORT ==="

# 2. Dọn dẹp nếu cổng đã bị chiếm (Tránh lỗi Address already in use)
if lsof -Pi :"$PORT" -sTCP:LISTEN -t >/dev/null ; then
    echo "Cảnh báo: Cổng $PORT đang bận. Đang thử đóng tiến trình cũ..."
    fuser -k "$PORT/tcp" || true
    sleep 1
fi

# 3. Chạy Receiver dưới nền
echo "1. Đang khởi tạo Receiver..."
PYTHONUNBUFFERED=1 \
RECEIVER_HOST="$HOST" \
RECEIVER_PORT="$PORT" \
SOCKET_TIMEOUT=10 \
python receiver.py &

receiver_pid=$!

# 4. Kiểm tra xem Receiver đã thực sự lắng nghe chưa thay vì chỉ sleep 1
echo "2. Đang đợi Receiver sẵn sàng..."
timeout 5 bash -c "until printf "" > /dev/tcp/$HOST/$PORT; do sleep 0.5; done" 2>/dev/null || \
{ echo "Lỗi: Receiver không phản hồi sau 5 giây"; kill $receiver_pid; exit 1; }

# 5. Chạy Sender
echo "3. Đang gửi thông điệp: '$MESSAGE'"
SERVER_IP="$HOST" \
SERVER_PORT="$PORT" \
MESSAGE="$MESSAGE" \
python sender.py

# 6. Đợi Receiver hoàn tất và đóng lại
echo "4. Đang đợi kết thúc tiến trình..."
wait "$receiver_pid"
echo "=== Demo hoàn tất thành công ==="
