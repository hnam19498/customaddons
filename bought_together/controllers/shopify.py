import shopify, binascii, os, werkzeug, json, string, random, datetime
from odoo import http, _
from odoo.http import request


class ShopifyMain(http.Controller):
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

                    shopify_infor = shopify.GraphQL().execute("{shop{id name email currencyCode url billingAddress{country}}}")
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

                        # existing_script_tag = shopify.ScriptTag.find()
                        # new_script_tag_url = 'https://odoo.website/bought_together/static/src/js/script_tag_1.js?v=' + str(datetime.datetime.now())
                        # if existing_script_tag:
                        #     if existing_script_tag.src != new_script_tag_url:
                        #         shopify.ScriptTag.find(existing_script_tag.id).destroy()
                        #         shopify.ScriptTag.create({
                        #             "event": "onload",
                        #             "src": new_script_tag_url
                        #         })
                        # else:
                        #     shopify.ScriptTag.create({
                        #         "event": "onload",
                        #         "src": new_script_tag_url
                        #     })

                        current_shopify_shop = request.env["shop.shopify"].sudo().search([("shopify_id", "=", shopify_id)], limit=1)

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

                        shop_app = request.env['shop.app.shopify'].sudo().search([("shop_id", '=', current_shopify_shop.id), ('app_id', '=', shopify_app.id)])
                        if not shop_app:
                            request.env['shop.app.shopify'].sudo().create({
                                "access_token": access_token,
                                'shop_id': current_shopify_shop.id,
                                'app_id': shopify_app.id,
                                "status": True
                            })

                        return werkzeug.utils.redirect(f'{shopify_app.base_url}/bought_together')
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')
