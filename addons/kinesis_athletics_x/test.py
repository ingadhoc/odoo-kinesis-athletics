# -*- coding: utf-8 -*-
##############################################################################
#
#    kinesis_athletics
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
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from datetime import datetime
import pdb

class test(osv.osv):
    """"""

    _inherit = 'kinesis_athletics.test'

    _columns = {
        # 'ref_result': fields.function(_get_results,
        #                             type='float',
        #                             string='Reference Minimum Value',
        #                             method=True,
        #                             multi='min_max'),
    }

    _defaults = {
    }
    def onchange_type(self, cr, uid, ids, type, context=None):
        v = {}

        if type=='selection':
            has_range = False
            v['has_range'] = False


        return {'value': v}



    def name_get(self, cr, uid, ids, context=None):

        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','uom_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['uom_id']:
                name = name +' ('+record['uom_id'][1]+')'
            res.append((record['id'], name))
        return res

    def _get_min_max(self, cr, uid, test_id, partner_id, context=None):
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        partner_age = partner.age
        partner_sex = partner.sex
        test_range_obj = self.pool.get('kinesis_athletics.test_range')
        val_min = False
        val_max = False
        extreme_maximum = False
        extreme_minimum = False
        if partner_age:
            range_domain = [('test_id', '=', test_id),('from_age', '<=', partner_age), ('to_age', '>=', partner_age)]
            # range_domain = [('test_id', '=', test_id), ()]
            range_domain.append(('sex', '=', 'both'))
            test_range_ids = test_range_obj.search(cr, uid, range_domain, context=context)
            if not test_range_ids:
                range_domain.remove(('sex', '=', 'both'))
                range_domain.append(('sex', '=', partner_sex))
                test_range_ids = test_range_obj.search(cr, uid, range_domain, context=context)
            if test_range_ids:
                test_range = test_range_obj.browse(cr, uid, test_range_ids[0], context=context)
                val_min = test_range.val_min
                val_max = test_range.val_max
                extreme_minimum = test_range.extreme_minimum
                extreme_maximum = test_range.extreme_maximum
        return (val_min, val_max, extreme_maximum, extreme_minimum)

    def _get_results(self, cr, uid, test_id, partner_id=False, group_id=False, level_id=False, age_range=None, company_id=False, context=None):

        """Devuelve para un test y segun los parametros, un listado de resultados de ese test
            Parametros (obligatorios):
            -test_id
            Parametros (opcionales):
            -group_id
            -level_id
            -age_range: tupla de valores enteros de minimo y maximmo de edad
            -company_id
        """
        if age_range:
            (age_from, age_to) = age_range
        else:
            (age_from, age_to) = False, False

        evaluation_detail_obj = self.pool['kinesis_athletics.evaluation_detail']
        domain = []
        if partner_id:
            domain.append(('evaluation_id.partner_id','=',partner_id))
        if test_id:
            domain.append(('test_id','=',test_id))
        # if group_id:
        #     domain.append(('evaluation_id.group_id','=',group_id))
        # if level_id:
        #   domain.append(('evaluation_id.group_id.group_level_id','=',level_id))
        if age_from and age_to:
          domain.append(('evaluation_id.age', '>=', age_from))
          domain.append(('evaluation_id.age', '<=', age_to))
            # today = datetime.strptime(time.strftime(DEFAULT_SERVER_DATE_FORMAT), DEFAULT_SERVER_DATE_FORMAT)
            # date_from = today - relativedelta(years=age_to + 1 or 0)
            # date_to = today - relativedelta(years=age_from or 0)
            # domain.append(('evaluation_id.partner_id.birthdate','>=',date_from))
            # domain.append(('evaluation_id.partner_id.birthdate','<=',date_to))
        evaluation_detail_ids = evaluation_detail_obj.search(cr, uid, domain, context=context)
        results = []
        for evaluation_detail in evaluation_detail_obj.browse(cr, uid, evaluation_detail_ids, context=context):
            results.append(evaluation_detail.result)
        return results

    _constraints = [
    ]
