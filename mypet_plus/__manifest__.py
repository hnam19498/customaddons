# -*- coding: utf-8 -*-
{
    'name': "My product pet",
    'summary': """My pet model""",
    'description': """Managing pet information""",
    'author': "hnam",
    'sequence': -100,
    'category': 'Uncategorized',
    'version': '99.1',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_pet_view.xml',
        'views/super_pet_view.xml',
        'views/product_pet_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
