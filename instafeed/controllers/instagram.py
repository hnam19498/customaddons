import shopify, binascii, os, werkzeug, json, string, random, datetime, base64, requests
from odoo import http, _
from odoo.http import request


class Instagram(http.Controller):
    @http.route('/instafeed/auth', auth='user')
    def instafeed_auth(self, **kw):
        instagram_app_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_app_id')
        instagram_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_redirect_uri')

        url = 'https://api.instagram.com/oauth/authorize?client_id=' + instagram_app_id + '&redirect_uri=' + instagram_redirect_uri + '&scope=user_profile,user_media&response_type=code'
        return werkzeug.utils.redirect(url)

    @http.route('/instafeed/oauth', auth='user')
    def instafeed_oauth(self, **kw):
        if 'code' in kw:
            instagram_app_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_app_id')
            instagram_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_redirect_uri')
            instagram_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_client_secret')

            oauth_data = {
                'grant_type': "authorization_code",
                'code': kw['code'],
                'redirect_uri': instagram_redirect_uri,
                'client_id': instagram_app_id,
                'client_secret': instagram_client_secret
            }

            header = {'Content-Type': 'application/x-www-form-urlencoded'}

            instafeed_oauth = requests.post('https://api.instagram.com/oauth/access_token', headers=header, data=oauth_data)
            oauth = instafeed_oauth.json()

            if instafeed_oauth.ok:
                instagram_user_result = requests.get('https://graph.instagram.com/' + str(oauth['user_id']) + '?fields=id,username&access_token=' + oauth['access_token'])

                if instagram_user_result.ok:
                    instagram_user = instagram_user_result.json()

                    current_user = request.env.user
                    current_shopify = request.env['shop.shopify'].sudo().search([('admin', '=', current_user.id)])
                    instagram_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_client_secret')

                    long_access_token = requests.get('https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=' + instagram_client_secret + f'&access_token={oauth["access_token"]}')

                    if long_access_token.ok:
                        user_data = {
                            'instagram_access_token': oauth['access_token'],
                            "code": kw['code'],
                            'instagram_id': instagram_user['id'],
                            "username": instagram_user["username"],
                            'shop_shopify': current_shopify.id,
                            "instagram_access_token_time_out": datetime.datetime.now() + datetime.timedelta(hours=1),
                            'instagram_long_access_token': long_access_token.json()['access_token'],
                            'instagram_long_access_token_time_out': datetime.datetime.now() + datetime.timedelta(seconds=long_access_token.json()['expires_in'])
                        }

                    exist_instagram_user = request.env['instagram.user'].sudo().search([('instagram_id', '=', instagram_user['id'])], limit=1)
                    exist_facebook_user = request.env['facebook.user'].sudo().search([('shop_shopify', '=', current_shopify.id)], limit=1)

                    if not exist_instagram_user:
                        if not exist_facebook_user:
                            request.env['instagram.user'].sudo().create(user_data)
                        else:
                            new_instagram_user = request.env['instagram.user'].sudo().create(user_data)
                            new_instagram_user.facebook_user_id = exist_facebook_user.id
                            exist_facebook_user.instagram_user_id = new_instagram_user.id
                    else:
                        if not exist_facebook_user:
                            exist_instagram_user.sudo().write(user_data)
                        else:
                            exist_instagram_user.sudo().write(user_data)
                            exist_instagram_user.facebook_user_id = exist_facebook_user.id
                            exist_facebook_user.instagram_user_id = exist_instagram_user.id

                    return werkzeug.utils.redirect('https://odoo.website/instafeed')

    @http.route('/instagram/get_posts', auth='user', type="json")
    def instafeed_get_posts(self, **kw):
        posts = request.env['instagram.post'].sudo().search([])
        post_data = []
        if posts:
            for post in posts:
                post_data.append({
                    'like_count': post.like_count,
                    "caption": post.caption,
                    'media_url': post.media_url,
                    'comments': post.comments,
                    "children": post.children
                })

        return {'post_data': post_data}
