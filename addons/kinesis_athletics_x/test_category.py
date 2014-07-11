# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields


class test_category(osv.osv):
    """"""

    _name = 'kinesis_athletics.test_category'
    _inherit = 'kinesis_athletics.test_category'

    def _get_first_parent(self, cr, uid, ids, fields, args, context=None):
        res = {}
        first_parent_id = False
        test_category_obj = self.pool['kinesis_athletics.test_category']

        for test_category in self.browse(cr, uid, ids, context=context):
            parent_id = test_category.parent_id.id

            while parent_id:
                first_parent_id = parent_id
                parent = test_category_obj.browse(cr, uid, parent_id, context=None)
                parent_id = parent.parent_id.id

            res[test_category.id] = first_parent_id

        return res


    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        ids = set()
        if name:
            ids.update(self.search(cr, user, args + [('name',operator,name)], limit=(limit and (limit-len(ids)) or False) , context=context))
            ids = list(ids)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context=context)

        return result


    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
                    ids = [ids]
        if not context:
            context = {}

        res = []
        test_category_obj = self.pool['kinesis_athletics.test_category']
        range_domain = []
        test_category_ids = test_category_obj.search(cr, uid, range_domain, context=context)
        for record_id in test_category_ids:
            record = self.browse(cr, uid, record_id, context=context)
            parent_id = record.parent_id.id
            name = record.name
            while parent_id:
                parent_obj = self.browse(cr, uid, parent_id, context=context)
                name = parent_obj.name + ' / ' + name
                parent_id = parent_obj.parent_id.id
            res.append((record['id'], name))

        return res


    _columns = {
        'first_parent_id': fields.function(_get_first_parent, type='many2one', relation='kinesis_athletics.test_category', string='First Parent', method=True, store=True)
    }

test_category()
