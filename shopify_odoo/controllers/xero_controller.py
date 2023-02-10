from odoo import http, _
from odoo.http import request
import werkzeug, base64, requests, datetime


class XeroController(http.Controller):
    @http.route('/xero/authenticate/', auth='public')
    def xero_auth(self, **kw):
        Menu = request.env.ref('shopify_odoo.menu_xero_connect').id
        redirectUrl = request.env["ir.config_parameter"].sudo().get_param("web.base.url") + '/web?#menu_id=' + str(Menu)
        xero_store = request.env['xero.store'].sudo().search([('shop_shopify_id', '=', request.env["shop.shopify"].sudo().search([("url", '=', kw['state'])]).id)], limit=1)
        try:
            current_app = request.env.ref('shopify_odoo.xero_app_data').sudo()
            xero_authorization = base64.urlsafe_b64encode((current_app.client_id + ":" + current_app.client_secret).encode()).decode()
            auth_headers = {
                'Authorization': "Basic " + xero_authorization,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            auth_body = {
                'grant_type': "authorization_code",
                'code': kw['code'],
                'redirect_uri': 'https://odoo.website/xero/authenticate/',
            }
            auth_xero = requests.post('https://identity.xero.com/connect/token', headers=auth_headers, data=auth_body).json()
            xero_store = request.env['xero.store'].sudo().search([('shop_shopify_id', '=', request.env["shop.shopify"].sudo().search([("url", '=', kw['state'])]).id)], limit=1)
            xero_token = request.env["xero.token"].sudo().search([('store_id', '=', xero_store.id), ("app_id", '=', current_app.id)])
            time_now = datetime.datetime.now()

            if xero_token:
                xero_token.sudo().write({
                    "access_token": auth_xero['access_token'],
                    "refresh_token": auth_xero['refresh_token'],
                    "id_token": auth_xero['id_token'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                })
            else:
                request.env['xero_token'].sudo().create({
                    "access_token": auth_xero['access_token'],
                    "refresh_token": auth_xero['refresh_token'],
                    'app_id': current_app.id,
                    "store_id": xero_store.id,
                    "id_token": auth_xero['id_token'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                })
            xero_store.sudo().write({'status_connect': "Connected"})
            return werkzeug.utils.redirect(redirectUrl)
        except  Exception as e:
            print(e)
            xero_store.sudo().write({'status_connect': "Disconnected"})
            return werkzeug.utils.redirect(redirectUrl)