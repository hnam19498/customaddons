from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one(comodel_name='res.users', string='Confirm user', required=True)
