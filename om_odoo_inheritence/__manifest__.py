# -*- coding: utf-8 -*-
{
    'name': "om_odoo_inheritence",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Hnam",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '19.04',
    'depends': ['sale', 'sale_stock'],
    'sequence': -99,
    'data': [
        'views/sale_order_view.xml',
    ],
    'demo': [],
}
