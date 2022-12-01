
from odoo import models, fields, api


class Person(models.Model):
    _name = 'parking.person'
    _description = 'Parking person'

    name = fields.Char()
    car = fields.Many2many('parking.car')
    # car_type = fields.Selection([('sedan', 'Sedan'), ('suv', 'SUV')])
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
