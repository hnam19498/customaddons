from odoo import api, models, fields


class Bundle(models.Model):
    _name = 'product.bundle'

    user = fields.Many2one('res.users')
    title = fields.Char()
    description = fields.Char()
    type = fields.Selection([('bundle', 'Multiple product bundle (Discount by purchasing multiple products)'),
                             ('tier', 'Quantity break bundle (Discount by purchasing a product in a larger quantity)')])
    discount_rule = fields.Selection([('discount_on_total_bundle', 'Discount on total bundle'),
                                      ('discount_on_each_products_variants', 'Discount on each products/variants')])
    discount_type = fields.Selection(
        [('percentage', 'Percentage'), ('hard_fix', 'Hard fix'), ('total_fix', 'Total fix')])
    discount_value = fields.Integer()
    priority = fields.Integer()
    enable = fields.Boolean()
    active = fields.Boolean()
    indefinite_bundle = fields.Boolean()
    start_time = fields.Datetime()
    end_time = fields.Datetime()

    product_ids = fields.One2many('product.product', 'product_ids')

    def check_indefinite_bundle(self):
        if self.indefinite_bundle:
            self.start_time = self.end_time = False

class ProductQty(models.Model):
    _name = 'product.bundle.qty'

    is_add_range = fields.Boolean()
    qty_start = fields.Integer()
    qty_end = fields.Integer()
    discount_value = fields.Integer()
    bundle_id = fields.Many2one('product.bundle')

class BundleSetting(models.Model):
    _name = 'product.bundle.setting'

    bundle_position = fields.Selection([('below', 'Below add to cart form'), ('above', 'Above add to cart form')])
    bundle_number = fields.Integer()
    bundle_title_color = fields.Char()
    button_label = fields.Char()

class BundleReport(models.Model):
    _name = 'product.bundle.report'

    bundle_id = fields.Many2one('product.bundle')
