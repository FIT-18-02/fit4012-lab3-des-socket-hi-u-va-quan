# Report 1 page - Lab 3

## Thông tin nhóm
- Thành viên 1: Phạm Anh Quân - MSSV: 1871020471
- Thành viên 2: Ngô Văn Hiếu - MSSV: 1871020167

## Mục tiêu
Mục tiêu của bài lab là xây dựng một hệ thống truyền tin an toàn cơ bản giữa hai máy (Sender và Receiver) thông qua giao thức Socket. Nhóm tập trung vào việc triển khai thuật toán mã hóa đối xứng DES ở chế độ CBC để bảo vệ tính bảo mật của dữ liệu. Qua đó, nhóm hiểu rõ cách đóng gói gói tin (Packet Framing), xử lý Padding PKCS#7 và tầm quan trọng của việc quản lý Khóa/IV trong an toàn thông tin

## Phân công thực hiện
Ngô Văn Hiếu: Phụ trách phát triển sender.py, thiết kế cấu trúc Header 20-byte, xây dựng logic mã hóa trong des_socket_utils.py và soạn thảo threat-model-1page.md.
Phạm Anh Quân: Phụ trách phát triển receiver.py, xử lý hàm đọc dữ liệu chính xác recv_exact, thực hiện toàn bộ các ca kiểm thử tự động (pytest) và quản lý hệ thống logs.
Làm chung: Hoàn thiện báo cáo, review mã nguồn chéo và thống nhất giao thức truyền nhận

## Cách làm
Nhóm triển khai hệ thống theo mô hình Client-Server.

- Mã hóa: Sử dụng thư viện pycryptodome để thực hiện DES-CBC. Dữ liệu được bổ sung Padding theo chuẩn PKCS#7 trước khi mã hóa.
- Giao thức: Mỗi gói tin gửi đi gồm một Header cố định 20 byte (8 byte Key | 8 byte IV | 4 byte Length) và phần Payload là Ciphertext.
- Sender: Đóng gói Header bằng struct.pack, kết nối Socket và gửi toàn bộ dữ liệu sang Receiver.
- Receiver: Sử dụng hàm recv_exact để đọc đủ 20 byte header, bóc tách thông số để giải mã phần Payload tương ứng.
- Kiểm thử: Sử dụng pytest để kiểm tra từ mức hàm (unit test) đến mức tích hợp hệ thống (integration test).
## Kết quả
Hệ thống đã vượt qua toàn bộ 6/6 ca kiểm thử tự động, bao gồm các kịch bản quan trọng:

- Happy path: Truyền tin và giải mã thành công giữa Sender và Receiver.
- Tamper data: Phát hiện lỗi và dừng xử lý khi dữ liệu bản mã bị thay đổi trên đường truyền.
- Wrong key: Đảm bảo không thể giải mã nếu phía nhận sử dụng sai khóa.
- Minh chứng: Kết quả chi tiết đã được lưu trữ tại thư mục logs/ (File 01-happy-path-Bao.txt và 02-happy-path-Dung.txt).
## Kết luận
Về mặt kỹ thuật, nhóm đã làm chủ được việc lập trình Socket và xử lý dữ liệu nhị phân trong Python. Về mặt bảo mật, bài lab giúp nhóm nhận ra rằng dù thuật toán mã hóa mạnh nhưng nếu không có cơ chế trao đổi khóa an toàn (Key Exchange) và bảo vệ tính toàn vẹn (Integrity), hệ thống vẫn tồn tại rủi ro bị tấn công trung gian (MITM). Bài học lớn nhất là việc đồng bộ hóa bảng mã (UTF-8) và cấu trúc gói tin là yếu tố tiên quyết để hệ thống hoạt động ổn định trên nhiều môi trường khác nhau.
