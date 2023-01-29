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


class GymMember(models.Model):
    _name = "gym.member"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Gym Member"


class MemberPartner(models.Model):
    _inherit = 'res.partner'

    membership_reference = fields.Many2one('gym.membership')
    membership_count = fields.Integer('membership_count',
                                      compute='_compute_membership_count')
    measurement_count = fields.Integer('measurement_count',
                                       compute='_compute_measurement_count')
    gym_membership_state = fields.Selection(selection=[('ongoing', 'Ongoing'),
                                                   ('expired', 'Expired'),
                                                   ('cancelled', 'Cancelled')],
                                        group_expand='_group_expand_states',
                        compute='_compute_gym_membership_state', store=True)
    measure_history_ids = fields.One2many('measurement.history', 'member')
    workout_plan_ids = fields.One2many('workout.plan', 'partner_id')
    assigned_workout_ids = fields.One2many('assigned.workout', 'partner_id')
    diet_ids = fields.One2many('diet.plan', 'partner_id')
    trainer_ids = fields.Many2many('hr.employee', string="Trainers",
                              domain="[('trainer','=',True)]")

    @api.depends('membership_reference')
    def _compute_gym_membership_state(self):
        today = fields.Date.today()
        if self.membership_reference:
            if self.membership_reference.membership_date_to >= today:
                self.gym_membership_state = 'ongoing'

    def expiry_state(self):
        today = fields.Date.today()
        records = self.env['res.partner'].search([
            ('membership_reference', '!=', False)])

        for rec in records:
            expiry_date = rec.membership_reference.membership_date_to
            if expiry_date < today:
                rec.gym_membership_state = 'expired'

    def cancelled_state(self):
        self.gym_membership_state = 'cancelled'
        self.membership_reference.state = 'cancelled'

    def action_membership(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'gym.membership',
                'view_mode': 'form',
                'res_id': self.membership_reference.id,
                'target': 'current',
                }

    def _compute_membership_count(self):
        """ number of membership for gym members """
        for rec in self:
            rec.membership_count = rec.env['gym.membership'].search_count([
                ('member.id', '=', rec.id)])

    def _compute_measurement_count(self):
        """ number of measurements for gym members """
        for rec in self:
            rec.measurement_count = rec.env['measurement.history'].search_count(
                [('member.id', '=', rec.id)])

    def _group_expand_states(self, states, domain, order):
        return [key for
                key, val in type(self).gym_membership_state.selection]

    # @api.onchange('gym_member')
    # def _onchange_gym_member(self):
    #     """ select sale person to assign workout plan """
    #     if self.gym_member:
    #         return {
    #             'warning': {
    #                 'title': 'Warning!',
    #                 'message': 'select sale person (sales & purchase) '
    #                            'to assign workout plan'}
    #         }

