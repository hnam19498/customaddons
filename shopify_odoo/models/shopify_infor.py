from odoo import api, models, fields, _
import shopify


class ShopifyOrder(models.Model):
    _name = 'shopify.order'

    shopify_order_id = fields.Char()
    name = fields.Char()
    total_price = fields.Char()
    shop_id = fields.Many2one('shop.shopify')
    fetch_order_id = fields.Many2one('fetch.shopify')


class ShopifyProduct(models.Model):
    _name = "shopify.product"

    shopify_product_id = fields.Char()
    name = fields.Char()
    fetch_product_id = fields.Many2one('fetch.shopify')
    shop_id = fields.Many2one('shop.shopify')
