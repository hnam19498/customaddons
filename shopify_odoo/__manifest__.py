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
        'security/ir.model.access.csv',
        "views/setting_view.xml",
        "views/shop_infor_view.xml",
        "views/fetch_shopify_view.xml",
        'views/xero_infor_view.xml',
        "views/bundle_view.xml",
        "views/sync_invoice_view.xml",
        "views/bundle_analytic_view.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            'shopify_odoo/static/src/js/script_tag_1.js',
        ]
    },
    "license": "LGPL-3",
}
