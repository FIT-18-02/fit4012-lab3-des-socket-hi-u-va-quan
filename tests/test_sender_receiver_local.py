import os
import socket
import subprocess
import sys
import time
from pathlib import Path

# Xác định thư mục gốc của project
REPO_ROOT = Path(__file__).resolve().parents[1]

def find_free_port() -> int:
    """Tìm một cổng trống để tránh xung đột khi chạy test"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def test_local_sender_receiver_roundtrip():
    """
    Kiểm tra luồng gửi-nhận thực tế: 
    Sender gửi tin nhắn mã hóa -> Receiver nhận và giải mã thành công.
    """
    port = find_free_port()
    test_message = "Xin chao FIT4012 - local integration test"
    
    # Thiết lập môi trường cho Receiver
    receiver_env = os.environ.copy()
    receiver_env.update({
        "PYTHONUNBUFFERED": "1",
        "RECEIVER_HOST": "127.0.0.1",
        "RECEIVER_PORT": str(port),
        "SOCKET_TIMEOUT": "10", # Tăng timeout để ổn định hơn trên CI
    })
    
    # Thiết lập môi trường cho Sender
    sender_env = os.environ.copy()
    sender_env.update({
        "PYTHONUNBUFFERED": "1",
        "SERVER_IP": "127.0.0.1",
        "SERVER_PORT": str(port),
        "MESSAGE": test_message,
    })

    # 1. Khởi chạy Receiver dưới nền
    receiver = subprocess.Popen(
        [sys.executable, "-u", "receiver.py"],
        cwd=REPO_ROOT,
        env=receiver_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        # 2. Đợi Receiver sẵn sàng (Lắng nghe)
        started = False
        start_time = time.time()
        collected = []
        while time.time() - start_time < 7: # Tăng thời gian chờ lên 7s
            line = receiver.stdout.readline()
            if line:
                collected.append(line)
                # Sửa logic này để khớp với câu thông báo trong receiver.py của Quân
                if "Đang lắng nghe" in line or "Listening" in line:
                    started = True
                    break
            time.sleep(0.1)
        
        assert started, "Receiver không khởi động đúng hoặc không in dòng 'Đang lắng nghe'. Output: " + "".join(collected)

        # 3. Khởi chạy Sender để gửi dữ liệu
        sender = subprocess.run(
            [sys.executable, "sender.py"],
            cwd=REPO_ROOT,
            env=sender_env,
            capture_output=True,
            text=True,
            timeout=15,
            check=True,
        )

        # 4. Lấy toàn bộ output từ Receiver
        try:
            receiver_out, _ = receiver.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            receiver.kill()
            receiver_out, _ = receiver.communicate()
            
        full_receiver_output = "".join(collected) + receiver_out

        # 5. Kiểm tra kết quả phía Sender
        assert "[+] Đã gửi bản mã." in sender.stdout
        assert "Key:" in sender.stdout
        assert "IV:" in sender.stdout
        assert "Ciphertext:" in sender.stdout
        
        # 6. Kiểm tra kết quả phía Receiver (Quan trọng nhất)
        # Receiver phải in ra đúng bản tin gốc sau khi giải mã
        assert f"[+] Bản tin gốc: {test_message}" in full_receiver_output or test_message in full_receiver_output

    finally:
        # Đảm bảo tắt Receiver sau khi test xong
        if receiver.poll() is None:
            receiver.kill()
            receiver.wait()
