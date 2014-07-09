# -*- coding: utf-8 -*-
##############################################################################
#
#    kinesis_athletics
#    Copyright (C) 2014 Ingenieria Adhoc
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{   'active': False,
    'name': 'Kinesis Athletics X',
    'author': 'Ingeniería Adhoc',
    'description': 'Kinesis Athletics X. xlrd should be installed.',
    'website': 'www.ingadhoc.com',
    'images': [
    ],
    'category': 'base.module_category_hidden',
    'demo_xml': [
      'data/product.uom.categ.csv',
      'data/product.uom.csv',
      'data/kinesis_athletics.company_type.csv',
      'data/res.partner.csv',
      'data/kinesis_athletics.test_category.csv',
      'data/kinesis_athletics.test.csv',
      'data/kinesis_athletics.test_range.csv',
      'data/stage_2/res_company.xml',
      'data/kinesis_athletics.level.csv',
      'data/kinesis_athletics.group.csv',
      'data/res_users.xml',
      'data/kinesis_athletics.evaluation.csv',
      'data/kinesis_athletics.test_selection.csv',
      #'data/kinesis_athletics.evaluation_detail.csv',
      'data/kinesis_athletics.test_selection.xml',
      'data/stage_2/res.partner.csv',
      'data/stage_2/kinesis_athletics.group.csv',
      ],
    'depends': ['kinesis_athletics','partner_person','board'],
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'test': [],
    'js': ['static/src/js/*.js'],
    'css': ['static/src/css/*.css'],
    'qweb': ['static/src/xml/*.xml'],
    'update_xml': [u'view/test_view.xml',
                      #u'security/kinesis_athletics_group.xml',
                      # u'view/users_view.xml',
                      # u'view/test_category_view.xml',
                      u'wizard/wizard_view.xml',
                      u'wizard/import_evaluation_wizard.xml',
                      u'view/evaluation_detail_view.xml',
                      u'view/partner_view.xml',
                      u'view/group_view.xml',
                      u'view/evaluation_view.xml',
                      u'view/test_range_view.xml',
                      u'view/test_selection_view.xml',
                      'view/company_view.xml',
                      # u'report/kinesis_athletics_evaluation_detail_report_view.xml',
                      'security/kinesis_athletics_security.xml',
                      'security/ir.model.access.csv',
                      'view/kinesis_athletics_x.xml',
                      # u'view/kinesis_athletics_x_menuitem.xml',
                      # u'data/users_properties.xml',
                      # u'data/test_category_properties.xml',
                      # u'data/evaluation_details_properties.xml',
                      ],
                      # u'data/test_properties.xml',
                      # u'data/partner_properties.xml',
                      # u'data/evaluation_properties.xml',
                      # u'data/users_track.xml',
                      # u'data/test_category_track.xml',
                      # u'data/evaluation_details_track.xml',
                      # u'data/test_track.xml',
                      # u'data/partner_track.xml',
                      # u'data/evaluation_track.xml',
                      # 'security/ir.model.access.csv'],
    'version':'1.0'
    }
