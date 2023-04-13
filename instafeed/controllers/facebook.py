import shopify, binascii, os, werkzeug, json, string, random, datetime, base64, requests
from odoo import http, _
from odoo.http import request


class Facebook(http.Controller):
    @http.route('/facebook/auth', auth='user')
    def facebook_auth(self, **kw):
        facebook_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_client_id')
        facebook_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_redirect_uri')

        url = f'https://www.facebook.com/v16.0/dialog/oauth?client_id={facebook_client_id}&redirect_uri={facebook_redirect_uri}'

        return werkzeug.utils.redirect(url)

    @http.route('/facebook/oauth', auth="user")
    def facebook_oauth(self, **kw):
        if 'code' in kw:
            facebook_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_client_id')
            facebook_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_redirect_uri')
            facebook_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_client_secret')

            facebook_token = requests.get(f'https://graph.facebook.com/v16.0/oauth/access_token?client_id={facebook_client_id}&redirect_uri={facebook_redirect_uri}&client_secret={facebook_client_secret}&code={kw["code"]}')
            if facebook_token.ok:
                facebook_data = requests.get('https://graph.facebook.com/debug_token?input_token=' + facebook_token.json()["access_token"] + "&access_token=" + facebook_token.json()["access_token"])
                if facebook_data.ok:
                    current_user = request.env.user
                    current_shopify = request.env['shop.shopify'].sudo().search([('admin', '=', current_user.id)])
                    facebook_user_data = {
                        'access_token': facebook_token.json()['access_token'],
                        "code": kw['code'],
                        'facebook_user_id': facebook_data.json()['data']['user_id'],
                        "username": requests.get('https://graph.facebook.com/' + facebook_data.json()['data']['user_id'] +'?access_token=' + facebook_token.json()['access_token']).json()['name'],
                        'shop_shopify': current_shopify.id
                    }

                    exist_instagram_user = request.env['instagram.user'].sudo().search([('shop_shopify', '=', current_shopify.id)], limit=1)
                    exist_facebook_user = request.env['facebook.user'].sudo().search([('facebook_user_id', '=', facebook_data.json()['data']['user_id'])], limit=1)

                    if not exist_instagram_user:
                        if not exist_facebook_user:
                            request.env['facebook.user'].sudo().create(facebook_user_data)
                        else:
                            exist_facebook_user.sudo().write(facebook_user_data)
                    else:
                        if not exist_facebook_user:
                            new_facebook_user = request.env['facebook.user'].sudo().create(facebook_user_data)
                            new_facebook_user.instagram_user_id = exist_instagram_user.id
                            exist_instagram_user.facebook_user_id = new_facebook_user.id
                        else:
                            exist_facebook_user.sudo().write(facebook_user_data)
                            exist_facebook_user.instagram_user_id = exist_instagram_user.id
                            exist_instagram_user.facebook_user_id = exist_facebook_user.id
                    return werkzeug.utils.redirect('https://odoo.website/instafeed')
