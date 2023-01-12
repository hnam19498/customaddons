from odoo import api, models, fields, _


class ShopifyShopXero(models.Model):
    _name = 'shopify.shop.xero'

    xero_token = fields.Char()
    shop = fields.Char()
    shop_shopify_id = fields.Many2one('shop.shopify')


class XeroConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    client_id = fields.Char(config_parameter="shopify_odoo.client_id")
    client_secret = fields.Char(config_parameter="shopify_odoo.client_secret")
    url_xero = fields.Char(config_parameter="shopify_odoo.url_xero")
    redirect_uri = fields.Char(config_parameter="shopify_odoo.redirect_uri")


class XeroToken(models.Model):
    _name = 'xero.token'

    id_token = fields.Char()
    access_token = fields.Char()
    refresh_token = fields.Char()
    access_token_time_out = fields.Datetime()
    refresh_token_time_out = fields.Datetime()
    id_token_time_out = fields.Datetime()
    token_type = fields.Char()
    shop_id = fields.Many2one('shop.shopify')
