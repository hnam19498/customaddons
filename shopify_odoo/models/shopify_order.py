from odoo import api, models, fields, _
import shopify


class ShopifyOrder(models.Model):
    _name = 'shopify.order'

    shopify_order_id = fields.Char()
    name = fields.Char()
    total_price = fields.Char()
    shopify_id = fields.Many2one('shop.shopify')
