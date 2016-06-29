# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class evaluation_detail(models.Model):

    """"""

    _inherit = 'kinesis_athletics.evaluation_detail'

    @api.multi
    def get_test_description(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kinesis_athletics.test',
            'view_mode': 'form',
            'res_id': self.test_id.id,
            'target': 'new'
        }

    # Lo sacamos total no interesa que se actualice en tiempo real y sacamos el
    # store por un tema de performance
    @api.depends(
        'result',
        # 'test_id',
        # 'test_id.type',
        # 'test_id.test_range_ids',
        # 'test_id.test_range_ids.from_age',
        # 'test_id.test_range_ids.to_age',
        # 'test_id.test_range_ids.sex',
        # 'test_id.test_range_ids.val_max',
        # 'test_id.test_range_ids.val_min',
        # 'test_id.test_range_ids.extreme_minimum',
        # 'test_id.test_range_ids.extreme_maximum',
        # 'evaluation_id',
        # 'evaluation_id.is_template',
        # 'evaluation_id.partner_id',
    )
    @api.one
    def _get_state(self):
        test = self.test_id
        evaluation = self.evaluation_id
        partner = self.evaluation_id.partner_id
        result = self.result

        state = False
        if not evaluation.is_template and partner:
            ref_min, ref_max, ref_ext_max, ref_ext_min = test._get_min_max(
                test.id, partner.id)
            if result > ref_max:
                state = self.test_id.rating_over_maximum
            if result < ref_min:
                state = self.test_id.rating_below_minimum
            if result >= ref_min and result <= ref_max:
                state = 'ideal'
            if ref_ext_min == ref_min and ref_max == ref_ext_max:
                state = 'none'
        self.state = state

    # Lo sacamos total no interesa que se actualice en tiempo real y sacamos el
    # store por un tema de performance
    # @api.depends(
    #     'test_id',
    #     'test_id.type',
    #     'test_id.test_range_ids',
    #     'test_id.test_range_ids.from_age',
    #     'test_id.test_range_ids.to_age',
    #     'test_id.test_range_ids.sex',
    #     'test_id.test_range_ids.val_max',
    #     'test_id.test_range_ids.val_min',
    #     'test_id.test_range_ids.extreme_minimum',
    #     'test_id.test_range_ids.extreme_maximum',
    #     'evaluation_id',
    #     'evaluation_id.is_template',
    #     'evaluation_id.partner_id',
    #     )
    @api.one
    def _get_age_avg(self):
        test = self.test_id
        evaluation = self.evaluation_id
        partner = self.evaluation_id.partner_id

        age_avg = False
        if not evaluation.is_template and partner:
            age_range = (partner.age, partner.age)
            age_results = test._get_results(
                test.id, sex=partner.sex, age_range=age_range)
            age_avg = False
            if age_results:
                age_avg = sum(age_results) / len(age_results)

        self.age_avg = age_avg

    # Lo sacamos total no interesa que se actualice en tiempo real y sacamos el
    # store por un tema de performance
    # @api.depends(
    #     'test_id',
    #     'test_id.type',
    #     'test_id.test_range_ids',
    #     'test_id.test_range_ids.from_age',
    #     'test_id.test_range_ids.to_age',
    #     'test_id.test_range_ids.sex',
    #     'test_id.test_range_ids.val_max',
    #     'test_id.test_range_ids.val_min',
    #     'test_id.test_range_ids.extreme_minimum',
    #     'test_id.test_range_ids.extreme_maximum',
    #     'evaluation_id',
    #     'evaluation_id.partner_id',
    #     )
    @api.one
    def _get_plotbands_values(self):
        test_ranges = self.env['kinesis_athletics.test_range']
        test = self.test_id
        partner = self.evaluation_id.partner_id

        plotband_ext_min = False
        plotband_val_min = False
        plotband_val_max = False
        plotband_ext_max = False

        test_ranges = test_ranges.search(
            [('test_id', '=', test.id)])
        if test_ranges and partner:
            plotband_val_min, plotband_val_max, plotband_ext_max, plotband_ext_min = test._get_min_max(
                test.id, partner.id)

        self.plotband_val_min = format(plotband_val_min, '.2f')
        self.plotband_val_max = format(plotband_val_max, '.2f')
        self.plotband_ext_max = format(plotband_ext_max, '.2f')
        self.plotband_ext_min = format(plotband_ext_min, '.2f')

    partner_id = fields.Many2one(
        'res.partner',
        'Partner',
        related='evaluation_id.partner_id',
        copy=False,
        readonly=True,
        store=True)
    uom_id = fields.Many2one(
        'product.uom',
        'Unit',
        related='test_id.uom_id',
        copy=False,
        readonly=True)
    age_avg = fields.Float(
        compute='_get_age_avg',
        string='Age Average',)
    plotband_ext_min = fields.Float(
        compute='_get_plotbands_values',
        # store=True,
        string='ext_min',)
    plotband_val_min = fields.Float(
        compute='_get_plotbands_values',
        # store=True,
        string="val_min",)
    plotband_val_max = fields.Float(
        compute='_get_plotbands_values',
        # store=True,
        string="val_max",)
    plotband_ext_max = fields.Float(
        compute='_get_plotbands_values',
        # store=True,
        string="ext_max",)
    rating_below_minimum = fields.Selection(
        related='test_id.rating_below_minimum',
        copy=False,
        readonly=True,
        string='rating_below_minimum')
    rating_between = fields.Selection(
        related='test_id.rating_between',
        copy=False,
        readonly=True,
        string='rating_between')
    rating_over_maximum = fields.Selection(
        related='test_id.rating_over_maximum',
        readonly=True,
        string='rating_over_maximum')
    state = fields.Selection(
        [('alert', 'Alert'), ('ideal', 'Ideal'),
         ('superior', 'Superior'), ('none', 'None')],
        compute='_get_state',
        string='State',
        store=True,)
    test_type = fields.Selection(
        related='test_id.type',
        copy=False,
        string="Test Type",
        readonly=True)
    test_description = fields.Char(
        related='test_id.description',
        copy=False,
        string="Test Description",
        readonly=True)
    first_parent_id = fields.Many2one(
        'kinesis_athletics.test_category',
        related='test_id.test_category_id.first_parent_id',
        copy=False,
        string='Test Class',
        readonly=True,
        store=True)
    group_id = fields.Many2one(
        'kinesis_athletics.group',
        related='evaluation_id.group_id',
        string="Group",
        copy=False,
        readonly=True,
        store=True)
    date = fields.Date(
        related='evaluation_id.date',
        string="Date",
        copy=False,
        readonly=True,
        store=True)
    company_id = fields.Many2one(
        'res.company',
        related='evaluation_id.company_id',
        string="Company",
        copy=False,
        readonly=True,
        store=True)

    @api.one
    @api.constrains('test_id', 'evaluation_id')
    def _check_duplicate_test(self):
        tests = self.search([
            ('test_id', '=', self.test_id.id),
            ('evaluation_id', '=', self.evaluation_id.id)])
        if len(tests) > 1:
            raise Warning(_('Already loaded the test'))

    @api.one
    @api.constrains(
        'evaluation_id', 'plotband_ext_min', 'plotband_ext_max', 'result')
    @api.onchange(
        'evaluation_id', 'plotband_ext_min', 'plotband_ext_max', 'result')
    def _check_result(self):
        if not self.evaluation_id.is_template:
            if self.plotband_ext_min and self.plotband_ext_max:
                if self.result != 0:
                    if self.result < self.plotband_ext_min or self.result > self.plotband_ext_max:
                        raise Warning(_('Result out of range'))
