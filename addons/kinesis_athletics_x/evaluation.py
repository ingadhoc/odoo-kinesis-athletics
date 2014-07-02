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


import re
from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class evaluation(osv.osv):
    """"""

    _inherit = 'kinesis_athletics.evaluation'
    _rec_name = 'complete_name'

# TODO ver si usamos name_search y name_get o no!
    # def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     ids = set()
    #     if name:
    #         ids.update(self.search(cr, user, args + [('partner_id.name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
    #         # if not limit or len(ids) < limit:
    #             # ids.update(self.search(cr, user, args + [('authorization_type_id.name',operator,name)], limit=limit, context=context))
    #         ids = list(ids)
    #     else:
    #         ids = self.search(cr, user, args, limit=limit, context=context)
    #     result = self.name_get(cr, user, ids, context=context)
    #     return result


    # def name_get(self, cr, uid, ids, context=None):
    #     if not ids:
    #         return []
    #     if isinstance(ids, (int, long)):
    #                 ids = [ids]
    #     if not context:
    #         context = {}
    #     lang = context.get('lang','en_US')
    #     lang_obj = self.pool.get('res.lang')
    #     lang_ids = lang_obj.search(cr, uid, [('code','=',lang)], context=context)
    #     lang_read = lang_obj.read(cr, uid, lang_ids, ['date_format'], context=context)
    #     if lang_read:
    #         date_format = lang_read[0]['date_format']

    #     # date_format = lang_obj.search_read(cr, uid, domain=[('code','=',lang)], fields=['date_format'], context=context)
    #     # print 'date_format', date_format
    #     res = []
    #     for record in self.browse(cr, uid, ids, context=context):
    #     # for record_id in ids:
    #     #     record_id = self.search(cr, uid, [('id','=', record_id)], context=context)
    #     #     record = self.browse(cr, uid, record_id, context=context)
    #         name = ''
    #         if record.is_template:
    #             name += record.template_name or ''
    #         else:
    #             if record.date:
    #                 date = datetime.strptime(record.date,DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
    #                 name += date
    #             if record.partner_id:
    #                 name = record.partner_id.name + ' - ' + name
    #             if record.template_id:
    #                 name = record.template_id.template_name + ' - ' + name
    #         res.append((record['id'], name))
    #     return res

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child location.
        @return: Dictionary of values
        """
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.is_template:
                name = record.name
            else:
                name = record.template_id.name
            res[record.id] = name
        return res

    _columns = {
        'complete_name': fields.function(_complete_name, type='char', string="Name", store=True,),
        # 'evaluation_detail_value_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Values', domain=[('test_type','=','value'),('result','!=',0.0)], readonly=True),
        'evaluation_detail_value_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Values', domain=[('test_type','=','value')], readonly=True),
        # 'evaluation_detail_selection_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Selections', domain=[('test_type','=','selection'),('test_selection_id','!=',False)], readonly=True),
        'evaluation_detail_selection_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Selections', domain=[('test_type','=','selection')], readonly=True),
        'has_group':fields.related('company_id','has_group',relation='res.company', type='boolean', string='Has Group', store=True),
    }

    _defaults = {
    }

    _order = 'date desc'


    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}

        default['evaluation_ids'] = []
        default['user_id'] = uid
        if not default.get("partner_id", False):
            default['partner_id'] = False

        # evaluation_rec = self.browse(cr, uid, id, context=context)
        # # if not default.get('template_name', False):
        # #     default.update(template_name=_("%s (copy)") % (evaluation_rec.template_name))
        res = super(evaluation, self).copy(cr, uid, id, default, context)
        return res

    def on_change_group(self, cr, uid, ids, group_id, context=None):
        v = {}
        if context is None:
            context = {}
        if group_id:
            group_obj = self.pool['kinesis_athletics.group']
            group = group_obj.browse(cr, uid, group_id, context=context)
            partner_list=[]


            for partner in group.partner_ids:
                partner_list.append(partner.id)

            v['partner_id']=False
        return {
            'value': v,
            'domain':
                {'partner_id':[('id','in',partner_list)]}
        }

    def on_change_company(self, cr, uid, ids, company_id, context=None):
        v = {}

        if context is None:
            context = {}
        if company_id:
            company_obj = self.pool['res.company']
            company = company_obj.browse(cr, uid, company_id, context=context)
            v['has_group']=company.has_group



        return {
            'value': v,

        }
    def new_evaluation(self, cr, uid, ids, context=None):
        if context is None:
            context={}
        new_evaluations = []
        for i in ids:
            context.update({'copy':True})
            current_evaluation = self.browse(cr, uid, i, context=context)
            if current_evaluation.is_template:
              new_id = self.copy(cr, uid, i, default = {
                                                  'template_id':i,
                                                  'is_template':False,
                                                  }, context=context)
            else:
              new_id = self.copy(cr, uid, i, default = {
                                'date': datetime.today(),
                                'partner_id': current_evaluation.partner_id.id,
                                'group_id': current_evaluation.partner_id.actual_group.id,
                                  }, context=context)
              evaluation_detail_ids = self.browse(cr, uid, new_id, context=context).evaluation_detail_ids

              for evaluation_detail in evaluation_detail_ids:
                evaluation_detail.write({'result': False}, context=context)

            new_evaluations.append(new_id)
        return {
            'name': _('Evaluation'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'kinesis_athletics.evaluation',
            'view_id': False,
            'res_id': new_evaluations[0],
            # 'views': [(form_view['res_id'],'form'),(tree_view['res_id'],'tree')],
            'type': 'ir.actions.act_window',
            # 'search_view_id': search_view['res_id'],
            'nodestroy': True
        }
    # def _check_company(self, cr, uid, ids, context=None):
    #     obj = self.browse(cr, uid, ids[0], context=context)
    #     if obj.company_id == obj.group_id.company_id or not obj.group_id:
    #         return True
    #     else:
    #         return False
    def _check_person(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        if obj.group_id.partner_ids and obj.partner_id:
            if obj.partner_id in obj.group_id.partner_ids:
                return True
            else:
                return False
        return True

    _constraints = [
         (_check_person, '', ['partner_id'])
    ]
