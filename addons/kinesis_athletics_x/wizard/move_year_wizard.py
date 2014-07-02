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
from openerp.tools.translate import _
from datetime import date
from dateutil.relativedelta import relativedelta

class kinesis_athletics_move_group_new_year_wizard(osv.osv_memory):

    _name = 'kinesis_athletics.move_group_new_year.wizard'
    _description = 'Wizard'

    _columns = {
        'new_year': fields.integer(string='New Year', required=True),
    }

    _defaults = {
        'new_year': (date.today() + relativedelta(years=1)).year,
    }

    def confirm(self, cr, uid, ids, context=None):

        wizard = self.browse(cr, uid, ids[0], context=context)
        actives_ids=context.get('active_ids', False)
        group_obj = self.pool['kinesis_athletics.group']

        for group in group_obj.browse(cr, uid, actives_ids, context=context):
            if not group.new_year_group_id:
                raise osv.except_osv(_('Error!'),
                    _('Group "%s" has no new year group defined (id:%d).') % (group.name, group.id))
            vals = {
                'name': group.new_year_group_id.name,
                'year': wizard.new_year,
                'company_id':group.new_year_group_id.company_id.id,
                'new_year_group_id': group.new_year_group_id.new_year_group_id.id,
                'group_level_id':group.new_year_group_id.group_level_id.id,
                'partner_ids': [(6, 0, [x.id for x in group.partner_ids])],
            }
            print vals
            group_obj.create(cr, uid, vals, context=context)



        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        # receipt = self.browse(cr, uid, ids[0], context=context)
        new_context = context.copy()
        new_context = {
            # 'default_partner_id': receipt.partner_id.id,
            # 'default_actual_year': wizard.new_year,
            'search_default_actual_year': False,
            'search_default_year': wizard.new_year,
            # 'default_receipt_id': receipt.id,
            # 'default_date': receipt.date,
            # 'default_receiptbook_id': receipt.receiptbook_id.id,
            # 'show_cancel_special': True,
            # 'show_cancel_special': True,
            # 'from_receipt': True,
        }
        action_group = mod_obj.get_object_reference(cr, uid, 'kinesis_athletics', 'action_kinesis_athletics_group_groups')
        action_group_id = action_group and action_group[1] or False
        action_group = act_obj.read(cr, uid, [action_group_id], context=context)[0]
        # action_group['target'] = 'new'
        action_group['context'] = new_context
        # action_group['views'] = [action_group['views'][1],action_group['views'][0]]
        print action_group
        return action_group

