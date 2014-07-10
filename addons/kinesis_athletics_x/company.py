# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class company(models.Model):
    """"""

    _name = 'res.company'
    _inherit = 'res.company'

    groups_ids = fields.One2many('kinesis_athletics.group', 'company_id', string='Groups')
    active = fields.Boolean(related='partner_id.active', string="Active")

    def _check_groups(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)

        if obj.has_group !=True:
            if obj.groups_ids:
                return False

        return True

    _constraints = [(_check_groups, 'Tiene cursos/areas cargadas', ['groups_ids'])
    ]

company()
