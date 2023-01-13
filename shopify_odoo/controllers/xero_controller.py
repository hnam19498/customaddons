from odoo import http, _
from odoo.http import request
import shopify, binascii, os, werkzeug, json, string, base64, logging, random, ssl, traceback, requests, datetime


class XeroController(http.Controller):
    @http.route('/xero/authenticate/', auth='public')
    def xero_authenticate(self, **kw):
        print(f'kw_xero: {kw}')
        time_now = datetime.datetime.now()
        xero_code = kw['code']
        shop_shopify_url = 'https://' + kw['state']

        client_id = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.client_id")
        client_secret = request.env["ir.config_parameter"].sudo().get_param("shopify_odoo.client_secret")
        callback_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url") + '/xero/authenticate'

        shop_shopify = request.env['shop.shopify'].sudo().search([('url', '=', shop_shopify_url)])
        xero_authorization = base64.urlsafe_b64encode((client_id + ":" + client_secret).encode()).decode()

        auth_headers = {
            'Authorization': "Basic " + xero_authorization,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        auth_body = {
            'grant_type': "authorization_code",
            'code': xero_code,
            'redirect_uri': 'https://odoo.website/xero/authenticate/',
        }

        auth_xero = requests.post('https://identity.xero.com/connect/token', headers=auth_headers, data=auth_body).json()
        print(f"auth_xero: {auth_xero}")

        xero_tokens = request.env['xero.token'].sudo().search([('shop_id', '=', shop_shopify.id)])

        if xero_tokens:
            for xero_token in xero_tokens:
                if xero_token.refresh_token_time_out >= time_now:
                    if xero_token.access_token_time_out >= time_now:
                        access_token = xero_token.access_token
                    else:
                        xero_token.write({
                            "id_token": auth_xero['id_token'],
                            "access_token": auth_xero['access_token'],
                            "refresh_token": auth_xero['refresh_token'],
                            'token_type': auth_xero['token_type'],
                            'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                            'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                            'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                        })

        else:
            request.env['xero.token'].sudo().create({
                "id_token": auth_xero['id_token'],
                'token_type': auth_xero['token_type'],
                "access_token": auth_xero['access_token'],
                "refresh_token": auth_xero['refresh_token'],
                'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                'shop_id': shop_shopify.id,
            })

        if shop_shopify_url:

            access_token = request.env['xero.token'].sudo().search([('shop_id', '=', shop_shopify.id)]).access_token

            check_headers = {
                'Authorization': "Bearer " + access_token,
                'Content-Type': 'application/json',
            }

            store_infor = requests.get('https://api.xero.com/connections', headers=check_headers).json()[0]

            if store_infor['id']:
                print(f"store_infors: {store_infor}")
                shop_xero = request.env['shopify.shop.xero'].sudo().search([('store_xero_name', '=', store_infor['tenantName'])])

                if not shop_xero:
                    shop_xero.create({
                        'store_xero_name': store_infor['tenantName'],
                        'shop_shopify_id': shop_shopify.id,
                        'status_connect': "Connected",
                    })

                else:
                    shop_xero.write({
                        'status_connect': "Connected",
                    })

            else:
                shop_xero.write({
                    'status_connect': "Disconnected",
                })

        Menu = request.env.ref('shopify_odoo.menu_xero').id
        redirectUrl = request.env["ir.config_parameter"].sudo().get_param("web.base.url") + '/web?#menu_id=' + str(Menu)

        return werkzeug.utils.redirect(redirectUrl)