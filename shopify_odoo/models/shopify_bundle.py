from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ShopifyBundle(models.Model):
    _name = "shopify.bundle"

    title = fields.Char()
    description = fields.Char()
    discount_value = fields.Float(default=1.0)
    enable = fields.Boolean(default=True)
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean(default=False)

    bundle_products = fields.Many2many("shopify.product", "bundle_shopify_rel")
    qty_ids = fields.One2many('bundle.product.quantity', 'bundle_id')

    @api.constrains('discount_value')
    def check_discount_value(self):
        try:
            float(self.discount_value)
            if float(self.discount_value) < 0:
                raise ValidationError(_("Discount value must be an int, greater than or equal to 0!"))
        except:
            raise ValidationError(_("Discount value must be an int, greater than or equal to 0!!"))


class ShopifyBundleSetting(models.Model):
    _name = "shopify.bundle.setting"

    color = fields.Char()
    bundle_position = fields.Selection([('below', "Below add to cart form"), ('above', 'Above add to cart form')], default='above')
    bundle_label = fields.Char(default='')
    shop_id = fields.Many2one('shop.shopify')
