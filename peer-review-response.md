# Peer Review Response

## Thông tin nhóm
- Thành viên 1: Ngô Văn Hiếu
- Thành viên 2: Phạm Anh Quân

## Thành viên 1 góp ý cho thành viên 2
Hiếu nhận xét: Quân đã xử lý rất tốt phần recv_exact trong receiver.py, đảm bảo đọc đúng số byte của Header và Ciphertext mà không bị mất dữ liệu. Các test case trong thư mục tests/ do Phương phụ trách chạy rất ổn định và bao quát được các trường hợp lỗi như sai Key hay dữ liệu bị sửa đổi (Tampered).

## Thành viên 2 góp ý cho thành viên 1
Quân nhận xét: Hiếu thiết kế cấu trúc gói tin (Packet Structure) rất chuyên nghiệp, sử dụng struct.pack để đóng gói Header 20-byte giúp việc bóc tách ở phía người nhận rất thuận tiện. Phần logic mã hóa DES-CBC trong des_socket_utils.py được viết rõ ràng, module hóa tốt, giúp mình dễ dàng tích hợp vào phần Receiver.

## Nhóm đã sửa gì sau góp ý
Đồng bộ Encoding: Sau khi review, nhóm phát hiện lỗi UnicodeEncodeError trên Windows nên đã thống nhất chuyển toàn bộ các dòng print thông báo sang tiếng Việt không dấu (ví dụ: "Dang lang nghe", "Ket noi tu").

Kiểm soát Header: Nhóm đã thống nhất lại thứ tự byte trong Header (Key, IV, Length) để đảm bảo hai phía Sender và Receiver luôn khớp nhau 100%.

Xử lý Timeout: Đã thêm cấu hình SOCKET_TIMEOUT để phía Receiver không bị treo vô hạn nếu quá trình truyền tin từ phía Sender gặp sự cố.
