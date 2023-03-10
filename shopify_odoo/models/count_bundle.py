from odoo import api, models, fields


class CountBundleOrder(models.Model):
    _name = 'count.bundle.order'

    bundle_id = fields.Many2one('shopify.bundle')
    time = fields.Integer()
    draft_order_id = fields.Char()
    price_reduce = fields.Float()
    date = fields.Date()


class CountBundleDatabase(models.Model):
    _name = "count.bundle.database"

    bundle_id = fields.Char()
    time = fields.Integer()
    price_reduce = fields.Float()
    bundle_analytic_id = fields.Many2one('bundle.analytic')
    date = fields.Date()
