from odoo import http, _
from odoo.http import request
from datetime import datetime


class ShopifyBundle(http.Controller):
    @http.route("/shopify_bundle/get_bundle_detail/", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def get_bundle_detail(self, **kw):

        bundle_ids = []
        shopify_product_id = kw['product_id']
        product = request.env['shopify.product'].sudo().search([('shopify_product_id', '=', shopify_product_id)], limit=1)
        list_bundle_ids = product.get_list_bundle()
        today = datetime.now()

        if list_bundle_ids:
            for id in list_bundle_ids:
                if id not in bundle_ids:
                    bundle_ids.append(id)

        if bundle_ids:
            bundle_detail = request.env["shopify.bundle"].sudo().browse(bundle_ids)
            bundle_infors = []
            quantity_infors = []
            for bundle in bundle_detail:
                bundle_infors.append({
                    'bundle_id': bundle.id,
                    "discount_value": bundle.discount_value,
                    "title": bundle.title
                })
                if bundle.indefinite_bundle or bundle.start_time <= today <= bundle.end_time:
                    product_lines = request.env['bundle.product.quantity'].sudo().search([("bundle_id", '=', bundle.id)])
                    for line in product_lines:
                        quantity_infors.append({
                            'product_id': line.product_id.id,
                            'product_name': request.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)], limit=1).name,
                            "bundle_id": line.bundle_id.id,
                            "quantity": line.qty,
                            'img': request.env['shopify.product'].sudo().search([("id", '=', line.product_id.id)], limit=1).url_img,
                        })
                        
            return {'bundle_infors': bundle_infors, "quantity_infors": quantity_infors}
        else:
            return {'bundle_infors': []}

    @http.route("/shopify_bundle/cart/", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def cart(self, **kw):
        
        list_bundle = []
        for line in kw['cart_infors']:
            product_id = request.env['shopify.product'].sudo().search([('shopify_product_id', '=', line["product_id"])]).id
            bundles = request.env['bundle.product.quantity'].sudo().search([("product_id", '=', product_id)])
            if bundles:
                for bundle in bundles:
                    list_bundle.append(bundle.bundle_id)

        print(list_bundle)
