# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class test_category(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.test_category'
    _description = 'test_category'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'test_ids': fields.one2many('kinesis_athletics.test', 'test_category_id', string='Tests'), 
        'parent_id': fields.many2one('kinesis_athletics.test_category', string='Parent'), 
        'child_ids': fields.one2many('kinesis_athletics.test_category', 'parent_id', string='Childs'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




test_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
