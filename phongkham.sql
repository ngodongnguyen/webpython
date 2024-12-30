INSERT INTO Khoa (ten_khoa, mo_ta) VALUES
('Khoa Nội', 'Chuyên điều trị các bệnh lý nội khoa như tim mạch, hô hấp, tiêu hóa.'),
('Khoa Ngoại', 'Chuyên điều trị các bệnh lý ngoại khoa và thực hiện phẫu thuật.'),
('Khoa Sản', 'Chuyên điều trị các vấn đề về sinh sản và sức khỏe bà mẹ, trẻ em.'),
('Khoa Nhi', 'Chuyên điều trị các bệnh lý ở trẻ em, từ sơ sinh đến tuổi trưởng thành.'),
('Khoa Da liễu', 'Chuyên điều trị các bệnh lý về da như eczema, vẩy nến, mụn.'),
('Khoa Mắt', 'Chuyên điều trị các bệnh lý về mắt như cận thị, viêm kết mạc, đục thủy tinh thể.'),
('Khoa Tai mũi họng', 'Chuyên điều trị các bệnh lý về tai, mũi, họng, bao gồm viêm, dị ứng, ung thư.'),
('Khoa Răng Hàm Mặt', 'Chuyên điều trị các vấn đề về răng miệng và phẫu thuật hàm mặt.'),
('Khoa Xét nghiệm', 'Chuyên thực hiện các xét nghiệm y tế như xét nghiệm máu, nước tiểu, sinh hóa.'),
('Khoa Chẩn đoán hình ảnh', 'Chuyên thực hiện các phương pháp chẩn đoán hình ảnh như X-quang, siêu âm, CT, MRI.')

-- Dữ liệu bảng bác sĩ
INSERT INTO nguoi_dung (ho, ten, gioi_tinh, cccd, ngay_sinh) VALUES
 ('Nguyễn Văn','A', 1, '123456789012', '1990-01-01'),
 ('Nguyễn Thị','B', 0, '123456789013', '1991-02-02'),
 ('Trần Văn','C', 1, '123456789014', '1992-03-03'),
 ('Lê Thị','D', 0, '123456789015', '1993-04-04'),
 ('Phạm Văn','E', 1, '123456789016', '1994-05-05'),
 ('Hoàng Thị','F', 0, '123456789017', '1995-06-06'),
 ('Vũ Văn','G', 1, '123456789018', '1996-07-07'),
 ('Đặng Thị','H', 0, '123456789019', '1997-08-08'),
 ('Ngô Văn', 'I',1, '123456789020', '1998-09-09'),
 ('Đỗ Thị','J', 0,'123456789021', '1999-10-10'),
 ('Nguyễn Văn','K', 1, '123456789022', '2000-11-11'),
 ('Trần Thị','L',  0, '123456789023', '2001-12-12'),
 ('Phan Văn','M',  1, '123456789024', '2002-01-13'),
 ('Bùi Thị','N',  0, '123456789025', '2003-02-14'),
 ('Lý Văn','O',  1, '123456789026', '2004-03-15'),
 ('Trương Thị','P',  0, '123456789027', '2005-04-16'),
 ('Tôn Văn','Q', 1, '123456789028', '2006-05-17'),
 ('Đinh Thị','R', 0, '123456789029', '2007-06-18'),
 ('Hồ Văn','S', 1, '123456789030', '2008-07-19'),
 ('Đặng Thị','T',  0, '123456789031', '2009-08-20');

