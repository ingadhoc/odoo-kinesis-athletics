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
