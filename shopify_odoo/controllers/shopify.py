from odoo import http, _
from odoo.http import request
import shopify, binascii, os, werkzeug, json, string, base64, logging, random, ssl, traceback


class ShopifyMain(http.Controller):

    def initSession(self):

        api_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify.Session.setup(api_key=api_key, secret=secret_key)
        shopify_url = "shop-odoo-hnam.myshopify.com"
        newSession = shopify.Session(shopify_url, api_version)

        return newSession

    @http.route("/shopify/shopify_test", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopifytest(self, **kw):

        api_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify.Session.setup(api_key=api_key, secret=secret_key)
        shopify_url = "shop-odoo-hnam.myshopify.com"
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = "https://odoo.website/auth/shopify/callback"
        scopes = ["read_products", "read_orders", 'read_script_tags', 'write_script_tags']
        newSession = shopify.Session(shopify_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route("/auth/shopify/callback", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def testshopify(self, **kw):

        api_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify.Session.setup(api_key=api_key, secret=secret_key)
        shopify_url = kw["shop"]
        session = shopify.Session(shopify_url, api_version)
        access_token = session.request_token(kw)
        shopify.ShopifyResource.activate_session(session)

        existing_webhooks = shopify.Webhook.find()
        for webhook in existing_webhooks:
            print(webhook.id, webhook.topic)
            shopify.Webhook.find(webhook.id).destroy()

        print("*******************")

        webhook_order_create = shopify.Webhook()
        webhook_order_create.topic = "orders/create"
        webhook_order_create.address = "https://0fa6-116-97-240-10.ap.ngrok.io/webhook/order_create"
        webhook_order_create.format = "json"
        webhook_order_create.save()
        print(f"{webhook_order_create.id}: {webhook_order_create.topic}")

        webhook_order_updated = shopify.Webhook()
        webhook_order_updated.topic = "orders/updated"
        webhook_order_updated.address = "https://0fa6-116-97-240-10.ap.ngrok.io/webhook/order_updated"
        webhook_order_updated.format = "json"
        webhook_order_updated.save()
        print(f"{webhook_order_updated.id}: {webhook_order_updated.topic}")

        webhook_products_create = shopify.Webhook()
        webhook_products_create.topic = "products/create"
        webhook_products_create.address = "https://0fa6-116-97-240-10.ap.ngrok.io/webhook/products_create"
        webhook_products_create.format = "json"
        webhook_products_create.save()
        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

        webhook_products_update = shopify.Webhook()
        webhook_products_update.topic = "products/update"
        webhook_products_update.address = "https://0fa6-116-97-240-10.ap.ngrok.io/webhook/products_update"
        webhook_products_update.format = "json"
        webhook_products_update.save()
        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")

        existing_script_tags = shopify.ScriptTag.find()
        for script_tag in existing_script_tags:
            print(f"old_script_tag.id: {script_tag.id}")
            shopify.ScriptTag.find(script_tag.id).destroy()

        new_script_tag = shopify.ScriptTag.create({
            "event": "onload",
            "src": 'https://odoo.website/shopify_odoo/static/src/js/script_tagg_1.js',
            "display_scope": "all",
        })
        print(f"new_script_tag.id: {new_script_tag.id}")
        print(f"new_script_tag.src: {new_script_tag.src}")

        shop_shopify = shopify.Shop.current()
        client = shopify.GraphQL()
        shopify_infor = client.execute("{shop{id name email currencyCode url billingAddress{country}}}")
        shopify_data = json.loads(shopify_infor)

        print(f"kw = {kw}")

        shopify_id = shopify_data["data"]["shop"]["id"].split("/")[-1]
        shopify_name = shopify_data["data"]["shop"]["name"]
        shopify_email = shopify_data["data"]["shop"]["email"]
        shopify_currencyCode = shopify_data["data"]["shop"]["currencyCode"]
        shopify_url = shopify_data["data"]["shop"]["url"]
        shopify_country = shopify_data["data"]["shop"]["billingAddress"]["country"]

        current_shopify_shop = request.env["shop.shopify"].sudo().search([("shopify_id", "=", shopify_id)], limit=1)

        if current_shopify_shop:
            current_shopify_shop.status = True
            if not current_shopify_shop.shopify_owner:
                current_shop = shopify.Shop.current()
                current_shopify_shop.shopify_owner = current_shop.attributes['shop_owner']

                current_shopify_shop.sudo().write({
                    "name": shopify_name,
                    "email": shopify_email,
                    "token": access_token,
                    "currencyCode": shopify_currencyCode,
                    "url": shopify_url,
                    "country": shopify_country,
                })

        else:
            current_shopify_shop = request.env["shop.shopify"].sudo().create({
                "shopify_id": shopify_id,
                "name": shopify_name,
                "email": shopify_email,
                "currencyCode": shopify_currencyCode,
                "token": access_token,
                "url": shopify_url,
                "country": shopify_country,
            })

        current_company = request.env['res.company'].sudo().search([('name', '=', kw['shop'])], limit=1)
        current_user = request.env['res.users'].sudo().search([('login', '=', kw['shop'])], limit=1)

        # generate password
        letters = string.ascii_letters
        password_generate = ''.join(random.choice(letters) for i in range(20))

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
                'parent_id': False,
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
                'email': shopify_email,
                'login': kw['shop'],
                'password': password_generate,
                'action_id': False,
            })

        print(current_shopify_shop)
        if not current_shopify_shop.admin:
            current_shopify_shop.admin = current_user.id
        if not current_shopify_shop.password:
            current_shopify_shop.password = password_generate

        Menu = request.env.ref('shopify_odoo.menu_shopify_root').id
        redirectUrl = request.env["ir.config_parameter"].sudo().get_param("web.base.url") + '/web?#menu_id=' + str(Menu)
        return werkzeug.utils.redirect(redirectUrl)
