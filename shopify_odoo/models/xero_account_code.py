from odoo import api, models, fields


class XeroAccountCode(models.Model):
    _name = 'xero.account.code'

    account_code = fields.Char()
    name = fields.Char()
