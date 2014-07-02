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


class reevaluate_wizard(osv.osv_memory):

    _name = 'kinesis_athletics.reevaluate.wizard'
    _description = 'Wizard'

    def confirm(self, cr, uid, ids, context=None):

        wizard = self.browse(cr, uid, ids[0], context=context)
        active_ids=context.get('active_ids', False)

        evaluation_obj = self.pool['kinesis_athletics.evaluation']

        evaluation_ids = evaluation_obj.browse(cr, uid, active_ids, context=context)

        new_evaluation_ids = []

        for evaluation in evaluation_ids:
          evaluation_id = evaluation_obj.new_evaluation(cr, uid, [evaluation.id], context=context)
          new_evaluation_ids.append(evaluation.id)

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        action_evaluation = mod_obj.get_object_reference(cr, uid, 'kinesis_athletics', 'action_kinesis_athletics_evaluation_evaluations')
        action_evaluation_id = action_evaluation and action_evaluation[1] or False
        action_evaluation = act_obj.read(cr, uid, [action_evaluation_id], context=context)[0]
        action_evaluation['domain'] = [('id','in',new_evaluation_ids)]

        return action_evaluation
