# HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN

## 1. Clone source code

```bash
git clone -b btl-quan-ly-du-an-cong-viec https://github.com/ThinhNguyen25/HN-QTDN-17-01-N9.git

cd HN-QTDN-17-01-N9
```

---

## 2. Tạo môi trường Python

```bash
python3 -m venv ../venv
source ../venv/bin/activate
```

---

## 3. Cài thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

## 4. Khởi động PostgreSQL bằng Docker

```bash
docker run -d \
--name postgres_odoo-base \
-e POSTGRES_USER=odoo \
-e POSTGRES_PASSWORD=odoo \
-e POSTGRES_DB=postgres \
-p 5431:5432 \
postgres:10-alpine
```

Nếu container đã tồn tại:

```bash
docker start postgres_odoo-base
```

Kiểm tra:

```bash
docker ps
```

Phải thấy:

```
postgres_odoo-base
0.0.0.0:5431->5432/tcp
```

---

## 5. Khởi động Odoo

```bash
source ../venv/bin/activate

python3 odoo-bin -c odoo.conf
```

Nếu chạy thành công sẽ xuất hiện:

```
HTTP service (werkzeug) running on localhost:8069
```

---

## 6. Truy cập hệ thống

Mở trình duyệt:

```
http://localhost:8069
```

---

## Chức năng đã xây dựng

### Module Nhân sự

* Quản lý nhân viên.

### Module Văn bản

* Quản lý văn bản đi và đến.

### Module Quản lý dự án - công việc

* Quản lý dự án.
* Quản lý công việc.
* Liên kết nhân viên phụ trách.
* Theo dõi tiến độ.
* Đánh dấu hoàn thành.

### Cảnh báo quá hạn

* Tự động phát hiện công việc quá hạn.
* Sinh cảnh báo.
* Chuyển trạng thái sang "Quá hạn".

### AI phân tích dự án

* Phân tích tiến độ dự án.
* Đánh giá tỷ lệ hoàn thành.
* Đưa ra nhận xét và gợi ý cải thiện.
