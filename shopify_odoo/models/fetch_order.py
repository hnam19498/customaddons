from odoo import api, models, fields, _
import shopify
from datetime import date


class FetchOrder(models.Model):
    _name = 'fetch.order'

    start_date = fields.Date()
    end_date = fields.Date()
    shopify_order_ids = fields.One2many('shopify.order', "shopify_order_id")
    shop_shopify_id = fields.Many2one('shop.shopify')

    def get_list_order(self):
        list_orders = shopify.Order.find()
        order_exist = self.env['shopify.order'].find()
