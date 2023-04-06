from odoo import fields, api, models


class InstagramSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    instagram_app_id = fields.Char('Instagram app id', config_parameter='instafeed.instagram_app_id')
    redirect_uri = fields.Char('Redirect URI', config_parameter='instafeed.redirect_uri')
    client_secret = fields.Char('Instagram client secret', config_parameter="instafeed.instagram_client_secret")
