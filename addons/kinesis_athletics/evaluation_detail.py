# -*- coding: utf-8 -*-


import re
from openerp import netsvc
from openerp.osv import osv, fields

class evaluation_detail(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.evaluation_detail'
    _description = 'evaluation_detail'

    _columns = {
        'result': fields.float(string='Result'),
        'color': fields.integer(string='Color Index'),
        'test_selection_id': fields.many2one('kinesis_athletics.test_selection', string='Test Selection'),
        'evaluation_id': fields.many2one('kinesis_athletics.evaluation', string='Evaluation', ondelete='cascade', required=True), 
        'test_id': fields.many2one('kinesis_athletics.test', string='Test', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




evaluation_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
