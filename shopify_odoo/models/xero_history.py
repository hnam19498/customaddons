from odoo import api, models, fields


class SyncHistory(models.Model):
    _name = 'sync.history'

    start_date = fields.Date()
    end_date = fields.Date()
    count = fields.Integer()
    store_name = fields.Char()
    store_id = fields.Many2one("xero.store")

class PutHistory(models.Model):
    _name = 'put.history'

    count_paid = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    store_id = fields.Many2one("xero.store")
    count = fields.Integer()
    store_name = fields.Char()
