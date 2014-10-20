# -*- coding: utf-8 -*-


import re
from openerp import netsvc
from openerp.osv import osv, fields

class company_type(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.company_type'
    _description = 'company_type'

    _columns = {
        'name': fields.char(string='name', required=True),
        'is_school': fields.boolean(string='Is school'),
        'company_id': fields.one2many('res.company', 'company_type_id', string='company_id'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




company_type()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
