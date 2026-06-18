from odoo import models, fields, api
from odoo.exceptions import ValidationError


class QLDuAn(models.Model):
    _name = 'ql_du_an'
    _description = 'Quản lý dự án'
    _rec_name = 'ten_du_an'
    _order = 'ngay_bat_dau desc'

    ma_du_an = fields.Char(string='Mã dự án', required=True)
    ten_du_an = fields.Char(string='Tên dự án', required=True)
    muc_tieu = fields.Text(string='Mục tiêu dự án')
    mo_ta = fields.Text(string='Mô tả')

    quan_ly_id = fields.Many2one(
        'nhan_vien',
        string='Quản lý dự án',
        required=True
    )

    thanh_vien_ids = fields.Many2many(
        'nhan_vien',
        'ql_du_an_nhan_vien_rel',
        'du_an_id',
        'nhan_vien_id',
        string='Thành viên dự án'
    )

    ngay_bat_dau = fields.Date(string='Ngày bắt đầu')
    ngay_ket_thuc = fields.Date(string='Ngày kết thúc')

    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('tam_dung', 'Tạm dừng'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], string='Trạng thái', default='draft', required=True)

    cong_viec_ids = fields.One2many(
        'ql_cong_viec',
        'du_an_id',
        string='Danh sách công việc'
    )

    so_cong_viec = fields.Integer(
        string='Số công việc',
        compute='_compute_project_stats'
    )

    so_cong_viec_hoan_thanh = fields.Integer(
        string='Công việc hoàn thành',
        compute='_compute_project_stats'
    )

    tien_do = fields.Float(
        string='Tiến độ dự án (%)',
        compute='_compute_project_stats',
        store=True
    )

    @api.depends('cong_viec_ids', 'cong_viec_ids.trang_thai', 'cong_viec_ids.tien_do')
    def _compute_project_stats(self):
        for rec in self:
            tasks = rec.cong_viec_ids
            rec.so_cong_viec = len(tasks)
            rec.so_cong_viec_hoan_thanh = len(tasks.filtered(lambda t: t.trang_thai == 'hoan_thanh'))

            if tasks:
                rec.tien_do = sum(tasks.mapped('tien_do')) / len(tasks)
            else:
                rec.tien_do = 0.0

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc and rec.ngay_bat_dau > rec.ngay_ket_thuc:
                raise ValidationError('Ngày bắt đầu không được lớn hơn ngày kết thúc.')

    def action_open_cong_viec(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc của dự án',
            'res_model': 'ql_cong_viec',
            'view_mode': 'tree,form',
            'domain': [('du_an_id', '=', self.id)],
            'context': {'default_du_an_id': self.id},
        }
