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

class test_range(osv.osv):
    """"""
    
    _name = 'kinesis_athletics.test_range'
    _description = 'test_range'

    _columns = {
        'from_age': fields.integer(string='From Age', required=True),
        'to_age': fields.integer(string='To Age', required=True),
        'sex': fields.selection([(u'F', u'Female'), (u'M', u'Male'), (u'both', u'M/F')], string='Gender', required=True),
        'val_max': fields.float(string='Maximum Value', digits=(4, 2)),
        'val_min': fields.float(string='Minimum Value', digits=(4, 2)),
        'extreme_minimum': fields.float(string='Extreme Minimum', required=True, digits=(4, 2)),
        'extreme_maximum': fields.float(string='Extreme Maximum', required=True, digits=(4, 2)),
        'test_id': fields.many2one('kinesis_athletics.test', string='test_id', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




test_range()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
