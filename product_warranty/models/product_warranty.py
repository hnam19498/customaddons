from odoo import api, fields, models
from datetime import datetime, date


class ProductWarranty(models.Model):
    _inherit = 'product.template'

    product_warranty = fields.Text(string='Warranty code', compute='sync_warranty_code')
    date_to = fields.Date(string='Date to')
    date_from = fields.Date(string='Date from')
    check_warranty_result = fields.Boolean(string='Check warranty result', compute='check_warranty')
    warranty_remaining = fields.Char(string='Warranty remaining', compute='product_warranty_remaining')

    def sync_warranty_code(self):
        for rec in self:
            if rec.date_to and rec.date_from:
                rec.product_warranty = 'PWR/' + rec.date_from.strftime('%d%m%y') + '/' + rec.date_to.strftime(
                    '%d%m%y')
            else:
                rec.product_warranty = ''

    def check_warranty(self):
        today = datetime.today()
        int_today = int(today.strftime('%Y%m%d'))
        for rec in self:
            if rec.date_from and rec.date_to:
                datefrom = int(rec.date_from.strftime('%Y%m%d'))
                dateto = int(rec.date_to.strftime('%Y%m%d'))
                if rec.product_warranty[:3] == 'PWR':
                    if datefrom <= int_today <= dateto:
                        rec.check_warranty_result = True
                    else:
                        rec.check_warranty_result = False
                else:
                    rec.check_warranty_result = False
            else:
                rec.check_warranty_result = False

    def product_warranty_remaining(self):
        today = date.today()
        for rec in self:
            if rec.date_from and rec.date_to:
                time_remaining = (rec.date_to - today).days
                year_remaining = time_remaining // 365
                month_remaining = (time_remaining - year_remaining * 365) // 30
                day_remaining = (time_remaining - year_remaining * 365 - month_remaining * 30)
                if year_remaining == 0:
                    if month_remaining == 0:
                        rec.warranty_remaining = f'{day_remaining} day(s)'
                    else:
                        rec.warranty_remaining = f'{month_remaining} month(s) {day_remaining} day(s)'
                else:
                    rec.warranty_remaining = f'{year_remaining} year(s) {month_remaining} month(s) {day_remaining} day(s)'
            else:
                rec.warranty_remaining = 'No information!'
