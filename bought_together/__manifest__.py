{
    "name": "Bought together",
    "application": True,
    "auto_install": False,
    "author": "Hnam",
    "sequence": -1000,
    "version": "1.0",
    "depends": ["base", "sale", "web"],
    "demo": [],
    "data": [
        'security/ir.model.access.csv',
        'views/index.xml',
        "views/shopify_view.xml",
        'data/ir_cron_bought_together.xml'
    ],
    'assets': {
    },
    "license": "LGPL-3",
}
