# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields
from datetime import date
from openerp.tools.translate import _


class group(osv.osv):
    """"""
    _inherit = 'kinesis_athletics.group'

    _columns = {
        'is_school': fields.related('company_id', 'company_type_id', 'is_school', type='boolean', relation='kinesis_athletics.company_type', string="Is School", readonly=True),
        'has_group': fields.related('company_id', 'has_group', type='boolean', relation='res.company', string="Has Group", readonly=True),
    }

    _defaults = {
        'year': date.today().year,
    }


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
