# -*- coding: utf-8 -*-

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

            group_obj.create(cr, uid, vals, context=context)

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        new_context = context.copy()
        new_context = {
            'search_default_actual_year': False,
            'search_default_year': wizard.new_year,
        }
        action_group = mod_obj.get_object_reference(cr, uid, 'kinesis_athletics', 'action_kinesis_athletics_group_groups')
        action_group_id = action_group and action_group[1] or False
        action_group = act_obj.read(cr, uid, [action_group_id], context=context)[0]
        action_group['context'] = new_context

        return action_group
