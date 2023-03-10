from odoo import http
from odoo.http import request, Response


class WebhookController(http.Controller):
    @http.route("/webhook/<string:topic>/<string:shopify_id>", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def webhook_shopify(self, topic, shopify_id):
        try:
            if 'order' in topic:
                exist_order = request.env['shopify.order'].sudo().search([("shopify_order_id", '=', request.jsonrequest['id']), ('shop_id', '=', request.env['shop.shopify'].sudo().search([("shopify_id", '=', shopify_id)]).id)])
                if not exist_order:
                    new_order = request.env['shopify.order'].sudo().create({
                        'shopify_order_id': request.jsonrequest['id'],
                        'financial_status': request.jsonrequest['financial_status'],
                        'name': request.jsonrequest['name'],
                        'total_price': request.jsonrequest['total_price'],
                        'shop_id': request.env['shop.shopify'].sudo().search([("shopify_id", '=', shopify_id)]).id
                    })
                    for line in request.jsonrequest['line_items']:
                        request.env['quantity.order.line'].sudo().create({
                            "order_id": new_order.id,
                            'quantity': line['quantity'],
                            'product_id': request.env['shopify.product'].sudo().search([('shopify_product_id', "=", line['product_id'])]).id
                        })
                else:
                    exist_order.sudo().write({
                        'financial_status': request.jsonrequest['financial_status']
                    })

            if 'product' in topic:
                if 'update' in topic:
                    exist_product = request.env['shopify.product'].sudo().search([('shop_id', '=', request.env['shop.shopify'].sudo().search([("shopify_id", '=', shopify_id)]).id), ("shopify_product_id", '=', request.jsonrequest['id'])])
                    if exist_product:
                        for variant in request.jsonrequest['variants']:
                            if str(variant['id']) == exist_product.variant_id:
                                exist_product.sudo().write({
                                    'name': request.jsonrequest['title'],
                                    'price': float(variant['price'])
                                })
                if "create" in topic:
                    request.env['shopify.product'].sudo().create({
                        'name': request.jsonrequest['title'],
                        'variant_id': request.jsonrequest['variants'][0]['id'],
                        'shop_id': request.env['shop.shopify'].sudo().search([("shopify_id", '=', shopify_id)]).id,
                        "shopify_product_id": request.jsonrequest['id'],
                        "price": float(request.jsonrequest['variants'][0]['price']),
                        'url_img': request.jsonrequest['image']['src']
                    })

            return Response("success", status=200)
        except Exception as err:
            print(err)
