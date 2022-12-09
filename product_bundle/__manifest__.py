{
    "name": "Product bundle",
    "application": True,
    "auto_install": False,
    "author": "hnam",
    "sequence": -1000,
    "version": "2.0",
    "depends": ["base", "product", "sale", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/bundle_view.xml",
        'views/bundle_template.xml',
    ],
    "demo": [],
    "license": "LGPL-3",
}
