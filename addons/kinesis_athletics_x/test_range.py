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
    _inherit = 'kinesis_athletics.test_range'

    _columns = {
        
    }

    _defaults = {
        'to_age':100,
    }
    
       

        
        

    def _check_ranges(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        test_range_obj = self.pool['kinesis_athletics.test_range']
        test_range_ids = test_range_obj.search(cr, uid, [('test_id', '=',obj.test_id.id)], context=context)
        print test_range_ids
        if len(test_range_ids) > 1:
            for record_id in test_range_ids :
                record = self.browse(cr, uid, record_id, context=context)
                # Verfica que el valor min no supere al max
                if obj.val_min > obj.val_max:
                    
                    return False
                if record.id != obj.id:
                    if obj.sex == record.sex or record.sex=='both' or obj.sex=='both':
                        if obj.from_age <= obj.to_age:
                            if obj.to_age < record.from_age:
                                return True
                            else:
                                if obj.from_age >= record.to_age:
                                    return True

                       
                        return False
             
        return True
    _constraints = [(_check_ranges, 'Existen rangos en conflicto', ['test_range_ids'])
    ]
test_range()