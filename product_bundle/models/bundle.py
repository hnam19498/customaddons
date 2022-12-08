from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class Bundle(models.Model):
    _name = 'product.bundle'

    user = fields.Many2one('res.users')
    title = fields.Char()
    description = fields.Char()
    type = fields.Selection([('bundle', 'Multiple product bundle (Discount by purchasing multiple products)'),
                             ('tier', 'Quantity break bundle (Discount by purchasing a product in a larger quantity)')])
    discount_rule = fields.Selection(
        [('total', 'Discount on total bundle'), ('product', 'Discount on each products/variants')])
    discount_type = fields.Selection(
        [('percentage', 'Percentage'), ('hard_fix', 'Hard fix'), ('total_fix', 'Total fix')])
    discount_value = fields.Integer()
    priority = fields.Integer()
    enable = fields.Boolean()
    active = fields.Boolean()
    indefinite_bundle = fields.Boolean(default=False)
    start_time = fields.Datetime()
    end_time = fields.Datetime()

    bundle_to_product_ids = fields.Many2many('product.product', 'bundle_to_product_rel')
    bundle_to_qty_ids = fields.Many2many('product.bundle.qty')
    bundle_total_product_ids = fields.Many2many('product.product', 'bundle_total_product_rel')
    bundle_tier_product_ids = fields.Many2many('product.product', 'bundle_tier_product_rel')
    bundle_product_ids = fields.Many2many('product.product', 'bundle_product_rel')

    @api.constrains('indefinite_bundle')
    def check_indefinite_bundle(self):
        if self.indefinite_bundle:
            self.start_time = self.end_time = False

    @api.constrains('discount_value')
    def check_discount_value(self):
        if float(self.discount_value) <= 0:
            raise ValidationError(_("Discount value must be an int, greater than or equal to 0!"))
        if float(self.discount_value):
            pass
        else:
            raise ValidationError(_("Discount value must be an int, greater than or equal to 0!!"))


class ProductQty(models.Model):
    _name = 'product.bundle.qty'

    qty_bundle_ids = fields.Integer()
    is_add_range = fields.Boolean(default=False)
    qty_start = fields.Integer()
    qty = fields.Integer()
    qty_end = fields.Integer()
    discount_value = fields.Integer()

    def check_qty(self):
        for product in self:
            if product.qty_start and product.qty_end:
                if product.qty_start >= product.qty_end:
                    product.qty_start = product.qty_end = 0
            else:
                if product.qty < 0 or product.qty.is_integer() == False:
                    product.qty = 0


class BundleSetting(models.Model):
    _name = 'product.bundle.setting'

    bundle_position = fields.Selection([('below', 'Below add to cart form'), ('above', 'Above add to cart form')])
    bundle_number = fields.Integer()
    bundle_title_color = fields.Char()
    button_label = fields.Char()


class BundleReport(models.Model):
    _name = 'product.bundle.report'

    bundle_report_id = fields.Many2one('product.bundle')
