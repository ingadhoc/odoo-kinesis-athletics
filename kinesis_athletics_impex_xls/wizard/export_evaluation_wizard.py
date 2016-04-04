# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _

class kinesis_athletics_group_evaluation_export_wizard(osv.osv_memory):
    _name = 'export.evaluation.wizard'
    _description = _('Wizard to export XLS evaluations for Kinesis groups')

    _columns = {     
        'template_id': fields.many2one('kinesis_athletics.evaluation', string='Template', context={'default_is_template': True}, domain=[('is_template', '=', True)], required=True), 
    }

    def generate_xls(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)[0]
        if context is None:
            context = {}
        datas = {}
        
        active_id = context.get('active_id', False)
        if not active_id:
            return {'type': 'ir.actions.act_window_close'}

        group = self.pool['kinesis_athletics.group'].browse(cr, uid, active_id, context=context)
        tests = [x.test_id.name for x in wizard.template_id.evaluation_detail_ids]

        partner_information = [{'id': partner.id, 'name': partner.name} for partner in group.partner_ids]

        datas['partner_information'] =  partner_information
        datas['tests'] =  tests
        datas['group_name'] = group.name
        datas['template_id'] = wizard.template_id.id

        return self.pool['report'].get_action(cr, uid, [], 'kinesis_athletics_export_xls.groups_xls', data=datas, context=context)
    
    
