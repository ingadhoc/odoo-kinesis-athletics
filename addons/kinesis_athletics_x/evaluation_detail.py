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


class evaluation_detail(osv.osv):
    """"""

    _name = 'kinesis_athletics.evaluation_detail'
    _inherit = 'kinesis_athletics.evaluation_detail'


    def _get_state (self, cr, uid, val_min, val_max, evaluation_detail, context=None):
        state=False
        if val_min and val_max:

            result = evaluation_detail.result
            if result > val_max:
                state=evaluation_detail.test_id.rating_over_maximum

            if result < val_min:
                state=evaluation_detail.test_id.rating_below_minimum

            if result >= val_min and result <= val_max:
                state='ideal'

        return state

    def get_test_description(self, cr, uid, ids, context=None):
        if context is None:
            context={}
        test_id = self.browse(cr, uid, ids[0], context).test_id.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kinesis_athletics.test',
            'view_mode': 'form',
            'res_id': test_id,
            'target': 'new'
        }

    def _get_test_statistics(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        test_obj = self.pool['kinesis_athletics.test']
        test_ids = test_obj.search(cr, uid, [('type','=','value')], context=context)

        for evaluation_detail in self.browse(cr, uid, ids, context=context):
            test = evaluation_detail.test_id

            evaluation = evaluation_detail.evaluation_id
            partner = evaluation_detail.evaluation_id.partner_id
            if evaluation.is_template!=True and partner:

                # Reference values
                ref_min, ref_max, ref_ext_max, ref_ext_min = test_obj._get_min_max(cr, uid, test.id, partner.id, context=context)
                state = self._get_state(cr, uid, ref_min, ref_max, evaluation_detail, context=context)

                # # Group values
                # group_min = group_max = False
                # group_results = test_obj._get_results(cr, uid, test.id, group_id=evaluation.group_id.id, context=context)
                # if group_results:
                #     group_min = min(group_results)
                #     group_max = max(group_results)
                #
                # # Level values
                # level_min = level_max = False
                # if evaluation.group_id.group_level_id:
                #     level_results = test_obj._get_results(cr, uid, test.id, level_id=evaluation.group_id.group_level_id.id, context=context)
                #     if level_results:
                #         level_min = min(level_results)
                #         level_max = max(level_results)

                # Age values
                age_range = (partner.age, partner.age)
                age_results = test_obj._get_results(cr, uid, test.id, age_range=age_range, context=context)
                age_avg = False
                if age_results:
                    age_avg = sum(age_results) / len(age_results)


                res[evaluation_detail.id] = {
                    # 'ref_min': ref_min,
                    # 'ref_max': ref_max,
                    # 'group_min': group_min,
                    # 'group_max': group_max,
                    # 'level_min': level_min,
                    # 'level_max': level_max,
                    # 'age_min': age_min,
                    # 'age_max': age_max,
                    'age_avg': age_avg,
                    'state': state,
                }
            else:
                res[evaluation_detail.id] = {}

        return res

    def _get_plotbands_values(self, cr, uid, ids, fields, arg, context=None):
      res = {}
      test_range_obj = self.pool['kinesis_athletics.test_range']
      test_obj = self.pool['kinesis_athletics.test']

      plotband_ext_min = False
      plotband_val_min = False
      plotband_val_max = False
      plotband_ext_max = False

      for evaluation_detail in self.browse(cr, uid, ids, context=context):
        test = evaluation_detail.test_id
        partner = evaluation_detail.evaluation_id.partner_id
        test_range_ids = test_range_obj.search(cr, uid, [('test_id', '=', test.id)], context=context)
        if test_range_ids and partner:
          plotband_val_min, plotband_val_max, plotband_ext_max, plotband_ext_min = test_obj._get_min_max(cr, uid, test.id, partner.id, context=None)

          res[evaluation_detail.id] = {
            'plotband_val_min': plotband_val_min,
            'plotband_val_max': plotband_val_max,
            'plotband_ext_max': plotband_ext_max,
            'plotband_ext_min': plotband_ext_min,
          }

        else:
          res[evaluation_detail.id] = {}

      return res

    # def onchange_is_school(self, cr, uid, ids, institution_id, context=None):
    #     v = {}

    #     if institution_id:
    #         institution_obj = self.pool.get('res.partner')
    #         institution = institution_obj.browse(cr, uid, institution_id, context=None)
    #         v['is_school'] = institution.institution_subtype_id.is_school
    #     else:
    #         v['is_school'] = False

    #     return {'value': v}

    _columns = {
        'partner_id': fields.related('evaluation_id', 'partner_id', relation='res.partner', type='many2one', string='Partner', readonly=True,),
        'uom_id': fields.related('test_id', 'uom_id', type='many2one',
                                 relation='product.uom', string="Unit",
                                 readonly=True),
        # 'ref_min': fields.function(_get_test_statistics,
        #                             type='float',
        #                             string='Reference Minimum Value',
        #                             method=True,
        #                             store=True,
        #                             multi='min_max'),
        # 'ref_max': fields.function(_get_test_statistics,
        #                             type='float',
        #                             string='Reference Maximum Value',
        #                             method=True,
        #                             store=True,
        #                             multi='min_max'),
        # 'group_min': fields.function(_get_test_statistics,
        #                             type='float',
        #                             string='Group Minimum',
        #                             method=True,
        #                             store=True,
        #                             multi='min_max'),
        # 'group_max': fields.function(_get_test_statistics, type='float', string='Group Maximum', multi='min_max'),
        # 'level_min': fields.function(_get_test_statistics, type='float', string='Level Minimum', multi='min_max'),
        # 'level_max': fields.function(_get_test_statistics, type='float', string='Level Maximum', multi='min_max'),
        # 'age_min': fields.function(_get_test_statistics, type='float', string='Age Minimum', multi='min_max'),
        # 'age_max': fields.function(_get_test_statistics, type='float', string='Age Maximum', multi='min_max'),
        'age_avg': fields.function(_get_test_statistics, type='float', string='Age Average', multi='min_max'),
        'plotband_ext_min': fields.function(_get_plotbands_values, type="float", string="ext_min", multi='plotband_values'),
        'plotband_val_min': fields.function(_get_plotbands_values, type="float", string="val_min", multi='plotband_values'),
        'plotband_val_max': fields.function(_get_plotbands_values, type="float", string="val_max", multi='plotband_values'),
        'plotband_ext_max': fields.function(_get_plotbands_values, type="float", string="ext_max", multi='plotband_values'),
        'rating_below_minimum': fields.related('test_id', 'rating_below_minimum',type='selection', selection=[('alert', 'Alert'), ('ideal', 'Ideal'), ('superior', 'Superior')], string='rating_below_minimum'),
        'rating_over_maximum': fields.related('test_id', 'rating_over_maximum',type='selection', selection=[('alert', 'Alert'), ('ideal', 'Ideal'), ('superior', 'Superior')], string='rating_over_maximum'),
        'state': fields.function(_get_test_statistics,
                                    type='selection',
                                    string='State',
                                    selection=[('alert', 'Alert'), ('ideal', 'Ideal'), ('superior', 'Superior')],
                                    method=True,
                                    store=True,
                                    multi='min_max'),
        'test_type': fields.related('test_id', 'type',
                                    type='selection',
                                    selection=[(u'value', 'value'), (u'selection', 'selection')],
                                    string="Test Type",
                                    readonly=True
                                    ),
        'test_description': fields.related('test_id', 'description',
                                    type='char',
                                    string="Test Description",
                                    readonly=True
                                    ),
        'first_parent_id': fields.related('test_id', 'test_category_id', 'first_parent_id', relation='kinesis_athletics.test_category', type='many2one', string='Test Class', readonly=True, store=True),
    }

    def onchange_test_id(self, cr, uid, ids, test_id, context=None):
        v = {}

        if test_id:
            test_obj = self.pool.get('kinesis_athletics.test')
            test = test_obj.browse(cr, uid, test_id, context=None)
            v['uom_id'] = test.uom_id.id
            v['test_type']=test.type

        else:
            v['test_type']=False
            v['uom_id'] = False

        return {'value': v}


    def _check_result(self, cr, uid, ids, context=None):
      obj = self.browse(cr, uid, ids[0], context=context)
      if obj.test_id.has_range:
        if obj.result < obj.plotband_ext_min or obj.result > obj.plotband_ext_max:
          return False
        else:
          return True


    _constraints = [(_check_result, 'Result out of range', ['result'])]


evaluation_detail()
