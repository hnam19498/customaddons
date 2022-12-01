# -*- coding: utf-8 -*-
{
    'name': "My pet",
    'summary': """My pet model""",
    'description': """Managing pet information""",
    'author': "hnam",
    'sequence': -100,
    'category': 'Uncategorized',
    'version': '8.1',
    'depends': [
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/my_pet_view.xml',
        'wizard/batch_update.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
