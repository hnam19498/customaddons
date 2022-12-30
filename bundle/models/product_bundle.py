from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProductBundle(models.Model):
    _name = "product.bundle"

    title = fields.Char()
    price_after_reduce = fields.Float()
    check_total = fields.Boolean(default=False)
    description = fields.Char()
    type = fields.Selection([("bundle", "Multiple Product Bundle (Discount by Purchasing Multiple Products"),
                             ("tier", "Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity")],
                            default="bundle", required=True)
    discount_rule = fields.Selection([("discount_total", "Discount on Total Bundle"), (
        "discount_product", "Discount on each Product/Variant")], default="discount_total")
    discount_type = fields.Selection([("percentage", "Percentage OFF"), ("hard_fixed", "Fixed Discount Amount OFF"),
                                      ("total_fixed", "Fixed Total Price")], default="percentage", required=True)
    discount_value = fields.Float(default=1.0)
    enable = fields.Boolean(default=True)
    active = fields.Boolean(default=True)
    priority = fields.Integer(
        help="(For bundles that have the same products), A value of ‘0’ indicates the highest priority to display in the product detail page.")
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean()
    sale_off = fields.Float(default=0)
    price_after_reduce = fields.Float(default=0)

    bundle_to_product_ids = fields.Many2many("product.template", "bundle_to_product_rel")
    bundle_to_qty_ids = fields.One2many("product.bundle.qty", "bundle_id")
    bundle_total_product_ids = fields.Many2many("product.template", "bundle_total_product_rel")
    bundle_tier_product_ids = fields.Many2many("product.template", "bundle_tier_product_rel")
    bundle_each_product_ids = fields.Many2many("product.template", "bundle_each_product_rel")

    @api.constrains("discount_value", "type", 'discount_rule')
    def check_discount_value(self):
        if float(self.discount_value) <= 0:
            if self.type == "bundle":
                if self.discount_rule == 'total':
                    raise ValidationError(_("Discount value must be an int, greater than or equal to 0!"))
        else:
            if float(self.discount_value):
                pass
            else:
                raise ValidationError(_("Discount value must be an int, greater than or equal to 0!!"))

    @api.constrains('type', 'discount_type')
    def check_discount_type(self):
        if self.type == 'tier' and self.discount_type == 'hard_fixed':
            raise ValidationError(_('Cannot set Bundle type = "Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity" and Discount type = "Fixed Discount Amount OFF"'))


class ProductBundleSetting(models.Model):
    _name = 'product.bundle.setting'

    user = fields.Many2one('res.users')
    bundle_position = fields.Selection([('below', "Below add to cart form"), ('above', 'Above add to cart form')])
    bundle_number = fields.Integer()
    bundle_tier_color = fields.Char()
    bundle_label = fields.Char()


class ProductsBundleReports(models.Model):
    _name = 'products.bundle.reports'
