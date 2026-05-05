[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/jjUQ5jLa)
# FIT4012 - Lab 3 - Hệ thống gửi và nhận dữ liệu mã hoá DES qua Socket

Chào mừng bạn đến với một chiếc lab nhìn thì hiền nhưng rất biết cách “hỏi xoáy đáp xoay”. Ở lab này, bạn sẽ làm một hệ thống nhỏ gồm **Sender** và **Receiver** chạy qua **TCP socket**, trong đó bản tin được mã hoá bằng **DES-CBC**, có **IV**, có **header độ dài**, và có đủ chỗ để bạn luyện cả kỹ năng kỹ thuật lẫn tư duy bảo mật.

Bài lab bám theo luồng hệ thống trong file hướng dẫn: Sender tạo **DES key 8 byte**, **IV 8 byte**, mã hoá bằng **DES-CBC + PKCS#7**, rồi gửi tuần tự **key + IV + length header + ciphertext**; Receiver lắng nghe socket, nhận đúng thứ tự này rồi giải mã và hiển thị lại bản rõ. Đây là mô hình học tập có chủ đích để quan sát quy trình giao tiếp, **không phải thiết kế an toàn để dùng ngoài đời thật**.

## Hình thức làm bài
- **Làm theo nhóm 2 người**.
- Hai bạn dùng **1 repo chung**.
- Cả hai đều phải hiểu toàn bộ hệ thống, không được chia kiểu “một bạn ôm hết, một bạn ngồi cổ vũ tinh thần”.
- Khi demo, giảng viên có thể hỏi chéo bất kỳ thành viên nào về **sender**, **receiver**, **DES-CBC**, **padding**, **threat model** và **ethics**.

## Team members
- **Thành viên 1**: TODO_MEMBER_1 - MSSV: TODO_MEMBER_1_ID
- **Thành viên 2**: TODO_MEMBER_2 - MSSV: TODO_MEMBER_2_ID

## Task division
- **Thành viên 1 phụ trách chính**: TODO_ROLE_MEMBER_1
- **Thành viên 2 phụ trách chính**: TODO_ROLE_MEMBER_2
- **Phần làm chung**: TODO_SHARED_WORK

## Demo roles
- **Bạn nào demo Sender / gói tin / log gửi**: TODO_DEMO_ROLE_1
- **Bạn nào demo Receiver / giải mã / log nhận**: TODO_DEMO_ROLE_2
- **Cả hai cùng trả lời threat model và ethics**: TODO_DEMO_ROLE_SHARED

## Mục tiêu học tập
- Hiểu luồng hoạt động của hệ thống Sender/Receiver qua TCP socket.
- Mô tả được vai trò của **key**, **IV**, **padding PKCS#7**, **header độ dài**.
- Cài đặt và chạy được hệ thống gửi/nhận dữ liệu mã hoá DES qua socket.
- Viết được **threat model** ngắn gọn cho hệ thống.
- Ghi nhận được các hạn chế bảo mật của thiết kế hiện tại và nêu hướng cải tiến.

## Cấu trúc repo
- `sender.py`: tiến trình người gửi
- `receiver.py`: tiến trình người nhận
- `des_socket_utils.py`: hàm pad/unpad, encrypt/decrypt, build/parse packet
- `tests/`: kiểm thử tự động
- `logs/`: nơi lưu log minh chứng
- `threat-model-1page.md`: threat model cho hệ thống
- `peer-review-response.md`: ghi nhận góp ý và chỉnh sửa sau peer review
- `report-1page.md`: báo cáo ngắn

## How to run
### 1) Cài môi trường
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Chạy Receiver
```bash
python receiver.py
```

### 3) Chạy Sender
```bash
python sender.py
```
Rồi nhập bản tin khi chương trình hỏi.

### 4) Chạy demo local bằng biến môi trường
Terminal 1:
```bash
RECEIVER_PORT=6001 python receiver.py
```

Terminal 2:
```bash
SERVER_IP=127.0.0.1 SERVER_PORT=6001 MESSAGE="Xin chao FIT4012" python sender.py
```

## Input / Output
### Input
- Sender nhận bản tin từ bàn phím hoặc từ biến môi trường `MESSAGE`.
- Receiver nhận packet qua TCP socket.

### Output
- Sender in ra: thông báo gửi thành công, `Key`, `IV`, `Ciphertext`.
- Receiver in ra: bản tin gốc sau giải mã.
- Bạn cần lưu **log chạy thật** vào thư mục `logs/` để làm minh chứng nộp bài.

## Deliverables bắt buộc
- `README.md`
- `report-1page.md`
- `threat-model-1page.md`
- `peer-review-response.md`
- `tests/` có ít nhất 5 test
- `logs/` có log chạy thật của các ca kiểm thử
- thông tin **nhóm 2 người + phân công** trong `README.md`

## Threat-model awareness
Vì lab này đang dùng mô hình **gửi key và IV dưới dạng plaintext trên cùng luồng TCP**, bạn cần chỉ ra đây là điểm yếu bảo mật nghiêm trọng nếu đưa ra thực tế. Trong `threat-model-1page.md`, hãy nêu rõ:
- assets
- attacker model
- threats
- mitigations
- residual risks

## Ethics & Safe use
- Chỉ chạy demo trên máy cá nhân, VM, hoặc mạng nội bộ phục vụ học tập.
- Không quét cổng, không thử nghiệm lên hệ thống không thuộc phạm vi lớp học.
- Không dùng dữ liệu cá nhân thật hoặc dữ liệu nhạy cảm để demo.
- Không trình bày hệ thống này như một giải pháp an toàn sẵn sàng triển khai ngoài đời.
- Nếu tham khảo code/tài liệu, hãy ghi nguồn rõ ràng.
- Tôn trọng nguyên tắc trung thực học thuật.

## Submission contract cho CI
CI sẽ kiểm tra:
- có đủ file nộp bài
- có ít nhất 5 test
- chạy được kiểm thử local sender/receiver
- có negative test cho **tamper** và **wrong key**
- `README.md` đã khai báo **2 thành viên**, **phân công**, **vai trò demo**
- các file `report-1page.md`, `threat-model-1page.md`, `peer-review-response.md` không còn dòng `TODO_STUDENT`
- thư mục `logs/` có ít nhất 1 file log thật

Nếu CI đỏ, đừng hoảng. Cứ xem nó như một trợ giảng hơi khó tính nhưng vẫn muốn bạn qua môn.
