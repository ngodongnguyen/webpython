
-- Dữ liệu bảng khoa
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
INSERT INTO nguoi_dung (ho_ten, username, password, gioi_tinh, cccd, type) VALUES
('Nguyễn Văn A', 'nguyenvana', 'password1', 1, '123456789012', 'nhan_vien'),
('Nguyễn Thị B', 'nguyenthib', 'password2', 0, '123456789013', 'nhan_vien'),
('Trần Văn C', 'tranvanc', 'password3', 1, '123456789014', 'nhan_vien'),
('Lê Thị D', 'lethid', 'password4', 0, '123456789015', 'nhan_vien'),
('Phạm Văn E', 'phamvane', 'password5', 1, '123456789016', 'nhan_vien'),
('Hoàng Thị F', 'hoangthif', 'password6', 0, '123456789017', 'nhan_vien'),
('Vũ Văn G', 'vuvang', 'password7', 1, '123456789018', 'nhan_vien'),
('Đặng Thị H', 'dangthih', 'password8', 0, '123456789019', 'nhan_vien'),
('Ngô Văn I', 'ngovanyi', 'password9', 1, '123456789020', 'nhan_vien'),
('Đỗ Thị J', 'dothij', 'password10', 0, '123456789021', 'nhan_vien'),
('Nguyễn Văn K', 'nguyenvank', 'password11', 1, '123456789022', 'nhan_vien'),
('Trần Thị L', 'tranthil', 'password12', 0, '123456789023', 'nhan_vien'),
('Phan Văn M', 'phanvanm', 'password13', 1, '123456789024', 'nhan_vien'),
('Bùi Thị N', 'buithin', 'password14', 0, '123456789025', 'nhan_vien'),
('Lý Văn O', 'lyvano', 'password15', 1, '123456789026', 'nhan_vien'),
('Trương Thị P', 'truongthip', 'password16', 0, '123456789027', 'nhan_vien'),
('Tôn Văn Q', 'tonvanq', 'password17', 1, '123456789028', 'nhan_vien'),
('Đinh Thị R', 'dinhthir', 'password18', 0, '123456789029', 'nhan_vien'),
('Hồ Văn S', 'hovans', 'password19', 1, '123456789030', 'nhan_vien'),
('Đặng Thị T', 'dangthit', 'password20', 0, '123456789031', 'nhan_vien');

INSERT INTO nhan_vien (id, chuc_vu) 
SELECT id, 'Bác sĩ' 
FROM nguoi_dung 
WHERE type = 'nhan_vien' AND id NOT IN (SELECT id FROM nhan_vien);

UPDATE nhan_vien SET type = 'bac_si' WHERE id IN (SELECT id FROM bac_si);

-- Liên kết bác sĩ với các khoa ngẫu nhiên
INSERT INTO bac_si (id, khoa_id)
SELECT id, (SELECT id FROM khoa ORDER BY RAND() LIMIT 1) FROM nhan_vien;
-- set ava cho bác sĩ
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513762/webpython/doctor/rqktahmpknhwdm8iea1z.jpg' WHERE id = 1;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513764/webpython/doctor/l6iv00ri9vu0fettzdon.jpg' WHERE id = 2;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513764/webpython/doctor/z8nenfvryfjcfnjsewzx.jpg' WHERE id = 3;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513765/webpython/doctor/q2dt17odfydslhjlkyxs.jpg' WHERE id = 4;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513768/webpython/doctor/drteti4xn9923mkp7qhs.jpg' WHERE id = 5;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513768/webpython/doctor/k5y5v71v40ggrusm2a44.jpg' WHERE id = 6;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513770/webpython/doctor/udl8vr64db9f4de6w2tj.jpg' WHERE id = 7;
Update nhan_vien
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513770/webpython/doctor/cpim4nhkemlisqegnc7i.jpg' WHERE id = 8;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513772/webpython/doctor/h0rc9fvfckvwwaxtv84p.jpg' WHERE id = 9;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513772/webpython/doctor/vfg11nygqzrerqvkl8n6.jpg' WHERE id = 10;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513773/webpython/doctor/auscidcj4rycfbojpne4.jpg' WHERE id = 11;
Update nhan_vien
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513774/webpython/doctor/r4um8m53vyrjehlwsveo.jpg' WHERE id = 12;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513776/webpython/doctor/placettba9jsc04vzu0d.jpg' WHERE id = 13;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513777/webpython/doctor/hrjfrm24noanqtjnhrtq.jpg' WHERE id = 14;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513778/webpython/doctor/gakbhbtxsur1d2fl9pt2.jpg' WHERE id = 15;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513779/webpython/doctor/pnqxek3qdi43zfd9ck5k.jpg' WHERE id = 16;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513782/webpython/doctor/ujytkplg7xt8larytz2m.jpg' WHERE id = 17;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513782/webpython/doctor/fadwf7jojzymotba522w.jpg' WHERE id = 18;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513788/webpython/doctor/zdkk9zkm0rc9n6fwjdp3.jpg' WHERE id = 19;
UPDATE nhan_vien 
SET avatar = 'https://res.cloudinary.com/ouweb/image/upload/v1734513790/webpython/doctor/vehzptcqomtioph7fzru.jpg' WHERE id = 20;
-- đổi khoa chỉ từ 1-10 th
UPDATE bac_si
SET khoa_id = CASE
    WHEN id BETWEEN 1 AND 10 THEN id      -- Giữ nguyên khoa_id bằng id nếu id từ 1 đến 10
    WHEN id BETWEEN 11 AND 20 THEN id - 10 -- Đặt khoa_id = id - 10 nếu id từ 11 đến 20
    ELSE khoa_id -- Giữ nguyên khoa_id cho các id còn lại
END;

