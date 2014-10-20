# -*- coding: utf-8 -*-


import re
from openerp import netsvc
from openerp.osv import osv, fields

class company(osv.osv):
    """"""
    
    _name = 'res.company'
    _inherits = {  }
    _inherit = [ 'res.company' ]

    _columns = {
        'has_group': fields.boolean(string='Has Group'),
        'company_type_id': fields.many2one('kinesis_athletics.company_type', string='Company Type'), 
        'groups_ids': fields.one2many('kinesis_athletics.group', 'company_id', string='Groups'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




company()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
