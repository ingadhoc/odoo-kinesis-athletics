# -*- coding: utf-8 -*-

from openerp import models, fields, tools


class kinesis_athletics_evaluation_detail_report(models.Model):
    """ Kinesis Evaluation Details Analysis Report """

    _name = "kinesis_athletics.evaluation_detail.report"
    _auto = False
    _description = "Kinesis Evaluation Details Analysis Report"

    evaluation_id = fields.Many2one(
        'kinesis_athletics.evaluation',
        string='Evaluation',
        readonly=True
    )

    test_id = fields.Many2one(
        'kinesis_athletics.test',
        string='Test',
        readonly=True
    )

    result_avg = fields.Float(
        string='Result Average',
        readonly=True,
        group_operator='avg'
    )

    result_sum = fields.Float(
        string='Result Sum',
        readonly=True,
        group_operator='sum'
    )

    result_max = fields.Float(
        string='Result Max',
        readonly=True,
        group_operator='max'
    )

    age = fields.Integer(
        string='Age',
        readonly=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Person',
        readonly=True,
        domain=[('is_company', '=', False)]
    )

    date = fields.Date(
        string='Evaluation Date',
        readonly=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        readonly=True
    )

    template_id = fields.Many2one(
        'kinesis_athletics.evaluation',
        string='Template',
        readonly=True
    )

    group_id = fields.Many2one(
        'kinesis_athletics.evaluation',
        string='Group',
        readonly=True
    )

    first_parent_id = fields.Many2one(
        'kinesis_athletics.test_category',
        string='First Parent',
        readonly=True
    )

    def _select(self):
        select_str = """
            SELECT
                ed.id,
                ed.evaluation_id,
                ed.test_id,
                ed.result,
                ed.result as result_max,
                ed.result as result_avg,
                ed.result as result_sum,
                tc.first_parent_id,                
                e.template_id,
                e.partner_id,
                e.age,
                e.is_template,
                e.group_id,
                e.date,
                e.user_id
        """
        return select_str

    def _from(self):
        from_str = """
            kinesis_athletics_evaluation_detail ed
            LEFT JOIN kinesis_athletics_evaluation e
                ON (ed.evaluation_id = e.id)
            LEFT JOIN kinesis_athletics_test t
                ON (ed.test_id = t.id)
            LEFT JOIN kinesis_athletics_test_category tc
                ON (t.test_category_id   = tc.id)
            """
        return from_str

    def _where(self):
        where_str = """
            WHERE e.is_template is False
        """
        return where_str

    def _order_by(self):
        order_str = """
            ORDER BY id
        """
        return order_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            %s
        )""" % (self._table, self._select(), self._from(), self._where(), self._order_by()))
