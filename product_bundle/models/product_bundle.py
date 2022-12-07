from odoo import api, models, fields


class ProductBundle(models.Model):
    _inherit = 'product.product'

    product_to_bundle_ids = fields.Many2one('product.bundle')
    product_vendor = fields.Char(compute='get_vendor')
    product_bundle_qty = fields.Integer()
    product_variant = fields.Char()
    discount_value = fields.Float()

    def get_vendor(self):
        for product in self:
            product.product_vendor = '0'


class ProductVariant(models.Model):
    _inherit = "product.product"
