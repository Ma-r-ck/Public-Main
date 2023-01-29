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

from odoo import fields, models


class BreakfastPlan(models.Model):
    _name = "breakfast.plan"
    _description = "Breakfast Plan"

    food = fields.Char('Food')
    quantity = fields.Integer('Quantity')
    measure = fields.Char('Measure Unit')
    partner_id = fields.Many2one('res.partner')
    diet_id = fields.Many2one('diet.plan')


class LunchPlan(models.Model):
    _name = "lunch.plan"
    _description = "Lunch Plan"

    food = fields.Char('Food')
    quantity = fields.Integer('Quantity')
    measure = fields.Char('Measure Unit')
    partner_id = fields.Many2one('res.partner')
    diet_id = fields.Many2one('diet.plan')


class DinnerPlan(models.Model):
    _name = "dinner.plan"
    _description = "Dinner Plan"

    food = fields.Char('Food')
    quantity = fields.Integer('Quantity')
    measure = fields.Char('Measure Unit')
    partner_id = fields.Many2one('res.partner')
    diet_id = fields.Many2one('diet.plan')


class DietPlan(models.Model):
    _name = 'diet.plan'
    _description = 'Diet Plan'

    name = fields.Char('Name', required=True)
    breakfast_ids = fields.One2many('breakfast.plan', 'diet_id')
    lunch_ids = fields.One2many('lunch.plan', 'diet_id')
    dinner_ids = fields.One2many('dinner.plan', 'diet_id')
    diet_suggestions = fields.Text('Additional diet_id')
    partner_id = fields.Many2one('res.partner')

