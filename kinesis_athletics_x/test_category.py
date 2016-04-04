# -*- coding: utf-8 -*-

from openerp import models, api, fields


class test_category(models.Model):
    """"""

    _inherit = 'kinesis_athletics.test_category'

    @api.one
    @api.depends('parent_id', 'parent_id.parent_id')
    def _get_first_parent(self):
        first_parent_id = False
        parent = self.parent_id

        while parent:
            first_parent_id = parent.id
            parent = parent.parent_id

        self.first_parent_id = first_parent_id

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    first_parent_id = fields.Many2one(
        'kinesis_athletics.test_category',
        compute='_get_first_parent',
        string='First Parent',
        store=True)
