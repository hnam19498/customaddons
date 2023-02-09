from odoo import api, models, fields, _


class XeroConfig(models.Model):
    _name = "xero.app"

    client_id = fields.Char()
    base_url = fields.Char()
    name = fields.Char()
    client_secret = fields.Char()
    redirect_uri = fields.Char()

