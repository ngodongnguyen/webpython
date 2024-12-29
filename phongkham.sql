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
('Khoa Chẩn đoán hình ảnh', 'Chuyên thực hiện các phương pháp chẩn đoán hình ảnh như X-quang, siêu âm, CT, MRI.'),
('Khoa Hồi sức cấp cứu', 'Chuyên điều trị các ca bệnh cấp cứu, cấp cứu ngoại khoa, nội khoa.'),
('Khoa Phục hồi chức năng', 'Chuyên điều trị phục hồi chức năng cho bệnh nhân sau phẫu thuật hoặc chấn thương.'),
('Khoa Ung bướu', 'Chuyên điều trị các bệnh ung thư, bao gồm xạ trị, hóa trị, và phẫu thuật.'),
('Khoa Tâm thần', 'Chuyên điều trị các bệnh lý tâm thần, rối loạn cảm xúc và hành vi.'),
('Khoa Tim mạch', 'Chuyên điều trị các bệnh lý về tim mạch như bệnh mạch vành, suy tim, huyết áp cao.'),
('Khoa Tiết niệu', 'Chuyên điều trị các bệnh lý về hệ tiết niệu như sỏi thận, viêm đường tiết niệu.'),
('Khoa Phẫu thuật thần kinh', 'Chuyên thực hiện phẫu thuật cho các bệnh lý thần kinh, đặc biệt là đột quỵ, u não.'),
('Khoa Nội tiết', 'Chuyên điều trị các bệnh lý về nội tiết như đái tháo đường, suy giáp, cường giáp.'),
('Khoa Hô hấp', 'Chuyên điều trị các bệnh lý về đường hô hấp như hen suyễn, viêm phổi, bệnh phổi tắc nghẽn mãn tính.'),
('Khoa Vật lý trị liệu', 'Chuyên hỗ trợ bệnh nhân phục hồi chức năng sau chấn thương, tai nạn hoặc phẫu thuật.');
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
(3, 'nv03', 'password03', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(4, 'nv04', 'password04', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(5, 'nv05', 'password05', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(6, 'nv06', 'password06', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(7, 'nv07', 'password07', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(8, 'nv08', 'password08', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(9, 'nv09', 'password09', 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si'),
(10, 'nv10', 'password10','https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg', 'bac_si');

INSERT INTO bac_si (id, khoa_id)
SELECT id, (SELECT id FROM khoa ORDER BY RAND() LIMIT 1) FROM nhan_vien;
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
SELECT id FROM nguoi_dung;
-- tạo 10 danh sách phiếu khám bệnh
INSERT INTO danh_sach_phieu_kham_benh (id)
VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);
-- tạo 20 phiếu khám bệnh
INSERT INTO phieu_kham_benh (id, trieu_chung, chuan_doan, benh_nhan_id, danhsach_id, bac_si_id) 
VALUES
(1, 'Sốt cao, đau đầu', 'Sốt xuất huyết', 1, 1, 1),
(2, 'Ho, đau họng', 'Viêm họng', 2, 1, 2),
(3, 'Đau bụng, tiêu chảy', 'Rối loạn tiêu hóa', 3, 2, 1),
(4, 'Khó thở, tức ngực', 'Hen suyễn', 4, 2, 3),
(5, 'Sốt nhẹ, mệt mỏi', 'Cảm cúm', 5, 3, 2),
(6, 'Đau lưng', 'Thoát vị đĩa đệm', 6, 3, 4),
(7, 'Đau khớp', 'Viêm khớp dạng thấp', 7, 4, 3),
(8, 'Ngứa, nổi mẩn đỏ', 'Dị ứng da', 8, 4, 2),
(9, 'Đau mắt, nhức mắt', 'Viêm kết mạc', 9, 5, 1),
(10, 'Đau răng, sưng nướu', 'Viêm lợi', 10, 5, 4),
(11, 'Đau tai, ù tai', 'Viêm tai giữa', 11, 6, 3),
(12, 'Khó ngủ, mệt mỏi', 'Rối loạn giấc ngủ', 12, 6, 1),
(13, 'Đau ngực, khó thở', 'Bệnh tim mạch', 13, 7, 2),
(14, 'Tay chân lạnh', 'Hạ huyết áp', 14, 7, 4),
(15, 'Ngất xỉu, chóng mặt', 'Thiếu máu', 15, 8, 1),
(16, 'Sốt, đau họng', 'Viêm amidan', 16, 8, 3),
(17, 'Đau bụng, buồn nôn', 'Viêm dạ dày', 17, 9, 2),
(18, 'Mệt mỏi, đau nhức toàn thân', 'Sốt xuất huyết', 18, 9, 4),
(19, 'Khó tiêu, đầy bụng', 'Rối loạn tiêu hóa', 19, 10, 1),
(20, 'Chóng mặt, đau đầu', 'Thiếu máu não', 20, 10, 3);

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
(11, '2024-12-30', 200000, 150000, 350000, 11, 11, 3),
(12, '2024-12-31', 150000, 50000, 200000, 12, 12, 1),
(13, '2025-01-01', 180000, 60000, 240000, 13, 13, 2),
(14, '2025-01-02', 190000, NULL, 190000, 14, 14, 3),
(15, '2025-01-03', 200000, 80000, 280000, 15, 15, 1),
(16, '2025-01-04', 170000, 90000, 260000, 16, 16, 2),
(17, '2025-01-05', 150000, 70000, 220000, 17, 17, 3),
(18, '2025-01-06', 180000, 80000, 260000, 18, 18, 1),
(19, '2025-01-07', 160000, 60000, 220000, 19, 19, 2),
(20, '2025-01-08', 200000, 100000, 300000, 20, 20, 3);
INSERT INTO nguoi_dung (id, ho, ten, gioi_tinh, cccd, ngay_sinh)
VALUES
(43, 'Nguyen', 'Thu', 1, '123456789012', '1990-01-01'),
(44, 'Tran', 'Lan', 0, '123456789013', '1992-02-02'),
(45, 'Le', 'Minh', 1, '123456789014', '1988-03-03'),
(46, 'Pham', 'Hoa', 0, '123456789015', '1995-04-04'),
(47, 'Hoang', 'Thao', 0, '123456789016', '1993-05-05')


INSERT INTO nhan_vien (id, username, password, avatar, type)
VALUES
(43, 'thu1', 'password_hash_1', NULL, 'thu_ngan'),
(44, 'thu2', 'password_hash_2', NULL, 'thu_ngan'),
(45, 'thu3', 'password_hash_3', NULL, 'thu_ngan'),
(46, 'thu4', 'password_hash_4', NULL, 'thu_ngan'),
(47, 'thu5', 'password_hash_5', NULL, 'thu_ngan')


INSERT INTO thu_ngan (id)
VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);