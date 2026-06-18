{
    'name': 'Quản lý dự án & Công việc',
    'version': '1.0',
    'category': 'Project Management',
    'summary': 'Quản lý dự án, công việc và liên kết với nhân sự',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/ql_du_an_views.xml',
        'views/ql_cong_viec_views.xml',
        'views/nhan_vien_extend_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
