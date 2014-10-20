# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class test_range(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.test_range'
    _description = 'test_range'

    _columns = {
        'from_age': fields.integer(string='From Age', required=True),
        'to_age': fields.integer(string='To Age', required=True),
        'sex': fields.selection([(u'F', u'Female'), (u'M', u'Male'), (u'both', u'M/F')], string='Gender', required=True),
        'val_max': fields.float(string='Maximum Value'),
        'val_min': fields.float(string='Minimum Value'),
        'extreme_minimum': fields.float(string='Extreme Minimum', required=True),
        'extreme_maximum': fields.float(string='Extreme Maximum', required=True),
        'test_id': fields.many2one('kinesis_athletics.test', string='test_id', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




test_range()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
