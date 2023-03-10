from odoo import api, models, fields


class XeroInvoice(models.Model):
    _name = 'xero.invoice'

    sync_invoice_id = fields.Many2one('sync.invoice')
    invoice_id = fields.Char()
    type = fields.Char()
    invoice_number = fields.Char()
    store_id = fields.Many2one('xero.store')
    reference = fields.Char()
    amount_due = fields.Float()
    financial_status = fields.Char()
    amount_paid = fields.Float()
    contact_id = fields.Char()
    currency_code = fields.Char()
    contact_name = fields.Char()
    invoice_date = fields.Date()
    price_total = fields.Float()
