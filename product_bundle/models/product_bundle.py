from odoo import api, models, fields


class ProductBundle(models.Model):
    _inherit = 'product.product'

    product_vendor = fields.Char(compute='get_vendor')
    product_bundle_qty = fields.Integer()
    product_bundle_variant = fields.Char(compute='get_variant')
    discount_value = fields.Float()

    def get_vendor(self):
        for product in self:
            product.product_vendor = product.company_id.name

    def get_variant(self):
        for product in self:
            temp1 = ''
            temp2 = ''
            for lol in product.product_template_variant_value_ids:
                if lol.display_name:
                    temp1 += lol.display_name + " - "
                    if temp1[-3:] == ' - ':
                        temp2 = temp1[:-3]
            if len(temp2) >= 1:
                product.product_bundle_variant = temp2
            else:
                product.product_bundle_variant = 'No information!'


class ProductVariant(models.Model):
    _inherit = "product.product"
