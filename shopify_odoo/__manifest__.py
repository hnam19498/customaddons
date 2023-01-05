{
    "name": "Shopify",
    "application": True,
    "auto_install": False,
    "author": "Hnam",
    "sequence": -1000,
    "version": "1.0",
    "depends": ["base", "product", "sale", "web"],
    "demo": [],
    "data": [
        "views/setting_view.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'shopify_odoo/static/src/js/main.js',
        ],
    },

    "license": "LGPL-3",
}
