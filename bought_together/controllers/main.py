from odoo import http
from odoo.http import request


class BoughtTogether(http.Controller):
    @http.route('/bought_together', auth='user', type='http', website=True)
    def bought_together(self):
        return request.render('bought_together.bought_together')
