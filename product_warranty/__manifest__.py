{
    'name': 'Product Warranty',
    'application': True,
    'auto_install': False,
    'author': "hnam",
    'sequence': -100,
    'version': '2.0',
    'depends': ['base', 'product', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/group.xml',
        'views/product_warranty_view.xml',
        'views/sale.xml',
        'wizard/mass_product_warranty_view.xml',
    ],
    'demo': [],
    'license': 'LGPL-3',
}
