# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date


class partner(models.Model):

    """"""

    _inherit = 'res.partner'

    @api.one
    @api.depends('partner_group_ids', 'partner_group_ids.year')
    def _get_actual_group(self):
        """
        Checks if the partner is in a group for the actual year and stores the
        actual group.
        """
        actual_year = date.today().year
        group_ids = self.env['kinesis_athletics.group'].search(
            [('year', '=', actual_year), ('partner_ids', '=', self.id)])
        self.actual_group_id = group_ids and group_ids[0].id or False
    @api.one
    def _evaluation_count(self):
        """
        Counts the number of evaluations the partner has, used for smart button
        """
        self.eval_count = len(self.sudo().evaluation_ids)

    actual_group_id = fields.Many2one(
        'kinesis_athletics.group',
        string='Actual Group',
        compute='_get_actual_group')
    use_groups = fields.Boolean(
        related='company_id.use_groups',
        string='Use Group',
        store=True)
    company_name = fields.Char(
        related='company_id.company_type_id.name',
        string='Company Name',
        store=True)
    eval_count = fields.Integer(compute='_evaluation_count')

    def _check_person_group(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if len(obj.partner_group_ids) >= 2:
            if obj.partner_group_ids[0].year == obj.partner_group_ids[1].year:
                return False
            else:
                return True
        else:
            return True

    def on_change_company(self, cr, uid, ids, company_id, context=None):
        v = {}

        if context is None:
            context = {}
        if company_id:
            company_obj = self.pool.get('res.company')
            company = company_obj.browse(cr, uid, company_id, context=context)
            v['use_groups'] = company.use_groups

        return {'value': v, }

    _constraints = [(_check_person_group, 'Ya pertenece a un curso este año', ['partner_group_ids'])
                    ]
