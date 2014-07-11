# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields


class test_range(osv.osv):
    """"""

    _name = 'kinesis_athletics.test_range'
    _inherit = 'kinesis_athletics.test_range'

    _defaults = {
        'to_age':100,
    }


    def _check_ranges(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        test_range_obj = self.pool['kinesis_athletics.test_range']
        test_range_ids = test_range_obj.search(cr, uid, [('test_id', '=',obj.test_id.id)], context=context)
        if obj.extreme_minimum < obj.val_min < obj.val_max < obj.extreme_maximum:
                    
            if len(test_range_ids) > 1:

                for record_id in test_range_ids :
                    record = self.browse(cr, uid, record_id, context=context)
                    if obj.val_min > obj.val_max:
                        return False

                    
                    if record.id != obj.id:
                        if obj.sex == record.sex or record.sex=='both' or obj.sex=='both':
                            if obj.from_age <= obj.to_age:
                                if obj.to_age < record.from_age:
                                    return True
                                else:
                                    if obj.from_age >= record.to_age:
                                        return True
                            return False
            return True


    _constraints = [(_check_ranges, 'Existen rangos en conflicto', ['val_min','extreme_minimum','val_max','extreme_maximum'])]


test_range()
