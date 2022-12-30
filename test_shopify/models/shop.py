from odoo import api, models, fields, _


class Shop(models.Model):
    _name = "shop.shopify"

    name = fields.Char()
