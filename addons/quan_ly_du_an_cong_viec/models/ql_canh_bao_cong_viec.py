from odoo import models, fields


class QLCanhBaoCongViec(models.Model):
    _name = 'ql_canh_bao_cong_viec'
    _description = 'Cảnh báo công việc'
    _rec_name = 'name'
    _order = 'ngay_canh_bao desc'

    name = fields.Char(
        string='Tiêu đề cảnh báo',
        required=True,
        default='Cảnh báo công việc quá hạn'
    )

    cong_viec_id = fields.Many2one(
        'ql_cong_viec',
        string='Công việc',
        required=True,
        ondelete='cascade'
    )

    du_an_id = fields.Many2one(
        'ql_du_an',
        string='Dự án',
        related='cong_viec_id.du_an_id',
        store=True
    )

    nguoi_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Người phụ trách',
        related='cong_viec_id.nguoi_phu_trach_id',
        store=True
    )

    quan_ly_id = fields.Many2one(
        'nhan_vien',
        string='Quản lý dự án',
        related='cong_viec_id.du_an_id.quan_ly_id',
        store=True
    )

    loai_canh_bao = fields.Selection([
        ('qua_han', 'Quá hạn'),
        ('rui_ro', 'Rủi ro tiến độ'),
    ], string='Loại cảnh báo', default='qua_han', required=True)

    muc_do = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
    ], string='Mức độ', default='cao', required=True)

    ngay_canh_bao = fields.Date(
        string='Ngày cảnh báo',
        default=fields.Date.context_today,
        required=True
    )

    noi_dung = fields.Text(string='Nội dung cảnh báo')

    trang_thai = fields.Selection([
        ('mo', 'Đang mở'),
        ('da_xu_ly', 'Đã xử lý'),
    ], string='Trạng thái', default='mo', required=True)

    def action_mark_resolved(self):
        for rec in self:
            rec.trang_thai = 'da_xu_ly'
