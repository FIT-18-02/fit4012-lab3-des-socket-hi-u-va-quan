import os
import struct
from typing import Tuple
from Crypto.Cipher import DES

# Định nghĩa các hằng số theo đúng yêu cầu bài Lab 3
BLOCK_SIZE = 8
HEADER_SIZE = 8 + 8 + 4  # 8 byte Key + 8 byte IV + 4 byte Length

def pad(data: bytes) -> bytes:
    """Thêm padding PKCS#7 để dữ liệu là bội số của 8 byte"""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad(data: bytes) -> bytes:
    """Loại bỏ padding PKCS#7 và kiểm tra tính hợp lệ"""
    if not data:
        raise ValueError("Dữ liệu rỗng, không thể bỏ padding.")
    if len(data) % BLOCK_SIZE != 0:
        raise ValueError("Dữ liệu không phải bội số của BLOCK_SIZE.")
    
    pad_len = data[-1]
    # Kiểm tra giá trị padding có nằm trong khoảng hợp lệ 1-8 không
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Padding không hợp lệ.")
    # Kiểm tra toàn bộ các byte padding có giống nhau không
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Padding PKCS#7 không hợp lệ.")
    return data[:-pad_len]

def encrypt_des_cbc(plain: bytes, key: bytes | None = None, iv: bytes | None = None) -> Tuple[bytes, bytes, bytes]:
    """Mã hóa DES ở chế độ CBC"""
    key = key or os.urandom(8)
    iv = iv or os.urandom(8)
    if len(key) != 8 or len(iv) != 8:
        raise ValueError("DES key và IV phải dài đúng 8 byte.")
    
    des = DES.new(key, DES.MODE_CBC, iv)
    cipher_bytes = des.encrypt(pad(plain))
    return key, iv, cipher_bytes

def decrypt_des_cbc(key: bytes, iv: bytes, cipher_bytes: bytes) -> bytes:
    """Giải mã DES và xử lý lỗi giải mã/padding"""
    if len(key) != 8 or len(iv) != 8:
        raise ValueError("DES key và IV phải dài đúng 8 byte.")
    if len(cipher_bytes) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext phải có độ dài là bội số của 8 byte.")
    
    des = DES.new(key, DES.MODE_CBC, iv)
    decrypted_data = des.decrypt(cipher_bytes)
    
    # Hàm unpad sẽ tự động ném lỗi nếu sai khóa (dẫn đến sai padding) hoặc dữ liệu bị sửa (tamper)
    return unpad(decrypted_data)

def build_packet(key: bytes, iv: bytes, cipher_bytes: bytes) -> bytes:
    """Đóng gói theo thứ tự: Key + IV + Length + Ciphertext"""
    return key + iv + struct.pack('!I', len(cipher_bytes)) + cipher_bytes

def parse_header(header: bytes) -> tuple[bytes, bytes, int]:
    """Phân tích 20 byte header đầu tiên"""
    if len(header) != HEADER_SIZE:
        raise ValueError(f"Header phải dài đúng {HEADER_SIZE} byte.")
    key = header[:8]
    iv = header[8:16]
    length = struct.unpack('!I', header[16:20])[0]
    return key, iv, length

def recv_exact(conn, n: int) -> bytes:
    """Đảm bảo nhận đúng và đủ n byte từ socket"""
    chunks = []
    received = 0
    while received < n:
        chunk = conn.recv(min(n - received, 4096))
        if not chunk:
            raise ConnectionError("Kết nối bị đóng trước khi nhận đủ dữ liệu.")
        chunks.append(chunk)
        received += len(chunk)
    return b''.join(chunks)
