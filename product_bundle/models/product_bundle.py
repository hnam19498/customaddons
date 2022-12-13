from odoo import api, models, fields


class ProductBundle(models.Model):
    _inherit = "product.product"

    product_vendor = fields.Char(compute="get_vendor")
    product_bundle_qty = fields.Integer()
    product_bundle_variant = fields.Char(compute="get_variant")
    discount_value = fields.Float()

    def get_list_bundle_total(self):
        self.env.cr.execute(
            "SELECT product_bundle_id FROM bundle_total_product_rel WHERE product_product_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids

    def get_list_bundle_product(self):
        self.env.cr.execute(
            "SELECT product_bundle_id FROM bundle_each_product_rel WHERE product_product_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids

    def get_list_bundle_tier(self):
        self.env.cr.execute(
            "SELECT product_bundle_id FROM bundle_tier_product_rel WHERE product_product_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids

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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def get_bundle_list(self):
        bundles = []
        bundle_ids = []
        products = self.product_variant_ids

        for product in products:
            bundle_total_ids = product.get_list_bundle_total()
            for id in bundle_total_ids:
                if id not in bundle_ids:
                    bundle_ids.append(id)

        for product in products:
            bundle_product_ids = product.get_list_bundle_product()
            for id in bundle_product_ids:
                if id not in bundle_ids:
                    bundle_ids.append(id)

        for product in products:
            bundle_tier_ids = product.get_list_bundle_tier()
            for id in bundle_tier_ids:
                if id not in bundle_ids:
                    bundle_ids.append(id)

        bundles = self.env['product.bundle'].browse(bundle_ids)

        return bundles
