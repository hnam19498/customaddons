from odoo import api, models, fields, _


class QuantityOrderLine(models.Model):
    _name = 'quantity.order.line'

    product_id = fields.Many2one('shopify.product')
    order_id = fields.Many2one('shopify.order')
    quantity = fields.Float()