INSERT INTO nhan_vien (id, username, password, avatar, type)
VALUES
(1, 'nv01', 'password01', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(2, 'nv02', 'password02', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(3, 'nv03', 'password03', 'https://res.cloudinary.com/ouweb/image/upload/v1734513764/webpython/doctor/z8nenfvryfjcfnjsewzx.jpg', 'bac_si'),
(4, 'nv04', 'password04', 'https://res.cloudinary.com/ouweb/image/upload/v1734513765/webpython/doctor/q2dt17odfydslhjlkyxs.jpg', 'bac_si'),
(5, 'nv05', 'password05', 'https://res.cloudinary.com/ouweb/image/upload/v1734513768/webpython/doctor/drteti4xn9923mkp7qhs.jpg', 'bac_si'),
(6, 'nv06', 'password06', 'https://res.cloudinary.com/ouweb/image/upload/v1734513768/webpython/doctor/k5y5v71v40ggrusm2a44.jpg', 'bac_si'),
(7, 'nv07', 'password07', 'https://res.cloudinary.com/ouweb/image/upload/v1734513770/webpython/doctor/udl8vr64db9f4de6w2tj.jpg', 'bac_si'),
(8, 'nv08', 'password08', 'https://res.cloudinary.com/ouweb/image/upload/v1734513770/webpython/doctor/cpim4nhkemlisqegnc7i.jpg', 'bac_si'),
(9, 'nv09', 'password09', 'https://res.cloudinary.com/ouweb/image/upload/v1734513772/webpython/doctor/h0rc9fvfckvwwaxtv84p.jpg', 'bac_si'),
(10, 'nv10', 'password10','https://res.cloudinary.com/ouweb/image/upload/v1734513772/webpython/doctor/vfg11nygqzrerqvkl8n6.jpg', 'bac_si');

INSERT INTO bac_si (id, khoa_id)
SELECT id, FLOOR(1 + (RAND() * 10)) AS random_khoa_id
FROM nhan_vien
WHERE type = 'bac_si';
INSERT INTO sdt (so_dien_thoai, nguoi_dung_id) VALUES
('0123456789', 1),
('0987654321', 2),
('0912345678', 3),
('0934567890', 4),
('0923456781', 5),
('0901234567', 6),
('0945678901', 7),
('0976543210', 8),
('0956789012', 9),
('0998765432', 10);
-- thêm 10 địa chỉ
INSERT INTO dia_chi (dia_chi, nguoi_dung_id) VALUES
('123 Đường ABC, Quận 1, TP.HCM', 1),
('456 Đường DEF, Quận 2, TP.HCM', 2),
('789 Đường GHI, Quận 3, TP.HCM', 3),
('101 Đường JKL, Quận 4, TP.HCM', 4),
('102 Đường MNO, Quận 5, TP.HCM', 5),
('103 Đường PQR, Quận 6, TP.HCM', 6),
('104 Đường STU, Quận 7, TP.HCM', 7),
('105 Đường VWX, Quận 8, TP.HCM', 8),
('106 Đường YZA, Quận 9, TP.HCM', 9),
('107 Đường BCD, Quận 10, TP.HCM', 10);
INSERT INTO email (email, nguoi_dung_id) VALUES
('nguyenvana@example.com', 1),
('tranthib@example.com', 2),
('phamvanc@example.com', 3),
('lethid@example.com', 4),
('hoangthie@example.com', 5),
('nguyenthif@example.com', 6),
('doanhgia@example.com', 7),
('vutuyet@example.com', 8),
('buiduc@example.com', 9),
('nguyenthihoa@example.com', 10);
-- Insert 20 bệnh nhân mẫu vào bảng `nguoi_dung`
INSERT INTO nguoi_dung (ho, ten, gioi_tinh, cccd, ngay_sinh)
VALUES
('Nguyen', 'Anh Tuan', 1, '079111111111', '1985-03-12'),
('Tran', 'Minh Thu', 0, '079222222222', '1990-07-18'),
('Le', 'Thanh Tung', 1, '079333333333', '1987-01-05'),
('Pham', 'Lan Huong', 0, '079444444444', '1993-12-25'),
('Hoang', 'Duy Khanh', 1, '079555555555', '1995-08-11'),
('Vu', 'Kim Chi', 0, '079666666666', '1992-10-30'),
('Ngo', 'Van Hieu', 1, '079777777777', '1991-09-09'),
('Do', 'Thanh Nga', 0, '079888888888', '1994-05-20'),
('Bui', 'Duc Anh', 1, '079999999999', '1989-06-15'),
('Nguyen', 'Bao Ngoc', 0, '079121212121', '1996-11-22'),
('Phan', 'Quang Huy', 1, '079232323232', '1990-02-14'),
('Tran', 'Thuy Linh', 0, '079343434343', '1988-07-07'),
('Le', 'Hoang Nam', 1, '079454545454', '1993-01-01'),
('Pham', 'Ngoc Mai', 0, '079565656565', '1995-03-30'),
('Hoang', 'Minh Phuc', 1, '079676767676', '1997-09-19'),
('Vu', 'Thanh Ha', 0, '079787878787', '1994-08-28'),
('Ngo', 'Quoc Bao', 1, '079898989898', '1986-04-16'),
('Do', 'Thuy Trang', 0, '079909090909', '1991-05-11'),
('Bui', 'Anh Quan', 1, '079101010101', '1990-12-08'),
('Nguyen', 'Minh Anh', 0, '079202020202', '1995-07-24');

-- Insert dữ liệu vào bảng `benh_nhan` liên kết với `nguoi_dung`
INSERT INTO benh_nhan (id)
SELECT id 
FROM nguoi_dung
WHERE id BETWEEN 21 AND 40;
INSERT INTO nguoi_dung (id, ho, ten, gioi_tinh, cccd, ngay_sinh)
VALUES
(41, 'Nguyen', 'Thu', 1, '123456789012', '1990-01-01'),
(42, 'Tran', 'Lan', 0, '123456789013', '1992-02-02'),
(43, 'Le', 'Minh', 1, '123456789014', '1988-03-03'),
(44, 'Pham', 'Hoa', 0, '123456789015', '1995-04-04'),
(45, 'Hoang', 'Thao', 0, '123456789016', '1993-05-05');


INSERT INTO nhan_vien (id, username, password, avatar, type)
VALUES
(41, 'thu1', 'password_hash_1', NULL, 'thu_ngan'),
(42, 'thu2', 'password_hash_2', NULL, 'thu_ngan'),
(43, 'thu3', 'password_hash_3', NULL, 'thu_ngan'),
(44, 'thu4', 'password_hash_4', NULL, 'thu_ngan'),
(45, 'thu5', 'password_hash_5', NULL, 'thu_ngan');


INSERT INTO thu_ngan (id)
VALUES
(1),
(2),
(3),
(4),
(5)
-- tạo 10 danh sách phiếu khám bệnh
INSERT INTO danh_sach_phieu_kham_benh (id, ngay_tao, tong_so)
VALUES
(1, '2024-12-30', 0),
(2, '2024-11-30', 0),
(3, '2024-10-30', 0),
(4, '2024-9-30', 0),
(5, '2024-8-30', 0),
(6, '2024-7-30', 0),
(7, '2024-6-30', 0),
(8, '2024-5-30', 0),
(9, '2024-4-30', 0),
(10, '2024-3-30', 0);

-- tạo 20 phiếu khám bệnh
INSERT INTO phieu_kham_benh (id, trieu_chung, chuan_doan, benh_nhan_id, danhsach_id, bac_si_id, ngay_kham) 
VALUES
(1, 'Sốt cao, đau đầu', 'Sốt xuất huyết', 1, 1, 1, '2024-12-20'),
(2, 'Ho, đau họng', 'Viêm họng', 2, 1, 2, '2024-12-20'),
(3, 'Đau bụng, tiêu chảy', 'Rối loạn tiêu hóa', 3, 2, 1, '2024-12-20'),
(4, 'Khó thở, tức ngực', 'Hen suyễn', 4, 2, 3, '2024-12-20'),
(5, 'Sốt nhẹ, mệt mỏi', 'Cảm cúm', 5, 3, 2, '2024-12-20'),
(6, 'Đau lưng', 'Thoát vị đĩa đệm', 6, 3, 4, '2024-12-20'),
(7, 'Đau khớp', 'Viêm khớp dạng thấp', 7, 4, 3, '2024-12-20'),
(8, 'Ngứa, nổi mẩn đỏ', 'Dị ứng da', 8, 4, 2, '2024-12-20'),
(9, 'Đau mắt, nhức mắt', 'Viêm kết mạc', 9, 5, 1, '2024-12-20'),
(10, 'Đau răng, sưng nướu', 'Viêm lợi', 10, 5, 4, '2024-12-20');


INSERT INTO hoa_don (id, ngay_tinh_tien, tien_kham_benh, tien_thuoc, tong_tien, phieu_kham_id, benh_nhan_id, thu_ngan_id)
VALUES
(1, '2024-12-20', 150000, 50000, 200000, 1, 1, 1),
(2, '2024-12-21', 200000, 100000, 300000, 2, 2, 2),
(3, '2024-12-22', 180000, 80000, 260000, 3, 3, 1),
(4, '2024-12-23', 150000, NULL, 150000, 4, 4, 2),
(5, '2024-12-24', 200000, 120000, 320000, 5, 5, 3),
(6, '2024-12-25', 170000, 70000, 240000, 6, 6, 1),
(7, '2024-12-26', 150000, 50000, 200000, 7, 7, 2),
(8, '2024-12-27', 180000, 60000, 240000, 8, 8, 3),
(9, '2024-12-28', 190000, 70000, 260000, 9, 9, 1),
(10, '2024-12-29', 160000, 40000, 200000, 10, 10, 2),
(11, '2024-12-30', 200000, 150000, 350000, 10, 11, 3),
(12, '2024-12-31', 150000, 50000, 200000, 10, 12, 1),
(13, '2025-01-01', 180000, 60000, 240000, 10, 13, 2),
(14, '2025-01-02', 190000, NULL, 190000, 10, 14, 3),
(15, '2025-01-03', 200000, 80000, 280000, 10, 15, 1),
(16, '2025-01-04', 170000, 90000, 260000, 10, 16, 2),
(17, '2025-01-05', 150000, 70000, 220000, 10, 17, 3),
(18, '2025-01-06', 180000, 80000, 260000, 10, 18, 1),
(19, '2025-01-07', 160000, 60000, 220000, 10, 19, 2),
(20, '2025-01-08', 200000, 100000, 300000, 10, 20, 3);
INSERT INTO thuoc (ten_thuoc, loai, so_luong, gia_tien, huong_dan_su_dung) VALUES
('Paracetamol', 'Viên', 100, 5000, 'Dùng 1 viên mỗi 4-6 giờ'),
('Ibuprofen', 'Viên', 50, 12000, 'Uống 1 viên mỗi 6 giờ khi cần'),
('Aspirin', 'Viên', 200, 3000, 'Uống 1 viên mỗi 8 giờ'),
('Amoxicillin', 'Vỉ', 300, 15000, 'Dùng 1 viên mỗi 12 giờ'),
('Cetirizine', 'Viên', 150, 7000, 'Dùng 1 viên mỗi ngày'),
('Loratadine', 'Viên', 80, 9000, 'Dùng 1 viên vào buổi sáng'),
('Vitamin C', 'Viên', 500, 2000, 'Uống 1 viên mỗi ngày'),
('Omeprazole', 'Viên', 120, 25000, 'Dùng 1 viên vào buổi sáng trước ăn'),
('Diphenhydramine', 'Viên', 200, 4000, 'Uống 1 viên trước khi ngủ'),
('Metformin', 'Viên', 100, 18000, 'Uống 1 viên sáng và tối'),
('Prednisolone', 'Viên', 150, 22000, 'Dùng theo chỉ định của bác sĩ'),
('Lorazepam', 'Viên', 80, 15000, 'Uống 1 viên vào buổi tối'),
('Clindamycin', 'Vỉ', 60, 35000, 'Dùng 1 viên mỗi 8 giờ trong 10 ngày'),
('Ciprofloxacin', 'Viên', 300, 12000, 'Uống 1 viên mỗi 12 giờ'),
('Doxycycline', 'Viên', 200, 10000, 'Dùng 1 viên vào buổi sáng và tối'),
('Prednisone', 'Viên', 80, 20000, 'Dùng 1 viên mỗi ngày'),
('Furosemide', 'Viên', 150, 8000, 'Uống 1 viên vào buổi sáng'),
('Losartan', 'Viên', 200, 14000, 'Dùng 1 viên mỗi ngày'),
('Alprazolam', 'Viên', 100, 22000, 'Dùng 1 viên khi cần thiết'),
('Simvastatin', 'Viên', 250, 10000, 'Uống 1 viên mỗi ngày vào buổi tối'),
('Amlodipine', 'Viên', 180, 14000, 'Dùng 1 viên mỗi ngày'),
('Clopidogrel', 'Viên', 100, 15000, 'Uống 1 viên mỗi ngày'),
('Ranitidine', 'Viên', 120, 7000, 'Uống 1 viên mỗi ngày vào buổi tối'),
('Losartan Potassium', 'Viên', 100, 11000, 'Dùng 1 viên vào buổi sáng'),
('Fluoxetine', 'Viên', 80, 19000, 'Dùng 1 viên mỗi ngày'),
('Sertraline', 'Viên', 130, 16000, 'Uống 1 viên vào buổi sáng'),
('Levothyroxine', 'Viên', 90, 25000, 'Uống 1 viên vào sáng sớm'),
('Hydrochlorothiazide', 'Viên', 160, 11000, 'Dùng 1 viên mỗi ngày'),
('Methylprednisolone', 'Viên', 200, 23000, 'Dùng theo chỉ định của bác sĩ');
insert into quy_dinh(so_benh_nhan,so_tien_kham)
values(40,100000)