# -*- coding: utf-8 -*-
import re
from openerp import netsvc
from openerp.osv import osv, fields

class test_selection(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.test_selection'
    _description = 'test_selection'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'image': fields.binary(string='Image'),
        'test_id': fields.many2one('kinesis_athletics.test', string='', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




test_selection()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
