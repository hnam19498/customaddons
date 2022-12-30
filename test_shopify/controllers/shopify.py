from odoo import http, _
from odoo.http import request
import shopify, binascii, os, werkzeug


class ShopifyMain(http.Controller):
    @http.route("/shopify/shopify_test", auth="public", type="http", csrf=False, cors="*", save_session=False)
    def shopifytest(self, **kw):
        print(kw)
        shopify.Session.setup(api_key='26b04e0bc1a1d962efafa373c9976372', secret='8a5a2bab02fce8cfff264d5583e47e0a')
        shop_url = "shop-odoo-hnam.myshopify.com"
        api_version = '2022-10'
        state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        redirect_uri = "http://localhost:8069/auth/shopify/callback"
        scopes = ['read_products', 'read_orders']

        newSession = shopify.Session(shop_url, api_version)
        auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        return werkzeug.utils.redirect(auth_url)

    @http.route('/auth/shopify/callback', auth="public", type="http", csrf=False, cors="*", save_session=False)
    def testshopify(self, **kw):
        print(kw)
        shopify.Session.setup(api_key='26b04e0bc1a1d962efafa373c9976372', secret='8a5a2bab02fce8cfff264d5583e47e0a')
        shop_url = kw['shop']
        api_version = '2022-10'
        session = shopify.Session(shop_url, api_version)
        access_token = session.request_token(kw)
        print(access_token)
        shopify.ShopifyResource.activate_session(session)
        shop = shopify.Shop.current()
        print(shop)
        a = shopify.GraphQL().execute("{ shop { name id } }")
        print(a)
        return 'hello world'
