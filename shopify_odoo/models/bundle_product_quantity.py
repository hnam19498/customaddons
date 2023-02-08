from odoo import api, models, fields


class BundleProductQuantity(models.Model):
    _name = 'bundle.product.quantity'

    qty = fields.Integer()
    bundle_id = fields.Many2one('shopify.bundle')
    product_id = fields.Many2one('shopify.product')
