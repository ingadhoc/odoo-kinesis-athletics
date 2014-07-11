# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class kinesis_athletics_group_evaluation_export_wizard(osv.osv_memory):
    _name = 'kinesis_athletics.group_evaluation_export_wizard'
    _description = 'Wizard to XLS for evalution import with Aeroo Reports'


    _columns = {     
        'template_id': fields.many2one('kinesis_athletics.evaluation', string='Template', context={'default_is_template': True}, domain=[('is_template', '=', True)], required=True), 
    }

    _defaults = {
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

        partner_information = [(partner.id, partner.name) for partner in group.partner_ids]

        datas['partner_information'] =  partner_information
        datas['tests'] =  tests

        return self.pool['report'].get_action(cr, uid, [], 'kinesis_athletics_export_xls.groups_xls', data=datas, context=context)
    
