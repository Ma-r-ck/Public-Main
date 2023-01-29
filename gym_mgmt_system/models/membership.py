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

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta



class GymMembership(models.Model):
    _name = "gym.membership"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Gym Membership"
    _rec_name = "reference"

    reference = fields.Char(string='GYM reference', required=True,
                            readonly=True, default=lambda self: _('New'))
    member = fields.Many2one('res.partner', string='Member', required=True,
                             tracking=True)
    membership_scheme = fields.Many2one('product.product',
                                        string='Membership Plan',
                                        required=True, tracking=True,
                                        domain="[('is_plan', '!=',False)]",
                    help="Choose Plan or Create from Membership Plan Menu...")
    trainer_ids = fields.Many2many('hr.employee', string="Trainers",
                              domain="[('trainer','=',True)]")
    membership_fees = fields.Float(string="Membership Fees", tracking=True,
                                   related='membership_scheme.list_price')
    sale_order_id = fields.Many2one('sale.order', string='Sales Order',
                                    ondelete='cascade', copy=False,
                                    readonly=True)
    invoice_id = fields.Many2one('account.move', string='invoice',
                                    ondelete='cascade', copy=False,
                                    readonly=True)
    membership_date_from = fields.Date(string='Membership Start Date',
                                       default=fields.Date.today(),
                                       help='Date from which membership '
                                            'becomes active.')
    membership_date_to = fields.Date(string='Membership End Date',
                                     compute='compute_fields', store=True,
                                     help='Date until which membership remains'
                                          ' active.')

    _sql_constraints = [
        ('membership_date_greater',
         'check(membership_date_to >= membership_date_from)',
         'Error ! Ending Date cannot be set before Beginning Date.')
    ]
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancelled', 'Cancelled')
    ], default='draft', string='Status')
    sale_count = fields.Integer(compute='compute_sale_count', store=True)
    invoice_count = fields.Integer(compute='compute_invoice_count', store=True)

    @api.depends('membership_scheme', 'membership_date_from')
    def compute_fields(self):
        for rec in self:
            if rec.membership_date_from:
                months = rec.membership_scheme.no_of_months
                rec.membership_date_to = rec.membership_date_from +\
                                          relativedelta(months=months)

    @api.depends('sale_order_id')
    def compute_sale_count(self):
        if self.sale_order_id:
            self.sale_count = 1

    @api.depends('invoice_id')
    def compute_invoice_count(self):
        if self.invoice_id:
            self.invoice_count = 1

    def create_invoice(self):
        invoices = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.member.id,
            'invoice_date': '2020-01-10',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.membership_scheme.id
                })
            ]}])
        self.invoice_id = invoices.id
        self.member.membership_reference = self.id
        self.state = 'confirm'
        if self.trainer_ids:
            self.member.trainer_ids = self.trainer_ids.ids

    def action_sale_order(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_mode': 'form',
                'res_id': self.sale_order_id.id,
                'target': 'current',
                }

    def action_invoice(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id,
                'target': 'current',
                }

    @api.model
    def create(self, vals):
        """ sequence number for membership """
        if vals.get('reference', ('New')) == ('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'gym.membership') or ('New')
        res = super(GymMembership, self).create(vals)
        return res




class SaleConfirm(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """ membership  created directly from sale order confirmed """
        product = self.env['product.product'].search([
            ('is_plan', '!=', False),
            ('id', '=', self.order_line.product_id.id)])
        for record in product:
            rec = self.env['gym.membership'].create([
                        {'member': self.partner_id.id,
                         'membership_scheme': record.id,
                         'sale_order_id': self.id,
                         'state': 'confirm'
                         }])
            self.partner_id.membership_reference = rec.id

        res = super(SaleConfirm, self).action_confirm()
        return res
