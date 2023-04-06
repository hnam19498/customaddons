import shopify, binascii, os, werkzeug, json, string, random, datetime, base64, requests
from odoo import http, _
from odoo.http import request


class Instagram(http.Controller):
    @http.route('/instafeed/auth', auth='public')
    def instafeed_auth(self, **kw):
        instagram_app_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_app_id')
        redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.redirect_uri')

        url = 'https://api.instagram.com/oauth/authorize?client_id=' + instagram_app_id + '&redirect_uri=' + redirect_uri + '&scope=user_profile,user_media&response_type=code'
        return werkzeug.utils.redirect(url)

    @http.route('/instafeed/oauth', auth='public')
    def instafeed_oauth(self, **kw):
        if 'code' in kw:
            instagram_app_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_app_id')
            redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.redirect_uri')
            client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.client_secret')

            data = {
                'grant_type': "authorization_code",
                'code': kw['code'],
                'redirect_uri': redirect_uri,
                'client_id': instagram_app_id,
                'client_secret': client_secret
            }

            header = {'Content-Type': 'application/x-www-form-urlencoded'}

            instafeed_oauth = requests.post('https://api.instagram.com/oauth/access_token', headers=header, data=data)
            oauth = instafeed_oauth.json()
            print(1)
