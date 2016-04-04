# -*- coding: utf-8 -*-
from openerp import models, fields


class company(models.Model):
    """"""

    _inherit = 'res.company'

    groups_ids = fields.One2many(
        'kinesis_athletics.group', 'company_id', string='Groups')
