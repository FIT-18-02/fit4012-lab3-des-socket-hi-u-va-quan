import struct
from des_socket_utils import encrypt_des_cbc, decrypt_des_cbc, build_packet, parse_header

def test_protocol_contract_order_is_key_iv_length_ciphertext():
    """Kiểm tra cấu trúc gói tin phải đúng thứ tự: Key -> IV -> Length -> Ciphertext"""
    test_plain = b"FIT4012 contract test"
    test_key = b"12345678"
    test_iv = b"abcdefgh"
    
    # 1. Thực hiện mã hóa
    key, iv, cipher_bytes = encrypt_des_cbc(test_plain, key=test_key, iv=test_iv)
    
    # 2. Đóng gói gói tin
    packet = build_packet(key, iv, cipher_bytes)
    
    # Kiểm tra Key (8 byte đầu)
    assert packet[:8] == key, "Key phải nằm ở 8 byte đầu tiên"
    
    # Kiểm tra IV (8 byte tiếp theo)
    assert packet[8:16] == iv, "IV phải nằm ở các byte từ 8 đến 16"
    
    # Kiểm tra trường Length (4 byte tiếp theo - dùng định dạng Big-endian '!I')
    length_in_packet = struct.unpack('!I', packet[16:20])[0]
    assert length_in_packet == len(cipher_bytes), "Trường Length trong header phải khớp với độ dài Ciphertext thực tế"
    
    # Kiểm tra Ciphertext (phần còn lại từ byte 20 trở đi)
    assert packet[20:] == cipher_bytes, "Ciphertext phải bắt đầu từ byte thứ 20"
    
    # Kiểm tra tính chất của DES (Ciphertext phải là bội số của 8 do có Padding)
    assert len(cipher_bytes) % 8 == 0, "Độ dài Ciphertext DES phải là bội số của 8"

def test_end_to_end_decryption_integrity():
    """Kiểm tra tính toàn vẹn: Dữ liệu sau khi giải mã phải giống hệt dữ liệu gốc"""
    original_msg = b"Hello Quan and Hieu! Lab 3 Cryptography."
    
    # Mã hóa
    key, iv, cipher_bytes = encrypt_des_cbc(original_msg)
    
    # Giải mã
    decrypted_msg = decrypt_des_cbc(key, iv, cipher_bytes)
    
    assert decrypted_msg == original_msg, "Dữ liệu giải mã không khớp với dữ liệu gốc"

def test_parse_header_functionality():
    """Kiểm tra hàm parse_header có tách đúng thông tin từ gói tin không"""
    test_key = b"KEY12345"
    test_iv = b"IV123456"
    test_cipher = b"SOME_CIPHER_DATA" # 16 bytes
    
    packet = build_packet(test_key, test_iv, test_cipher)
    header = packet[:20]
    
    p_key, p_iv, p_len = parse_header(header)
    
    assert p_key == test_key
    assert p_iv == test_iv
    assert p_len == len(test_cipher)
