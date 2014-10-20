# -*- coding: utf-8 -*-


import re
from openerp import netsvc
from openerp.osv import osv, fields

class group(osv.osv):
    """Kinesis Groups"""
    
    _name = 'kinesis_athletics.group'
    _description = 'Kinesis Groups'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'year': fields.integer(string='Year', required=True),
        'new_year_group_id': fields.many2one('kinesis_athletics.group', string='Escalte Group'),
        'partner_ids': fields.many2many('res.partner', 'kinesis_athletics_partner_ids_partner_group_ids_rel', 'group_id', 'partner_id', string='Members', context={'default_is_company':False,'is_person':True,'show_actual_group':False}, domain=[('is_company','=', False)]), 
        'group_level_id': fields.many2one('kinesis_athletics.level', string='Level'), 
        'company_id': fields.many2one('res.company', string='Company', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




group()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
