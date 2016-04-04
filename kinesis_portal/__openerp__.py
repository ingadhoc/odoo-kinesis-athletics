# -*- coding: utf-8 -*-

{
    'name': 'Portal Kinesis',
    'version': '0.1',
    'category': 'Tools',
    'complexity': 'easy',
    'description': """

    """,
    'author': 'Ingeniería ADHOC',
    'depends': ['kinesis_athletics_x','portal'],
    'data': [
        'portal_kinesis_view.xml',
        'security/ir.model.access.csv',
        'security/portal_security.xml',
    ],
    'installable': True,
    'auto_install': True,
    'category': 'Hidden',
}
