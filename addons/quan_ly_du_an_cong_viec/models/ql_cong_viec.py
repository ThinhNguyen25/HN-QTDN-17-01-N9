from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QLCongViec(models.Model):
    _name = 'ql_cong_viec'
    _description = 'Quản lý công việc'
    _rec_name = 'ten_cong_viec'
    _order = 'deadline asc'

    ten_cong_viec = fields.Char(string='Tên công việc', required=True)
    mo_ta = fields.Text(string='Mô tả công việc')

    du_an_id = fields.Many2one(
        'ql_du_an',
        string='Dự án',
        required=True,
        ondelete='cascade'
    )

    nguoi_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Người phụ trách',
        required=True
    )

    ngay_bat_dau = fields.Date(string='Ngày bắt đầu')
    deadline = fields.Date(string='Hạn hoàn thành')
    ngay_hoan_thanh = fields.Date(string='Ngày hoàn thành')

    muc_uu_tien = fields.Selection([
        ('thap', 'Thấp'),
        ('trung_binh', 'Trung bình'),
        ('cao', 'Cao'),
        ('khan_cap', 'Khẩn cấp'),
    ], string='Mức ưu tiên', default='trung_binh')

    trang_thai = fields.Selection([
        ('chua_lam', 'Chưa làm'),
        ('dang_lam', 'Đang làm'),
        ('cho_duyet', 'Chờ duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
        ('qua_han', 'Quá hạn'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='chua_lam', required=True)

    tien_do = fields.Float(string='Tiến độ (%)', default=0.0)

    is_qua_han = fields.Boolean(
        string='Đã quá hạn',
        compute='_compute_is_qua_han'
    )

    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('deadline', 'trang_thai')
    def _compute_is_qua_han(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_qua_han = bool(
                rec.deadline
                and rec.deadline < today
                and rec.trang_thai not in ['hoan_thanh', 'huy']
            )

    @api.constrains('tien_do')
    def _check_tien_do(self):
        for rec in self:
            if rec.tien_do < 0 or rec.tien_do > 100:
                raise ValidationError('Tiến độ phải nằm trong khoảng từ 0 đến 100.')

    @api.constrains('ngay_bat_dau', 'deadline')
    def _check_dates(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.deadline and rec.ngay_bat_dau > rec.deadline:
                raise ValidationError('Ngày bắt đầu không được lớn hơn hạn hoàn thành.')

    def action_mark_done(self):
        for rec in self:
            rec.trang_thai = 'hoan_thanh'
            rec.tien_do = 100.0
            rec.ngay_hoan_thanh = fields.Date.today()
