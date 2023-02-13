from odoo import api, models, fields, _


class BundleProduct(models.Model):
    _inherit = "product.template"

    bundle = fields.Many2one('product.bundle', string="Bundle")
    discount_value = fields.Float('Discount Value', default=1)
    qty = fields.Integer('Quantity', default=1)

    def get_list_bundle_total(self):
        self.env.cr.execute("SELECT product_bundle_id FROM bundle_total_product_rel WHERE product_template_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids

    def get_list_bundle_product(self):
        self.env.cr.execute("SELECT product_bundle_id FROM bundle_each_product_rel WHERE product_template_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids

    def get_list_bundle_tier(self):
        self.env.cr.execute("SELECT product_bundle_id FROM bundle_tier_product_rel WHERE product_template_id = %s" % self.id)
        bundle_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_ids
