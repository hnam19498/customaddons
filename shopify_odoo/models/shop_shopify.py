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
    fetch_ids = fields.One2many('fetch.shopify', 'shop_id')
