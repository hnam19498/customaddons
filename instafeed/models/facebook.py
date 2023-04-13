from odoo import fields, api, models


class FacebookSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    facebook_client_id = fields.Char('Facebook app id', config_parameter='instafeed.facebook_client_id')
    facebook_redirect_uri = fields.Char('Facebook redirect URI', config_parameter='instafeed.facebook_redirect_uri')
    facebook_client_secret = fields.Char('Facebook client secret', config_parameter="instafeed.facebook_client_secret")


class FacebookUser(models.Model):
    _name = "facebook.user"

    access_token = fields.Char()
    username = fields.Char()
    code = fields.Char()
    shop_shopify = fields.Many2one('shop.shopify')
    facebook_user_id = fields.Char()
    instagram_user_id = fields.Many2one('instagram.user')


class FacebookPage(models.Model):
    _name = 'facebook.page'

    page_id = fields.Char()
    name = fields.Char()
    instagram_user_id = fields.Many2one('instagram.user')
