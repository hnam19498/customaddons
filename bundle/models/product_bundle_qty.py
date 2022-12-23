from odoo import api, models, fields, _


class ProductBundle(models.Model):
    _name = "product.bundle.qty"

    is_add_range = fields.Boolean()
    qty_start = fields.Integer()
    qty_end = fields.Integer()
    discount_value = fields.Float()
    bundle_id = fields.Many2one('product.bundle')



