from odoo import api, fields, models


class PartnerVip(models.Model):
    _inherit = 'res.partner'

    customer_discount_code = fields.Char(string='Discount code', default='')

    def open_vip_view(self):
        partner_vip_ids = []
        res_ids = self.env['res.partner'].sudo().search([])
        for rec in res_ids:
            if rec.customer_discount_code:
                if len(rec.customer_discount_code) == 6:
                    if rec.customer_discount_code[:3] == 'vip':
                        if int(rec.customer_discount_code[-2:]):
                            partner_vip_ids.append(rec.id)

        return {
            'name': 'Vip Customer',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', partner_vip_ids)],
            'res_model': 'res.partner',
        }
