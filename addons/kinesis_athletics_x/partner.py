# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields
from datetime import date


class partner(osv.osv):
    """"""

    _name = 'res.partner'
    _inherit = 'res.partner'


    def _get_actual_group(self, cr, uid, ids, fields, args, context=None):
        res = {}
        actual_year = date.today().year


        for partner in self.browse(cr, uid, ids, context=context):
            if partner.partner_group_ids:
                if partner.company_name=='Empresa':
                    for group in partner.partner_group_ids:
                        res[partner.id] = group.id
                else:
                    for group in partner.partner_group_ids:
                        if group.year == actual_year:
                            res[partner.id] = group.id

        return res
    def _evaluation_count(self, cr, uid, ids, field_name, arg, context=None):
        res ={}
        # the user may not have access rights for opportunities or meetings
        
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = len(partner.evaluation_ids)
            
        print res[partner.id]
        # except:
        #     pass
        # for partner in self.browse(cr, uid, ids, context):
        #     res[partner_id] = len(partner.evaluation_ids)
        return res

    _columns = {
        'actual_group': fields.function(_get_actual_group, type='many2one', relation='kinesis_athletics.group', string='Actual Group', store=True),
        'has_group':fields.related('company_id','has_group',relation='res.company', type='boolean', string='Has Group', store=True),
        'company_name':fields.related('company_id','company_type_id','name',relation='kinesis_athletics.company_type', type='char', string='Company name', store=True),
        'eval_count': fields.function(_evaluation_count, type="integer"),  
    }


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
            v['has_group']=company.has_group

        return {'value': v,}


    _constraints = [(_check_person_group, 'Ya pertenece a un curso este año', ['partner_group_ids'])
    ]

partner()
