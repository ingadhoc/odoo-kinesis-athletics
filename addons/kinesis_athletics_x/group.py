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
from datetime import date
from openerp.tools.translate import _

class group(osv.osv):
    """"""
    _inherit = 'kinesis_athletics.group'

    _columns = {
        'is_school': fields.related('company_id', 'company_type_id', 'is_school', type='boolean',
                                 relation='kinesis_athletics.company_type', string="Is School",
                                 readonly=True),
        'has_group': fields.related('company_id', 'has_group', type='boolean',
                                 relation='res.company', string="Has Group",
                                 readonly=True),
    }

    _defaults = {
        'year': date.today().year,
    }

    # No lo usamos por ahora porque vimos que trabajando desde cada cliente/compania no tiene mucho sentido
    # def name_get(self, cr, uid, ids, context=None):
    #     if not ids:
    #         return []
    #     if isinstance(ids, (int, long)):
    #                 ids = [ids]
    #     res = []
    #     for record in self.browse(cr, uid, ids, context=context):
    #         name= str(record.year)+' - '+ record.company_id.name+' - '+ record.name
    #         res.append((record['id'], name))
    #     return res


    def onchange_is_school(self, cr, uid, ids, company_id, context=None):
        v = {}

        if company_id:
            company_obj = self.pool.get('res.company')
            company = company_obj.browse(cr, uid, company_id, context=None)
            v['is_school'] = company.company_type_id.is_school
        else:
            v['is_school'] = False

        return {'value': v}


    def unlink(self, cr, uid, ids, context=None):
      for record in self.browse(cr, uid, ids, context=context):
        if record.partner_ids:
          raise osv.except_osv(_('Invalid Action!'), _('You cannot delete a group containing persons.'))
        else:
          return super(group, self).unlink(cr, uid, ids, context=context)


group()
