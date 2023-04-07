import hashlib, hmac, json, base64
from odoo import http
from odoo.http import request, Response


class WebhookController(http.Controller):
    @http.route("/webhook/<string:topic>/<string:shopify_id>", auth="public", type="json", csrf=False, cors="*", save_session=False)
    def webhook_shopify(self, topic, shopify_id):
        try:
            client_secret = request.env['ir.config_parameter'].sudo().get_param('bought_together.client_secret')
            digest = hmac.new(client_secret.encode('utf-8'), request.httprequest.data, hashlib.sha256).digest()
            computed_hmac = base64.b64encode(digest)
            if not hmac.compare_digest(computed_hmac, request.httprequest.headers.get('X-Shopify-Hmac-Sha256').encode('utf-8')):
                return Response('Secret key is not verified', status=500)
            else:
                current_shop = request.env['shop.shopify'].sudo().search([("shopify_id", '=', shopify_id)], limit=1)
                if 'update' in topic:
                    exist_product = request.env['shopify.product'].sudo().search([('shop_id', '=', current_shop.id), ("shopify_product_id", '=', request.jsonrequest['id'])])
                    if exist_product:
                        if str(request.jsonrequest['variants'][0]['id']) == exist_product.variant_id:
                            exist_product.sudo().write({
                                'name': request.jsonrequest['title'],
                                'price': float(request.jsonrequest['variants'][0]['price']),
                                'qty': float(request.jsonrequest['variants'][0]['inventory_quantity']),
                                'url_img': request.jsonrequest['image']['src'],
                                "compare_at_price": float(request.jsonrequest['variants'][0]['compare_at_price']),
                                'url': current_shop.url + '/' + request.jsonrequest['handle']
                            })
                if "create" in topic:
                    request.env['shopify.product'].sudo().create({
                        'name': request.jsonrequest['title'],
                        'variant_id': request.jsonrequest['variants'][0]['id'],
                        'shop_id': current_shop.id,
                        'qty': float(request.jsonrequest['variants'][0]['inventory_quantity']),
                        "shopify_product_id": request.jsonrequest['id'],
                        "price": float(request.jsonrequest['variants'][0]['price']),
                        "compare_at_price": float(request.jsonrequest['variants'][0]['compare_at_price']),
                        'url_img': request.jsonrequest['image']['src'],
                        'url': current_shop.url + '/' + request.jsonrequest['handle']
                    })
                return Response("success", status=200)
        except Exception as err:
            return Response(err, status=500)
