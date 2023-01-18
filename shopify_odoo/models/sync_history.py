from odoo import api, models, fields, _


class SyncHistory(models.Model):
    _name = 'sync.history'

    type = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    count = fields.Integer()
    shopify_name = fields.Char()
