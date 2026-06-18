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

    canh_bao_ids = fields.One2many(
        'ql_canh_bao_cong_viec',
        'cong_viec_id',
        string='Cảnh báo'
    )

    so_canh_bao = fields.Integer(
        string='Số cảnh báo',
        compute='_compute_so_canh_bao'
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

    @api.depends('canh_bao_ids', 'canh_bao_ids.trang_thai')
    def _compute_so_canh_bao(self):
        for rec in self:
            rec.so_canh_bao = len(rec.canh_bao_ids.filtered(lambda a: a.trang_thai == 'mo'))

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
            rec.canh_bao_ids.filtered(lambda a: a.trang_thai == 'mo').write({
                'trang_thai': 'da_xu_ly'
            })

    def action_check_overdue_now(self):
        self._cron_check_overdue_tasks()

    @api.model
    def _cron_check_overdue_tasks(self):
        today = fields.Date.today()

        overdue_tasks = self.search([
            ('deadline', '<', today),
            ('trang_thai', 'not in', ['hoan_thanh', 'huy']),
        ])

        Alert = self.env['ql_canh_bao_cong_viec']

        for task in overdue_tasks:
            task.trang_thai = 'qua_han'

            existed_alert = Alert.search([
                ('cong_viec_id', '=', task.id),
                ('loai_canh_bao', '=', 'qua_han'),
                ('trang_thai', '=', 'mo'),
            ], limit=1)

            if existed_alert:
                continue

            Alert.create({
                'name': 'Công việc quá hạn: %s' % task.ten_cong_viec,
                'cong_viec_id': task.id,
                'loai_canh_bao': 'qua_han',
                'muc_do': 'cao',
                'ngay_canh_bao': today,
                'noi_dung': (
                    'Công việc "%s" thuộc dự án "%s" đã quá hạn. '
                    'Người phụ trách: %s. Hạn hoàn thành: %s.'
                ) % (
                    task.ten_cong_viec,
                    task.du_an_id.ten_du_an,
                    task.nguoi_phu_trach_id.display_name,
                    task.deadline,
                )
            })
