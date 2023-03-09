import requests, werkzeug, shopify
from odoo import http
from odoo.http import request


class BoughtTogether(http.Controller):
    @http.route('/bought_together', auth='public', type='http', website=True)
    def bought_together(self, **kw):
        return request.render('bought_together.bought_together')
