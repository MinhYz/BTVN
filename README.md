HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY CHƯƠNG TRÌNH QUẢN LÝ KHO HÀNG

1. Yêu cầu hệ thống:

Máy tính cần cài đặt sẵn Python (phiên bản 3.x trở lên).

Không cần cài thêm bất kỳ thư viện bên ngoài nào vì chương trình chỉ sử dụng các thư viện có sẵn của Python (os, pickle).

2. Cách khởi chạy chương trình:

Bước 1: Gom file code (ví dụ: main.py) vào một thư mục trống.

Bước 2: Mở Terminal (hoặc Command Prompt / PowerShell) tại thư mục đó.

Bước 3: Gõ lệnh sau và nhấn Enter để chạy: python main.py

3. Lưu ý về File Dữ Liệu (du_lieu_kho.dat):

Ở lần chạy đầu tiên: Chương trình sẽ báo chưa có file dữ liệu, sau đó tự động tạo ra một vài dữ liệu mẫu (nhân viên, hàng hóa) và sinh ra file du_lieu_kho.dat nằm cùng thư mục với file code.

Ở các lần chạy sau: Hệ thống sẽ tự động đọc (load) toàn bộ dữ liệu từ file du_lieu_kho.dat lên bộ nhớ.

Khi thoát chương trình: Bắt buộc phải chọn phím 0 ở Menu chính để hệ thống lưu lại toàn bộ các thao tác (nhập, xuất, thêm hàng...) vào file. Nếu tắt nóng bằng dấu X trên cửa sổ terminal, dữ liệu phiên làm việc đó có thể không được lưu.
