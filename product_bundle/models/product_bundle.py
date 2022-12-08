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
        tempp1 = ''
        for product in self:
            for variantid in product.product_variant_ids:
                tempp1 = ''
                for template_variant in variantid.product_template_variant_value_ids:
                    tempp1 += template_variant.display_name + " - "
                    if tempp1[-3:] == ' - ':
                        temm2 = tempp1[:-3]
            product.product_bundle_variant = temm2
            if product.product_bundle_variant:
                pass
            else:
                product.product_bundle_variant = 'No information!'


class ProductVariant(models.Model):
    _inherit = "product.product"
