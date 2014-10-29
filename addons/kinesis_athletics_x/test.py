# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time
from datetime import datetime


class test(models.Model):
    """"""

    _inherit = 'kinesis_athletics.test'


    def onchange_type(self, cr, uid, ids, type, context=None):
        v = {}

        if type=='selection':
            has_range = False
            v['has_range'] = False

        return {'value': v}


    def on_change_has_range(self, cr, uid, ids, has_range, context=None):
        v = {}

        if not has_range:
            v['rating_below_minimum'] = 'none'
            v['rating_between'] = 'none'
            v['rating_over_maximum'] = 'none'

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
        """"""
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

        if age_from and age_to:
          domain.append(('evaluation_id.age', '>=', age_from))
          domain.append(('evaluation_id.age', '<=', age_to))

        evaluation_detail_ids = evaluation_detail_obj.search(cr, uid, domain, context=context)
        results = []

        for evaluation_detail in evaluation_detail_obj.browse(cr, uid, evaluation_detail_ids, context=context):
            results.append(evaluation_detail.result)

        return results


    _defaults = {
        'rating_below_minimum': 'none',
        'rating_between': 'none',
        'rating_over_maximum': 'none',
    }
