from odoo import api, fields, models


class MyPetPlus(models.Model):
    _name = "my.pet"
    _inherit = "my.pet"
    _description = "Extend mypet model"

    age = fields.Integer('Pet Age', default=2)
    type = fields.Selection([('dog', "Dog"), ("cat", "Cat")], string='Type')
