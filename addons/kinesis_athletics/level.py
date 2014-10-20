# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class level(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.level'
    _description = 'level'

    _columns = {
        'name': fields.char(string='name'),
        'group_ids': fields.one2many('kinesis_athletics.group', 'group_level_id', string='Group'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




level()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
