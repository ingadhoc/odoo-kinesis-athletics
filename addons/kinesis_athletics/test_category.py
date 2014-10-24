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
