from odoo import api, models, fields, _
import datetime, base64, requests


class XeroToken(models.Model):
    _name = 'xero.token'

    id_token = fields.Char()
    access_token = fields.Char()
    refresh_token = fields.Char()
    access_token_time_out = fields.Datetime()
    refresh_token_time_out = fields.Datetime()
    id_token_time_out = fields.Datetime()
    token_type = fields.Char()
    store_id = fields.Many2one('xero.store')
    app_id = fields.Many2one('xero.app')

    def update_token(self):
        current_app = self.env.ref('shopify_odoo.xero_app_data').sudo()
        time_now = datetime.datetime.now()
        if self.refresh_token_time_out >= time_now:
            if self.access_token_time_out < time_now:
                xero_authorization = base64.urlsafe_b64encode((current_app.client_id + ":" + current_app.client_secret).encode()).decode()
                auth_headers = {
                    'Authorization': "Basic " + xero_authorization,
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
                auth_body = {
                    'grant_type': "refresh_token",
                    'refresh_token': self.refresh_token,
                }
                new_xero_token = requests.post('https://identity.xero.com/connect/token', headers=auth_headers, data=auth_body).json()

                self.sudo().write({
                    "id_token": new_xero_token['id_token'],
                    "access_token": new_xero_token['access_token'],
                    "refresh_token": new_xero_token['refresh_token'],
                    'token_type': new_xero_token['token_type'],
                    'id_token_time_out': time_now + datetime.timedelta(minutes=5),
                    'access_token_time_out': time_now + datetime.timedelta(minutes=30),
                    'refresh_token_time_out': time_now + datetime.timedelta(days=60),
                })
