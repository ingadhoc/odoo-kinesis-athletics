# -*- coding: utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import Warning
import base64
import tempfile
import xlrd


class evaluation(models.Model):

    """"""
    _inherit = 'kinesis_athletics.evaluation'

    @api.model
    def import_evaluation(
            self, data, group=False, evaluation=False):
        """
        Si no se pasa grupo entonces buscamos los grupos del partner
        Si no se pasa evaluation entonces se crean las mismas
        """
        evaluations = self.env['kinesis_athletics.evaluation']
        evaluation_details = self.env[
            'kinesis_athletics.evaluation_detail']
        tests = self.env['kinesis_athletics.test']

        # Prepare data from file
        try:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            tmp_file.write(
                base64.b64decode(data and data.evaluation_data or _(
                    'Invalid file')))
            tmp_file.close()
            xls_tmp_file = xlrd.open_workbook(tmp_file.name)
            date = data.date
        except:
            raise Warning(_(
                'Unable to open the file. Make sure the file format is correct.'))

        sheet = xls_tmp_file.sheet_by_name(xls_tmp_file.sheet_names()[0])

        record_list = [sheet.row_values(i) for i in range(sheet.nrows)]
        record_header = record_list[0]
        record_list = record_list[1:]
        evaluation_ids = []
        evaluation_matrix = []
        for line in record_list:
            evaluation_matrix.append(dict(zip(record_header, line)))

        for evaluation_dic in evaluation_matrix:
            # Consider if we came from an evaluation
            partner_id = int(evaluation_dic.get('partner_id'))
            if not evaluation:
                # Create evaluations
                template = evaluations.browse(
                    int(evaluation_dic.get('Template')))

                # Consider if we dont came from groups
                if not group:
                    person = self.env['res.partner'].browse(partner_id)
                    group = person.actual_group_id

                vals = {
                    'name': template.name,
                    'template_id': template.id,
                    'date': date,
                    'company_id': group.company_id.id,
                    'group_id': group.id,
                    'partner_id': partner_id,
                }
                evaluation_id = evaluations.create(vals).id
                evaluation_ids.append(evaluation_id)
            else:
                if partner_id != evaluation.partner_id.id:
                    raise Warning(
                        _('To update an evaluation, partner must be the same'))
                evaluation_id = evaluation.id

            # Load test data
            for test_name in record_header[3:]:
                if evaluation_dic.get(test_name) != "":
                    test = tests.search(
                        [('name', 'ilike', test_name)], limit=1)
                    if not test:
                        raise Warning(_('Test %s not found') % test_name)
                    vals = {
                        'evaluation_id': evaluation_id,
                        'test_id': test.id,
                    }

                    if test.type == 'selection':
                        test_selection = self.env[
                            'kinesis_athletics.test_selection'].search(
                            [('test_id', '=', test.id),
                             ('name', 'ilike', evaluation_dic.get(test_name))],
                            limit=1)
                        if not test_selection:
                            raise Warning(
                                _('Result %s not found for test %s') % (
                                    evaluation_dic.get(test_name), test_name))
                        vals['test_selection_id'] = test_selection.id
                    else:
                        vals['result'] = float(evaluation_dic.get(test_name))

                    evaluation_detail = evaluation_details.search(
                        [('evaluation_id', '=', evaluation_id),
                         ('test_id', '=', test.id)], limit=1)

                    if evaluation_detail:
                        evaluation_detail.write(vals)
                    else:
                        evaluation_detail.create(vals)
            # If called from one evaluation
            if evaluation:
                return False

        action_evaluation = self.env['ir.model.data'].get_object_reference(
            'kinesis_athletics',
            'action_kinesis_athletics_evaluation_evaluations')
        action_evaluation_id = action_evaluation and action_evaluation[
            1] or False
        action_evaluation = self.env['ir.actions.act_window'].browse(
            action_evaluation_id)
        action_evaluation_read = action_evaluation.read()[0]
        action_evaluation_read['domain'] = [('id', 'in', evaluation_ids)]
        return action_evaluation_read

    def generate_eval_xls(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        obj = self.browse(cr, uid, ids[0], context=context)
        datas = {}

        group = obj.group_id

        tests = [x.test_id.name for x in obj.evaluation_detail_ids]

        partner_information = [
            {'id': obj.partner_id.id, 'name': obj.partner_id.name}]

        datas['partner_information'] = partner_information
        datas['tests'] = tests
        datas['group_name'] = group.name

        return self.pool['report'].get_action(
            cr, uid, [], 'kinesis_athletics_export_xls.groups_xls',
            data=datas, context=context)
