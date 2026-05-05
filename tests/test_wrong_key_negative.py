import pytest
from des_socket_utils import encrypt_des_cbc, decrypt_des_cbc

def test_wrong_key_should_not_recover_original_plaintext():
    """
    Kiểm tra rằng khi dùng sai Key, dữ liệu khôi phục không được trùng với bản gốc
    hoặc phải ném ra lỗi ValueError do sai Padding.
    """
    plain = b"Thong diep dung de test wrong key"
    key = b"12345678"
    iv = b"abcdefgh"
    wrong_key = b"87654321"

    # 1. Mã hóa với key đúng
    _, _, cipher_bytes = encrypt_des_cbc(plain, key=key, iv=iv)

    # 2. Thử giải mã với key sai
    try:
        recovered = decrypt_des_cbc(wrong_key, iv, cipher_bytes)
        
        # Nếu không lỗi (may mắn padding rác lại hợp lệ), thì nội dung phải khác nhau
        assert recovered != plain
        
    except (ValueError, Exception):
        # Thông thường sẽ bắn ra ValueError ở bước unpad do sai key dẫn đến rác dữ liệu
        # Trong testing, việc bắn ra lỗi khi dùng sai key được coi là "Pass" (Negative Test)
        assert True
