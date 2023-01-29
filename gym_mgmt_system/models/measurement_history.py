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

from odoo import api, fields, models


class MeasurementHistory(models.Model):
    _name = "measurement.history"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Measurement History"

    _rec_name = "member"

    def _get_default_weight_uom(self):
        """ to get default weight uom """
        return self.env[
            'product.template']._get_weight_uom_name_from_ir_config_parameter()

    member = fields.Many2one('res.partner', string='Member', tracking=True,
                             required=True,
                             domain="[('membership_reference', '!=',False)]")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender", required=True)
    age = fields.Integer(string='Age', tracking=True, required=True)
    weight = fields.Float(
        'Weight', digits='Stock Weight', store=True)
    weight_uom_name = fields.Char(string='Weight unit of measure label',
                                  default=_get_default_weight_uom)
    height = fields.Float(
        'Height', digits='Stock Height', store=True)
    height_uom_name = fields.Char(string='Weight unit of measure label',
                                  default='cm')
    activity_type = fields.Selection(string='Daily Activity Range', selection=[
        ('sedentary', 'Sedentary - little or no exercise'),
        ('light', 'Light - Light exercise/sports 1-3 days per week'),
        ('moderate', 'Moderate - Moderate exercise/sports 3 -5 days per week'),
        ('very', 'Very - Hard exercise/sports 6-7 days per week'),
        ('extra', 'Extra - '
                  'Extreme hard daily exercise/sports and physical job')],
                                     default='sedentary')
    bmi = fields.Float('BMI', store=True, compute='compute_display_name')
    bmr = fields.Float('BMR', store=True, compute='compute_display_name')
    amr = fields.Float(string='AMR', store=True, compute='compute_amr')
    amr_description = fields.Text(default='AMR represents the total amount of '
        'calories you expend through the day. With regard to calories, AMR '
        'also represents the number of calories you need to consume each day '
        'to stay at your current weight. If your goal is to lose weight, you '
        'need to increase your level of physical activity and/or decrease the '
        'amount of calories you eat each day.', readonly=True,
                                  string='Description')
    neck = fields.Float('Neck')
    biceps = fields.Float('Biceps')
    calf = fields.Float('Calf')
    hips = fields.Float('Hips')
    chest = fields.Float('Chest')
    waist = fields.Float('Waist')
    thighs = fields.Float('Thighs')
    date = fields.Date(string='Date', required=True,
                       help='Date from which measurement was taken.')

    @api.depends('weight', 'height')
    def compute_display_name(self):
        """ based on weight and height ,calculate the bmi and bmr"""
        if self.weight and self.height:
            self.bmi = (self.weight / self.height / self.height) * 10000

            if self.gender == "male":
                self.bmr = 66.47 + (13.75 * self.weight) + \
                           (5.003 * self.height) - (6.755 * self.age)

            if self.gender == "female":
                self.bmr = 655.1 + (9.563 * self.weight) + \
                           (1.85 * self.height) - (6.755 * self.age)

    @api.depends('bmr', 'activity_type')
    def compute_amr(self):
        if self.bmr:
            if self.activity_type == 'sedentary':
                self.amr = self.bmr * 1.2
            elif self.activity_type == 'light':
                self.amr = self.bmr * 1.375
            elif self.activity_type == 'moderate':
                self.amr = self.bmr * 1.55
            elif self.activity_type == 'very':
                self.amr = self.bmr * 1.725
            elif self.activity_type == 'extra':
                self.amr = self.bmr * 1.9
