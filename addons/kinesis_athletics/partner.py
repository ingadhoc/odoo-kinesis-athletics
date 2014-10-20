# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class partner(osv.osv):
    """"""
    
    _name = 'res.partner'
    _inherits = {  }
    _inherit = [ 'res.partner' ]

    _columns = {
        'evaluation_ids': fields.one2many('kinesis_athletics.evaluation', 'partner_id', string='Evaluation'), 
        'partner_group_ids': fields.many2many('kinesis_athletics.group', 'kinesis_athletics_partner_ids_partner_group_ids_rel', 'partner_id', 'group_id', string='Institution', context={'show_institutions':True}), 
    }

    _defaults = {
    }


    _constraints = [
    ]




partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
