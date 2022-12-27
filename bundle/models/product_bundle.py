from odoo import api, models, fields, _


class ProductBundle(models.Model):
    _name = "product.bundle"

    title = fields.Char()
    description = fields.Char()
    type = fields.Selection([("bundle", "Multiple Product Bundle (Discount by Purchasing Multiple Products"),
                             ("tier", "Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity")
                             ], default="bundle", required=True)
    discount_rule = fields.Selection(
        [("discount_total", "Discount on Total Bundle"), ("discount_product", "Discount on each Product/Variant")
         ], default="discount_total")
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

    bundle_to_product_ids = fields.Many2many("product.template", "bundle_to_product_rel")
    bundle_to_qty_ids = fields.One2many("product.bundle.qty", "bundle_id")
    bundle_total_product_ids = fields.Many2many("product.template", "bundle_total_product_rel")
    bundle_tier_product_ids = fields.Many2many("product.template", "bundle_tier_product_rel")
    bundle_each_product_ids = fields.Many2many("product.template", "bundle_each_product_rel")
