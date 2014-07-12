# -*- coding: utf-8 -*-
{
    'active': False,
    'name': 'Import/Export Groups Evaluations',
    'author': 'Ingenieria Adhoc',
    'description': 'Import/Export Groups Evaluations',
    'website': 'www.ingadhoc.com',
    'images': [],
    'category': 'base.module_category_hidden',
    'demo_xml': [],
    'depends': [
        'kinesis_athletics_x', 
    ],
    'description': '',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'test': [],
    'update_xml': [
        'wizard/export_evaluation_wizard_view.xml',
        'wizard/import_evaluation_wizard_view.xml',
        'report/export_evaluation_report.xml',
        'group_view.xml',
    ],
    'version':'1.0'
}
