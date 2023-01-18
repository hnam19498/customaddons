from odoo import api, models, fields, _


class XeroStore(models.Model):
    _name = 'xero.store'

    store_xero_name = fields.Char()
    status_connect = fields.Char(default='Disconnected')
    shop_shopify_id = fields.Many2one('shop.shopify')
    tenantId = fields.Char()
    sync_id = fields.Many2one('sync.invoice')
