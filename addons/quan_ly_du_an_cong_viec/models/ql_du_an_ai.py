import os
import requests

from odoo import models, fields
from odoo.exceptions import UserError


class QLDuAnAI(models.Model):
    _inherit = 'ql_du_an'

    ai_phan_tich = fields.Text(string='AI phân tích dự án')
    ai_last_generated_at = fields.Datetime(string='Thời điểm AI phân tích gần nhất')

    def _build_ai_prompt(self):
        self.ensure_one()

        task_lines = []
        for task in self.cong_viec_ids:
            task_lines.append(
                '- {name} | Phụ trách: {owner} | Deadline: {deadline} | '
                'Trạng thái: {state} | Tiến độ: {progress}% | Ưu tiên: {priority}'.format(
                    name=task.ten_cong_viec or '',
                    owner=task.nguoi_phu_trach_id.display_name or '',
                    deadline=task.deadline or '',
                    state=task.trang_thai or '',
                    progress=task.tien_do or 0,
                    priority=task.muc_uu_tien or '',
                )
            )

        if not task_lines:
            task_lines.append('- Dự án chưa có công việc nào.')

        return """
Bạn là trợ lý AI hỗ trợ quản lý dự án trong Odoo ERP.
Hãy phân tích dự án sau bằng tiếng Việt, ngắn gọn, rõ ràng.

THÔNG TIN DỰ ÁN:
Mã dự án: {ma}
Tên dự án: {ten}
Mục tiêu: {muc_tieu}
Quản lý dự án: {quan_ly}
Thành viên: {thanh_vien}
Trạng thái: {trang_thai}
Tiến độ hệ thống tính: {tien_do}%
Số công việc: {so_cv}
Số công việc hoàn thành: {so_done}

DANH SÁCH CÔNG VIỆC:
{tasks}

Yêu cầu trả lời đúng 3 phần:
1. TÓM TẮT TIẾN ĐỘ
2. RỦI RO CHÍNH
3. GỢI Ý HÀNH ĐỘNG ƯU TIÊN
""".format(
            ma=self.ma_du_an or '',
            ten=self.ten_du_an or '',
            muc_tieu=self.muc_tieu or '',
            quan_ly=self.quan_ly_id.display_name or '',
            thanh_vien=', '.join(self.thanh_vien_ids.mapped('display_name')),
            trang_thai=self.trang_thai or '',
            tien_do=self.tien_do or 0,
            so_cv=self.so_cong_viec or 0,
            so_done=self.so_cong_viec_hoan_thanh or 0,
            tasks='\n'.join(task_lines),
        )

    def action_ai_phan_tich_du_an(self):
        self.ensure_one()

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise UserError('Chưa cấu hình OPENAI_API_KEY trong terminal chạy Odoo.')

        payload = {
            'model': os.environ.get('OPENAI_MODEL', 'gpt-4o-mini'),
            'input': self._build_ai_prompt(),
        }

        headers = {
            'Authorization': 'Bearer %s' % api_key,
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(
                'https://api.openai.com/v1/responses',
                headers=headers,
                json=payload,
                timeout=60
            )
        except Exception as exc:
            raise UserError('Không gọi được AI API: %s' % exc)

        if response.status_code >= 400:
            raise UserError('AI API lỗi %s: %s' % (response.status_code, response.text[:800]))

        data = response.json()
        ai_text = data.get('output_text', '')

        if not ai_text:
            for item in data.get('output', []):
                for content in item.get('content', []):
                    if content.get('text'):
                        ai_text += content.get('text') + '\n'

        ai_text = ai_text.strip()
        if not ai_text:
            raise UserError('AI API phản hồi nhưng không có nội dung văn bản.')

        self.write({
            'ai_phan_tich': ai_text,
            'ai_last_generated_at': fields.Datetime.now(),
        })

        return {'type': 'ir.actions.client', 'tag': 'reload'}
