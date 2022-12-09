from odoo import api, models, fields


class ProductBundle(models.Model):
    _inherit = "product.product"

    product_vendor = fields.Char(compute="get_vendor")
    product_bundle_qty = fields.Integer()
    product_bundle_variant = fields.Char(compute="get_variant")
    discount_value = fields.Float()

    def get_list_bundle(self):
        list_ids = self.env['res.partner'].sudo().search([])

    def get_vendor(self):
        for product in self:
            product.product_vendor = product.company_id.name

    def get_variant(self):
        for product in self:
            temp1 = ""
            temp2 = ""
            for variant_value in product.product_template_variant_value_ids:
                if variant_value.display_name:
                    temp1 += variant_value.display_name + " - "
                    if temp1[-3:] == " - ":
                        temp2 = temp1[:-3]
            if len(temp2) >= 1:
                product.product_bundle_variant = temp2
            else:
                product.product_bundle_variant = "No information!"


class ProductVariant(models.Model):
    _inherit = "product.product"
