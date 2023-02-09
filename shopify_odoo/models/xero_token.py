from odoo import api, models, fields, _


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
