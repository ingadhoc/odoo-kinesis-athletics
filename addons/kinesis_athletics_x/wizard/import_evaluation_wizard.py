# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Noviat nv/sa (www.noviat.be). All rights reserved.
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
import base64
import time

import tempfile
import xlrd

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

import logging

_logger = logging.getLogger(__name__)

class import_evaluation_wizard(osv.osv_memory):
    _name = 'import.evaluation.wizard'
    _description = 'Import Evaluation wizard'
    _columns = {
        'date': fields.date(string='Date', required=True),
        'evaluation_data': fields.binary('Evaluation File', required=True),
        'evaluation_fname': fields.char('Evaluation Filename', size=128, required=True),
    }

    _defaults = {
        'evaluation_fname': lambda *a: '',
    }

    def import_evaluation(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        active_id = context.get('active_id', False)
        group = self.pool['kinesis_athletics.group'].browse(cr, uid, active_id, context=context)
        if not active_id:
            return {'type': 'ir.actions.act_window_close'}

        data = self.browse(cr, uid, ids)[0]
        try:
            tmp_file = tempfile.NamedTemporaryFile(delete = False)
            tmp_file.write(base64.b64decode(data and data.evaluation_data or _('Invalid file')))
            tmp_file.close()
            xls_tmp_file = xlrd.open_workbook(tmp_file.name)
            
            date = data.date
        except:
            raise osv.except_osv(_('Error'), _('Unable to open the file. Make sure the file format is correct.'))
            return False

        sheet = xls_tmp_file.sheet_by_name(xls_tmp_file.sheet_names()[0])
        
        record_list = [sheet.row_values(i) for i in range(sheet.nrows)]
        record_header = record_list[0]
        record_list = record_list[1:]
        
        evaluation_matrix = []
        for line in record_list:
            evaluation_matrix.append(dict(zip(record_header, line)))
        
        evaluation_obj = self.pool.get('kinesis_athletics.evaluation')
        evaluation_detail_obj = self.pool.get('kinesis_athletics.evaluation_detail')

        try:
            for evaluation_dic in evaluation_matrix:
                val = {
                    'date': date,
                    'group_id': group.id,
                    'partner_id': int(evaluation_dic.get('partner_id'))
                }
                evaluation_id = evaluation_obj.create(cr, uid, val, context=context)

                detail_fields = ['evaluation_id/.id', 'test_id', 'result']
                detail_data = []

                for test_name in record_header[2:]:
                    eval_detail = [evaluation_id, test_name, float(evaluation_dic.get(test_name))]
                    detail_data.append(eval_detail)

                evaluation_detail_obj.load(cr, uid, detail_fields, detail_data, context=context)
        except:
            raise osv.except_osv(_('Error'), _('File is does not have the correct format, check that the Persons in the file belong to the underlygin Group.'))
            return False

        return True