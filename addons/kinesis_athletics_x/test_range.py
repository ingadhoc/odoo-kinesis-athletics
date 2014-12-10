# -*- coding: utf-8 -*-

from openerp import models, api, _
from openerp.exceptions import Warning


class test_range(models.Model):

    _inherit = 'kinesis_athletics.test_range'

    _defaults = {
        'to_age': 99,
    }

    @api.one
    @api.constrains('extreme_minimum', 'val_min', 'val_max', 'extreme_maximum', 'sex', 'from_age', 'to_age')
    def _check_ranges(self):
        if self.extreme_minimum <= self.val_min < self.val_max <= self.extreme_maximum:
            if self.from_age <= self.to_age:
                test_ranges = self.env['kinesis_athletics.test_range'].search(
                    [('test_id', '=', self.test_id.id)])
                if len(test_ranges) > 1:
                    for test_range in test_ranges:
                        if test_range.id != self.id:
                            if self.sex == test_range.sex or test_range.sex == 'both' or self.sex == 'both':
                                if self.to_age > test_range.from_age:
                                    if self.from_age <= test_range.to_age:
                                        raise Warning(
                                            _('There are ranges in conflict'))

        else:
            raise Warning(_('There are values in conflict'))
        return True
