from odoo import models, fields


class NhanVien(models.Model):
    _inherit = 'nhan_vien'

    du_an_quan_ly_ids = fields.One2many(
        'ql_du_an',
        'quan_ly_id',
        string='Dự án quản lý'
    )

    du_an_tham_gia_ids = fields.Many2many(
        'ql_du_an',
        'ql_du_an_nhan_vien_rel',
        'nhan_vien_id',
        'du_an_id',
        string='Dự án tham gia'
    )

    cong_viec_phu_trach_ids = fields.One2many(
        'ql_cong_viec',
        'nguoi_phu_trach_id',
        string='Công việc phụ trách'
    )

    so_cong_viec_phu_trach = fields.Integer(
        string='Số công việc',
        compute='_compute_project_task_count'
    )

    def _compute_project_task_count(self):
        for rec in self:
            rec.so_cong_viec_phu_trach = self.env['ql_cong_viec'].search_count([
                ('nguoi_phu_trach_id', '=', rec.id)
            ])

    def action_open_cong_viec_phu_trach(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Công việc phụ trách',
            'res_model': 'ql_cong_viec',
            'view_mode': 'tree,form',
            'domain': [('nguoi_phu_trach_id', '=', self.id)],
            'context': {'default_nguoi_phu_trach_id': self.id},
        }
