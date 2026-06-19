<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP được áp dụng vào học phần Thực tập doanh nghiệp dựa trên mã nguồn mở Odoo. 

---

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

---

## 🚀 3. Các project đã thực hiện dựa trên Platform

Một số project sinh viên đã thực hiện:
- #### [Khoá 15](./docs/projects/K15/README.md)
- #### [Khoá 16](./docs/projects/K16/README.md)
- #### [Khoá 17](./docs/projects/K17/README.md)

---

## ⚙️ 4. Hướng dẫn cài đặt và chạy dự án

### 4.1. Tải Source Code & Tạo môi trường Python
Thực hiện clone dự án từ nhánh phát triển và di chuyển vào thư mục dự án:
```bash
git clone -b btl-quan-ly-du-an-cong-viec [https://github.com/ThinhNguyen25/HN-QTDN-17-01-N9.git](https://github.com/ThinhNguyen25/HN-QTDN-17-01-N9.git)
cd HN-QTDN-17-01-N9

```

Khởi tạo và kích hoạt môi trường ảo `venv` (nằm ngoài thư mục dự án):

```bash
python3 -m venv ../venv
source ../venv/bin/activate

```

### 4.2. Cài đặt các thư viện cần thiết

Cài đặt các gói phụ thuộc từ file `requirements.txt`:

```bash
pip install -r requirements.txt

```

### 4.3. Khởi động Cơ sở dữ liệu (PostgreSQL) bằng Docker

Chạy container PostgreSQL với cấu hình cổng và tài khoản tương thích cho Odoo:

```bash
docker run -d \
--name postgres_odoo-base \
-e POSTGRES_USER=odoo \
-e POSTGRES_PASSWORD=odoo \
-e POSTGRES_DB=postgres \
-p 5431:5432 \
postgres:10-alpine

```

> 💡 **Lưu ý:** Nếu container đã tồn tại sẵn từ trước, bạn chỉ cần khởi động lại bằng lệnh:
> ```bash
> docker start postgres_odoo-base
> 
> ```
> 
> 

Kiểm tra trạng thái hoạt động của container:

```bash
docker ps

```

Đảm bảo kết quả hiển thị có chứa thông tin: `postgres_odoo-base` và `0.0.0.0:5431->5432/tcp`.

### 4.4. Cấu hình tham số hệ thống

Đảm bảo bạn đã cấu hình tệp **odoo.conf** (kế thừa từ `odoo.conf.template`) khớp với thông số Docker ở trên:

```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069

```

### 4.5. Khởi động Odoo và truy cập hệ thống

Kích hoạt lại môi trường ảo (nếu chưa bật) và chạy file binary của Odoo kèm file cấu hình:

```bash
source ../venv/bin/activate
python3 odoo-bin -c odoo.conf

```

Nếu chạy thành công, hệ thống sẽ xuất hiện dòng thông báo:

```text
HTTP service (werkzeug) running on localhost:8069

```

Mở trình duyệt và truy cập hệ thống theo đường dẫn: **http://localhost:8069**

---

## ✨ 5. Các chức năng đã xây dựng

### 👤 Module Nhân sự

* Quản lý thông tin chi tiết của nhân viên.

### 📄 Module Văn bản

* Quản lý và lưu trữ hệ thống văn bản đi và văn bản đến.

### 💼 Module Quản lý dự án - công việc

* Khởi tạo và quản lý toàn diện các dự án.
* Phân rã, quản lý danh sách công việc chi tiết.
* Liên kết, chỉ định nhân viên phụ trách trực tiếp.
* Theo dõi trực quan tiến độ và đánh dấu trạng thái hoàn thành.

### ⚠️ Cảnh báo quá hạn

* Tự động quét và phát hiện các đầu việc bị chậm tiến độ.
* Hệ thống tự động sinh cảnh báo.
* Tự động chuyển trạng thái công việc sang **"Quá hạn"**.

### 🧠 AI phân tích dự án

* Tự động phân tích sâu tiến độ tổng thể của toàn dự án.
* Đánh giá chính xác tỷ lệ hoàn thành công việc.
* Đưa ra nhận xét thông minh kèm gợi ý tối ưu, cải thiện hiệu suất.

---

## 📝 6. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.
