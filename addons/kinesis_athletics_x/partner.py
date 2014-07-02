# -*- coding: utf-8 -*-
##############################################################################
#
#    Kinesis Athletics
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
              # else:
              #   res[partner.id] = 0
        # res[partner.id] = 0
      return res

    _columns = {
        'actual_group': fields.function(_get_actual_group, type='many2one', relation='kinesis_athletics.group', string='Actual Group', store=True),
        'has_group':fields.related('company_id','has_group',relation='res.company', type='boolean', string='Has Group', store=True),
        'company_name':fields.related('company_id','company_type_id','name',relation='kinesis_athletics.company_type', type='char', string='Company name', store=True),
    }
    

    _defaults = {
    }
    def _check_person_group(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        # print obj.partner_group_ids[1]
        # print obj.partner_group_ids[0]
        if len(obj.partner_group_ids) >= 2:
          if obj.partner_group_ids[0].year == obj.partner_group_ids[1].year:
                return False
          else:
              return True
        else:
          return True
                
                          
        # return True

    def on_change_company(self, cr, uid, ids, company_id, context=None):
        v = {}

        if context is None:
            context = {}
        if company_id:
            company_obj = self.pool.get('res.company')
            company = company_obj.browse(cr, uid, company_id, context=context)
            v['has_group']=company.has_group



        return {
            'value': v,

        }


    _constraints = [(_check_person_group, 'Ya pertenece a un curso este año', ['partner_group_ids'])
    ]




partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
