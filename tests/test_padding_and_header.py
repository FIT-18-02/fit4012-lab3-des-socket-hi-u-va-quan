from des_socket_utils import pad, unpad, encrypt_des_cbc, build_packet, parse_header, HEADER_SIZE

def test_pad_unpad_roundtrip():
    """Kiểm tra tính toàn vẹn của dữ liệu sau khi pad và unpad."""
    data = b"hello DES socket"
    # Đảm bảo unpad(pad(x)) trả về đúng x ban đầu
    assert unpad(pad(data)) == data

def test_build_packet_contains_correct_length():
    """Kiểm tra cấu trúc gói tin (Header + Ciphertext)."""
    # 1. Chuẩn bị dữ liệu mẫu (7 bytes, cần được pad lên 8 bytes bên trong encrypt_des_cbc)
    message = b"FIT4012"
    key, iv, cipher_bytes = encrypt_des_cbc(message)
    
    # 2. Đóng gói
    packet = build_packet(key, iv, cipher_bytes)
    
    # 3. Tách Header dựa trên hằng số HEADER_SIZE (thay vì số 20 cứng nhắc)
    header = packet[:HEADER_SIZE]
    k2, iv2, length = parse_header(header)
    
    # 4. Kiểm tra các thành phần trong Header
    assert k2 == key
    assert iv2 == iv
    assert length == len(cipher_bytes)
    
    # 5. Kiểm tra phần nội dung (Payload) sau Header
    assert packet[HEADER_SIZE:] == cipher_bytes

def test_padding_logic():
    """Bổ sung: Kiểm tra xem padding có luôn tạo ra bội số của 8 (block size của DES) không."""
    assert len(pad(b"123")) == 8
    assert len(pad(b"12345678")) == 16  # PKCS5/7 luôn thêm ít nhất 1 block nếu dữ liệu đã vừa khít
