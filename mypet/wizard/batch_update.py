from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class BatchUpdateWizard(models.TransientModel):
    _name = 'my.pet.batchupdate.wizard'
    _description = 'Batch update wizard for my.pet model'

    gender = fields.Selection([('male', "Male"), ("female", "Female")], string='Gender')
    owner_id = fields.Many2one(comodel_name='res.partner', string='Owner', default=False)
    basic_price = fields.Float(string='Basic price', default=0)

    def multi_update(self):
        ids = self.env.context['active_ids']
        my_pets = self.env['my.pet'].browse(ids)
        new_data = {}
        if self.gender:
            new_data['gender'] = self.gender
        if self.owner_id:
            new_data['owner_id'] = self.owner_id
        if self.basic_price > 0:
            new_data['basic_price'] = self.basic_price

        my_pets.write(new_data)
