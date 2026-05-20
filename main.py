import os
import pickle

# ==========================================
# 1. THIẾT KẾ CÁC LỚP ĐỐI TƯỢNG (CLASSES)
# ==========================================

class HangHoa:
    # NOTE 1: Bí ẩn của biến tự tăng (id_counter)
    # id_counter được khai báo ngoài hàm __init__, là biến chung của cả Class.
    # Mỗi lần tạo mặt hàng mới, mã hàng lấy giá trị hiện tại của id_counter,
    # sau đó += 1 cộng lên. Nhờ vậy mã luôn tự động tăng và không bao giờ bị trùng.
    id_counter = 1 

    def __init__(self, ten, don_vi, so_luong, gia_nhap, gia_xuat):
        self.__ma_hang = HangHoa.id_counter
        HangHoa.id_counter += 1
        self.__ten = ten
        self.__don_vi = don_vi
        self.__so_luong = so_luong
        self.__gia_nhap = gia_nhap
        self.__gia_xuat = gia_xuat

    def get_ma_hang(self): return self.__ma_hang
    def get_ten(self): return self.__ten
    def get_don_vi(self): return self.__don_vi
    def get_so_luong(self): return self.__so_luong
    # NOTE 2: Hai dấu gạch dưới (__) để làm gì? (Tính Đóng Gói - Encapsulation)
    # Biến thuộc tính thành private, chặn việc gán bậy bạ ở ngoài (ví dụ: hang_hoa.so_luong = -100).
    # Muốn sửa số lượng tồn, bắt buộc phải gọi hàm set_so_luong() này.
    def set_so_luong(self, so_luong): self.__so_luong = so_luong
    def get_gia_nhap(self): return self.__gia_nhap
    def get_gia_xuat(self): return self.__gia_xuat

    def hien_thi(self):
        print(f"Mã: {self.__ma_hang} | Tên: {self.__ten:<15} | ĐVT: {self.__don_vi:<5} | Tồn kho: {self.__so_luong:<5} | Giá nhập: {self.__gia_nhap:<8} | Giá xuất: {self.__gia_xuat}")


class NhanVien:
    id_counter = 1

    def __init__(self, ho_ten, gioi_tinh, chuc_vu, sdt):
        self.__ma_nv = NhanVien.id_counter
        NhanVien.id_counter += 1
        self.__ho_ten = ho_ten
        self.__gioi_tinh = gioi_tinh
        self.__chuc_vu = chuc_vu
        self.__sdt = sdt

    def get_ma_nv(self): return self.__ma_nv
    def get_ho_ten(self): return self.__ho_ten
    
    def hien_thi(self):
        print(f"Mã NV: {self.__ma_nv} | Tên: {self.__ho_ten:<15} | Giới tính: {self.__gioi_tinh:<5} | Chức vụ: {self.__chuc_vu:<10} | SĐT: {self.__sdt}")


class PhieuNhapXuat:
    id_counter = 1

    def __init__(self, ngay_lap, nhan_vien, loai_phieu):
        self.__ma_phieu = PhieuNhapXuat.id_counter
        PhieuNhapXuat.id_counter += 1
        self.__ngay_lap = ngay_lap
        self.__nhan_vien = nhan_vien 
        self.__loai_phieu = loai_phieu 
        self.__danh_sach_hang = [] 

    def them_hang_vao_phieu(self, hang_hoa, so_luong):
        self.__danh_sach_hang.append((hang_hoa, so_luong))

    def get_loai_phieu(self): return self.__loai_phieu
    def get_ma_phieu(self): return self.__ma_phieu

    def tinh_tong_gia_tri(self):
        tong_tien = 0
        for hang_hoa, so_luong in self.__danh_sach_hang:
            if self.__loai_phieu == "Nhap":
                tong_tien += so_luong * hang_hoa.get_gia_nhap()
            else:
                tong_tien += so_luong * hang_hoa.get_gia_xuat()
        return tong_tien

    def hien_thi_phieu(self):
        loai = "PHIẾU NHẬP" if self.__loai_phieu == "Nhap" else "PHIẾU XUẤT"
        print(f"--- {loai} | Mã phiếu: {self.__ma_phieu} | Ngày: {self.__ngay_lap} | NV: {self.__nhan_vien.get_ho_ten()} ---")
        for hang_hoa, so_luong in self.__danh_sach_hang:
            don_gia = hang_hoa.get_gia_nhap() if self.__loai_phieu == "Nhap" else hang_hoa.get_gia_xuat()
            thanh_tien = so_luong * don_gia
            print(f"  + {hang_hoa.get_ten()}: {so_luong} {hang_hoa.get_don_vi()} x {don_gia} = {thanh_tien}")
        print(f"  => Tổng giá trị phiếu: {self.tinh_tong_gia_tri()}")


