from odoo import api, models, fields, _


class Shop(models.Model):
    _name = "shop.shopify"

    shopify_id = fields.Char()
    token = fields.Char()
    name = fields.Char()
    email = fields.Char()
    currencyCode = fields.Char()
    url = fields.Char()
    country = fields.Char()
    status = fields.Boolean()
    shopify_owner = fields.Char()
    password = fields.Char()
    admin = fields.Many2one('res.users')
    fetch_order_id = fields.Many2one('fetch.order')


class ShopKey(models.TransientModel):
    _inherit = "res.config.settings"

    app_api_version = fields.Char(config_parameter="shopify_odoo.app_api_version")
    app_api_key = fields.Char(config_parameter="shopify_odoo.app_api_key")
    app_secret_key = fields.Char(config_parameter="shopify_odoo.app_secret_key")
