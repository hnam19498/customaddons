import shopify, binascii, os, werkzeug, json, string, random, datetime, base64
from odoo import http, _
from odoo.http import request
from odoo.modules import get_resource_path


class ShopifyMain(http.Controller):
    @http.route('/bought_together/change_status_widget', type='json', auth="user")
    def change_status_widget(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env["shop.shopify"].sudo().search([('admin', '=', current_user.id)])
            exist_widget = request.env['shopify.widget'].sudo().search([('shop_id', '=', current_shop.id)], limit=1)
            exist_widget.sudo().write({'status': kw['widget_status']})
            return {}
        except Exception as e:
            return {'error': e}

    @http.route('/bought_together/get_widget', type='json', auth='public', method=['POST'], csrf=False, cors="*")
    def get_widget(self, **kw):
        try:
            if not kw:
                if not request.env.user:
                    return {'error': 'not login'}
                else:
                    current_user = request.env.user
                    current_shop = request.env["shop.shopify"].sudo().search([('admin', '=', current_user.id)])
            else:
                current_shop = request.env["shop.shopify"].sudo().search([('url', '=', kw['shop_url'])])

            widget = request.env['shopify.widget'].sudo().search([('shop_id', '=', current_shop.id)], limit=1)

            if not widget:
                return {}
            else:
                list_recommendation_shopify_product_ids = []
                list_excluded_shopify_product_ids = []
                recommendation_products = []

                for product in widget.recommendation_product_ids:
                    recommendation_products.append({
                        'img': product.url_img,
                        "name": product.name,
                        "variant_id": product.variant_id,
                        'url': product.url,
                        'price': product.price,
                        "compare_at_price": product.compare_at_price,
                    })

                for product in widget.excluded_product_ids:
                    list_excluded_shopify_product_ids.append(product.shopify_product_id)

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
                    "recommendation_products": recommendation_products
                }

                return {
                    'products_included': len(widget.recommendation_product_ids),
                    'widget_data': widget_data
                }
        except Exception as e:
            return {'error': e}

    @http.route("/bought_together/save_widget", type='json', auth="user")
    def save_widget(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env["shop.shopify"].sudo().search([('admin', '=', current_user.id)])

            list_excluded_product_ids = []
            list_recommendation_product_ids = []

            for product in kw['recommendation_products']:
                list_recommendation_product_ids.append(
                    request.env['shopify.product'].sudo().search([("shop_id", '=', current_shop.id), ("shopify_product_id", '=', product['id'])]).id
                )

            for product in kw['excluded_products']:
                list_excluded_product_ids.append(
                    request.env['shopify.product'].sudo().search([("shop_id", '=', current_shop.id), ("shopify_product_id", '=', product['id'])]).id
                )

            exist_widget = request.env['shopify.widget'].sudo().search([("shop_id", '=', current_shop.id)], limit=1)

            try:
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
                    'status': True,
                    'shop_id': current_shop.id
                }
                if not exist_widget:
                    request.env['shopify.widget'].sudo().create(data)
                else:
                    exist_widget.sudo().write(data)
            except Exception as error_data:
                return {"error_data": error_data}
            return {}
        except Exception as e:
            return {"error": e}

    @http.route('/bought_together/get_product', auth="user", type="json", csrf=False, cors="*", save_session=False)
    def get_product(self):
        try:
            product_data = []
            current_user = request.env.user
            current_shop = request.env["shop.shopify"].sudo().search([('admin', '=', current_user.id)])
            products = request.env['shopify.product'].sudo().search([("shop_id", '=', current_shop.id)])

            if products:
                for product in products:
                    product_data.append({
                        'id': product.shopify_product_id,
                        'name': product.name,
                        'price': product.price,
                        "url_img": product.url_img,
                        'compare_at_price': product.compare_at_price,
                        "qty": product.qty
                    })
            return {
                'product_data': product_data,
                'shop_url': current_shop.url,
                "shop_owner": current_shop.shopify_owner,
                'user_avatar': current_user.image_1920
            }
        except Exception as e:
            return {'error': e}

    @http.route("/bought_together/shopify_auth", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopify_auth(self, **kw):
        try:
            if "shop" in kw:
                api_key = request.env['ir.config_parameter'].sudo().get_param('bought_together.api_key')
                secret_key = request.env['ir.config_parameter'].sudo().get_param('bought_together.secret_key')
                base_url = request.env['ir.config_parameter'].sudo().get_param('bought_together.base_url')
                api_version = request.env['ir.config_parameter'].sudo().get_param('bought_together.api_version')

                shopify.Session.setup(api_key=api_key, secret=secret_key)
                state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
                redirect_uri = f"{base_url}/auth/shopify/callback"
                scopes = [
                    "read_products",
                    "read_orders",
                    'read_script_tags',
                    'write_script_tags',
                    "read_draft_orders",
                    'write_draft_orders'
                ]
                new_session = shopify.Session(kw['shop'], api_version)
                auth_url = new_session.create_permission_url(scopes, redirect_uri, state)
                return werkzeug.utils.redirect(auth_url)
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')

    @http.route("/auth/shopify/callback", auth="public", type="http", csrf=False, cors="*")
    def shopify_callback(self, **kw):
        try:
            if 'shop' in kw:
                api_key = request.env['ir.config_parameter'].sudo().get_param('bought_together.api_key')
                secret_key = request.env['ir.config_parameter'].sudo().get_param('bought_together.secret_key')
                api_version = request.env['ir.config_parameter'].sudo().get_param('bought_together.api_version')

                shopify.Session.setup(api_key=api_key, secret=secret_key)
                session = shopify.Session(kw["shop"], api_version)
                access_token = session.request_token(kw)
                shopify.ShopifyResource.activate_session(session)
                shopify_infor = shopify.GraphQL().execute('''
                {
                    shop{
                        id 
                        name 
                        email
                        currencyCode 
                        url 
                        billingAddress{
                            country
                        }
                    }
                }''')
                shopify_data = json.loads(shopify_infor)
                shopify_id = shopify_data["data"]["shop"]["id"].split("/")[-1]

                if access_token:
                    existing_webhooks = shopify.Webhook.find()
                    if not existing_webhooks:
                        print("*******************")

                        ngrok_url = request.env['ir.config_parameter'].sudo().get_param('bought_together.ngrok_url')
                        if not ngrok_url:
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

                    existing_script_tags = shopify.ScriptTag.find()
                    new_script_tag_url = 'https://odoo.website/bought_together/static/js/shopify.js?v=' + str(datetime.datetime.now())
                    if existing_script_tags:
                        for script_tag in existing_script_tags:
                            if script_tag.src != new_script_tag_url:
                                shopify.ScriptTag.find(script_tag.id).destroy()
                                shopify.ScriptTag.create({
                                    "event": "onload",
                                    "src": new_script_tag_url
                                })
                    else:
                        shopify.ScriptTag.create({
                            "event": "onload",
                            "src": new_script_tag_url
                        })

                    current_company = request.env['res.company'].sudo().search([('name', '=', kw['shop'])], limit=1)
                    current_user = request.env['res.users'].sudo().search([('login', '=', kw['shop'])], limit=1)
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
                        img_path = get_resource_path('bought_together', 'static/app/img', 'HOF.jpg')
                        img_content = base64.b64encode(open(img_path, "rb").read())
                        current_user = request.env['res.users'].sudo().create({
                            'company_ids': [[6, False, [current_company.id]]],
                            'company_id': current_company.id,
                            'active': True,
                            'lang': 'en_US',
                            'tz': 'Europe/Brussels',
                            '__last_update': False,
                            'name': kw['shop'],
                            'email': shopify_data["data"]["shop"]["email"],
                            'login': kw['shop'],
                            'password': password_generate,
                            'action_id': False,
                            'image_1920': img_content
                        })

                    current_shop = shopify.Shop.current()
                    current_shopify_shop = request.env["shop.shopify"].sudo().search([("shopify_id", "=", shopify_id)], limit=1)

                    if current_shopify_shop:
                        current_shopify_shop.status = True
                        if not current_shopify_shop.shopify_owner:
                            current_shopify_shop.shopify_owner = current_shop.attributes['shop_owner']
                            current_shopify_shop.sudo().write({
                                "access_token": access_token,
                                "name": shopify_data["data"]["shop"]["name"],
                                "email": shopify_data["data"]["shop"]["email"],
                                "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                                "url": shopify_data["data"]["shop"]["url"],
                                "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                            })
                    else:
                        current_shopify_shop = request.env["shop.shopify"].sudo().create({
                            "shopify_id": shopify_id,
                            'access_token': access_token,
                            "name": shopify_data["data"]["shop"]["name"],
                            "email": shopify_data["data"]["shop"]["email"],
                            'status': True,
                            "shopify_owner": current_shop.attributes['shop_owner'],
                            "currencyCode": shopify_data["data"]["shop"]["currencyCode"],
                            "url": shopify_data["data"]["shop"]["url"],
                            "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                        })

                    if not current_shopify_shop.admin:
                        current_shopify_shop.admin = current_user.id
                    if not current_shopify_shop.password:
                        current_shopify_shop.password = password_generate

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
                                try:
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
                                except Exception as error_create_product:
                                    print("error_create_product: " + str(error_create_product))
                                    continue
                            else:
                                print(f'Product id "{product.id}" đã trong database!')
                    db = http.request.env.cr.dbname
                    request.env.cr.commit()
                    request.session.authenticate(db, kw['shop'], current_shopify_shop.password)
                    return werkzeug.utils.redirect('/bought_together')
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')
