from odoo import fields, models, api


class MyPet(models.Model):
    _name = 'my.pet'
    _description = 'My pet model'

    name = fields.Char(string='Pet name', required=True)
    age = fields.Integer(string='Age')
    weight = fields.Integer(string='Weight')
    gender = fields.Selection([('male', "Male"), ("female", "Female")], string='Gender')
    pet_image = fields.Image(string="Pet image")
    owner_id = fields.Many2one('res.partner', string='Owner')
    product_ids = fields.Many2many(comodel_name='product.product', string="Related Products",
                                   relation='pet_product_rel', column1='col_pet_id', column2='col_product_id')
    price = fields.Float(string='Price')
