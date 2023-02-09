from odoo import api, models, fields, _


class ShopifyOrder(models.Model):
    _name = 'shopify.order'

    shopify_order_id = fields.Char()
    name = fields.Char()
    total_price = fields.Char()
    ship_cost = fields.Float()
    created_date = fields.Char()
    financial_status = fields.Char()
    xero_invoice_id = fields.Char()
    shop_id = fields.Many2one('shop.shopify')
    fetch_order_id = fields.Many2one('fetch.shopify')
    products = fields.Many2many('shopify.product', 'orders_to_products_shopify')


class ShopifyProduct(models.Model):
    _name = "shopify.product"

    shopify_product_id = fields.Char()
    name = fields.Char()
    fetch_product_id = fields.Many2one('fetch.shopify')
    shop_id = fields.Many2one('shop.shopify')
    price = fields.Float()
    qty = fields.Integer('Quantity')
    url_img = fields.Char()

    def get_list_bundle(self):
        list_bundle = []
        self.env.cr.execute("SELECT bundle_id FROM bundle_product_quantity WHERE product_id = %s" % self.id)
        bundle_ids = self.env.cr.fetchall()
        for id in bundle_ids:
            list_bundle.append(id[0])
        return list_bundle