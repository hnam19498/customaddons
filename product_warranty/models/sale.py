from odoo import api, fields, models


class SaleLine(models.Model):
    _inherit = 'sale.order.line'

    sale_order_discount_estimated_line = fields.Float(string='Sale', compute='sale_order_discount')

    def sale_order_discount(self):
        for rec in self:
            if rec.product_id.check_warranty_result:
                rec.sale_order_discount_estimated_line = 0
            else:
                rec.sale_order_discount_estimated_line = rec.price_unit * rec.product_uom_qty * -0.1

    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] + line.sale_order_discount_estimated_line,
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
