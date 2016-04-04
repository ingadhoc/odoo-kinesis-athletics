# -*- coding: utf-8 -*-

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
            new_evaluation_ids.append(evaluation_id['res_id'])

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        action_evaluation = mod_obj.get_object_reference(cr, uid, 'kinesis_athletics', 'action_kinesis_athletics_evaluation_evaluations')
        action_evaluation_id = action_evaluation and action_evaluation[1] or False
        action_evaluation = act_obj.read(cr, uid, [action_evaluation_id], context=context)[0]
        action_evaluation['domain'] = [('id','in',new_evaluation_ids)]

        return action_evaluation
