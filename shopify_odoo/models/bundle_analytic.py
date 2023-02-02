from odoo import api, models, fields


class BundleAnalytic(models.Model):
    _name = 'bundle.analytic'

    end_time = fields.Datetime()
    start_time = fields.Datetime()
    bundle_id = fields.Many2one('shopify.bundle')
    count_time = fields.Integer()

    def open_analytic_view(self):
        return {
            'name': 'Vip Customer',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'target': 'current',
            'res_model': 'res.partner',
        }
