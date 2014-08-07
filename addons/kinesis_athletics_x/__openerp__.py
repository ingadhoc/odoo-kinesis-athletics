# -*- coding: utf-8 -*-

{   'active': False,
    'name': 'Kinesis Athletics X',
    'author': 'Ingeniería Adhoc',
    'description': 'Kinesis Athletics X. xlrd should be installed.',
    'website': 'www.ingadhoc.com',
    'images': [],
    'category': 'base.module_category_hidden',
    'demo': [
      'data/product.uom.categ.csv',
      'data/product.uom.csv',
      'data/kinesis_athletics.company_type.csv',
      'data/res.partner.csv',
      'data/kinesis_athletics.test_category.csv',
      'data/kinesis_athletics.test.csv',
      'data/kinesis_athletics.test_range.csv',
      'data/res_company.xml',
      'data/stage_2/res_company.xml',
      'data/kinesis_athletics.level.csv',
      'data/kinesis_athletics.group.csv',
      'data/res_users.xml',
      'data/kinesis_athletics.evaluation.csv',
      'data/kinesis_athletics.test_selection.csv',
      'data/kinesis_athletics.evaluation_detail.csv',
      'data/kinesis_athletics.test_selection.xml',
      'data/stage_2/res.partner.csv',
      'data/stage_2/kinesis_athletics.group.csv',
      ],
    'depends': ['kinesis_athletics','partner_person','board'],
    'init': [],
    'installable': True,
    'license': 'AGPL-3',
    'test': [],
    'js': ['static/src/js/*.js'],
    'css': ['static/src/css/*.css'],
    'qweb': ['static/src/xml/*.xml'],
    'data': [
      u'view/test_view.xml',
      u'wizard/wizard_view.xml',
      u'view/evaluation_detail_view.xml',
      u'view/partner_view.xml',
      u'view/group_view.xml',
      u'view/evaluation_view.xml',
      u'view/test_range_view.xml',
      u'view/test_selection_view.xml',
      u'view/report_evaluation.xml',
      u'view/report_external_layout_header.xml',
      u'kinesis_athletics_report.xml',
      u'view/company_view.xml',
      u'security/kinesis_athletics_security.xml',
      u'security/ir.model.access.csv',
      u'view/kinesis_athletics_x.xml',
      # 'view/kinesis_athletics_x_menuitem.xml',
      'report/kinesis_athletics_evaluation_detail_report_view.xml',
      ],
    'version':'1.0'
    }
