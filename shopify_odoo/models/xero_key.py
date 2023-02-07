from odoo import api, models, fields, _


class XeroConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    client_id = fields.Char(config_parameter="shopify_odoo.client_id")
    client_secret = fields.Char(config_parameter="shopify_odoo.client_secret")
    url_xero = fields.Char(config_parameter="shopify_odoo.url_xero")
    redirect_uri = fields.Char(config_parameter="shopify_odoo.redirect_uri")
