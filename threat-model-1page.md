# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: Phạm Anh Quân
- Thành viên 2: Ngô Văn Hiếu

## Assets
- Nội dung bản tin (Payload): Dữ liệu gốc mà người gửi muốn truyền tới người nhận một cách bí mật.

- Khóa giải mã (DES Key): Khóa 8-byte dùng để mã hóa và giải mã dữ liệu.

- Vector khởi tạo (IV): Tham số cần thiết cho chế độ mã hóa DES-CBC để đảm bảo tính ngẫu nhiên.
## Attacker model
- Kẻ tấn công đóng vai trò là thực thể đứng giữa đường truyền (Man-in-the-Middle).
//quanhieu
- Đối tượng có khả năng nghe lén, bắt các gói tin TCP chạy qua mạng nội bộ hoặc Internet.

- Đối tượng có thể can thiệp, chỉnh sửa các bit dữ liệu trong gói tin trước khi nó đến tay người nhận.
## Threats
- Nghe lén thông tin nhạy cảm: Do hệ thống gửi trực tiếp Key và IV ở dạng plaintext trong gói tin, kẻ tấn công có thể dễ dàng lấy được khóa để giải mã toàn bộ bản tin.

- Tấn công giả mạo (Tampering): Kẻ tấn công sửa đổi ciphertext trên đường truyền, khiến người nhận giải mã ra thông tin sai lệch mà không hề hay biết.

- Tấn công phát lại (Replay Attack): Kẻ tấn công bắt gói tin hợp lệ và gửi lại nhiều lần cho Receiver để gây nhiễu hoặc thực hiện lại một hành động trái phép.
## Mitigations
- Sử dụng TLS/SSL: Mã hóa toàn bộ kênh truyền socket để bảo vệ cả Key, IV và dữ liệu khỏi bị nghe lén.

- Giao thức Diffie-Hellman: Sử dụng cơ chế trao đổi khóa an toàn để thống nhất khóa bí mật mà không cần gửi trực tiếp qua mạng.

- Dùng Message Authentication Code (MAC): Thêm mã xác thực (như HMAC) vào gói tin để người nhận có thể kiểm tra xem dữ liệu có bị chỉnh sửa hay không
## Residual risks
- Điểm yếu của thuật toán DES: Ngay cả khi bảo vệ được khóa, thuật toán DES với độ dài khóa 56-bit vẫn có thể bị tấn công bạo lực (Brute-force) bằng máy tính hiện đại trong thời gian ngắn.
