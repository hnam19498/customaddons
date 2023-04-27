{
    "name": "Instafeed",
    "application": True,
    "auto_install": False,
    "author": "Hnam",
    "sequence": -1000,
    "version": "1.0",
    "depends": ["base", "sale", "web"],
    "demo": [],
    "data": [
        'security/ir.model.access.csv',
        "data/ir_cron_instafeed.xml",
        'views/settings.xml',
        'views/index.xml',
        'views/shopify.xml',
        'views/instagram_view.xml'
    ],
    'assets': {},
    "license": "LGPL-3",
}