# -*- encoding: utf-8 -*-
from openerp import fields, models, api, _
from openerp.exceptions import Warning


class import_evaluation_wizard(models.TransientModel):
    _name = 'import.evaluation.wizard'
    _description = 'Wizard to import XLS evaluations for Kinesis groups'

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today
        )
    evaluation_data = fields.Binary(
        'Evaluation File',
        required=True
        )
    evaluation_fname = fields.Char(
        'Evaluation Filename',
        required=True,
        default='Imported Evaluation',
        )

    @api.multi
    def import_evaluation(self):
        active_model = self._context.get('active_model', False)
        active_id = self._context.get('active_id', False)
        evaluations = self.env['kinesis_athletics.evaluation']
        if active_model == 'res.partner':
            return evaluations.import_evaluation(self[0])
        elif active_model == 'kinesis_athletics.group':
            group = self.env['kinesis_athletics.group'].browse(active_id)
            return evaluations.import_evaluation(
                self[0], group=group)
        elif active_model == 'kinesis_athletics.evaluation':
            evaluation = self.env['kinesis_athletics.evaluation'].browse(
                active_id)
            return evaluations.import_evaluation(
                self[0], evaluation=evaluation)
        else:
            raise Warning(
                _('Active model different from partner, group or evaluation.'))
