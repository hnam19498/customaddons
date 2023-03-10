from odoo import api, models, fields


class ShopifyOdooHistory(models.Model):
    _name = 'fetch.history'

    type = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    count = fields.Integer()
    shopify_name = fields.Char()
    shop_id = fields.Many2one("shop.shopify")
