import werkzeug, json, datetime, requests
from odoo import http, _
from odoo.http import request


class Instagram(http.Controller):
    @http.route('/instafeed/auth', auth='user')
    def instafeed_auth(self, **kw):
        instagram_app_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_app_id')
        instagram_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_redirect_uri')

        return werkzeug.utils.redirect(f'https://api.instagram.com/oauth/authorize?client_id={instagram_app_id}&redirect_uri={instagram_redirect_uri}&scope=user_profile,user_media&response_type=code')

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
                instagram_user_result = requests.get(f"https://graph.instagram.com/{str(oauth['user_id'])}?fields=id,username&access_token={oauth['access_token']}")

                if instagram_user_result.ok:
                    instagram_user = instagram_user_result.json()
                    current_user = request.env.user
                    current_shopify = request.env['shop.shopify'].sudo().search([('admin', '=', current_user.id)])
                    instagram_client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.instagram_client_secret')

                    long_access_token = requests.get(f'https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={instagram_client_secret}&access_token={oauth["access_token"]}')

                    exist_instagram_user = request.env['instagram.user'].sudo().search([('shop_shopify', '=', current_shopify.id)], limit=1)
                    exist_facebook_user = request.env['facebook.user'].sudo().search([('shop_shopify', '=', current_shopify.id)], limit=1)

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

                        if not exist_instagram_user:
                            if not exist_facebook_user:
                                request.env['instagram.user'].sudo().create(user_data)
                            else:
                                new_instagram_user = request.env['instagram.user'].sudo().create(user_data)
                                new_instagram_user.facebook_user_id = exist_facebook_user.id
                                exist_facebook_user.instagram_user_id = new_instagram_user.id
                                page = requests.get(f"https://graph.facebook.com/me/accounts?access_token={exist_facebook_user.access_token}")
                                if page.ok:
                                    instagram_business_account = requests.get(f"https://graph.facebook.com/{page.json()['data'][0]['id']}?fields=instagram_business_account&access_token={exist_facebook_user.access_token}")
                                    if instagram_business_account.ok:
                                        instagram_user_avatar = requests.get(f"https://graph.facebook.com/{instagram_business_account.json()['instagram_business_account']['id']}?fields=profile_picture_url&access_token={exist_facebook_user.access_token}")
                                        if instagram_user_avatar.ok:
                                            new_instagram_user.avatar_url = instagram_user_avatar.json()['profile_picture_url']
                        else:
                            if not exist_facebook_user:
                                exist_instagram_user.sudo().write(user_data)
                            else:
                                exist_instagram_user.sudo().write(user_data)
                                exist_instagram_user.facebook_user_id = exist_facebook_user.id
                                exist_facebook_user.instagram_user_id = exist_instagram_user.id
                                page = requests.get(f"https://graph.facebook.com/me/accounts?access_token={exist_facebook_user.access_token}")
                                if page.ok:
                                    instagram_business_account = requests.get(f"https://graph.facebook.com/{page.json()['data'][0]['id']}?fields=instagram_business_account&access_token={exist_facebook_user.access_token}")
                                    if instagram_business_account.ok:
                                        instagram_user_avatar = requests.get(f"https://graph.facebook.com/{instagram_business_account.json()['instagram_business_account']['id']}?fields=profile_picture_url&access_token={exist_facebook_user.access_token}")
                                        if instagram_user_avatar.ok:
                                            exist_instagram_user.avatar_url = instagram_user_avatar.json()['profile_picture_url']

                    return werkzeug.utils.redirect('https://odoo.website/instafeed')

    @http.route('/instagram/get_posts', auth='user', type="json")
    def instafeed_get_posts(self, **kw):
        try:
            current_instagram_user = request.env['instagram.user'].sudo().search([('username', "=", kw['instagram_username'])])
            posts = request.env['instagram.post'].sudo().search([('instagram_user', '=', current_instagram_user.id)])
            post_data = []
            if posts:
                for post in posts:
                    post_data.append({
                        'like_count': post.like_count,
                        "caption": post.caption,
                        'media_url': post.media_url,
                        'hover_status': post.hover_status,
                        'comments': post.comments,
                        'post_id': post.post_id,
                        "id": post.id,
                        'link_to_post': post.link_to_post,
                        "media_type": post.media_type,
                        'thumbnail_url': post.thumbnail_url
                    })
            return {'post_data': post_data}
        except Exception as e:
            return {"error": e}

    @http.route("/instafeed/save_feed", auth='user', type="json")
    def instafeed_save_feed(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env['shop.shopify'].sudo().search([('admin', '=', current_user.id)], limit=1)
            feed_data = {
                'list_tag': json.dumps(kw['list_tag']),
                "feed_title": kw['feed_title'],
                "number_column": kw['number_column'],
                'on_post_click': kw['on_post_click'],
                'shop_id': current_shop.id,
                "feed_layout": kw['feed_layout'],
                "selected_posts": json.dumps(kw['selected_posts']),
                "enable_status": True,
                'post_spacing': kw['post_spacing']
            }
            if 'feed_id' in kw:
                edit_feed = request.env['instagram.feed'].sudo().search([('shop_id', '=', current_shop.id), ('id', "=", kw['feed_id'])], limit=1)
                edit_feed.sudo().write(feed_data)
                edit_feed['enable_status'] = kw['enable_status']
                return {"success": f'Feed id = {kw["feed_id"]} has been edited!'}
            else:
                request.env['instagram.feed'].sudo().create(feed_data)
                return {"success": 'Created new feed!'}
        except Exception as e:
            return {"error": e}

    @http.route('/instafeed/get_feed', type='json', auth='public', method=['POST'], csrf=False, cors="*")
    def instafeed_get_feed(self, **kw):
        try:
            list_feed = []
            if 'shop_url' not in kw:
                if request.env.user:
                    current_shop = request.env['shop.shopify'].sudo().search([('admin', '=', request.env.user.id)], limit=1)
                    feeds = request.env['instagram.feed'].sudo().search([('shop_id', "=", current_shop.id)])
                    current_instagram_user = request.env['instagram.user'].sudo().search([("shop_shopify", '=', current_shop.id)], limit=1)
                    if feeds:
                        for feed in feeds:
                            if feed.selected_posts:
                                list_feed.append({
                                    'list_tag': feed.list_tag,
                                    "feed_title": feed.feed_title,
                                    'number_column': feed.number_column,
                                    "on_post_click": feed.on_post_click,
                                    'enable_status': feed.enable_status,
                                    "feed_layout": feed.feed_layout,
                                    "selected_posts": json.loads(feed.selected_posts),
                                    'id': feed.id,
                                    "post_spacing": feed.post_spacing
                                })
                            else:
                                list_feed.append({
                                    'list_tag': feed.list_tag,
                                    'id': feed.id,
                                    "feed_title": feed.feed_title,
                                    "enable_status": feed.enable_status,
                                    'number_column': feed.number_column,
                                    "on_post_click": feed.on_post_click,
                                    "feed_layout": feed.feed_layout,
                                    "selected_posts": [],
                                    "post_spacing": feed.post_spacing
                                })
                    return {
                        'list_feed': list_feed,
                        'shop_owner': current_shop.shopify_owner,
                        "instagram_user": current_instagram_user.username
                    }
                else:
                    return {'error': 'not login'}
            else:
                current_shop = request.env['shop.shopify'].sudo().search([('url', '=', kw['shop_url'])], limit=1)
                feed = request.env['instagram.feed'].sudo().search([('shop_id', "=", current_shop.id), ("id", '=', kw['feed_id'])], limit=1)
                current_instagram_user = request.env['instagram.user'].sudo().search([("shop_shopify", '=', current_shop.id)], limit=1)
                if feed:
                    if feed.enable_status:
                        if feed.selected_posts:
                            list_feed.append({
                                'list_tag': feed.list_tag,
                                "feed_title": feed.feed_title,
                                'number_column': feed.number_column,
                                "on_post_click": feed.on_post_click,
                                'enable_status': feed.enable_status,
                                "feed_layout": feed.feed_layout,
                                "selected_posts": json.loads(feed.selected_posts),
                                'id': feed.id,
                                "post_spacing": feed.post_spacing
                            })
                        else:
                            list_feed.append({
                                'list_tag': feed.list_tag,
                                'id': feed.id,
                                "feed_title": feed.feed_title,
                                "enable_status": feed.enable_status,
                                'number_column': feed.number_column,
                                "on_post_click": feed.on_post_click,
                                "feed_layout": feed.feed_layout,
                                "selected_posts": [],
                                "post_spacing": feed.post_spacing
                            })
                return {
                    'list_feed': list_feed,
                    'shop_owner': current_shop.shopify_owner,
                    "instagram_user": current_instagram_user.username,
                    "instagram_avatar": current_instagram_user.avatar_url
                }
        except Exception as e:
            return {"error": e}

    @http.route('/instafeed/fetch_post', type="json", auth="user")
    def fetch_post_instagram(self, **kw):
        try:
            current_user = request.env.user
            if current_user:
                current_instagram_user = request.env['instagram.user'].sudo().search([("username", '=', kw['instagram_username'])], limit=1)
                current_instagram_user.get_topic_instagram()
                return {"fetch_post_instagram_success": 'Fetch post instagram success!'}
        except Exception as e:
            return {'fetch_post_instagram_error': e}

    @http.route('/instafeed/change_status_feed', auth='user', type='json')
    def instafeed_enable_feed(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env['shop.shopify'].sudo().search([("admin", '=', current_user.id)], limit=1)
            current_feed = request.env['instagram.feed'].sudo().search([('shop_id', '=', current_shop.id), ("id", "=", kw['feed_id'])], limit=1)
            current_feed.enable_status = kw['status']
            if current_feed.enable_status:
                return {'change_status_feed': f"Turn on feed id = {current_feed.id} success!"}
            else:
                return {'change_status_feed': f"Feed id = {current_feed.id} was disabled!"}
        except Exception as e:
            return {"error_enable_feed": e}

    @http.route("/instafeed/edit", auth='user', type="json")
    def instafeed_edit(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env['shop.shopify'].sudo().search([("admin", '=', current_user.id)], limit=1)
            edit_feed = request.env['instagram.feed'].sudo().search([("shop_id", '=', current_shop.id), ('id', '=', kw['feed_id'])], limit=1)
            return {'edit_feed': {
                "id": edit_feed.id,
                "list_tag": edit_feed.list_tag,
                "feed_title": edit_feed.feed_title,
                'number_column': edit_feed.number_column,
                "post_spacing": edit_feed.post_spacing,
                'on_post_click': edit_feed.on_post_click,
                "feed_layout": edit_feed.feed_layout,
                "enable_status": edit_feed.enable_status,
                'selected_posts': edit_feed.selected_posts
            }}
        except Exception as e:
            return {'error': e}

    @http.route("/instafeed/delete", auth='user', type="json")
    def instafeed_delete(self, **kw):
        try:
            current_user = request.env.user
            current_shop = request.env['shop.shopify'].sudo().search([("admin", '=', current_user.id)], limit=1)
            edit_feed = request.env['instagram.feed'].sudo().search([("shop_id", '=', current_shop.id), ('id', '=', kw['feed_id'])], limit=1)
            feed_id = edit_feed.id
            edit_feed.sudo().unlink()
            return {'success': f"Deleted feed id {feed_id}!"}
        except Exception as e:
            return {'error': e}
