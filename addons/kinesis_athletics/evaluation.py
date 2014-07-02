# -*- coding: utf-8 -*-
##############################################################################
#
#    Kinesis Athletics
#    Copyright (C) 2014 Ingenieria Adhoc
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
from openerp import netsvc
from openerp.osv import osv, fields

class evaluation(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.evaluation'
    _description = 'evaluation'

    _columns = {
        'date': fields.date(string='Date'),
        'note': fields.text(string='Note'),
        'is_template': fields.boolean(string='Is Template?'),
        'name': fields.char(string='Name'),
        'group_id': fields.many2one('kinesis_athletics.group', string='Group'),
        'user_id': fields.many2one('res.users', string='User'),
        'company_id': fields.many2one('res.company', string='Company'),
        'evaluation_detail_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'evaluation_id', string='Evaluation Details', required=True), 
        'partner_id': fields.many2one('res.partner', string='Person', context={'default_is_company':False,'is_person':True}, domain=[('is_company','=',False),('is_company','=', False)]), 
        'evaluation_ids': fields.one2many('kinesis_athletics.evaluation', 'template_id', string='Evaluations', domain=[('is_template', '=', False)]), 
        'template_id': fields.many2one('kinesis_athletics.evaluation', string='Template', readonly=True, context={'default_is_template': True}, domain=[('is_template', '=', True)]), 
    }

    _defaults = {
        'date': fields.date.context_today,
        'user_id': lambda s, cr, u, c: u,
        'company_id': lambda s, cr, u, c: s.pool.get('res.users').browse(cr, u, u, c).company_id.id,
    }


    _constraints = [
    ]




evaluation()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
