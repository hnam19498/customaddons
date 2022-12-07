from odoo import api, models, fields


class ProductBundle(models.Model):
    _inherit = 'product.product'

    product_ids = fields.Many2one('product.bundle')
    # hard_fix_vendor = fields.Char(compute='get_hard_fix_vendor')
    # percentage_vendor = fields.Char(compute='get_vendor_percentage')
    product_vendor = fields.Char(compute='get_vendor')

    # discount_value = fields.Float(compute='')

    def get_vendor(self):
        for product in self:
            product.product_vendor = '0'
    # def get_vendor_hard_fix(self):
    # def et_vendor_percentage(self):


class ProductVariant(models.Model):
    _inherit = "product.product"
