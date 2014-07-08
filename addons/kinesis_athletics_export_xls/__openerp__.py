# -*- coding: utf-8 -*-
##############################################################################
#
#    kinesis_athletics
#    Copyright (C) 2014 No author.
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
    'author': 'Sistemas Adhoc',
    'category': 'base.module_category_hidden',
    'demo_xml': [
      ],
    'depends': [
      'kinesis_athletics_x', 
      ],
    'description': '',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': 'Export Groups Evaluations',
    'test': [],
    'update_xml': [
                  'wizard/group_evaluation_export_wizard_view.xml', 
                  'report/group_evaluation_export_report.xml', 
                  'group_view.xml',
                      ],
    'version':'1.0',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
