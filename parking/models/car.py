from odoo import models, fields, api


class Car(models.Model):
    _name = 'parking.car'
    _description = 'Parking car'

    name = fields.Char()
    car_type = fields.Selection([('sedan', 'Sedan'), ('suv', 'SUV')])
    owner = fields.Many2many('parking.person')
