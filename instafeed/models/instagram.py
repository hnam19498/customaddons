import datetime, requests, json
from odoo import fields, api, models


class InstaFeed(models.Model):
    _name = "instagram.feed"

    list_tag = fields.Char()
    feed_title = fields.Char()
    number_column = fields.Integer()
    on_post_click = fields.Char()
    feed_layout = fields.Char()
    enable_status = fields.Boolean()
    selected_posts = fields.Char()
    shop_id = fields.Many2one('shop.shopify')


class InstagramSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    instagram_app_id = fields.Char('Instagram app id', config_parameter='instafeed.instagram_app_id')
    instagram_redirect_uri = fields.Char('Instagram redirect URI', config_parameter='instafeed.instagram_redirect_uri')
    instagram_client_secret = fields.Char('Instagram client secret', config_parameter="instafeed.instagram_client_secret")


class InstagramPost(models.Model):
    _name = 'instagram.post'

    like_count = fields.Integer()
    caption = fields.Char()
    post_id = fields.Char()
    link_to_post = fields.Char()
    media_type = fields.Char()
    media_url = fields.Char()
    thumbnail_url = fields.Char()
    comments = fields.Char()
    instagram_user = fields.Many2one('instagram.user')
    hover_status = fields.Boolean(default=False)


class InstagramUser(models.Model):
    _name = 'instagram.user'

    username = fields.Char()
    instagram_id = fields.Char()
    code = fields.Char()
    instagram_access_token = fields.Char()
    instagram_long_access_token = fields.Char()
    instagram_access_token_time_out = fields.Datetime()
    instagram_long_access_token_time_out = fields.Datetime()
    widget_datas = fields.One2many('widget.data', 'instagram_user')
    shop_shopify = fields.Many2one('shop.shopify')
    facebook_user_id = fields.Many2one('facebook.user')
    followers_count = fields.Integer()

    def get_topic_instagram(self):
        time_now = datetime.datetime.now()
        if self.instagram_long_access_token_time_out >= time_now:
            new_long_access_token = requests.get('https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=' + self.instagram_long_access_token)
            if new_long_access_token.ok:
                self.sudo().write({
                    'instagram_long_access_token': new_long_access_token.json()['access_token'],
                    'instagram_long_access_token_time_out': time_now + datetime.timedelta(seconds=new_long_access_token.json()['expires_in'])
                })

        page = requests.get('https://graph.facebook.com/me/accounts?access_token=' + self.facebook_user_id.access_token)
        if page.ok:
            page_id = page.json()['data'][0]['id']
            instagram_business_account = requests.get("https://graph.facebook.com/" + page_id + "?fields=instagram_business_account&access_token=" + self.facebook_user_id.access_token)
            if instagram_business_account.ok:
                instagram_business_account_id = instagram_business_account.json()['instagram_business_account']['id']
                posts = requests.get('https://graph.facebook.com/' + instagram_business_account_id + "?fields=media,followers_count&access_token=" + self.facebook_user_id.access_token)
                if posts.ok:
                    self.followers_count = posts.json()['followers_count']
                    for id in posts.json()['media']['data']:
                        post = requests.get('https://graph.facebook.com/' + id['id'] + '?fields=permalink,thumbnail_url,media_type,like_count,caption,media_url,comments{username,text},children&access_token=' + self.facebook_user_id.access_token)
                        if post.ok:
                            post_json = post.json()
                            exist_post = self.env['instagram.post'].sudo().search([('post_id', "=", post_json['id'])])

                            post_data = {
                                'media_url': post_json['media_url'],
                                "post_id": post_json['id'],
                                "instagram_user": self.id,
                                "like_count": post_json['like_count'],
                                'media_type': post_json['media_type'],
                                "link_to_post": post_json['permalink']
                            }

                            if not exist_post:
                                exist_post = self.env['instagram.post'].sudo().create(post_data)
                            else:
                                exist_post.sudo().write(post_data)

                            if 'comments' in post_json:
                                exist_post.comments = json.dumps(post_json['comments']['data'])
                            else:
                                exist_post.comments = ''

                            if 'thumbnail_url' in post_json:
                                exist_post.thumbnail_url = post_json['thumbnail_url']
                            else:
                                exist_post.thumbnail_url = ''

                            if 'children' in post_json:
                                first_child = requests.get("https://graph.facebook.com/" + post_json['children']['data'][0]['id'] + '?fields=media_type,thumbnail_url,media_url&access_token=' + self.facebook_user_id.access_token)
                                if first_child.ok:
                                    exist_post.media_type = first_child.json()['media_type']
                                    exist_post.media_url = first_child.json()['media_url']
                                    if 'thumbnail_url' in first_child.json():
                                        exist_post.thumbnail_url = first_child.json()['thumbnail_url']
                                    else:
                                        exist_post.thumbnail_url = ''

                            if 'caption' in post_json:
                                exist_post.caption = post_json['caption']
                            else:
                                exist_post.caption = ''
