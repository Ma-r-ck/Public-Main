# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Muhammed Rishad (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class MembershipPlan(models.Model):
    _inherit = 'product.product'

    no_of_months = fields.Integer(string='No of Months')
    is_plan = fields.Boolean(string='Gym Membership Plan')

    @api.constrains('no_of_months')
    def _check_months(self):
        if self.is_plan and self.no_of_months < 1:
            raise ValidationError('No of Months of Membership Plan should '
                                  'be minimum one month')
