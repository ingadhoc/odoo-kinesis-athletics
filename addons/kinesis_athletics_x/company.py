# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields

class company(osv.osv):
    """"""

    _name = 'res.company'
    _inherit = 'res.company'

    _columns = {
    'groups_ids': fields.one2many('kinesis_athletics.group', 'company_id', string='Groups'),
    'active': fields.related('partner_id', 'active', relation='res.partner', type='boolean', string="Active"),
    }

    def _check_groups(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)

        if obj.has_group !=True:
            if obj.groups_ids:
                return False

        return True

    _constraints = [(_check_groups, 'Tiene cursos/areas cargadas', ['groups_ids'])
    ]

company()
