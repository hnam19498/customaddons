import werkzeug, base64, requests, datetime
from odoo import http, _
from odoo.http import request


class XeroController(http.Controller):
    @http.route('/xero/authenticate/', auth='public')
    def xero_auth(self, **kw):
        xero_app = request.env.ref('shopify_odoo.xero_app_data').sudo()
        menu_id = request.env.ref('shopify_odoo.menu_xero_connect').id
        redirect_url = xero_app.base_url + '/web?#menu_id=' + str(menu_id)
        xero_store = request.env['xero.store'].sudo().search([('shop_shopify_id', '=', request.env["shop.shopify"].sudo().search([("url", '=', kw['state'])]).id)], limit=1)
        try:
            xero_authorization = base64.urlsafe_b64encode((xero_app.client_id + ":" + xero_app.client_secret).encode()).decode()
            auth_headers = {
                'Authorization': f"Basic {xero_authorization}",
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            auth_body = {
                'grant_type': "authorization_code",
                'code': kw['code'],
                'redirect_uri': xero_app.redirect_uri
            }
            auth_xero = requests.post(url='https://identity.xero.com/connect/token', headers=auth_headers, data=auth_body).json()
            xero_token = request.env["xero.token"].sudo().search([('store_id', '=', xero_store.id), ("app_id", '=', xero_app.id)])
            time_now = datetime.datetime.now()

            if xero_token:
                xero_token.sudo().write({
                    "access_token": auth_xero['access_token'],
                    "refresh_token": auth_xero['refresh_token'],
                    "id_token": auth_xero['id_token'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60)
                })
            else:
                request.env['xero.token'].sudo().create({
                    "access_token": auth_xero['access_token'],
                    "refresh_token": auth_xero['refresh_token'],
                    'app_id': xero_app.id,
                    "store_id": xero_store.id,
                    "id_token": auth_xero['id_token'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60)
                })

            check_headers = {
                'Authorization': f"Bearer {auth_xero['access_token']}",
                'Content-Type': 'application/json',
            }
            store_infor = requests.get(url='https://api.xero.com/connections', headers=check_headers).json()[0]
            xero_store.sudo().write({
                'status_connect': "Connected",
                "tenantId": store_infor['tenantId'],
                'name': store_infor['tenantName']
            })
            return werkzeug.utils.redirect(redirect_url)

        except Exception as e:
            print(e)
            xero_store.sudo().write({'status_connect': "Disconnected"})
            return werkzeug.utils.redirect(redirect_url)
