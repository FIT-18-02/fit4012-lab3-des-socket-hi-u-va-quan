import os
import socket
import sys
from des_socket_utils import encrypt_des_cbc, build_packet

# Lấy cấu hình từ biến môi trường hoặc dùng mặc định
SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '6000'))
MESSAGE_ENV = os.getenv('MESSAGE')
LOG_FILE = os.getenv('SENDER_LOG_FILE', '')

def get_message() -> bytes:
    """Lấy bản tin từ biến môi trường hoặc từ bàn phím"""
    if MESSAGE_ENV is not None:
        return MESSAGE_ENV.encode('utf-8')
    try:
        plain = input("Nhập bản tin cần gửi: ")
        return plain.encode('utf-8')
    except EOFError:
        return b"Default message from CI"

def main() -> None:
    try:
        # 1. Chuẩn bị dữ liệu
        plain = get_message()
        print(f"[*] Đang xử lý bản tin: {plain.decode('utf-8', errors='ignore')}")
        
        # 2. Mã hóa DES-CBC
        key, iv, cipher_bytes = encrypt_des_cbc(plain)
        
        # 3. Đóng gói packet (Key + IV + Length + Ciphertext)
        overall = build_packet(key, iv, cipher_bytes)

        # 4. Gửi qua Socket
        print(f"[*] Đang kết nối tới {SERVER_IP}:{SERVER_PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10) # Tránh treo chương trình nếu server không phản hồi
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(overall)
            print("[+] Gửi gói tin thành công!")

        # 5. Hiển thị thông tin minh chứng (Quan trọng để copy vào log)
        lines = [
            "--- SENDER LOG ---",
            f"Plaintext: {plain.decode('utf-8', errors='ignore')}",
            f"Key (hex): {key.hex()}",
            f"IV (hex):  {iv.hex()}",
            f"Ciphertext (hex): {cipher_bytes.hex()}",
            f"Total Packet Size: {len(overall)} bytes",
            "------------------"
        ]
        
        for line in lines:
            print(line)

        # 6. Ghi log ra file nếu có yêu cầu (Dùng cho CI)
        if LOG_FILE:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) if os.path.dirname(LOG_FILE) else None
            with open(LOG_FILE, 'a', encoding='utf-8') as f: # Dùng 'a' để ghi nối tiếp nếu cần
                f.write('\n'.join(lines) + '\n\n')

    except ConnectionRefusedError:
        print(f"[!] Lỗi: Không thể kết nối tới Server tại {SERVER_IP}:{SERVER_PORT}. Hãy chạy receiver.py trước!")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Lỗi không xác định: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
