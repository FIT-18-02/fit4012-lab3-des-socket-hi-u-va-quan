import os
import socket
import sys
from des_socket_utils import encrypt_des_cbc, build_packet

# Nhom: Pham Anh Quan & Ngo Van Hieu
# Lab 3 - FIT4012

SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '6000'))
MESSAGE_ENV = os.getenv('MESSAGE')
LOG_FILE = os.getenv('SENDER_LOG_FILE', '')

def get_message() -> bytes:
    if MESSAGE_ENV is not None:
        return MESSAGE_ENV.encode('utf-8')
    try:
        plain = input("Nhập bản tin cần gửi: ")
        return plain.encode('utf-8')
    except EOFError:
        return b"Default message for CI"

def main() -> None:
    try:
        plain = get_message()
        key, iv, cipher_bytes = encrypt_des_cbc(plain)
        overall = build_packet(key, iv, cipher_bytes)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(overall)
            # Bat buoc phai in dong nay de pass test
            print("[+] Đã gửi bản mã.")

        # Format in ra phai dung tung ky tu de test case tim thay
        lines = [
            f"Key: {key.hex()}",
            f"IV: {iv.hex()}",
            f"Ciphertext: {cipher_bytes.hex()}",
            f"Total Packet Size: {len(overall)} bytes"
        ]
        
        for line in lines:
            print(line)

        if LOG_FILE:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n\n')

    except Exception as e:
        print(f"[!] Lỗi: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
