# -*- encoding: utf-8 -*-

import base64
import tempfile
import xlrd

from openerp.osv import fields, osv
from openerp.tools.translate import _

class import_evaluation_person_wizard(osv.osv_memory):
    _name = 'import.evaluation.person.wizard'
    _description = _('Wizard to import XLS evaluations for Kinesis groups')

    _columns = {
        'date': fields.date(string=_('Date')),
        'evaluation_data': fields.binary(_('Evaluation File'), required=True),
        'evaluation_fname': fields.char(_('Evaluation Filename'), size=128, required=True),
    }

    _defaults = {
        'evaluation_fname':'Imported Evaluation',
        # 'evaluation_fname': lambda *a: 'imported_evaluation',
        'date':fields.date.context_today,
    }

    def import_evaluation_person(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        active_ids = context.get('active_ids', False)

        persons = self.pool['res.partner'].browse(cr, uid, active_ids, context=context)
        if not active_ids:
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
        print evaluation_matrix[:1]

       
        evaluation_obj = self.pool.get('kinesis_athletics.evaluation')
        evaluation_detail_obj = self.pool.get('kinesis_athletics.evaluation_detail')


        try:
            for evaluation_dic in evaluation_matrix:
                for person in persons:
                    val = {
                        'name':'Evaluation',
                        'date': date,
                        'company_id':person.company_id.id,
                        'group_id': person.actual_group_id.id,
                        'partner_id': person.id,
                    }
                    print val 
                    evaluation_id = evaluation_obj.create(cr, uid, val, context=context)

                    detail_fields = ['evaluation_id/.id', 'test_id', 'result']
                    detail_data = []
                        
                    for test_name in record_header[2:]:
                        print test_name
                        if evaluation_dic.get(test_name) != "":
                            eval_detail = [evaluation_id, test_name, float(evaluation_dic.get(test_name))]
                            detail_data.append(eval_detail)

            evaluation_detail_obj.load(cr, uid, detail_fields, detail_data, context=context)
        except Exception as e:
            raise osv.except_osv(
                _('Error'),
                _('File is does not have the correct format, check that the Persons in the file belong to the underlygin Group.\nError Details: %s') % e)
            return False

        return True
