from odoo import models, fields, api
from datetime import datetime, timedelta


class EmployeeResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    expiry_email = fields.Integer(string='Expiry Email')

    @api.model
    def get_values(self):
        res = super(EmployeeResConfigSetting, self).get_values()

        res['expiry_email'] = self.env[
            'ir.config_parameter'].sudo().get_param(
            'expiry_email.expiry_email', default=0)
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'expiry_email.expiry_email', self.expiry_email)
        super(EmployeeResConfigSetting, self).set_values()

class HrContract(models.Model):
    _inherit = 'hr.contract'

    def expiry_email(self):
        records = self.env['hr.contract'].search([('state', '=', 'open')])

        params = self.env['ir.config_parameter'].sudo()
        email_days = params.get_param('expiry_email.expiry_email')

        for rec in records:
            employee = rec.employee_id.name
            manager_email = rec.employee_id.parent_id.work_email
            manager = rec.employee_id.parent_id.name
            end_date = rec.date_end
            if end_date:
                email_date = end_date - timedelta(days=int(email_days))
                today = fields.Date.today()
                if email_date == today:
                    body = '<p>Mr '+manager+',<br>' \
                            'Employee Contract for '+employee+'' \
                                        ' expires on '+str(end_date)+'.</p>'
                    mail_template = self.env.ref(
                        'expiry_email.contract_expiry_email_template')
                    mail_template.sudo().write({
                        'email_to': manager_email,
                        'body_html': body
                    })
                    mail_template.send_mail(self.id, force_send=True)