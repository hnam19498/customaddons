{
    "name": "Bundle",
    "application": True,
    "auto_install": False,
    "author": "Hnam",
    "sequence": -1000,
    "version": "1.0",
    "depends": ["base", "product", "sale", "web"],
    "data": [
        "security/ir.model.access.csv",
        'views/product_bundle.xml',
        'views/menu_items.xml'
    ],
    "demo": [],
    'assets': {
        'web.assets_frontend': [
            'bundle/static/js/main.js',
        ],
    },
    "license": "LGPL-3",
}
