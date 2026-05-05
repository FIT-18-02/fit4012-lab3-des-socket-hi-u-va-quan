import pytest
from des_socket_utils import encrypt_des_cbc, decrypt_des_cbc

def test_tampered_ciphertext_should_fail_or_change_plaintext():
    """
    Kịch bản: Kẻ tấn công can thiệp vào bản mã (Tamper).
    Kết quả mong đợi: Hàm giải mã phải ném ra lỗi Padding (do dữ liệu bị sai lệch)
    hoặc bản tin giải mã được phải khác hoàn toàn với bản tin gốc.
    """
    # 1. Chuẩn bị dữ liệu gốc
    plain = b"Thong diep dung de test tamper"
    test_key = b"12345678"
    test_iv = b"abcdefgh"
    
    # 2. Mã hóa dữ liệu chuẩn
    key, iv, cipher_bytes = encrypt_des_cbc(plain, key=test_key, iv=test_iv)
    
    # 3. Giả lập hành vi can thiệp (Tamper): Thay đổi byte cuối cùng của bản mã
    tampered = bytearray(cipher_bytes)
    tampered[-1] ^= 0xFF  # Đảo ngược toàn bộ các bit của byte cuối
    tampered_bytes = bytes(tampered)

    # 4. Kiểm tra phản ứng của hệ thống
    try:
        recovered = decrypt_des_cbc(key, iv, tampered_bytes)
        
        # Nếu không văng lỗi (xác suất rất thấp với PKCS#7), 
        # bản tin giải mã phải khác với bản tin gốc.
        assert recovered != plain, "Bản tin sau khi bị tamper không được phép giống bản tin gốc."
        
    except ValueError as e:
        # Với DES-CBC và Padding PKCS#7, việc sửa đổi ciphertext thường 
        # dẫn đến lỗi Padding không hợp lệ khi giải mã.
        print(f"[!] He thong phat hien tamper thong qua loi: {e}")
        assert "Padding" in str(e) or "Dữ liệu" in str(e)
    except Exception as e:
        pytest.fail(f"He thong nem ra loi khong mong doi: {type(e).__name__}: {e}")

def test_tamper_at_beginning_of_ciphertext():
    """Kiểm tra việc can thiệp vào những byte đầu tiên của bản mã"""
    plain = b"Tin nhan mat quan trong"
    key, iv, cipher_bytes = encrypt_des_cbc(plain)
    
    # Sửa đổi byte đầu tiên
    tampered = bytearray(cipher_bytes)
    tampered[0] = (tampered[0] + 1) % 256
    
    try:
        recovered = decrypt_des_cbc(key, iv, bytes(tampered))
        assert recovered != plain
    except ValueError:
        # Chap nhan viec văng loi Padding
        assert True
