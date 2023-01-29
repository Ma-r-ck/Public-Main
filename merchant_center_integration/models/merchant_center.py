from __future__ import print_function
from odoo import models, fields, api
import sys
import pathlib
from . import google
import json

# The common module provides setup functionality used by the samples,
# such as authentication and unique id generation.
# from shopping.content import common
from . import common




class ProductPublish(models.Model):
    _inherit = 'product.product'

    merchant_center_id = fields.Char()
    merchant_center_product_id = fields.Char()
    show_button = fields.Boolean(compute="compute_show_button", readonly=False)

    @api.depends('merchant_center_id')
    def compute_show_button(self):
        if self.merchant_center_product_id:
            self.show_button = True
        else:
            self.show_button = False

    def add_to_merchant_center(self):
        offer_id = ""
        if self.merchant_center_id:
            offer_id = self.merchant_center_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import',
            'res_model': 'merchant.product.add',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
                'default_description': self.name+", "+self.product_tmpl_id.description_sale,
                'default_price': self.lst_price,
                'default_product_ctgry': self.categ_id.display_name,
                'default_product_offer_id': offer_id,
                'default_shipping_weight': self.weight,

            }
        }

    def update_merchant_center_product(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import',
            'res_model': 'merchant.product.add',
            'view_mode': 'form',
            'view_id': self.env.ref(
                'merchant_center_integration.view_product_update_wizard_form_').id,
            'target': 'new',
            'context': {
                'default_item_id': self.merchant_center_product_id,
                'default_product_id': self.id,
                'default_description': self.name + ", " + self.product_tmpl_id.description_sale,
                'default_price': self.lst_price,
                'default_product_ctgry': self.categ_id.display_name,
                'default_shipping_weight': self.weight,

            }
        }

    def delete_product(self, argv=[str(pathlib.Path(__file__).parent.resolve())+'/merchant_center.py']):
        product_id = self.merchant_center_product_id
        service, config, _ = common.init(argv, __doc__)
        merchant_id = config['merchantId']
        request = service.products().delete(merchantId=merchant_id,
                                            productId=product_id)
        result = request.execute()
        self.merchant_center_product_id = ''
        self.merchant_center_id = ''

class GoogleAuthentication(models.TransientModel):
    _inherit = "res.config.settings"
    # _name = 'google.merchant.authentication'
    # _description = 'Google Authentication'

    merchant_id = fields.Integer(string='Merchant ID',
                              config_parameter="merchant.merchant_id")
    user_email = fields.Char(string='User Email',
                             config_parameter="merchant.user_email")
    private_key_id = fields.Char(string="Private Key ID",
                                 config_parameter="merchant.private_key_id")
    private_key = fields.Char(string="Private Key",
                              config_parameter="merchant.private_key")
    client_email = fields.Char(string="Client Email",
                               config_parameter="merchant.client_email")
    client_id = fields.Char(string="Client ID",
                            config_parameter="merchant.client_id")
    client_x509_cert_url = fields.Char(string="Client x509 Cert URL",
                            config_parameter="merchant.client_x509_cert_url")
    cloud_console_client_id = fields.Char(string="Console Client ID",
                        config_parameter="merchant.cloud_console_client_id")
    project_id = fields.Char(string="Project ID",
                                    config_parameter="merchant.project_id")
    client_secret = fields.Char(string='Client Secret',
                                config_parameter="merchant.client_secret")
    show_grp = fields.Boolean()

    @api.model
    def get_values(self):
        res = super(GoogleAuthentication, self).get_values()

        res['show_grp'] = self.env[
            'ir.config_parameter'].sudo().get_param(
            'merchant_center_integration.show_grp', default=0)
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'merchant_center_integration.show_grp', self.show_grp)
        super(GoogleAuthentication, self).set_values()



    def save_credentials(self):
        params = self.env['ir.config_parameter'].sudo()
        merchant_id = params.get_param('merchant.merchant_id')
        user_email = params.get_param('merchant.user_email')
        private_key_id = params.get_param('merchant.private_key_id')
        private_key = params.get_param('merchant.private_key')
        client_email = params.get_param('merchant.client_email')
        client_id = params.get_param('merchant.client_id')
        client_x509_cert_url = params.get_param('merchant.client_x509_cert_url')
        project_id = params.get_param('merchant.project_id')

        merchant_credentials = {
            "merchantId": int(merchant_id),
            "accountSampleUser": user_email
        }
        service_file_credentials = {
            "type": "service_account",
            "project_id": project_id,
            "private_key_id":private_key_id,
            "private_key":str(private_key.replace("\\n", "\n")),
            "client_email": client_email,
            "client_id": int(client_id),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": client_x509_cert_url

        }
        with open(str(pathlib.Path(__file__).parent.resolve())+"/shopping-samples/content/merchant-info.json", "w") as outfile:
            outfile.write(json.dumps(merchant_credentials, indent=3))
            outfile.close()

        with open(str(pathlib.Path(__file__).parent.resolve())+"/shopping-samples/content/service-account.json", "w") as outfile:
            outfile.write(json.dumps(service_file_credentials, indent=3))
            outfile.close()
