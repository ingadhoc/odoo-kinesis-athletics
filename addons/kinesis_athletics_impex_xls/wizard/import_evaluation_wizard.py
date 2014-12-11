# -*- encoding: utf-8 -*-

import base64
import tempfile
import xlrd

from openerp.osv import fields, osv
from openerp.tools.translate import _


class import_evaluation_wizard(osv.osv_memory):
    _name = 'import.evaluation.wizard'
    _description = _('Wizard to import XLS evaluations for Kinesis groups')

    _columns = {
        'date': fields.date(string=_('Date')),
        'evaluation_data': fields.binary(_('Evaluation File'), required=True),
        'evaluation_fname': fields.char(_('Evaluation Filename'), size=128, required=True),
    }

    _defaults = {
        'evaluation_fname': 'Imported Evaluation',
        # 'evaluation_fname': lambda *a: 'imported_evaluation',
        'date': fields.date.context_today,
    }

    def import_evaluation(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        active_id = context.get('active_id', False)
        eval_created = context.get('eval_created', False)

        group = self.pool['kinesis_athletics.group'].browse(
            cr, uid, active_id, context=context)
        if not active_id:
            return {'type': 'ir.actions.act_window_close'}

        data = self.browse(cr, uid, ids)[0]
        try:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file.write(
                base64.b64decode(data and data.evaluation_data or _('Invalid file')))
            tmp_file.close()
            xls_tmp_file = xlrd.open_workbook(tmp_file.name)

            date = data.date
        except:
            raise osv.except_osv(
                _('Error'), _('Unable to open the file. Make sure the file format is correct.'))
            return False

        sheet = xls_tmp_file.sheet_by_name(xls_tmp_file.sheet_names()[0])

        record_list = [sheet.row_values(i) for i in range(sheet.nrows)]
        record_header = record_list[0]
        record_list = record_list[1:]
        evaluation_ids = []
        evaluation_matrix = []
        for line in record_list:
            evaluation_matrix.append(dict(zip(record_header, line)))

        evaluation_obj = self.pool['kinesis_athletics.evaluation']
        evaluation_detail_obj = self.pool[
            'kinesis_athletics.evaluation_detail']
        test_obj = self.pool.get('kinesis_athletics.test_selection')
        try:
            for evaluation_dic in evaluation_matrix:
                if eval_created:
                    evaluation_id = active_id
                    evaluation = evaluation_obj.browse(
                        cr, uid, evaluation_id, context=context)

                    for test in record_header[2:]:

                        for detail in evaluation.evaluation_detail_ids:
                            if test == detail.test_id.name:
                                if evaluation_dic.get(test) != "":
                                    if detail.test_id.test_selection_ids:
                                        test_selection = test_obj.search(cr, uid, [(
                                            'name', '=', evaluation_dic.get(test)), ('test_id', '=', test)], context=context)
                                        vals = {

                                            'test_selection_id': test_selection[0]

                                        }
                                    else:
                                        vals = {

                                            'result': float(evaluation_dic.get(test))

                                        }
                                    evaluation_detail_obj.write(cr, uid, detail.id, vals, context=None)
                                break
                            else:
                                pass
                                # detail_fields = ['evaluation_id/.id', 'test_id', 'result']
                                # detail_data = []

                                # if evaluation_dic.get(test) != "":
                                # Fijarte si existe un tst con ese test name,si existe
                                #     eval_detail = [evaluation_id, test, float(evaluation_dic.get(test))]
                                #     detail_data.append(eval_detail)

                                # evaluation_detail_obj.load(cr, uid, detail_fields, detail_data, context=context)

                else:
                    name_eval_id = evaluation_obj.browse(
                        cr, uid, int(evaluation_dic.get('Template')), context=context)
                    val = {
                        'name': name_eval_id.name,
                        'date': date,
                        'company_id': group.company_id.id,
                        'group_id': group.id,
                        'partner_id': int(evaluation_dic.get('partner_id'))
                    }
                    evaluation_id = evaluation_obj.create(
                        cr, uid, val, context=context)
                    detail_data = []
                    evaluation_ids.append(evaluation_id)

                    if int(evaluation_dic.get('Template')) == 1:
                        detail_fields = [
                            'evaluation_id/.id', 'test_id', 'result']
                        for test_name in record_header[3:]:
                            if evaluation_dic.get(test_name) != "":
                                eval_detail = [
                                    evaluation_id, test_name, float(evaluation_dic.get(test_name))]
                                detail_data.append(eval_detail)
                    else:
                        detail_fields = [
                            'evaluation_id/.id', 'test_id', 'test_selection_id']
                        detail_data = []
                        for test_name in record_header[3:]:
                            # print test_name
                            if evaluation_dic.get(test_name) != "":
                                eval_detail = [
                                    evaluation_id, test_name, str(evaluation_dic.get(test_name))]
                                detail_data.append(eval_detail)

                    evaluation_detail_obj.load(
                        cr, uid, detail_fields, detail_data, context=context)
        except Exception as e:
            raise osv.except_osv(
                _('Error'),
                _('File is does not have the correct format, check that the Persons in the file belong to the underlygin Group.\nError Details: %s') % e)
            return False


        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        action_evaluation = mod_obj.get_object_reference(cr, uid, 'kinesis_athletics', 'action_kinesis_athletics_evaluation_evaluations')
        action_evaluation_id = action_evaluation and action_evaluation[1] or False
        action_evaluation = act_obj.read(cr, uid, [action_evaluation_id], context=context)[0]
        action_evaluation['domain'] = [('id','in',evaluation_ids)]

        return action_evaluation
