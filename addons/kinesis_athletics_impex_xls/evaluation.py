# -*- coding: utf-8 -*-

from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
# from openerp import models, fields, api, _
class evaluation(osv.osv):
    """"""
    _name = 'kinesis_athletics.evaluation'
    _inherit = 'kinesis_athletics.evaluation'

    

    def generate_eval_xls(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        obj = self.browse(cr, uid, ids[0], context=context)
        datas = {}
    

        group = obj.group_id
        

        tests = [x.test_id.name for x in obj.evaluation_detail_ids]

        partner_information = [{'id': obj.partner_id.id, 'name': obj.partner_id.name}]
        print partner_information

        datas['partner_information'] =  partner_information
        datas['tests'] =  tests
        datas['group_name'] = group.name
        
        return self.pool['report'].get_action(cr, uid, [], 'kinesis_athletics_export_xls.groups_xls', data=datas, context=context)


