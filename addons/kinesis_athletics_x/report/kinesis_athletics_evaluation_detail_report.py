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
from openerp import tools

# AGREGAR CAMPO FUNCIÓN QUE TRAIGA EL PADRE SUPERIOR DE LA CATEGORÍA

class kinesis_athletics_evaluation_detail_report(osv.osv):
    """ Kinesis Evaluation Details Analysis Report """
    _name = "kinesis_athletics.evaluation_detail.report"
    _auto = False
    _description = "Kinesis Evaluation Details Analysis Report"

    _columns = {
        'evaluation_id': fields.many2one('kinesis_athletics.evaluation', 'Evaluation', readonly=True),
        'test_id': fields.many2one('kinesis_athletics.test', 'Test', readonly=True),
        'company_id': fields.many2one('res.partner', 'Company', readonly=True,),
        'group_id': fields.many2one('kinesis_athletics.group', 'Group', readonly=True),
        'result': fields.float('Result Average', readonly=True, group_operator="avg"),
        'result_max': fields.float('Result Max', readonly=True, group_operator="max"),
        'partner_id': fields.many2one('res.partner', 'Person', readonly=True, domain=[('is_company','=',False)]),
        'date': fields.date('Evaluation Date', readonly=True),
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'val_min': fields.float(string='Minimum Value', readonly=True),
        'val_max': fields.float('Maximum Value', readonly=True),
        'uom_id': fields.many2one('product.uom', 'Unit', readonly=True),
        'color': fields.integer('Color Index', readonly=True),
    }

    def init(self, cr):

        """
            Kinesis Evaluation Details Analysis Report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'kinesis_athletics_evaluation_detail_report')
        cr.execute("""
            CREATE OR REPLACE VIEW kinesis_athletics_evaluation_detail_report AS (
                  SELECT
                        ed.id,
                        ed.evaluation_id,
                        ed.test_id,
                        ed.result,
                        ed.result as result_max,
                        ed.state,
                        --ed.ref_min,
                        --ed.ref_max,
                        e.partner_id,
                        e.group_id,
                        g.company_id,
                        e.is_template,
                        e.date,
                        e.user_id,
                        t.uom_id,
                        1 as color,
                        1 as val_min,
                        10 as val_max
                    FROM kinesis_athletics_evaluation_detail ed
                    LEFT JOIN kinesis_athletics_evaluation e
                        ON (ed.evaluation_id = e.id)
                    LEFT JOIN kinesis_athletics_test t
                        ON (ed.test_id = t.id)
                    LEFT JOIN kinesis_athletics_group g
                                ON (e.group_id = g.id)
                    WHERE e.is_template is False
                    ORDER BY
                        id
                )""")
