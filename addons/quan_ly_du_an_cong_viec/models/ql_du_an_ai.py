import requests

from odoo import models, fields


class QLDuAnAI(models.Model):
    _inherit = 'ql_du_an'

    ai_phan_tich = fields.Text(string='AI phân tích')

    ai_du_bao = fields.Text(
        string='AI dự báo'
    )

    ai_uu_tien = fields.Text(
        string='AI ưu tiên công việc'
    )

    ai_nguy_co = fields.Text(
        string='AI nguy cơ trễ'
    )

    ai_bao_cao = fields.Html(
        string='Báo cáo AI'
    )

    def action_ai_phan_tich_du_an(self):
        self.ensure_one()

        ds_cong_viec = ""

        for cv in self.cong_viec_ids:
            ds_cong_viec += f"""
Tên công việc: {cv.ten_cong_viec}
Trạng thái: {cv.trang_thai}
Hạn hoàn thành: {cv.deadline}
--------------------------
"""

        prompt = f"""
Bạn là chuyên gia quản lý dự án ERP.

Tên dự án:
{self.ten_du_an}

Số lượng công việc:
{len(self.cong_viec_ids)}

Danh sách công việc:

{ds_cong_viec}

Yêu cầu:

1. Đánh giá tiến độ dự án.
2. Tính tỷ lệ hoàn thành.
3. Xác định công việc có nguy cơ chậm.
4. Phân tích rủi ro.
5. Đề xuất giải pháp cải thiện.
6. Đề xuất phân bổ nhân sự.
7. Xếp hạng mức ưu tiên công việc.
8. Dự đoán khả năng hoàn thành đúng hạn (%).
9. Kết luận tổng thể.

Trả lời bằng tiếng Việt.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        data = response.json()

        self.ai_phan_tich = data["response"]

        # dự báo
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": f"""
Hãy dự đoán khả năng hoàn thành dự án {self.ten_du_an}.

Cho biết:

- Khả năng thành công (%)
- Mức độ rủi ro
- Công việc cần ưu tiên
- Khuyến nghị quản lý

Dữ liệu:

{ds_cong_viec}
""",
                "stream": False
            }
        )

        self.ai_du_bao = response.json()["response"]

        # ưu tiên công việc
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": f"""
Hãy xếp loại từng công việc thành:

- Khẩn cấp
- Quan trọng
- Bình thường

Giải thích lý do.

{ds_cong_viec}
""",
                "stream": False
            }
        )

        self.ai_uu_tien = response.json()["response"]

        # nguy cơ trễ
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": f"""
Hãy phát hiện các công việc có nguy cơ trễ.

Cho biết:

- Công việc
- Mức độ nguy hiểm
- Nguyên nhân
- Đề xuất

{ds_cong_viec}
""",
                "stream": False
            }
        )

        self.ai_nguy_co = response.json()["response"]

        # báo cáo html
        self.ai_bao_cao = f"""
<h2>Tổng quan dự án</h2>

<h3>Phân tích tiến độ</h3>
<pre>{self.ai_phan_tich}</pre>

<h3>Dự báo hoàn thành</h3>
<pre>{self.ai_du_bao}</pre>

<h3>Ưu tiên công việc</h3>
<pre>{self.ai_uu_tien}</pre>

<h3>Nguy cơ trễ</h3>
<pre>{self.ai_nguy_co}</pre>
"""

        return {
            'type': 'ir.actions.client',
            'tag': 'reload'
        }
