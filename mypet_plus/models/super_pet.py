from odoo import fields, api, models


class SuperPet(models.Model):
    _name = "super.pet"  # <- new model name
    _inherit = "my.pet"  # <- inherit fields and methods from model "my.pet"
    _description = "Prototype inheritance"

    is_super_strength = fields.Boolean("Is super strength", default=False)
    is_fly = fields.Boolean("Is fly", default=False)
    planet = fields.Char("Planet")

    product_ids = fields.Many2many(comodel_name='product.product', string="Related Products",
                                   relation='super_pet_product_rel', column1='col_pet_id', column2='col_product_id')