# ==========================================
# 2. LỚP QUẢN LÝ (CHỨA MENU & FILE I/O)
# ==========================================

class QuanLyKho:
    def __init__(self):
        self.file_name = "du_lieu_kho.dat"
        self.ds_hang_hoa = []
        self.ds_nhan_vien = []
        self.ds_phieu = []
        
        # Tự động đọc file nếu đã tồn tại, nếu chưa thì tạo dữ liệu mẫu
        if os.path.exists(self.file_name):
            self.doc_file()
        else:
            print("[!] Chưa có file dữ liệu, tiến hành tạo dữ liệu mẫu và tạo file...")
            self.tao_du_lieu_mau()
            self.luu_file()

    def luu_file(self):
        """Lưu toàn bộ danh sách và các biến tĩnh vào file"""
        # NOTE 3: Lưu file bằng pickle
        # Thư viện pickle giống như một cái hộp. Ta có thể vứt thẳng nguyên một mảng list đối tượng
        # vào hộp (dump) rồi ghi ra file nhị phân (wb). Khi đọc lên (load) sẽ lấy lại được y nguyên
        # mảng đối tượng cũ xài luôn, không cần cắt/ghép chuỗi khổ sở như file .txt bình thường.
        with open(self.file_name, 'wb') as f:
            data = {
                "hang_hoa": self.ds_hang_hoa,
                "nhan_vien": self.ds_nhan_vien,
                "phieu": self.ds_phieu,
                "id_hh": HangHoa.id_counter,
                "id_nv": NhanVien.id_counter,
                "id_phieu": PhieuNhapXuat.id_counter
            }
            pickle.dump(data, f)

    def doc_file(self):
        """Đọc và khôi phục toàn bộ đối tượng từ file"""
        with open(self.file_name, 'rb') as f:
            data = pickle.load(f)
            self.ds_hang_hoa = data["hang_hoa"]
            self.ds_nhan_vien = data["nhan_vien"]
            self.ds_phieu = data["phieu"]
            # Khôi phục lại biến đếm ID để mã tiếp tục tăng đúng
            HangHoa.id_counter = data["id_hh"]
            NhanVien.id_counter = data["id_nv"]
            PhieuNhapXuat.id_counter = data["id_phieu"]
        print(f"[!] Đã tải thành công dữ liệu từ file {self.file_name}")

    def tao_du_lieu_mau(self):
        self.ds_hang_hoa.append(HangHoa("Bàn phím cơ", "Cái", 50, 500, 800))
        self.ds_hang_hoa.append(HangHoa("Chuột máy tính", "Cái", 100, 150, 250))
        self.ds_hang_hoa.append(HangHoa("Màn hình 24inc", "Cái", 20, 2000, 2800))
        self.ds_nhan_vien.append(NhanVien("Nguyen Van A", "Nam", "Thủ kho", "0901234567"))
        self.ds_nhan_vien.append(NhanVien("Tran Thi B", "Nữ", "Nhân viên", "0912345678"))

    def tim_hang_hoa_theo_ma(self, ma_hang):
        for hh in self.ds_hang_hoa:
            if hh.get_ma_hang() == ma_hang: return hh
        return None

    def tim_nhan_vien_theo_ma(self, ma_nv):
        for nv in self.ds_nhan_vien:
            if nv.get_ma_nv() == ma_nv: return nv
        return None

    # --- CÁC CHỨC NĂNG MENU ---
    def hien_thi_ds_hang(self):
        print("\n--- DANH SÁCH HÀNG HÓA ---")
        for hh in self.ds_hang_hoa: hh.hien_thi()

    def hien_thi_ds_nhan_vien(self):
        print("\n--- DANH SÁCH NHÂN VIÊN ---")
        for nv in self.ds_nhan_vien: nv.hien_thi()

    def them_hang_hoa(self):
        ten = input("Nhập tên hàng: ")
        dv = input("Nhập đơn vị tính: ")
        sl = int(input("Nhập số lượng tồn: "))
        gn = float(input("Nhập giá nhập: "))
        gx = float(input("Nhập giá xuất: "))
        self.ds_hang_hoa.append(HangHoa(ten, dv, sl, gn, gx))
        self.luu_file()  # Lưu lại thay đổi vào file
        print("=> Thêm hàng hóa thành công và đã lưu file!")

    def lap_phieu_nhap_xuat(self):
        self.hien_thi_ds_nhan_vien()
        ma_nv = int(input("Nhập mã nhân viên lập phiếu: "))
        nv = self.tim_nhan_vien_theo_ma(ma_nv)
        if not nv:
            print("Không tìm thấy nhân viên!")
            return

        loai_phieu = input("Nhập loại phiếu ('Nhap' hoặc 'Xuat'): ")
        if loai_phieu not in ["Nhap", "Xuat"]:
            print("Loại phiếu không hợp lệ!")
            return

        ngay_lap = input("Nhập ngày lập (DD/MM/YYYY): ")
        phieu = PhieuNhapXuat(ngay_lap, nv, loai_phieu)

        while True:
            self.hien_thi_ds_hang()
            ma_hang = int(input("Nhập mã hàng muốn đưa vào phiếu (nhập 0 để dừng): "))
            if ma_hang == 0: break
            
            hh = self.tim_hang_hoa_theo_ma(ma_hang)
            if not hh:
                print("Mã hàng không tồn tại!")
                continue

            sl = int(input("Nhập số lượng: "))
            ton_kho_hien_tai = hh.get_so_luong()
            
            if loai_phieu == "Xuat":
                # NOTE 4: Chặn lỗi khi xuất kho (Cốt lõi nghiệp vụ)
                # Trích xuất tồn kho hiện tại, so sánh với số xuất (sl). Nếu số xuất lớn hơn tồn
                # thì lệnh continue sẽ ngắt ngang vòng lặp và bắt nhập lại. Nếu hợp lệ mới tiến hành trừ.
                if sl > ton_kho_hien_tai:
                    print(f"Lỗi: Số lượng xuất lớn hơn tồn kho (Tồn: {ton_kho_hien_tai})!")
                    continue
                hh.set_so_luong(ton_kho_hien_tai - sl)
            else:
                hh.set_so_luong(ton_kho_hien_tai + sl)

            phieu.them_hang_vao_phieu(hh, sl)
            print("=> Đã thêm vào phiếu!")

        self.ds_phieu.append(phieu)
        self.luu_file() # Lưu lại các thay đổi về tồn kho và phiếu mới vào file
        print("\n=> LẬP PHIẾU THÀNH CÔNG VÀ ĐÃ LƯU DỮ LIỆU!")
        phieu.hien_thi_phieu()

    def run(self):
        while True:
            print("\n" + "="*35)
            print("   HỆ THỐNG QUẢN LÝ KHO HÀNG (Lưu File)")
            print("="*35)
            print("1. Hiển thị danh sách hàng hóa (Tồn kho)")
            print("2. Thêm hàng hóa mới")
            print("3. Hiển thị danh sách nhân viên")
            print("4. Lập phiếu Nhập / Xuất hàng")
            print("0. Lưu và thoát chương trình")
            print("="*35)
            
            chon = input("Chọn chức năng: ")
            
            if chon == '1': self.hien_thi_ds_hang()
            elif chon == '2': self.them_hang_hoa()
            elif chon == '3': self.hien_thi_ds_nhan_vien()
            elif chon == '4': self.lap_phieu_nhap_xuat()
            elif chon == '0':
                self.luu_file()
                print("Đã lưu dữ liệu. Cảm ơn đã sử dụng chương trình!")
                break
            else:
                print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    app = QuanLyKho()
    app.run()
