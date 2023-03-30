import shopify, binascii, os, werkzeug, json, string, random, datetime
from odoo import http, _
from odoo.http import request


class ShopifyMain(http.Controller):
    @http.route('/bought_together/change_status_widget', type='json', auth="user")
    def change_status_widget(self, **kw):
        exist_widget = request.env['shopify.widget'].sudo().search([], limit=1)
        exist_widget.sudo().write({'status': kw['widget_status']})

    @http.route('/bought_together/get_widget', type='json', auth='public', method=['POST'], csrf=False, cors="*")
    def get_widget(self):
        widget = request.env['shopify.widget'].sudo().search([], limit=1)
        list_recommendation_shopify_product_ids = []
        list_excluded_shopify_product_ids = []
        recommendation_products = []
        excluded_products = []
        for product in widget.recommendation_product_ids:
            list_recommendation_shopify_product_ids.append(product.shopify_product_id)
            recommendation_products.append({
                'img': product.url_img,
                "name": product.name,
                "variant_id": product.variant_id,
                'url': product.url,
                'price': product.price,
                "compare_at_price": product.compare_at_price,
                'shopify_product_id': product.shopify_product_id
            })
        for product in widget.excluded_product_ids:
            list_excluded_shopify_product_ids.append(product.shopify_product_id)
            excluded_products.append({
                'img': product.url_img,
                "name": product.name,
                'price': product.price,
                "compare_at_price": product.compare_at_price,
                'shopify_product_id': product.shopify_product_id,
                "variant_id": product.variant_id
            })

        widget_data = {
            "id": widget.id,
            'widget_title': widget.widget_title,
            'widget_description': widget.widget_description,
            "total_price": widget.total_price,
            "status": widget.status,
            'title_color': widget.title_color,
            "background_color": widget.background_color,
            'description_font_size': widget.description_font_size,
            'btn_text': widget.btn_text,
            'total_compare_at_price': widget.total_compare_at_price,
            "description_color": widget.description_color,
            'border_color': widget.border_color,
            "title_font_size": widget.title_font_size,
            "text_color": widget.text_color,
            'list_excluded_shopify_product_ids': list_excluded_shopify_product_ids,
            "list_recommendation_shopify_product_ids": list_recommendation_shopify_product_ids,
            "excluded_products": excluded_products,
            "recommendation_products": recommendation_products
        }
        return {
            'products_included': len(widget.recommendation_product_ids),
            'widget_data': widget_data
        }

    @http.route("/bought_together/save_widget", type='json', auth="user")
    def save_widget(self, **kw):
        list_excluded_product_ids = []
        list_recommendation_product_ids = []
        for product in kw['recommendation_products']:
            list_recommendation_product_ids.append(
                request.env['shopify.product'].sudo().search([("shopify_product_id", '=', product['id'])]).id
            )
        for product in kw['excluded_products']:
            list_excluded_product_ids.append(
                request.env['shopify.product'].sudo().search([("shopify_product_id", '=', product['id'])]).id
            )

        exist_widget = request.env['shopify.widget'].sudo().search([])
        data = {
            'excluded_product_ids': [(6, 0, list_excluded_product_ids)],
            'recommendation_product_ids': [(6, 0, list_recommendation_product_ids)],
            "widget_description": kw['widget_description'],
            "total_compare_at_price": float(kw['total_compare_at_price']),
            'title_color': kw['title_color'],
            'background_color': kw['background_color'],
            "description_font_size": kw["description_font_size"],
            'btn_text': kw['btn_text'],
            "widget_title": kw['widget_title'],
            "total_price": float(kw['total_price']),
            'description_color': kw['description_color'],
            "border_color": kw['border_color'],
            'title_font_size': kw['title_font_size'],
            'text_color': kw['text_color'],
            'status': True
        }
        if not exist_widget:
            request.env['shopify.widget'].sudo().create(data)
        else:
            exist_widget.sudo().write(data)

    @http.route('/bought_together/get_product', auth="user", type="json", csrf=False, cors="*", save_session=False)
    def get_product(self):
        product_data = []
        products = request.env['shopify.product'].sudo().search([])
        for product in products:
            product_data.append({
                'id': product.shopify_product_id,
                'name': product.name,
                'price': product.price,
                "url_img": product.url_img,
                'compare_at_price': product.compare_at_price,
                "qty": product.qty
            })
        return {'product_data': product_data, 'shop_url': request.env.user.login}

    @http.route("/bought_together/shopify_auth", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopify_auth(self, **kw):
        try:
            if "shop" in kw:
                shopify_app = request.env.ref('bought_together.shopify_app_data').sudo()
                if shopify_app:
                    shopify.Session.setup(api_key=shopify_app.api_key, secret=shopify_app.secret_key)
                    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
                    redirect_uri = f"{shopify_app.base_url}/auth/shopify/callback"
                    scopes = [
                        "read_products",
                        "read_orders",
                        'read_script_tags',
                        'write_script_tags',
                        "read_draft_orders",
                        'write_draft_orders'
                    ]
                    new_session = shopify.Session(kw['shop'], shopify_app.api_version)
                    auth_url = new_session.create_permission_url(scopes, redirect_uri, state)
                    return werkzeug.utils.redirect(auth_url)
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')

    @http.route("/auth/shopify/callback", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopify_callback(self, **kw):
        try:
            if 'shop' in kw:
                shopify_app = request.env.ref('bought_together.shopify_app_data').sudo()
                if shopify_app:
                    shopify.Session.setup(api_key=shopify_app.api_key, secret=shopify_app.secret_key)
                    session = shopify.Session(kw["shop"], shopify_app.api_version)
                    access_token = session.request_token(kw)
                    shopify.ShopifyResource.activate_session(session)

                    shopify_infor = shopify.GraphQL().execute(
                        "{shop{id name email currencyCode url billingAddress{country}}}")
                    shopify_data = json.loads(shopify_infor)
                    shopify_id = shopify_data["data"]["shop"]["id"].split("/")[-1]

                    if access_token:
                        existing_webhooks = shopify.Webhook.find()
                        for webhook in existing_webhooks:
                            print(webhook.id, webhook.topic)
                            shopify.Webhook.find(webhook.id).destroy()

                        print("*******************")
                        ngrok_url = 'https://bce9-116-97-240-10.ap.ngrok.io'

                        webhook_order_create = shopify.Webhook()
                        webhook_order_create.topic = "orders/create"
                        webhook_order_create.address = ngrok_url + "/webhook/order_create/" + shopify_id
                        webhook_order_create.format = "json"
                        webhook_order_create.save()
                        print(f"{webhook_order_create.id}: {webhook_order_create.topic}")

                        webhook_order_updated = shopify.Webhook()
                        webhook_order_updated.topic = "orders/updated"
                        webhook_order_updated.address = ngrok_url + "/webhook/order_updated/" + shopify_id
                        webhook_order_updated.format = "json"
                        webhook_order_updated.save()
                        print(f"{webhook_order_updated.id}: {webhook_order_updated.topic}")

                        webhook_products_create = shopify.Webhook()
                        webhook_products_create.topic = "products/create"
                        webhook_products_create.address = ngrok_url + "/webhook/products_create/" + shopify_id
                        webhook_products_create.format = "json"
                        webhook_products_create.save()
                        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

                        webhook_products_update = shopify.Webhook()
                        webhook_products_update.topic = "products/update"
                        webhook_products_update.address = ngrok_url + "/webhook/products_update/" + shopify_id
                        webhook_products_update.format = "json"
                        webhook_products_update.save()
                        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")

                        existing_script_tag = shopify.ScriptTag.find()
                        new_script_tag_url = 'https://odoo.website/bought_together/static/js/shopify.js?v=' + str(
                            datetime.datetime.now())
                        if existing_script_tag:
                            for script_tag in existing_script_tag:
                                if script_tag.src != new_script_tag_url:
                                    shopify.ScriptTag.find(script_tag.id).destroy()
                                    new_script_tag = shopify.ScriptTag.create({
                                        "event": "onload",
                                        "src": new_script_tag_url
                                    })
                        else:
                            shopify.ScriptTag.create({
                                "event": "onload",
                                "src": new_script_tag_url
                            })

                        current_shopify_shop = request.env["shop.shopify"].sudo().search(
                            [("shopify_id", "=", shopify_id)], limit=1)

                        if current_shopify_shop:
                            current_shopify_shop.status = True
                            if not current_shopify_shop.shopify_owner:
                                current_shop = shopify.Shop.current()
                                current_shopify_shop.shopify_owner = current_shop.attributes['shop_owner']
                                current_shopify_shop.sudo().write({
                                    "name": shopify_data["data"]["shop"]["name"],
                                    "email": shopify_data["data"]["shop"]["email"],
                                    "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                                    "url": shopify_data["data"]["shop"]["url"],
                                    "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                                })
                        else:
                            current_shopify_shop = request.env["shop.shopify"].sudo().create({
                                "shopify_id": shopify_id,
                                "name": shopify_data["data"]["shop"]["name"],
                                "email": shopify_data["data"]["shop"]["email"],
                                "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                                "url": shopify_data["data"]["shop"]["url"],
                                "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                            })

                        current_company = request.env['res.company'].sudo().search([('name', '=', kw['shop'])], limit=1)
                        current_user = request.env['res.users'].sudo().search([('login', '=', kw['shop'])], limit=1)

                        # generate password
                        password_generate = ''.join(random.choice(string.ascii_letters) for i in range(20))

                        if not current_company:
                            current_company = request.env['res.company'].sudo().create({
                                'logo': False,
                                'currency_id': 2,
                                'sequence': 10,
                                'name': kw['shop'],
                                'street': False,
                                'street2': False,
                                'city': False,
                                'state_id': False,
                                'zip': False,
                                'country_id': False,
                                'phone': False,
                                'email': False,
                                'website': False,
                                'vat': False,
                                'company_registry': False,
                                'parent_id': False
                            })

                        if not current_user:
                            current_user = request.env['res.users'].sudo().create({
                                'company_ids': [[6, False, [current_company.id]]],
                                'company_id': current_company.id,
                                'active': True,
                                'lang': 'en_US',
                                'tz': 'Europe/Brussels',
                                'image_1920': False,
                                '__last_update': False,
                                'name': kw['shop'],
                                'email': shopify_data["data"]["shop"]["email"],
                                'login': kw['shop'],
                                'password': password_generate,
                                'action_id': False
                            })

                        if not current_shopify_shop.admin:
                            current_shopify_shop.admin = current_user.id
                        if not current_shopify_shop.password:
                            current_shopify_shop.password = password_generate

                        shop_app = request.env['shop.app.shopify'].sudo().search(
                            [("shop_id", '=', current_shopify_shop.id), ('app_id', '=', shopify_app.id)])
                        if not shop_app:
                            request.env['shop.app.shopify'].sudo().create({
                                "access_token": access_token,
                                'shop_id': current_shopify_shop.id,
                                'app_id': shopify_app.id,
                                "status": True
                            })

                        products = shopify.Product.find()
                        exist_products = request.env['shopify.product'].sudo().search([])
                        list_product_ids = []

                        if exist_products:
                            for product in exist_products:
                                if str(product.shopify_product_id) not in list_product_ids:
                                    list_product_ids.append(product.shopify_product_id)

                        if products:
                            for product in products:
                                if str(product.id) not in list_product_ids:
                                    request.env['shopify.product'].sudo().create({
                                        'shopify_product_id': product.id,
                                        'name': product.title,
                                        'url': "https://" + kw['shop'] + "/products/" + product.attributes['handle'],
                                        'shop_id': current_shopify_shop.id,
                                        'url_img': product.attributes['images'][0].attributes['src'],
                                        'price': float(product.variants[0].price),
                                        "compare_at_price": product.variants[0].compare_at_price,
                                        'qty': product.variants[0].inventory_quantity,
                                        "variant_id": product.attributes['variants'][0].id
                                    })
                                else:
                                    print(f'Product id "{product.id}" đã trong database!')
                        return werkzeug.utils.redirect(f'{shopify_app.base_url}/bought_together')
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')
