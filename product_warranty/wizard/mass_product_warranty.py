from odoo import fields, models, api


class MassProductWarranty(models.TransientModel):
    _name = 'mass.product.warranty'

    date_to = fields.Date(string='Date to')
    date_from = fields.Date(string='Date from')

    def multi_update(self):
        ids = self.env.context['active_ids']
        product_updates = self.env['product.template'].browse(ids)
        new_data = {}
        if self.date_from:
            new_data['date_from'] = self.date_from
        if self.date_to:
            new_data['date_to'] = self.date_to

        product_updates.write(new_data)