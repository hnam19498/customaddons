from odoo import api, fields, models
import json


class SaleVip(models.Model):
    _inherit = 'sale.order'

    sale_order_discount_estimated = fields.Float(string='Sale order discount estimated', compute='sale_vip_int')

    def sale_vip_int(self):
        tong = 0
        try:
            if len(self.partner_id.customer_discount_code) == 6:
                if self.partner_id.customer_discount_code[:3] == 'vip':
                    coupon = int(self.partner_id.customer_discount_code[-2:])
                    for order in self:
                        a = order.order_line
                        for line in a:
                            tong += line.product_uom_qty * line.price_unit
                    self.sale_order_discount_estimated = tong * coupon / - 100
        except:
            self.sale_order_discount_estimated = 0

    # def _compute_tax_totals_json(self):
    #     pass
    # self.sale_order_discount_estimated = json.loads(self.tax_totals_json)['amount_total'] * -0.1
