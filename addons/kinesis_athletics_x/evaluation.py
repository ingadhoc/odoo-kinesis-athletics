# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields
from openerp import models, api
from openerp import fields as fields_new
from openerp.tools.translate import _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare


class evaluation(models.Model):
    """"""

    _inherit = 'kinesis_athletics.evaluation'
    _rec_name = 'complete_name'

    @api.one
    @api.depends('template_id', 'name')
    def _complete_name(self):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        if self.template_id.name:
            self.complete_name = self.template_id.name
        else:
            self.complete_name = self.name

    @api.one
    @api.depends('company_id', 'date')
    def _calc_date(self):
        if self.date:
            eval_year_id=(datetime.strptime(self.date, '%Y-%m-%d')).date()
            self.eval_year= eval_year_id.year
        else:
            self.eval_year = False
        

    eval_year = fields_new.Integer(
        compute='_calc_date',
        string="Year",
        store=True)
    complete_name = fields_new.Char(
        compute='_complete_name',
        string="Name",
        store=True)

    def _get_partner_age(self, cr, uid, ids, name, arg, context=None):
        res = {}

        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.partner_id.age

        return res


    _columns = {
        'age': fields.function(_get_partner_age, type='integer', string="Age", store=True),
        'evaluation_detail_value_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Values', domain=[('test_type','=','value')], readonly=True),
        'evaluation_detail_selection_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Selections', domain=[('test_type','=','selection')], readonly=True),
        'use_groups':fields.related('company_id','use_groups',relation='res.company', type='boolean', string='Use Group', store=True),
        #we overwrite this field because in v8 o2m fields has copy=False by default and copy is not implemented on xmi2oerp
        'evaluation_detail_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Evaluation Details', required=True, copy=True),
    }

    _order = 'date desc'



    def copy(self, cr, uid, id, default, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}

        default['user_id'] = uid

        if not default.get("partner_id", False):
            default['partner_id'] = False
        res = super(evaluation, self).copy(cr, uid, id, default=default, context=None)
        return res


    def on_change_group(self, cr, uid, ids, group_id, context=None):
        v = {}
        if context is None:
            context = {}
        partner_list = []
        domain_dic = {}
        if group_id:
            group_obj = self.pool['kinesis_athletics.group']
            group = group_obj.browse(cr, uid, group_id, context=context)

            for partner in group.partner_ids:
                partner_list.append(partner.id)
            domain_dic['partner_id'] = [('id','in',partner_list)]

        v['partner_id'] = False

        return {
            'value': v,
            'domain': domain_dic,
        }


    def on_change_company(self, cr, uid, ids, company_id, context=None):
        v = {}

        if context is None:
            context = {}
        if company_id:
            company_obj = self.pool['res.company']
            company = company_obj.browse(cr, uid, company_id, context=context)
            v['use_groups'] = company.use_groups
        v['group_id'] = False
        v['partner_id'] = False

        return {
            'value': v,

        }


    def new_evaluation(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        new_evaluations = []

        for i in ids:
            context.update({'copy':True})
            current_evaluation = self.browse(cr, uid, i, context=context)
            if current_evaluation.is_template:
              new_id = self.copy(cr, uid, i, default = {
                                                  'date': datetime.today(),
                                                  'template_id':i,
                                                  'is_template':False,
                                                  }, context=context)
            else:
              new_id = self.copy(cr, uid, i, default = {
                                'date': datetime.today(),
                                'partner_id': current_evaluation.partner_id.id,
                                'group_id': current_evaluation.partner_id.actual_group_id.id,
                                  }, context=context)

              for evaluation_detail in self.browse(cr, uid, new_id, context=context).evaluation_detail_ids:
                evaluation_detail.write({'result': False})
                evaluation_detail.write({'test_selection_id': False})

        return {
            'name': _('Evaluation'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'kinesis_athletics.evaluation',
            'view_id': False,
            'res_id': new_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True
        }


    def _check_person(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.group_id.partner_ids and obj.partner_id:
            if obj.partner_id in obj.group_id.partner_ids:
                return True
            else:
                return False
        return True

    _constraints = [(_check_person, '', ['partner_id'])]
