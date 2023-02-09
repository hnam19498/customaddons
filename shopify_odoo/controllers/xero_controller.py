from odoo import http, _
from odoo.http import request
import werkzeug, base64, requests, datetime


class XeroController(http.Controller):
    @http.route('/xero/authenticate/', auth='public')
    def xero_authenticate(self, **kw):
        try:
            current_app = request.env.ref('shopify_odoo.xero_app_data').sudo()
            xero_store = request.env['xero.store'].sudo().search([('shop_shopify_id', '=', request.env["shop.shopify"].sudo().search([("url", '=', kw['state'])]).id)])
            time_now = datetime.datetime.now()
            xero_token = request.env["xero.token"].sudo().search([('store_id', '=', xero_store.id), ("app_id", '=', current_app.id)])

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

            if xero_token:
                if xero_token.refresh_token_time_out >= time_now:
                    if xero_token.access_token_time_out >= time_now:
                        access_token = xero_token.access_token
                    else:
                        xero_token.write({
                            "id_token": auth_xero['id_token'],
                            "access_token": auth_xero['access_token'],
                            "refresh_token": auth_xero['refresh_token'],
                            'token_type': auth_xero['token_type'],
                            'app_id': current_app.id,
                            "store_id": xero_store.id,
                            'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                            'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                            'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                        })
                        access_token = auth_xero['access_token']
            else:
                request.env['xero.token'].sudo().create({
                    "id_token": auth_xero['id_token'],
                    'app_id': current_app.id,
                    "store_id": xero_store.id,
                    'token_type': auth_xero['token_type'],
                    "access_token": auth_xero['access_token'],
                    "refresh_token": auth_xero['refresh_token'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                })
                access_token = auth_xero['access_token']

            
            check_headers = {
                'Authorization': "Bearer " + access_token,
                'Content-Type': 'application/json',
            }

            store_infor = requests.get('https://api.xero.com/connections', headers=check_headers).json()[0]

            if store_infor['id']:
                xero_store.write({
                    'tenantId': store_infor['tenantId'],
                    'status_connect': "Connected",
                    'name': store_infor['tenantName'],
                })
            else:
                xero_store.write({
                    'status_connect': "Disconnected",
                })

            Menu = request.env.ref('shopify_odoo.menu_xero').id
            redirectUrl = request.env["ir.config_parameter"].sudo().get_param("web.base.url") + '/web?#menu_id=' + str(Menu)
            
            return werkzeug.utils.redirect(redirectUrl)
        except:
            return werkzeug.utils.redirect('https://www.xero.com/')