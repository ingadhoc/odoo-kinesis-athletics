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

class test(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.test'
    _description = 'test'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'description': fields.char(string='Description'),
        'uom_id': fields.many2one('product.uom', string='Unit'),
        'image': fields.binary(string='Image'),
        'measure_description': fields.text(string='Measure Description'),
        'has_range': fields.boolean(string='Has Range'),
        'type': fields.selection([(u'value', u'Value'), (u'selection', u'Selection')], string='type', required=True),
        'rating_below_minimum': fields.selection([(u'alert', u'Alert'), (u'ideal', u'Ideal'), (u'superior', u'Superior'), (u'none', u'None')], string='Rating Below Minimum', required=True),
        'rating_over_maximum': fields.selection([(u'alert', u'Alert'), (u'ideal', u'Ideal'), (u'superior', u'Superior'), (u'none', u'None')], string='Rating Over Maximum', required=True),
        'invert': fields.boolean(string='Invert'),
        'rating_between': fields.selection([(u'alert', u'Alert'), (u'ideal', u'Ideal'), (u'superior', u'Superior'), (u'none', u'None')], string='Rating Between', required=True),
        'test_category_id': fields.many2one('kinesis_athletics.test_category', string='Category', required=True), 
        'evaluation_detail_ids': fields.one2many('kinesis_athletics.evaluation_detail', 'test_id', string='Evaluation Details'), 
        'test_range_ids': fields.one2many('kinesis_athletics.test_range', 'test_id', string='test_range_ids'), 
        'test_selection_ids': fields.one2many('kinesis_athletics.test_selection', 'test_id', string='Test Selections'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
