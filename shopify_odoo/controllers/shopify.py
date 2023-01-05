from odoo import http, _
from odoo.http import request
import shopify, binascii, os, werkzeug, json


class ShopifyMain(http.Controller):
    @http.route("/shopify/shopify_test", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopifytest(self, **kw):

        api_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify.Session.setup(api_key=api_key, secret=secret_key)
        shop_url = "shop-odoo-hnam.myshopify.com"
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = "http://localhost:8069/auth/shopify/callback"
        scopes = ["read_products", "read_orders"]
        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route("/auth/shopify/callback", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def testshopify(self, **kw):

        api_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_key")
        secret_key = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_secret_key")
        api_version = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.app_api_version")

        shopify.Session.setup(api_key=api_key, secret=secret_key)
        shop_url = kw["shop"]
        session = shopify.Session(shop_url, api_version)
        access_token = session.request_token(kw)
        shopify.ShopifyResource.activate_session(session)

        existing_webhooks = shopify.Webhook.find()
        for webhook in existing_webhooks:
            print(webhook.id, webhook.topic)
            shopify.Webhook.find(webhook.id).destroy()

        print("*******************")

        webhook_order_create = shopify.Webhook()
        webhook_order_create.topic = "orders/create"
        webhook_order_create.address = "https://2395-116-97-240-10.ap.ngrok.io/webhook/order_create"
        webhook_order_create.format = "json"
        webhook_order_create.save()
        print(f"{webhook_order_create.id}: {webhook_order_create.topic}")

        webhook_order_updated = shopify.Webhook()
        webhook_order_updated.topic = "orders/updated"
        webhook_order_updated.address = "https://2395-116-97-240-10.ap.ngrok.io/webhook/order_updated"
        webhook_order_updated.format = "json"
        webhook_order_updated.save()
        print(f"{webhook_order_updated.id}: {webhook_order_updated.topic}")

        webhook_products_create = shopify.Webhook()
        webhook_products_create.topic = "products/create"
        webhook_products_create.address = "https://2395-116-97-240-10.ap.ngrok.io/webhook/products_create"
        webhook_products_create.format = "json"
        webhook_products_create.save()
        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

        webhook_products_update = shopify.Webhook()
        webhook_products_update.topic = "products/update"
        webhook_products_update.address = "https://2395-116-97-240-10.ap.ngrok.io/webhook/products_update"
        webhook_products_update.format = "json"
        webhook_products_update.save()
        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")

        shop = shopify.Shop.current()
        client = shopify.GraphQL()
        shop_infor = client.execute("{shop{id name email currencyCode url billingAddress{country}}}")
        shop_data = json.loads(shop_infor)

        print(f"kw = {kw}")

        shop_id = shop_data["data"]["shop"]["id"].split("/")[-1]
        shop_name = shop_data["data"]["shop"]["name"]
        shop_email = shop_data["data"]["shop"]["email"]
        shop_currencyCode = shop_data["data"]["shop"]["currencyCode"]
        shop_url = shop_data["data"]["shop"]["url"]
        shop_country = shop_data["data"]["shop"]["billingAddress"]["country"]

        if request.env["shop.shopify"].sudo().search([("shop_id", "=", shop_id)], limit=1):
            request.env["shop.shopify"].sudo().write({
                "name": shop_name,
                "email": shop_email,
                "token": access_token,
                "currencyCode": shop_currencyCode,
                "url": shop_url,
                "country": shop_country,
            })
        else:
            request.env["shop.shopify"].sudo().create({
                "shop_id": shop_id,
                "name": shop_name,
                "email": shop_email,
                "currencyCode": shop_currencyCode,
                "token": access_token,
                "url": shop_url,
                "country": shop_country,
            })

        return "Hello shopify"
