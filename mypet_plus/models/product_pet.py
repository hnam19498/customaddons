from odoo import fields, api, models


class ProductPet(models.Model):
    _name = 'product.pet'
    _inherit = {'my.pet': 'my_pet_id'}
    _description = 'Product pet'

    my_pet_id = fields.Many2one('my.pet', 'My pet', auto_join=True, index=True, ondelete="cascade", required=True)
    pet_type = fields.Selection(
        [('basic', "Basic"), ('intermediate', 'Intermediate'), ('vip', 'VIP'), ('cute', 'Cute'), ])
    pet_color = fields.Selection([('white', 'White'), ('black', 'Black'), ('grey', 'Grey'), ('yellow', 'Yellow'), ],
                                 string='Pet Color')
    bonus_price = fields.Float('Bonus price')
    final_price = fields.Float(string='Final price', compute='compute_final_price')
    product_ids = fields.Many2many(comodel_name='product.product',
                                   string="Related Products",
                                   relation='product_pet_rel',  # <- change this relation name!
                                   column1='col_pet_id',
                                   column2='col_product_id')

    def compute_final_price(self):
        for rec in self:
            rec.final_price = rec.price - rec.bonus_price
